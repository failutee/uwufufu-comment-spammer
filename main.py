import random
import threading

import colorama
import requests
from colorama import Fore
from requests.auth import HTTPProxyAuth
from requests.exceptions import ProxyError


def post_comment(g_id, nick_name, comment, proxy):
    url = "https://prod-api.uwufufu.com/v1/comments"

    parsed_proxy = None
    auth = None

    if proxy is not None:
        parsed_proxy, auth = parse_proxy(proxy)

    payload = {
        "gameId": g_id,
        "depth": 0,
        "name": nick_name,
        "body": comment,
        "isAnonymous": False
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers, proxies=parsed_proxy, auth=auth)
    except ProxyError:
        print(f'{Fore.RED}Cannot connect to proxy! Failed to send request!')
        return

    print(f'{Fore.YELLOW}Comment sent! => {response} ({parsed_proxy}, {auth})')

def read_file(file_path):
    io = open(file_path, 'r')
    return io.readlines()

def random_from_list(some_list):
    return some_list[random.randint(0, len(some_list) - 1)]

def parse_proxy(proxy: str):
    split = proxy.split(":")
    length = len(split)

    proxy_type = split[0]
    host = split[1]
    port = split[2]

    auth = None

    if length == 5:
        uname = split[3]
        password = split[4]

        auth = HTTPProxyAuth(uname, password)

    return { proxy_type: f'{host}:{port}' }, auth

if __name__ == '__main__':
    colorama.init(autoreset=True)

    random = random.Random()

    game_id = input(f'{Fore.MAGENTA} [$] Game ID: ')
    proxy_path = input(f'{Fore.MAGENTA} [$] Proxy file path (OPTIONAL): ')
    nick_names = input(f'{Fore.MAGENTA} [$] Nicknames (example: Test, Test1): ').split(", ")
    comments = input(f'{Fore.MAGENTA} [$] Comments (example: Example Comment, Its example comment): ').split(", ")
    times = int ( input(f'{Fore.MAGENTA} [$] Times (NUMBER): ') )

    proxies = None

    if proxy_path.strip() != '':
        proxy_list = read_file(proxy_path)
        proxies = list(map(lambda line: line.replace('\n', ''), proxy_list))

    using_proxy = True if proxies is not None else False

    for i in range(0, times):
        # Random comment
        random_comment = random_from_list(comments)
        nick = random_from_list(nick_names)

        unparsed_proxy = None

        if using_proxy:
            unparsed_proxy = random_from_list(proxies)

        t = threading.Thread(target=post_comment, args=(game_id, nick, random_comment, unparsed_proxy))
        t.start()