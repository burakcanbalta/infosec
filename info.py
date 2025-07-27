
import requests
import re
import random
import time
import json
import sys
import threading
from urllib.parse import urlparse, parse_qs, urlencode
import urllib3
from colorama import Fore, Style
urllib3.disable_warnings()

class DBMSFingerprint:
    def __init__(self, target_url, proxies=None, headers=None, timeout=8, verbose=True, waf_bypass=False, delay=0):
        self.target_url = target_url
        self.timeout = timeout
        self.verbose = verbose
        self.waf_bypass = waf_bypass
        self.delay = delay
        self.headers = headers if headers else {
            'User-Agent': self.random_user_agent(),
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.proxies = proxies if proxies else {}
        self.payloads = {
            "MySQL": "'",
            "PostgreSQL": "'",
            "MSSQL": "'",
            "Oracle": "'",
            "SQLite": "'"
        }
        self.error_signatures = {
            "MySQL": ["You have an error in your SQL syntax", "MySQL server version for the right syntax"],
            "PostgreSQL": ["PostgreSQL.*ERROR", "pg_query\\(\\): Query failed"],
            "MSSQL": ["Microsoft SQL Server", "Unclosed quotation mark after the character string"],
            "Oracle": ["ORA-\\d+", "quoted string not properly terminated"],
            "SQLite": ["SQLite3::SQLException", "unrecognized token"]
        }

    def random_user_agent(self):
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (X11; Linux x86_64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        ]
        return random.choice(agents)

    def inject_payload(self, url, payload):
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        new_query = {}
        for key in query:
            p = payload
            if self.waf_bypass:
                p = f"%27{payload}%27"
            new_query[key] = query[key][0] + p
        injected_query = urlencode(new_query, doseq=True)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{injected_query}"

    def detect_for_db(self, dbms, payload, results, findings_lock):
        test_url = self.inject_payload(self.target_url, payload)
        if self.verbose:
            print(f"{Fore.CYAN}[?] Testing {dbms} payload on: {test_url}{Style.RESET_ALL}")
        try:
            if self.delay > 0:
                time.sleep(self.delay)
            response = requests.get(test_url, headers=self.headers, proxies=self.proxies, timeout=self.timeout, verify=False, allow_redirects=False)
            for sig in self.error_signatures[dbms]:
                if re.search(sig, response.text, re.IGNORECASE):
                    if self.verbose:
                        print(f"{Fore.GREEN}[+] {dbms} signature matched: {sig}{Style.RESET_ALL}")
                    with findings_lock:
                        results["findings"].append(dbms)
                        results["details"][dbms] = {
                            "payload": payload,
                            "signature": sig,
                            "url": test_url
                        }
                    break
        except requests.RequestException as e:
            if self.verbose:
                print(f"{Fore.RED}[-] Request failed for {dbms}: {str(e)}{Style.RESET_ALL}")

    def detect(self):
        threads = []
        results = {"findings": [], "details": {}}
        findings_lock = threading.Lock()
        for dbms, payload in self.payloads.items():
            t = threading.Thread(target=self.detect_for_db, args=(dbms, payload, results, findings_lock))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        if results["findings"]:
            output = {
                "url_tested": self.target_url,
                "dbms_detected": list(set(results["findings"])),
                "details": results["details"]
            }
            print(f"{Fore.YELLOW}[!] Muhtemelen kullanılan veritaban(lar)ı: {', '.join(output['dbms_detected'])}{Style.RESET_ALL}")
            with open("dbms_fingerprint_result.json", "w") as f:
                json.dump(output, f, indent=2)
        else:
            print(f"{Fore.MAGENTA}[-] Veritabanı tespit edilemedi.{Style.RESET_ALL}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Gelişmiş DBMS Fingerprint Tool")
    parser.add_argument("url", help="Hedef URL (örn: http://site.com/page.php?id=1)")
    parser.add_argument("--proxy", help="Proxy (örn: http://127.0.0.1:8080)", default=None)
    parser.add_argument("--waf-bypass", action="store_true", help="WAF bypass için encode edilmiş payload kullan")
    parser.add_argument("--delay", type=float, default=0, help="İstekler arası gecikme (saniye)")
    parser.add_argument("--silent", action="store_true", help="Çıktıyı sessize al (verbose kapalı)")
    args = parser.parse_args()

    if not args.url.startswith("http"):
        print(f"{Fore.RED}Geçersiz URL. http veya https ile başlamalı.{Style.RESET_ALL}")
        sys.exit(1)

    proxy_dict = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    fingerprint = DBMSFingerprint(
        args.url,
        proxies=proxy_dict,
        verbose=not args.silent,
        waf_bypass=args.waf_bypass,
        delay=args.delay
    )
    fingerprint.detect()
