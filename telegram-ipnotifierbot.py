import requests
import telegram
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class IpNotifierBot:
    def __init__(self, file_path, chat_id, bot_token):
        self.requests = requests
        self.public_ip = ""
        self.file_with_ip_addr = None
        self.file_path = file_path
        self.chat_id = chat_id
        self.bot_token = bot_token

        self.bot = self.connect_bot()
        self.setup_file()

    def setup_file(self):
        self.file_with_ip_addr = open(self.file_path, "r+")

    def check(self):
        self.get_my_public_ip()
        self.notify_telegram()
        self.close_file()

    def connect_bot(self):
        return telegram.Bot(self.bot_token)

    def get_me(self):
        print(self.bot.get_me())

    def update_file(self):
        self.file_with_ip_addr.close()
        
        file = open(self.file_path, 'w')

        file.write(self.public_ip)

        file.close()

    def close_file(self):
        self.file_with_ip_addr.close()

    def get_my_public_ip(self):
        request = self.requests.get("https://ifconfig.me/all.json")
        
        if(request.json()):
            response = request.json()

            self.public_ip = response['ip_addr']

    def notify_telegram(self):
        ip_in_file = self.file_with_ip_addr.readline()
        
        print("IP in file: %s" % (ip_in_file))
        print("Public IP: %s" % (self.public_ip))

        print("IPs are different? %s" % (ip_in_file != self.public_ip))

        if ip_in_file != self.public_ip:
            self.update_file()
            
            print("Sending Telegram message...")

            self.bot.send_message(
                text="Amigo o teu IP mudou!!!\n\nNovo IP: %s" % (self.public_ip), 
                chat_id=self.chat_id
            )

IpNotifierBot = IpNotifierBot(
    os.getenv('FILE_PATH'), 
    os.getenv('CHAT_ID'),
    os.getenv('BOT_TOKEN')
)
IpNotifierBot.check()
