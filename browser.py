from bs4 import BeautifulSoup
from collections import deque
from colorama import Fore
import os
import requests
import sys


dir_ = sys.argv[1]
if not os.access(dir_, os.F_OK):
    os.makedirs(dir_)

history = deque()
url = input()
while url != 'exit':
    if url == 'back':
        if len(history) > 1:
            history.pop()
            with open(os.path.join(dir_, history[-1]), 'r') as f:
                print(f.read())
    else:
        if url.startswith('https://'):
            url = url[len('https://'):]
        if os.access(os.path.join(dir_, url[:url.rfind('.')]), os.F_OK):
            with open(os.path.join(dir_, url[:url.rfind('.')]), 'r') as f:
                print(f.read())
            history.append(url)
        else:
            if not url.startswith('https://'):
                url = 'https://' + url
            try:
                response = requests.get(url)
            except requests.exceptions.ConnectionError:
                print("Error: Incorrect URL")
            else:
                if response.status_code == 200:
                    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'al', 'li']
                    formatted_text = ''
                    soup = BeautifulSoup(response.content, 'html.parser')
                    for tag in soup.find_all(tags):
                        if tag.name == 'a':
                            formatted_text += Fore.BLUE + tag.get_text() + '\n'
                        elif tag.name in tags:
                            formatted_text += Fore.BLACK + tag.text + '\n'
                    print(formatted_text)
                    url = url[len('https://'):url.rfind('.')]
                    with open(os.path.join(dir_, url), 'w', encoding='utf-8') as f:
                        f.write(formatted_text)
                    history.append(url)
    url = input()
