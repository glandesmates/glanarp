#How i mean before, i just 'expand the tool arp-scan'
#the tool wich i use in this script its from: https://github.com/royhills/arp-scan

import ftplib, os, argparse
from colorama import init, Fore, Style, Back
def clear(): os.system('clear')
init(autoreset=True)

class c:
    g = Fore.LIGHTGREEN_EX
    w = Fore.LIGHTWHITE_EX
    r = Fore.LIGHTRED_EX + Style.BRIGHT
    y = Fore.LIGHTYELLOW_EX
    s = Fore.LIGHTMAGENTA_EX
    c = Fore.RESET

bf = Style.RESET_ALL
bt = Style.BRIGHT

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-f')
parser.add_argument('--add')
args = parser.parse_args()

clear()
print(rf""" {c.y}
   ___   __    _        __  _      __    ___ 
  / _ \ / /   /_\    /\ \ \/_\    /__\  / _ \ 
 / /_\// /   //_\\  /  \/ //_\\  / \// / /_)/    {c.r + 'by glandesmates' + c.y}
/ /_\\/ /___/  _  \/ /\  /  _  \/ _  \/ ___/  
\____/\____/\_/ \_/\_\ \/\_/ \_/\/ \_/\/      
{c.g}   this tool only works with arp package
"""); print()

if not os.path.exists('/usr/share/man/man1/arp-scan.1.gz'):
    print(f"{'  '*5} [{c.s + bt}!{bf}] {c.w + bt} Installing arp-scan..." + bf); print()
    os.system('sudo apt-get install arp-scan > .txt')
else:
    pass

print();print()

def connect(ip):
    with ftplib.FTP() as ftp:
        try:
            ftp.connect(ip, timeout=3.6)
            print(f"[{c.g + '✔' + c.c}] {c.g + bt + 'Accesible '+ c.c} > {c.g + ip + c.c}")
        except:
            print(f"[{c.r + 'x' + c.c + bf}] {c.r + bt + 'Cant' + c.c + bf} {c.w + 'connect to ' + c.c + bt} > {c.y + ip + c.c}")


if not args.f:
    MSG = f"    [{c.y + '>' + c.c}] {c.g + f'Enter a name to your file {bt}(press enter if you dont want){bf}' + c.c} > "
    name = f"{input(MSG)}.txt"; print(); print()
    os.system(f'sudo arp-scan --interface=eth0 --localnet > {name}')

    with open(name, 'r') as f:
        lines = f.readlines()

        for item in lines:
            if item.startswith('1'):
                ip = item[:14]; print(c.s + item.strip())
                connect(ip); print()
            else:
                pass
else:
    with open(args.f, 'r') as f:
        lines = f.readlines()
        for ip in lines:
            connect(ip)

print(); print(f"{'         '*3}[{c.g + '✔' + c.c}] {c.w + 'Scan completed'}")


if os.path.exists('.txt'): os.system('rm .txt')
else: pass

