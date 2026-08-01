#!/usr/bin/env python3
"""
OsintHawk - Automated OSINT Reconnaissance Framework
Author: Srinivasan S (SRINIVASAN55)
Performs DNS enumeration, WHOIS, subdomain discovery, email harvesting, and more.
"""

import sys
import json
import socket
import argparse
import urllib.request
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── ANSI Colors ─────────────────────────────────────────────────────────────
class C:
    RED    = "\033[91m"; GREEN  = "\033[92m"; YELLOW = "\033[93m"
    CYAN   = "\033[96m"; BLUE   = "\033[94m"; BOLD   = "\033[1m"; RESET  = "\033[0m"

BANNER = f"""{C.GREEN}{C.BOLD}
  ██████╗ ███████╗██╗███╗   ██╗████████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
  ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝
  ██║   ██║███████╗██║██╔██╗ ██║   ██║   ███████║███████║██║ █╗ ██║█████╔╝
  ██║   ██║╚════██║██║██║╚██╗██║   ██║   ██╔══██║██╔══██║██║███╗██║██╔═██╗
  ╚██████╔╝███████║██║██║ ╚████║   ██║   ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
                    OSINT Reconnaissance Framework v1.0
                         Author: SRINIVASAN55
{C.RESET}"""

COMMON_SUBDOMAINS = [
    "www","mail","ftp","remote","blog","webmail","server","ns1","ns2","smtp","secure",
    "vpn","api","dev","staging","test","portal","admin","login","app","cdn","static",
    "media","img","images","assets","shop","store","support","help","docs","git","gitlab",
    "jenkins","ci","jira","confluence","dashboard","monitor","status","m","mobile",
    "forum","community","wiki","news","old","new","beta","alpha","demo","sandbox",
    "mx","pop","pop3","imap","exchange","autodiscover","cpanel","whm","webdisk",
]

DNS_RECORD_TYPES = ["A","AAAA","MX","NS","TXT","CNAME","SOA"]

class OsintHawk:
    def __init__(self, domain: str, threads: int = 50, output: str = None):
        self.domain   = domain.lower().strip()
        self.threads  = threads
        self.output   = output
        self.results  = {
            "target": self.domain,
            "timestamp": datetime.now().isoformat(),
            "whois": {}, "dns": {}, "subdomains": [],
            "ip_info": {}, "emails": [], "tech_hints": [], "ports": []
        }

    def _log(self, msg, color="", end="\n"):
        print(f"{color}{msg}{C.RESET}", end=end, flush=True)

    # ── WHOIS (uses IANA whois server) ────────────────────────────────────────
    def run_whois(self):
        self._log("\n[+] Running WHOIS Lookup...", C.GREEN)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect(("whois.iana.org", 43))
            sock.send(f"{self.domain}\r\n".encode())
            raw = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk: break
                raw += chunk
            sock.close()
            text = raw.decode(errors="ignore")
            parsed = {}
            for line in text.splitlines():
                for key in ["registrar","creation date","updated date","expiry date",
                            "name server","registrant","status","registrant email"]:
                    if line.lower().startswith(key):
                        field, _, val = line.partition(":")
                        if val.strip():
                            parsed[field.strip().title()] = val.strip()
            self.results["whois"] = parsed if parsed else {"raw_preview": text[:800]}
            for k, v in (self.results["whois"] if isinstance(self.results["whois"], dict) else {}).items():
                self._log(f"    {k}: {v}", C.CYAN)
        except Exception as e:
            self._log(f"    WHOIS failed: {e}", C.YELLOW)
            self.results["whois"] = {"error": str(e)}

    # ── DNS Records ───────────────────────────────────────────────────────────
    def run_dns(self):
        self._log("\n[+] DNS Record Enumeration...", C.GREEN)
        found = {}
        for rtype in DNS_RECORD_TYPES:
            try:
                import subprocess
                result = subprocess.run(
                    ["dig", "+short", rtype, self.domain],
                    capture_output=True, text=True, timeout=5
                )
                records = [r.strip() for r in result.stdout.strip().splitlines() if r.strip()]
                if records:
                    found[rtype] = records
                    self._log(f"    {rtype:6s}: {', '.join(records)}", C.CYAN)
            except Exception:
                # Fallback: socket for A record
                if rtype == "A":
                    try:
                        ip = socket.gethostbyname(self.domain)
                        found["A"] = [ip]
                        self._log(f"    A     : {ip}", C.CYAN)
                    except Exception:
                        pass
        self.results["dns"] = found

    # ── Subdomain Enumeration ─────────────────────────────────────────────────
    def run_subdomain_enum(self):
        self._log(f"\n[+] Subdomain Enumeration ({len(COMMON_SUBDOMAINS)} wordlist)...", C.GREEN)
        found = []

        def check_sub(sub):
            fqdn = f"{sub}.{self.domain}"
            try:
                ip = socket.gethostbyname(fqdn)
                return (fqdn, ip)
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = {ex.submit(check_sub, s): s for s in COMMON_SUBDOMAINS}
            for fut in as_completed(futures):
                res = fut.result()
                if res:
                    fqdn, ip = res
                    found.append({"subdomain": fqdn, "ip": ip})
                    self._log(f"    ✓ {fqdn:<45} → {ip}", C.GREEN)

        self.results["subdomains"] = found
        self._log(f"\n    Found {len(found)} live subdomains", C.BOLD)

    # ── IP Geolocation & ASN ──────────────────────────────────────────────────
    def run_ip_info(self):
        self._log("\n[+] IP Geolocation & ASN Lookup...", C.GREEN)
        try:
            ip = socket.gethostbyname(self.domain)
            url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,lat,lon,timezone"
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.loads(r.read())
            self.results["ip_info"] = data
            self._log(f"    IP      : {ip}", C.CYAN)
            self._log(f"    Country : {data.get('country','?')} / {data.get('regionName','?')} / {data.get('city','?')}", C.CYAN)
            self._log(f"    ISP     : {data.get('isp','?')}", C.CYAN)
            self._log(f"    ASN     : {data.get('as','?')}", C.CYAN)
            self._log(f"    Timezone: {data.get('timezone','?')}", C.CYAN)
        except Exception as e:
            self._log(f"    IP info failed: {e}", C.YELLOW)

    # ── Port Scan (common ports) ───────────────────────────────────────────────
    def run_port_scan(self):
        self._log("\n[+] Common Port Scan...", C.GREEN)
        PORTS = {
            21:"FTP", 22:"SSH", 23:"Telnet", 25:"SMTP", 53:"DNS",
            80:"HTTP", 110:"POP3", 143:"IMAP", 443:"HTTPS", 465:"SMTPS",
            993:"IMAPS", 995:"POP3S", 3306:"MySQL", 3389:"RDP",
            5432:"PostgreSQL", 6379:"Redis", 8080:"HTTP-Alt", 8443:"HTTPS-Alt",
            27017:"MongoDB", 9200:"Elasticsearch"
        }
        open_ports = []
        try:
            ip = socket.gethostbyname(self.domain)
        except Exception:
            return

        def check_port(p):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            try:
                s.connect((ip, p))
                s.close()
                return p
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = {ex.submit(check_port, p): p for p in PORTS}
            for fut in as_completed(futures):
                port = fut.result()
                if port:
                    service = PORTS[port]
                    open_ports.append({"port": port, "service": service})
                    self._log(f"    ✓ {port:<6} {service}", C.GREEN)

        self.results["ports"] = sorted(open_ports, key=lambda x: x["port"])
        if not open_ports:
            self._log("    No common ports found open", C.YELLOW)

    # ── Email Harvesting (via crt.sh) ─────────────────────────────────────────
    def run_email_harvest(self):
        self._log("\n[+] Email Pattern Discovery (via Certificate Transparency)...", C.GREEN)
        try:
            url = f"https://crt.sh/?q=%25%40{self.domain}&output=json"
            req = urllib.request.Request(url, headers={"User-Agent": "OsintHawk/1.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                certs = json.loads(r.read())
            emails = set()
            for cert in certs:
                name = cert.get("name_value","")
                if "@" in name:
                    for part in name.split("\n"):
                        if "@" in part and self.domain in part:
                            emails.add(part.strip().lower())
            self.results["emails"] = list(emails)
            for e in emails:
                self._log(f"    ✉  {e}", C.CYAN)
            if not emails:
                self._log("    No emails found in certificates", C.YELLOW)
        except Exception as e:
            self._log(f"    Email harvest failed: {e}", C.YELLOW)

    # ── Web Tech Hints ────────────────────────────────────────────────────────
    def run_tech_detection(self):
        self._log("\n[+] Web Technology Detection...", C.GREEN)
        hints = []
        try:
            req = urllib.request.Request(f"https://{self.domain}", headers={"User-Agent": "OsintHawk/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=10) as r:
                    headers = dict(r.info())
                    body = r.read(8192).decode(errors="ignore")
            except Exception:
                req = urllib.request.Request(f"http://{self.domain}", headers={"User-Agent": "OsintHawk/1.0"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    headers = dict(r.info())
                    body = r.read(8192).decode(errors="ignore")

            tech_signatures = {
                "WordPress": ["wp-content", "wp-includes", "WordPress"],
                "Drupal": ["Drupal", "drupal.org"],
                "Joomla": ["Joomla", "com_content"],
                "React": ["react.js", "_next/", "__next"],
                "Angular": ["ng-version", "angular"],
                "Vue.js": ["vue.js", "__vue__"],
                "PHP": ["X-Powered-By: PHP", ".php"],
                "ASP.NET": ["X-Powered-By: ASP.NET", "__VIEWSTATE"],
                "Nginx": ["nginx"],
                "Apache": ["Apache"],
                "Cloudflare": ["cf-ray", "cloudflare"],
                "jQuery": ["jquery"],
            }
            server = headers.get("Server","") or headers.get("server","")
            if server:
                hints.append(f"Server: {server}")
                self._log(f"    Server: {server}", C.CYAN)
            powered = headers.get("X-Powered-By","") or headers.get("x-powered-by","")
            if powered:
                hints.append(f"X-Powered-By: {powered}")
                self._log(f"    X-Powered-By: {powered}", C.CYAN)
            for tech, sigs in tech_signatures.items():
                if any(s.lower() in body.lower() or s.lower() in str(headers).lower() for s in sigs):
                    hints.append(tech)
                    self._log(f"    ✓ {tech}", C.GREEN)
        except Exception as e:
            self._log(f"    Tech detection error: {e}", C.YELLOW)
        self.results["tech_hints"] = hints

    # ── Report ────────────────────────────────────────────────────────────────
    def save_report(self):
        fname = self.output or f"osinthawk_{self.domain.replace('.','_')}_{int(datetime.now().timestamp())}.json"
        with open(fname, "w") as f:
            json.dump(self.results, f, indent=2)
        self._log(f"\n[✓] Report saved: {fname}", C.GREEN)
        return fname

    def print_summary(self):
        r = self.results
        print(f"\n{C.BOLD}{'═'*55}{C.RESET}")
        print(f"{C.BOLD}  OSINTHAWK SUMMARY — {r['target']}{C.RESET}")
        print(f"{C.BOLD}{'═'*55}{C.RESET}")
        print(f"  Subdomains found : {len(r['subdomains'])}")
        print(f"  DNS records      : {len(r['dns'])} types")
        print(f"  Open ports       : {len(r['ports'])}")
        print(f"  Emails found     : {len(r['emails'])}")
        print(f"  Tech detected    : {len(r['tech_hints'])}")
        if r['ip_info']:
            ip_data = r['ip_info']
            print(f"  Location         : {ip_data.get('city','?')}, {ip_data.get('country','?')}")
            print(f"  ASN              : {ip_data.get('as','?')}")
        print(f"{C.BOLD}{'═'*55}{C.RESET}\n")

    # ── Main ─────────────────────────────────────────────────────────────────
    def run(self, modules=None):
        print(BANNER)
        self._log(f"[*] Target : {self.domain}", C.BOLD)
        self._log(f"[*] Started: {self.results['timestamp']}\n", C.BOLD)
        all_modules = {
            "whois": self.run_whois, "dns": self.run_dns,
            "subdomains": self.run_subdomain_enum, "ip": self.run_ip_info,
            "ports": self.run_port_scan, "emails": self.run_email_harvest,
            "tech": self.run_tech_detection,
        }
        active = modules if modules else list(all_modules.keys())
        for mod in active:
            if mod in all_modules:
                try: all_modules[mod]()
                except Exception as e: self._log(f"  Module {mod} error: {e}", C.YELLOW)
        self.print_summary()
        self.save_report()

def main():
    parser = argparse.ArgumentParser(
        description="OsintHawk — Automated OSINT Reconnaissance Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python osinthawk.py -d example.com
  python osinthawk.py -d target.com -m whois dns subdomains
  python osinthawk.py -d company.com -t 100 -o report.json
        """
    )
    parser.add_argument("-d","--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("-m","--modules", nargs="+",
                        choices=["whois","dns","subdomains","ip","ports","emails","tech"],
                        help="Modules to run (default: all)")
    parser.add_argument("-t","--threads", type=int, default=50, help="Threads for subdomain scan (default: 50)")
    parser.add_argument("-o","--output", help="Output JSON file path")
    args = parser.parse_args()
    hawk = OsintHawk(domain=args.domain, threads=args.threads, output=args.output)
    hawk.run(modules=args.modules)

if __name__ == "__main__":
    main()
