import json, time, threading, websocket, requests,uuid, random
from tls_client import Session
import h
from toml import load

config = load('config.toml')
settings = config['Settings']
Invite = settings['Invite']
Api_Key = settings['Api_Key']
files = config['Files']
tokens_file = files['Tokens_File']
proxies_file = files['Proxies_File']

def Join(token, invite, proxy):
    session = Session(client_identifier="confirmed_android", random_tls_extension_order=True)
    session.proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy
    }
    session_id, ws = h.get_session_id(token)
    time.sleep(4)
    url = f"https://discord.com/api/v9/invites/{invite}"
    headers = {
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "Authorization": token,
        "Connection": "Keep-Alive",
        "Content-Type": "application/json",
        "Host": "discord.com",
        "User-Agent": f"Discord-Android/{''.join(str(random.randint(0, 9)) for _ in range(6))};RNA",
        "x-context-properties": "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "GMT",
        "x-super-properties": "eyJvcyI6IkFuZHJvaWQiLCJicm93c2VyIjoiRGlzY29yZCBBbmRyb2lkIiwiZGV2aWNlIjoiZW11NjR4Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X3ZlcnNpb24iOiIyMTYuMTQgLSBybiIsInJlbGVhc2VfY2hhbm5lbCI6Imdvb2dsZVJlbGVhc2UiLCJkZXZpY2VfdmVuZG9yX2lkIjoiNzcwNjg3MDItYmNmNS00MWRmLWI1NDctZDQ3MmYzNjQxOWRjIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiIiwiYnJvd3Nlcl92ZXJzaW9uIjoiIiwib3NfdmVyc2lvbiI6IjMzIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjE2MDE0MDAxNTExNjgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0="
    }
    cookies = h.cookies(session=session)
    response = session.post(url, json={"session_id": session_id}, headers=headers, cookies=cookies)
    if response.status_code in [200, 201, 202, 203, 204]:
        print(f'Succesfully Add Token {token}')
    elif response.status_code == 400:
        rq_data = response.json()['captcha_rqdata']
        rq_token = response.json()['captcha_rqtoken']
        captcha_sitekey = response.json()['captcha_sitekey']
        headers = {"Content-Type": "application/json", "apikey": apikey}
        payload = {
            "rqdata": rq_data,
            "type": "hcaptcha",
            "enterprise": True,
            "url": "discord.com",
            "sitekey": captcha_sitekey,
            "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        response = requests.post('https://token.nocaptchaai.com/token', json=payload, headers=headers).json()
        start_time = time.time()
        print("task status:", response)
        print("waiting 7 sec for response...")
        time.sleep(7)
        while True:
            sts = requests.get(response["url"], headers=headers).json()
            if sts["status"] in ["processed", "failed"]:
                print(f'time since request: {int(time.time() - start_time)} seconds')
                print(f'status: {sts["status"]}\n{sts["token"]}')
                url = f"https://discord.com/api/v9/invites/{invite}"
                headers = {
                    "Accept-Encoding": "gzip",
                    "Accept-Language": "en-US",
                    "Authorization": token,
                    "Connection": "Keep-Alive",
                    "Content-Type": "application/json",
                    "Host": "discord.com",
                    "User-Agent": f"Discord-Android/{''.join(str(random.randint(0, 9)) for _ in range(6))};RNA",
                    'X-Captcha-Key': sts["token"],
                    'X-Captcha-Rqtoken': rq_token,
                    "x-context-properties": "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
                    "x-debug-options": "bugReporterEnabled",
                    "x-discord-locale": "en-US",
                    "x-discord-timezone": "GMT",
                    "x-super-properties": "eyJvcyI6IkFuZHJvaWQiLCJicm93c2VyIjoiRGlzY29yZCBBbmRyb2lkIiwiZGV2aWNlIjoiZW11NjR4Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X3ZlcnNpb24iOiIyMTYuMTQgLSBybiIsInJlbGVhc2VfY2hhbm5lbCI6Imdvb2dsZVJlbGVhc2UiLCJkZXZpY2VfdmVuZG9yX2lkIjoiNzcwNjg3MDItYmNmNS00MWRmLWI1NDctZDQ3MmYzNjQxOWRjIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiIiwiYnJvd3Nlcl92ZXJzaW9uIjoiIiwib3NfdmVyc2lvbiI6IjMzIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjE2MDE0MDAxNTExNjgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0="
                }
                response = session.post(url, json={"session_id": session_id}, headers=headers, cookies=cookies)
                if response.status_code in [200, 201, 202, 203, 204]:
                    print(f'Succesfully Add Token {token}')
                else:
                    print(f'Can`t add a token with a respone - {response.json()}')
                time.sleep(1)
                ws.close()
                break
            print("status:", sts["status"])
with open(f'{tokens_file}', "r") as file:
    for line in file:
        token = line.strip()
        threading.Thread(target=Join, args=(token, Invite, (random.choice(open(proxies_file, "r").readlines()).strip() if len(open(proxies_file, "r").readlines()) != 0 else None))).start()
        time.sleep(2)
