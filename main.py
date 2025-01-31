import requests
import time
import json
import html
from pystyle import Write, Colors
from colorama import Fore, init

init(autoreset=True))

Write.Print(r"""
█████ █   █ ████ █   █  █    ███   ██  █████  ███  █    ████
█    █ █  █ █    █   █  █    █  ███ █  █   █   █   █    ██
█████   █   ██   █   █  █    █      █  █████   █   █      ██
█      █    ███   ███   ████ █      █  █   █  ███  ███  ████

[1] Generate Mail
[2] Exit
""", Colors.blue_to_white, interval=0.0001)

BASE_URL = "http://api.guerrillamail.com/ajax.php"

def get_email_address(session):
    params = {'f': 'get_email_address'}
    response = session.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(Fore.BLUE + f"DEBUG: get_email_address response -> {data}")
    return data.get("email_addr", ""), data.get("sid_token", "")

def check_email(session, sid_token, seq):
    params = {'f': 'check_email', 'sid_token': sid_token, 'seq': seq}
    response = session.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(Fore.BLUE + f"DEBUG: check_email response -> {data}")
    return data.get("list", []), data.get("seq", seq)

def fetch_email(session, mail_id, sid_token):
    params = {'f': 'fetch_email', 'email_id': mail_id, 'sid_token': sid_token}
    response = session.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(Fore.BLUE + f"DEBUG: fetch_email response -> {data}")
    return html.unescape(data.get('mail_body', 'No content'))

def generate_mail():
    print(Fore.YELLOW + "[!] Generating email, please wait...")
    time.sleep(1.5)
    
    session = requests.Session()
    email_address, sid_token = get_email_address(session)

    if email_address:
        print(Fore.GREEN + f"[+] Email generated: {email_address}")
    else:
        print(Fore.RED + "[!] Failed to generate email. Please try again.")
        return

    print(Fore.YELLOW + "[!] Waiting for messages... (This may take a few minutes)")
    seq = 0
    time.sleep(5)

    while True:
        messages, seq = check_email(session, sid_token, seq)
        
        if messages:
            for msg in messages:
                mail_id = msg.get('mail_id')
                mail_from = msg.get('mail_from', 'Unknown')
                mail_subject = msg.get('mail_subject', 'No Subject')

                print(Fore.CYAN + f"\n[+] New message from {mail_from}:")
                print(Fore.WHITE + f"Subject: {mail_subject}")
                
                mail_content = fetch_email(session, mail_id, sid_token)
                print(Fore.WHITE + mail_content)
                
                # Wait for the next check without returning to the root menu
                time.sleep(2)
        else:
            print(Fore.YELLOW + "[!] No new messages yet. Checking again in 15 seconds...")
            time.sleep(15)  # Recheck every 15 seconds

while True:
    opc = Write.Input('\nroot@mail>> ', Colors.blue_to_white)
    if opc.strip() == '1':
        generate_mail()  # Generate mail and wait for new messages
    elif opc.strip() == '2':
        print(Fore.GREEN + "Exiting...")
        break
    else:
        print(Fore.RED + "Invalid option!")
