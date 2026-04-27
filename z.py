#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 2 – Simple Captive Portal Bypass (Fallback)
"""
import requests
import re
import urllib3
import time
import sys
from urllib.parse import urljoin, urlparse

urllib3.disable_warnings()

# ==========================================
# 1. Check if real internet is available
# ==========================================
def internet_up():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

# ==========================================
# 2. Detect portal via redirect
# ==========================================
def get_portal_url():
    try:
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204",
                         allow_redirects=True, timeout=5)
        if r.url != "http://connectivitycheck.gstatic.com/generate_204":
            return r.url
    except:
        pass
    # Fallback: try common redirect target
    try:
        r = requests.get("http://captive.apple.com/hotspot-detect.html",
                         allow_redirects=True, timeout=5)
        if r.url != "http://captive.apple.com/hotspot-detect.html":
            return r.url
    except:
        pass
    return None

# ==========================================
# 3. Find and submit the login form
# ==========================================
def auto_submit(session, portal_url):
    """Find the most likely login/accept form and submit it"""
    try:
        resp = session.get(portal_url, verify=False, timeout=10)
    except:
        print("[!] Cannot reach portal page.")
        return False

    html = resp.text
    base = portal_url

    # Look for forms
    forms = re.findall(r'<form[^>]*>.*?</form>', html, re.DOTALL | re.IGNORECASE)
    if not forms:
        # No form? Maybe just a button that does a redirect.
        # Check for a link containing 'connect' or 'login'
        match = re.search(r'href="([^"]*)"', html)
        if match:
            next_url = urljoin(base, match.group(1))
            try:
                session.get(next_url, timeout=5)
                return True
            except:
                pass
        return False

    # Find the form that has a submit button with label like "connect", "agree", "login", etc.
    for form_html in forms:
        action_match = re.search(r'action="([^"]*)"', form_html)
        action = urljoin(base, action_match.group(1)) if action_match else base

        # Collect all inputs (hidden + visible)
        inputs = re.findall(r'<input[^>]*>', form_html, re.IGNORECASE)
        data = {}
        for inp in inputs:
            name = re.search(r'name="([^"]*)"', inp)
            value = re.search(r'value="([^"]*)"', inp)
            if name:
                data[name.group(1)] = value.group(1) if value else ""

        # Check if the form contains a submit button with an encouraging word
        submit_match = re.search(r'<input[^>]*type="submit"[^>]*value="([^"]*)"', form_html, re.IGNORECASE)
        if not submit_match:
            submit_match = re.search(r'<button[^>]*type="submit"[^>]*>(.*?)</button>', form_html, re.IGNORECASE)
        if submit_match:
            label = submit_match.group(1).lower()
            # Accept any of these keywords
            if any(k in label for k in ["connect", "agree", "login", "accept", "continue", "ok", "submit"]):
                print(f"[*] Using form with button: '{label}'")
                try:
                    if "method" not in form_html.lower() or "post" in form_html.lower():
                        resp = session.post(action, data=data, timeout=10)
                    else:
                        resp = session.get(action, params=data, timeout=10)
                    if resp.status_code in (200, 302, 303, 307):
                        time.sleep(2)
                        return True
                except:
                    continue

    # If no promising submit button, just try the first form
    form_html = forms[0]
    action_match = re.search(r'action="([^"]*)"', form_html)
    action = urljoin(base, action_match.group(1)) if action_match else base
    inputs = re.findall(r'<input[^>]*>', form_html, re.IGNORECASE)
    data = {}
    for inp in inputs:
        name = re.search(r'name="([^"]*)"', inp)
        value = re.search(r'value="([^"]*)"', inp)
        if name:
            data[name.group(1)] = value.group(1) if value else ""

    try:
        session.post(action, data=data, timeout=10)
        time.sleep(2)
        return True
    except:
        pass

    return False

# ==========================================
# 4. Main bypass loop
# ==========================================
def main():
    print("[*] Checking internet connection...")
    if internet_up():
        print("[✓] Already online – nothing to do.")
        return

    print("[*] Looking for captive portal...")
    portal = get_portal_url()
    if not portal:
        print("[!] No portal detected – maybe DNS is blocked?")
        return

    print(f"[*] Portal found: {portal}")
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    print("[*] Attempting automatic bypass...")
    if auto_submit(session, portal):
        if internet_up():
            print("[✓] SUCCESS! You are now online.")
        else:
            print("[!] Form submitted, but internet not detected. Portal may require real credentials.")
    else:
        print("[!] Automatic bypass failed. The portal may need manual interaction.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Aborted.")
    except Exception as e:
        print(f"[X] Error: {e}")