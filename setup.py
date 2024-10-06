from subprocess import getoutput
import sys
import os


def unix_install() -> None:
    try:
        if "daebot" in getoutput("ls /etc/systemd/system/"):
            os.system("rm -rf /usr/bin/daebot")
        print("\x1B[33m [!] Try to install DaemonBot \x1B[0m")
        os.system("pyinstaller -F daemon_bot.py -n daebot")
        print("\x1B[32m [+] DaemonBot was compiled \x1B[0m")
        os.system("cp ./dist/daebot /usr/bin/")
        os.system("rm -rf dist build *.spec")
        print("\x1B[32m [+] Success, binary was installed \x1B[0m")
    except OSError:
        print("\x1B[31m [+] Unknown error, try again.. \x1B[0m")


def remove_daebot() -> None:
    print("\x1B[33m [!] Try to remove DaemonBot \x1B[0m")
    os.system("rm -rf /usr/bin/daebot /etc/systemd/system/daebot.service")
    print("\x1B[32m [!] Daebot was removed \x1B[0m")

def man_page() -> None:
    sys.exit(""" \x1B[33m
DaemonBotInstaller v1.1
    
    Commands:
        
        -h, --help - Show manual page of bot installer
        
        -d, --daemon - Install DaemonBot like system daemon
        
        -r, --remove - Remove DaemonBot from machine 
  \x1B[0m""")

def creat_deamon() -> None:
    if "-d" in sys.argv or "--daemon" in sys.argv:
        msg = """
[Unit]
Description=DaemonBot
After=network.target
[Service]
Type=oneshot
User=root
ExecStart=/usr/bin/daebot
[Install]
WantedBy=multi-user.target           
"""
        with open("/etc/systemd/system/daebot.service", "w", encoding="utf-8") as f:
            f.write(msg)
            os.system("systemctl restart daebot")
        print("x1B[32m [+] DaemonBot was written in systemd 1xB[0m")
    

def main() -> None:
    if "-h" in sys.argv or "--help":
        man_page()
    if "-r" in sys.argv or "--remove" in sys.argv:
        remove_daebot()
    else:
        man_page()
    unix_install()
    creat_deamon()

if __name__ == '__main__':
    main()
