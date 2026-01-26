import hashlib

def letterCasePermutaion(s: str):
    res = []
    def dfs(idx, n, s:str):
        if idx == n:
            res.append(s)
            return
        if s[idx].islower():
            dfs(idx + 1, n, s[:idx] + chr(ord(s[idx]) - 32) + s[idx + 1:])
        if s[idx].isupper():
            dfs(idx + 1, n, s[:idx] + chr(ord(s[idx]) + 32) + s[idx + 1:])
        dfs(idx + 1, n, s)

    dfs(0, len(s), s)
    return res


for s in letterCasePermutaion("y0U_RE4lLy_kn0W_TH1S_ConGr4tUlAT10Ns"):
    if hashlib.md5(s.encode(encoding='UTF-8')).hexdigest() == "7513209051f455fa44d0fa5cd0f3e051":
        print(s)
        print("success")
        exit()
# y0U_Re4llY_kN0w_TH1s_coNgr4TULat10nS