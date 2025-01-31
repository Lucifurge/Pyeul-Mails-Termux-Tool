import requests
import time
import json
from requests.cookies import RequestsCookieJar
from pystyle import Write, Colors
from colorama import Fore, init

init(autoreset=True)

Write.Print(r"""
█████  █   █  ████  █   █  █      ███   ██  █████  ███  █    ████
█    █  █  █  █     █   █  █      █  ███ █  █   █   █   █    ██
█████    █    ███   █   █  █      █      █  █████   █   █      ██
█       █     ███    ███   ████   █      █  █   █  ███  ███  ████

\n\n[1] Generate Mail
""", Colors.blue_to_white, interval=0.0001)

# Guerrilla Mail API base URL
BASE_URL = "http://api.guerrillamail.com/ajax.php"

# Function to get a new email address and session
def get_email_address(session):
    params = {
        'f': 'get_email_address',
        'ip': '127.0.0.1',
        'agent': 'Mozilla'
    }
    response = session.get(BASE_URL, params=params)
    return response.json()

# Function to check for new emails
def check_email(session, seq):
    params = {
        'f': 'check_email',
        'seq': seq,
        'ip': '127.0.0.1',
        'agent': 'Mozilla'
    }
    response = session.get(BASE_URL, params=params)
    return response.json()

# Function to fetch the content of an email
def fetch_email(session, mail_id):
    params = {
        'f': 'fetch_email',
        'email_id': mail_id,
        'ip': '127.0.0.1',
        'agent': 'Mozilla'
    }
    response = session.get(BASE_URL, params=params)
    return response.json()

def generate_mail():
    print(Fore.YELLOW + "[!] Generating email, please wait...")
    time.sleep(1.5)

    # Create a session with cookie handling
    session = requests.Session()
    
    # Step 1: Initialize a session and get an email address
    email_data = get_email_address(session)
    email_address = email_data.get("email_addr", "")
    email_timestamp = email_data.get("email_timestamp", "")

    if email_address:
        print(Fore.GREEN + f"[+] Email generated: {email_address}")
    else:
        print(Fore.RED + "[!] Failed to generate email. Please try again.")
        return

    print(Fore.YELLOW + "[!] Waiting for messages...")
    time.sleep(2)

    while True:
        try:
            # Step 2: Check for new emails
            check_data = check_email(session, email_timestamp)
            print(Fore.BLUE + f"DEBUG: check_email response -> {check_data}")

            if "list" in check_data:
                messages_data = check_data["list"]
            else:
                messages_data = []

            if messages_data:
                for msg in messages_data:
                    mail_id = msg['mail_id']
                    mail_from = msg['mail_from']
                    mail_subject = msg['mail_subject']

                    # Step 3: Fetch the message content
                    fetch_data = fetch_email(session, mail_id)
                    print(Fore.BLUE + f"DEBUG: fetch_email response -> {fetch_data}")
                    mail_content = fetch_data.get('mail_body', 'No content')

                    print(Fore.CYAN + f"\n[+] Message received from {mail_from}:")
                    print(Fore.WHITE + f"Subject: {mail_subject}")
                    print(Fore.WHITE + mail_content)
                    break
            else:
                print(Fore.YELLOW + "[!] No new messages yet. Checking again in 10 seconds...")
                time.sleep(10)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[!] Error: {e}")
            break
        except json.JSONDecodeError as e:
            print(Fore.RED + f"[!] JSON Decode Error: {e}")
            break

opc = Write.Input('\nroot@mail>> ', Colors.blue_to_white)
if opc.strip() == '1':
    generate_mail()
else:
    print(Fore.RED + "Invalid option!")
