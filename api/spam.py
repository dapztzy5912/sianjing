from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import random
import string
import requests
import os
import time

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Backend is running!".encode('utf-8'))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        nglusername = data.get('nglusername')
        message = data.get('message')
        count = int(data.get('count', 1))  # Default ke 1 jika tidak ada count
        use_proxy = data.get('use_proxy', False)

        results = []
        for i in range(count):
            success = self.send_ngl_message(nglusername, message, use_proxy)
            results.append(success)
            time.sleep(1)  # Delay 1 detik

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
        self.end_headers()
        response = {'results': results}
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def deviceId(self):
        characters = string.ascii_lowercase + string.digits
        part1 = ''.join(random.choices(characters, k=8))
        part2 = ''.join(random.choices(characters, k=4))
        part3 = ''.join(random.choices(characters, k=4))
        part4 = ''.join(random.choices(characters, k=4))
        part5 = ''.join(random.choices(characters, k=12))
        device_id = f"{part1}-{part2}-{part3}-{part4}-{part5}"
        return device_id

    def UserAgent(self):
        try:
            with open('user-agents.txt', 'r') as file:
                user_agents = file.readlines()
                random_user_agent = random.choice(user_agents).strip()
                return random_user_agent
        except:
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            ]
            return random.choice(user_agents)

    def Proxy(self):
        try:
            with open('proxies.txt', 'r') as file:
                proxies_list = file.readlines()
                if not proxies_list:
                    return None
                random_proxy = random.choice(proxies_list).strip()
            proxies = {
                'http': random_proxy,
                'https': random_proxy
            }
            return proxies
        except:
            return None

    def send_ngl_message(self, nglusername: str, message: str, use_proxy: bool = False):
        headers = {
            'Host': 'ngl.link',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': f'{self.UserAgent()}',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://ngl.link',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://ngl.link/{nglusername}',
            'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        data = {
            'username': f'{nglusername}',
            'question': f'{message}',
            'deviceId': f'{self.deviceId()}',
            'gameSlug': '',
            'referrer': '',
        }

        proxies = self.Proxy() if use_proxy else None

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=data, proxies=proxies, timeout=10)
            return response.status_code == 200
        except:
            return False
