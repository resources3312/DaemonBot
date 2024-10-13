#! /usr/bin/python
"""
DaemonBot v1.1

Telegram Bot for remote control home or work
machine
Coded by: ViCoder32
"""
import os
import sys
import socket
from subprocess import getoutput
from urllib.request import urlopen
from urllib.error import URLError
import telebot
from telebot import types
from dotenv import load_dotenv
load_dotenv()
global markup
bot = telebot.TeleBot(os.getenv("TOKEN"))

def get_info_ipv4() -> str:
    """
    Returning local or global ipv4
    
    no argument - Local ipv4
    
    -w, --wan - Global ipv4 
    
    Not connection - 127.0.0.1
    """
    try:
        if "-w" in sys.argv or "--wan" in sys.argv:
            with urlopen("https://ifconfig.me/ip") as res:
                return res.read().decode()
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
    except (URLError, socket.error):
        return "127.0.0.1"


def definedistr() -> str:
    """
    Returning your linux distribtion from os-release
    file
    
    """
    try:
        with open('/etc/os-release', 'r', encoding="utf-8") as f:
            return f.read().split()[9].split('=')[1].lower()
    except EOFError:
        return "distr"


        
def shutdown_machine() -> None:
    """
    Crossplatform function for turn off
    you machine
    
    """
    if "win" in sys.platform.lower():
        os.system("shutdown -s -t 0")
    else:
        os.system("shutdown -h now")

def parse_argument(option: str):
    """
    
    Function for parse short and long arguments of command line
    
    """
    try:
        for i in sys.argv[1:]:  # Saving memory
            if option in i:
                return sys.argv[i.index(option) + 1 if len(option) > 2 else 2]
    except (ValueError, IndexError):
        return None

def man_page() -> None:
    """
    Manual page

    """
    sys.exit(""" \x1B[33m
DaemonBot v1.1
    
    Commands:
        
        -h, --help - Show manual page of bot
        
        -w, --wan - Set you own ipv4, for debug or WAN connection
        
        -i, --id - Set your telegram id, for security
  \x1B[0m""")

def conf_write_option(file: str, param: str, option: str) -> None:
    """
    Changing option in config file
    
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            raw = f.read().split()
            index = raw.index(param)
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
                data = text.replace(raw[index], option)
                with open(file, "w", encoding="utf-8") as f:
                    f.write(data)
    except (EOFError, IndexError):
        pass

def conf_write_value(file: str, param: str, option: str) -> None:
    """
    Changing value of option in config file
    
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            raw = f.read().split()
            index = raw.index(param) + 1
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
                data = text.replace(raw[index], option)
                with open(file, "w", encoding="utf-8") as f:
                    f.write(data)
    except (EOFError, IndexError):
        pass

def init_ssh() -> None:
    """
    Installing if not install, and running SSH-server

    """
    if "nt" in os.name:
        pass
        # In development stage
    else:
        if "not found" in getoutput("which sshd"):
            match definedistr():
                case "debian":
                    os.system('apt update -y')
                    os.system('apt install openssh-server -y')
                case "ubuntu":
                    os.system('apt update -y')
                    os.system('apt install openssh-server -y')
                case "centos":
                    pass
                case "fedora":
                    os.system("dnf update")
                    os.system('dnf install openssh-server -y')
                case "arch":
                    os.system('pacman -Sy')
                    os.system('pacman -S openssh')
                case "gentoo":
                    os.system('emerge --sync')
                    os.system('emerge openssh')
            conf_write_option("/etc/ssh/sshd_config", "#ListenAddress", "ListenAddress")
            conf_write_option("/etc/ssh/sshd_config", "#Port", "Port")
        conf_write_value("/etc/ssh/sshd_config", "ListenAddress", get_info_ipv4())
        os.system("systemctl restart ssh")

def get_uptime():
    """
    Returning uptime

    """
    return ' '.join(getoutput("uptime -p").split()[1:])
def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_power_off = types.KeyboardButton("🖥Отключить машину")
    button_uptime = types.KeyboardButton("⌛️Получить uptime")
    button_ssh = types.KeyboardButton("Поднять ssh")
    markup.add(button_power_off, button_uptime, button_ssh)
    return markup
@bot.message_handler(commands=["start"])
def get_start(message):
    """
    /start activity of DaemonBot

    """
    if message.chat.id != parse_argument("-i"):
        bot.send_message(message.chat.id, "Прошу вас уйти сэр, мой хозяин сегодня не ждет гостей..")
    else:
        bot.send_message(message.chat.id, "Приветствую вас, мой темный лорд..")
        bot.send_message(message.chat.id, f"Текущий uptime вашей машины {get_uptime()}", reply_markup=get_keyboard())
@bot.message_handler(content_types=["text"])
def handler(message):
    """
    Message handler

    """
    if "uptime" in message.text and message.chat.id == parse_argument("-i"):
        bot.send_message(message.chat.id, f"Текущий uptime вашей машины {get_uptime()}")
        bot.send_message(message.chat.id, "Еще пожелания, мой лорд?")
    elif "ssh" in message.text and message.chat.id == parse_argument("-i"):
        init_ssh()
        bot.send_message(message.chat.id, "Ssh сервер готов к использованию, мой темный лорд..")
        bot.send_message(message.chat.id, f"Адрес для подключения: {get_info_ipv4()}")
    elif "машину" in message.text and message.chat.id == parse_argument("-i"):
        bot.send_message(message.chat.id, "Машина была отключена сэр, доброго вам дня..")
        shutdown_machine()



def main():
    """
    Entry point

    """

    if "-h" in sys.argv or "--help" in sys.argv:
        man_page()
    else:
        bot.infinity_polling()
if __name__ == '__main__':
    main()
