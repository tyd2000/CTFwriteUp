import requests, time, json, sys
BASE='http://160.202.254.160:17732'
ANS={
 1:'E',
 2:'flag{WebStack-1.2024}',
 3:'flag{CVE-2026-1555-POST-/wp-admin/admin-ajax.php?action=img_upload}',
 4:'flag{wp-content/uploads/2026/06/20260617192508_4dc56fd5.php}',
 5:'flag{2026-06-17}',
 6:'flag{key}',
 7:'flag{Godzilla}',
 8:'flag{4.8.5}',
 9:'flag{7.0}',
 10:'flag{wordpress,123456}',
}
ORDER=[1,2,3,4,5,6,7,8,9,10]

def new_cookie():
    r=requests.get(BASE+'/state')
    return r.cookies.get_dict()['session']

def attempt(cookie, qid, ans):
    r=requests.post(BASE+'/submit', json={'id':qid,'answer':ans},
                    headers={'Cookie':'session='+cookie}, timeout=10)
    return r

for run in range(1,6):
    cookie=new_cookie()
    expected=0
    ok=True
    print('=== run',run,'cookie',cookie[:20],'...')
    for qid in ORDER:
        done=False
        for att in range(120):
            r=attempt(cookie,qid,ANS[qid])
            try: d=r.json()
            except Exception:
                print(' bad json',r.status_code,r.text[:100]); time.sleep(0.5); continue
            rotated=('Set-Cookie' in r.headers) or bool(r.cookies)
            solved=d.get('solved', -1)
            if d.get('completed'):
                print('*** COMPLETED flag=',d.get('flag'))
                print(json.dumps(d,ensure_ascii=False))
                sys.exit(0)
            if d.get('ok'):
                if (not rotated) and solved==expected+1:
                    expected+=1; done=True; break
                elif (not rotated) and solved==expected:
                    # already recorded on this worker
                    done=True; break
                # rotated -> miss, retry
            else:
                # possibly locked or wrong? retry a few
                pass
            time.sleep(0.02)
        if not done:
            print(' q',qid,'failed to pin on this session (expected',expected+1,')')
            ok=False; break
        print(' q%-2d solved=%d'%(qid,expected))
    if not ok:
        continue
    # final state via same-cookie reads (may land anywhere); try a few
    for i in range(30):
        r=requests.get(BASE+'/state',headers={'Cookie':'session='+cookie})
        d=r.json()
        if d.get('completed'):
            print('*** COMPLETED(state) flag=',d.get('flag')); sys.exit(0)
        if d.get('solved_count',0)>=10:
            print('state says 10 solved but no flag:',d)
    print(' run ended with expected',expected)
print('no completion')
