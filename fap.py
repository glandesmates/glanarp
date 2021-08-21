import ftplib, os, argparse, nmap3
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

color = {
 'exyellow': Fore.YELLOW + Style.BRIGHT,
 'green': Fore.GREEN,
 'red': Fore.LIGHTRED_EX,
 'exgreen': Fore.BLUE + Style.BRIGHT,
 'white': Fore.LIGHTWHITE_EX,
 'reset': Fore.RESET + Style.RESET_ALL,
}

cash = color['green'] + '$'
cause = color['exyellow'] + '*'

bf = Style.RESET_ALL
bt = Style.BRIGHT

parser = argparse.ArgumentParser(add_help=False, usage=f"""{c.w + Style.BRIGHT}
[    -i    ]                    interface
[    -f    ]            read directions from a file

[   --add  ]               save only directions
[ --filter ]    filter directions (accessibles and not accessibles)

[  --nmap  ]    show the avaliable services (ftp, telnet, ssh, etc)

""")
parser.add_argument('-i', help=f'{c.w}[interface]')
parser.add_argument('-f', help='[SCAN AN LIST WITH DIRECTIONS]')
parser.add_argument('--add', help='[ADD ALL LOCAL DIRECTIONS TO A LIST]')
parser.add_argument('--filter', help='[SEPARATE NO ACCESSIBLES AND ACCESSIBLES DIRECTIONS]', action='store_true')
parser.add_argument('--nmap', action='store_true')
parser.add_argument('--ftp', action='store_true')
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

nm = nmap3.NmapScanTechniques()

def scan(ip):
    print(f"Scanning {color['exgreen'] + ip + color['reset']}...")
    scan = nm.nmap_tcp_scan(ip, args='-Pn')
    for ports in scan[ip]['ports']:

        state = ports['state']
        if state == 'open':
            state = color['exgreen'] + state
        else:
            state = color['red'] + state

        print(f"Service: {color['white'] + ports['service']['name']}  {cash + color['reset']}  State: {state} {cause} {color['reset'] + ports['reason']}  {cash}  {color['reset']}Port ID: {color['exyellow'] + ports['portid']}")
    
    print()
    
    for hn in scan[ip]['hostname']:
        print(f"Hostname: {hn['name']}  {cash}  {color['reset']}type: {hn['type']}\n")

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

def doit(ip):
    if not args.ftp and not args.nmap:
        connect(ip.rstrip('\n'))
    elif args.ftp and args.nmap:
        connect(ip.rstrip('\n'))
        scan(ip.rstrip('\n'))
    elif args.nmap and not args.ftp:
        scan(ip.rstrip('\n'))


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
                doit(ip); print()
            else:
                pass
else:
    with open(args.f, 'r+') as f:
        lines = f.readlines()
        for ip in lines:
            count += 1
            doit(ip)

print(); print(); print(f"{'         '*2}[{c.g + '✔' + c.c}] {c.w + 'Scan completed, with ' + f'{c.g + bt + str(count) + bf + c.w}' + ' directions finded'}")

if os.path.exists('.txt'): os.system('rm .txt')
else: pass
