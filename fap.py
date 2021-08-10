# Some options in this script was maded using arp-scan from: https://github.com/royhills/arp-scan

import ftplib, os, argparse
from colorama import init, Fore, Style
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

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='[SCAN AN LIST WITH DIRECTIONS]')
parser.add_argument('--add', help='[ADD ALL LOCAL DIRECTIONS TO A LIST]')
parser.add_argument('--filter', help='[SEPARATE NO ACCESSIBLES AND ACCESSIBLES DIRECTIONS]')
parser.add_argument('-i')

args = parser.parse_args()

clear()
print(rf""" {c.y}
   ___   __    _        __  _      __    ___ 
  / _ \ / /   /_\    /\ \ \/_\    /__\  / _ \ 
 / /_\// /   //_\\  /  \/ //_\\  / \// / /_)/    {c.r + 'by glandesmates' + c.y}
/ /_\\/ /___/  _  \/ /\  /  _  \/ _  \/ ___/  
\____/\____/\_/ \_/\_\ \/\_/ \_/\/ \_/\/      
{c.g}     be careful with this beast
"""); print()

if not os.path.exists('/usr/share/man/man1/arp-scan.1.gz'):
    print(f"{'  '*10} {c.w}[{c.s + bt}!{bf + c.w}] {c.w + bt} Installing arp-scan..." + bf); print()
    os.system('sudo apt-get install arp-scan > .txt')
    print(f"{'  '*10} {c.w + bt}[{c.g}✔{c.w}] arp-scan was {c.g}installed")
else:
    pass

print();print()

def filter(c, ip):
    if args.f and args.filter:
        name = f'{args.f}#{c}'; l = list()
        
        if os.path.exists(name): pass
        else: open(name, 'w')

        l.append(ip)
        with open(name, 'a+') as f:
            for item in l:
                f.write(item + '\n')

def connect(ip):
    with ftplib.FTP() as ftp:
        try:
            ftp.connect(ip, timeout=5)
            print(f"[{c.g + '✔' + c.c}] {c.g + bt + 'Accessible '+ c.c} > {c.g + ip + c.c}")
            filter('true', ip)
        except KeyboardInterrupt:
            print(f"\n{'    '*6}{c.y + bt}[{c.r}!{c.y}] {c.r}Break"); exit()
        except:
            print(f"[{c.r + 'x' + c.c + bf}] {c.r + bt + 'Accessible ' + c.c + bt} > {c.y + ip + c.c}")
            filter('false', ip)


global count
count = 0

if not args.f:
    MSG = f"    [{c.y + '>' + c.c}] {c.g + f'Enter a name to your file {bt}(press enter if you dont want){bf}' + c.c} > "
    name = f"{input(MSG)}.txt"; print(); print()

    if args.i == 'eth0':
        os.system(f'sudo arp-scan --interface=eth0 --localnet > {name}')
    else:
        os.system(f'sudo arp-scan --interface=wlan0 --localnet > {name}')

    with open(name, 'r') as f:
        lines = f.readlines()

        for item in lines:
            if item.startswith('1'):
                count += 1
                ip = item[:14]; print(c.s + item.strip() + f"  {c.g + bt}---> {c.w + str(count)}")
                if args.add:
                    if os.path.exists(args.add):
                        with open(args.add, 'a+') as f:
                            f.write(ip + '\n')
                    else:
                        with open(args.add, 'w') as f:
                            f.write(ip + '\n')
                connect(ip.rstrip('\n')); print()
            else:
                pass
else:
    with open(args.f, 'r+') as f:
        lines = f.readlines()
        for ip in lines:
            count += 1
            connect(ip.rstrip('\n'))

print(); print(); print(f"{'         '*2}[{c.g + '✔' + c.c}] {c.w + 'Scan completed, with ' + f'{c.g + bt + str(count) + bf + c.w}' + ' directions finded'}")

if os.path.exists('.txt'): os.system('rm .txt')
else: pass
