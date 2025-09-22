#!/usr/bin/env python3
"""
Obsidian Waitlist Auto-Signup Script (ForestArmy Edition)
Automatically generates random word+number codes & emails for Obsidian waitlist API
"""

import requests
import random
import string
import time
from typing import Dict, Optional
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class ObsidianWaitlistBot:
    def __init__(self, inviter_code: str):
        self.base_url = "https://obsidian.build"
        self.api_endpoint = f"{self.base_url}/api/waitlist"
        self.inviter_code = inviter_code
        self.session = requests.Session()
        
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'origin': 'https://obsidian.build',
            'referer': f'https://obsidian.build/?code={inviter_code}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/130.0.0.0 Safari/537.36'
        }
        self.session.headers.update(self.headers)

    def generate_random_email(self) -> str:
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'protonmail.com']
        domain = random.choice(domains)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
        return f"{username}@{domain}"

    def generate_random_word(self, length: int = None) -> str:
        """Generate a random pronounceable word"""
        vowels = "aeiou"
        consonants = "".join(set(string.ascii_lowercase) - set(vowels))
        if length is None:
            length = random.randint(4, 8)
        word = ""
        for i in range(length):
            if i % 2 == 0:
                word += random.choice(consonants)
            else:
                word += random.choice(vowels)
        return word.upper()

    def generate_word_number_code(self) -> str:
        """Random word + number code"""
        word = self.generate_random_word(random.randint(4, 7))
        number = str(random.randint(10, 9999))
        return f"{word}{number}"

    def submit_to_waitlist(self, email: str, custom_code: str) -> Optional[Dict]:
        payload = {
            "email": email,
            "inviterCode": self.inviter_code,
            "customCode": custom_code
        }
        try:
            r = self.session.post(self.api_endpoint, json=payload, timeout=30)
            if r.status_code == 201:
                return r.json()
            else:
                print(f"{Fore.RED}{Style.BRIGHT}❌ Error {r.status_code}: {r.text}")
                return None
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}❌ Request failed: {e}")
            return None

    def run_bulk(self, limit: Optional[int] = None, delay: float = 2.0):
        count = 0
        while True:
            count += 1
            email = self.generate_random_email()
            code = self.generate_word_number_code()

            print(f"\n{Fore.BLUE}{Style.BRIGHT}📝 Attempt {count}:")
            print(f"{Fore.WHITE}  📧 Email: {Fore.CYAN}{email}")
            print(f"{Fore.WHITE}  🔑 Code: {Fore.YELLOW}{code}")
            print(f"{Fore.WHITE}  👥 Referrer: {Fore.GREEN}{self.inviter_code}")

            result = self.submit_to_waitlist(email, code)
            if result and result.get("ok"):
                print(f"{Fore.GREEN}{Style.BRIGHT}  ✅ SUCCESS! Rank: {Fore.MAGENTA}{result.get('rank','N/A')}")
            else:
                print(f"{Fore.RED}{Style.BRIGHT}  ❌ FAILED")

            if limit and count >= limit:
                print(f"{Fore.CYAN}{Style.BRIGHT}\n🎯 Reached target of {limit} referrals. Stopping.")
                break

            time.sleep(delay)

def display_banner():
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║        🌟 OBSIDIAN WAITLIST AUTO-SIGNUP TOOL 🌟              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Fore.CYAN}{Style.BRIGHT}             ⚡ POWERED BY: {Fore.YELLOW}FORESTARMY ⚡\n")

def main():
    display_banner()
    ref_code = input(f"{Fore.CYAN}{Style.BRIGHT}Enter Your Referrer Code: {Style.RESET_ALL}").strip().upper()
    referrals = input(f"{Fore.CYAN}{Style.BRIGHT}How Many Referral You Want (number or unlimited): {Style.RESET_ALL}").strip()

    try:
        limit = int(referrals)
    except ValueError:
        limit = None  # unlimited

    bot = ObsidianWaitlistBot(inviter_code=ref_code)
    bot.run_bulk(limit=limit, delay=2)

if __name__ == "__main__":
    main()
