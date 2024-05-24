import json, time, threading, websocket, requests,uuid, random
from tls_client import Session
def get_session_id(token):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
    hello = json.loads(ws.recv())
    auth = {
      "op": 2,
      "d": {
        "token": token,
        "properties": {
          "os": "Android",
          "browser": "Discord Android",
          "device": "emu64x",
          "system_locale": "en-US",
          "client_version": "216.14 - rn",
          "release_channel": "googleRelease",
          "device_vendor_id": str(uuid.uuid4()),
          "browser_user_agent": "",
          "browser_version": "",
          "os_version": "33",
          "client_build_number": random.randint(10000000000000, 99999999999999),
          "client_event_source": None
        },
        "capabilities": 16383,
        "client_state": {
          "guild_versions": {},
          "read_state_version": 7,
          "user_guild_settings_version": 0,
          "user_settings_version": 6,
          "private_channels_version": "0",
          "api_code_version": 1
        }
      }
    }
    ws.send(json.dumps(auth))
    res = json.loads(ws.recv())
    return res["d"]["session_id"], ws
def cookies(session):
    headers = {
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json",
        "Host": "discord.com",
        "User-Agent": f"Discord-Android/{''.join(str(random.randint(0, 9)) for _ in range(6))};RNA",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "GMT",
        "x-super-properties": "eyJvcyI6IkFuZHJvaWQiLCJicm93c2VyIjoiRGlzY29yZCBBbmRyb2lkIiwiZGV2aWNlIjoiZW11NjR4Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X3ZlcnNpb24iOiIyMTYuMTQgLSBybiIsInJlbGVhc2VfY2hhbm5lbCI6Imdvb2dsZVJlbGVhc2UiLCJkZXZpY2VfdmVuZG9yX2lkIjoiNzcwNjg3MDItYmNmNS00MWRmLWI1NDctZDQ3MmYzNjQxOWRjIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiIiwiYnJvd3Nlcl92ZXJzaW9uIjoiIiwib3NfdmVyc2lvbiI6IjMzIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjE2MDE0MDAxNTExNjgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0="
    }
    response = session.get('https://discord.com/api/v9/experiments', headers=headers)
    cookies = {'__dcfduid': response.cookies.get('__dcfduid'),'__sdcfduid': response.cookies.get('__sdcfduid'),'__cfruid': response.cookies.get('__cfruid'),'_cfuvid': response.cookies.get('_cfuvid')}
    return cookies
