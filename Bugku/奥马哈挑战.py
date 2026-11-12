import socket
import re
from itertools import combinations

HOST = "160.202.254.160"
PORT = 13736

RANK_MAP = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "T": 10, "10": 10,
    "J": 11, "Q": 12, "K": 13, "A": 14
}

SUITS = ["♠", "♥", "♣", "♦"]

CARD_RE = re.compile(r"(10|[2-9TJQKA])\s*([♠♥♣♦])")


def parse_card(rank, suit):
    return (RANK_MAP[rank], suit)


def card_name(card):
    r, s = card
    rev = {v: k for k, v in RANK_MAP.items() if k != "10"}
    return rev[r] + s


def eval_5(cards):
    ranks = sorted([r for r, _ in cards], reverse=True)
    suits = [s for _, s in cards]

    cnt = {}
    for r in ranks:
        cnt[r] = cnt.get(r, 0) + 1

    flush = len(set(suits)) == 1

    uniq = sorted(set(ranks), reverse=True)
    straight_high = None

    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4:
            straight_high = uniq[0]
        elif uniq == [14, 5, 4, 3, 2]:
            straight_high = 5

    if flush and straight_high:
        return (8, straight_high)

    items = sorted(cnt.items(), key=lambda x: (x[1], x[0]), reverse=True)

    if items[0][1] == 4:
        quad = items[0][0]
        kicker = max(r for r in ranks if r != quad)
        return (7, quad, kicker)

    if items[0][1] == 3 and items[1][1] == 2:
        return (6, items[0][0], items[1][0])

    if flush:
        return (5, *ranks)

    if straight_high:
        return (4, straight_high)

    if items[0][1] == 3:
        trip = items[0][0]
        kickers = sorted([r for r in ranks if r != trip], reverse=True)
        return (3, trip, *kickers)

    if items[0][1] == 2 and items[1][1] == 2:
        p1, p2 = sorted([items[0][0], items[1][0]], reverse=True)
        kicker = max(r for r in ranks if r != p1 and r != p2)
        return (2, p1, p2, kicker)

    if items[0][1] == 2:
        pair = items[0][0]
        kickers = sorted([r for r in ranks if r != pair], reverse=True)
        return (1, pair, *kickers)

    return (0, *ranks)


def omaha_best(hand4, board5):
    best = None
    for h2 in combinations(hand4, 2):
        for b3 in combinations(board5, 3):
            v = eval_5(list(h2) + list(b3))
            if best is None or v > best:
                best = v
    return best


def count_outs(hero, opponents, board4):
    deck = [(r, s) for r in range(2, 15) for s in SUITS]

    known = set(hero + board4)
    for opp in opponents:
        known.update(opp)

    outs = []

    for river in deck:
        if river in known:
            continue

        board5 = board4 + [river]
        hero_best = omaha_best(hero, board5)

        ok = True
        for opp in opponents:
            opp_best = omaha_best(opp, board5)
            if hero_best <= opp_best:
                ok = False
                break

        if ok:
            outs.append(river)

    return len(outs), outs


def parse_round(text):
    idx = text.rfind("========= Round")
    if idx == -1:
        return None

    block = text[idx:]
    found = CARD_RE.findall(block)

    if len(found) < 20:
        return None

    cards = [parse_card(r, s) for r, s in found[:20]]

    hero = cards[0:4]
    board = cards[4:8]
    opponents = [
        cards[8:12],
        cards[12:16],
        cards[16:20],
    ]

    return hero, board, opponents


def main():
    s = socket.create_connection((HOST, PORT))
    buf = ""

    while True:
        data = s.recv(4096)
        if not data:
            break

        text = data.decode("utf-8", errors="ignore")
        print(text, end="")
        buf += text

        if "How many outs" in buf and ">" in buf:
            parsed = parse_round(buf)
            if parsed is None:
                continue

            hero, board, opponents = parsed
            ans, outs = count_outs(hero, opponents, board)

            print(f"\n[+] outs = {ans}")
            if outs:
                print("[+] river cards:", " ".join(card_name(c) for c in outs))

            s.sendall((str(ans) + "\n").encode())
            buf = ""

    s.close()


if __name__ == "__main__":
    main()