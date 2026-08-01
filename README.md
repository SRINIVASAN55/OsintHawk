<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=24&height=80&text=🦅%20OsintHawk&fontSize=34&fontColor=ffffff" width="100%"/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OSINT](https://img.shields.io/badge/OSINT-Recon-orange?style=for-the-badge)]()
[![No Dependencies](https://img.shields.io/badge/stdlib-only-green?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**Automated OSINT Reconnaissance Framework — runs entirely on Python stdlib.**  
DNS enumeration, WHOIS, subdomain discovery, port scanning, email harvesting, technology fingerprinting, and IP geolocation in one CLI tool.

</div>

---

## ✨ Modules

| Module | What it does |
|---|---|
| 🔍 `whois` | WHOIS lookup — registrar, dates, nameservers, registrant |
| 🌐 `dns` | DNS record enumeration (A, AAAA, MX, NS, TXT, CNAME, SOA) |
| 🕸️ `subdomains` | Multithreaded subdomain enumeration (75+ wordlist) |
| 📍 `ip` | IP geolocation, ASN, ISP via ip-api.com |
| 🔌 `ports` | Common port scan (20 ports: SSH, HTTP, MySQL, Redis, etc.) |
| 📧 `emails` | Email discovery via certificate transparency (crt.sh) |
| 🛠️ `tech` | Technology fingerprinting (WordPress, React, Nginx, Cloudflare…) |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/SRINIVASAN55/OsintHawk.git
cd OsintHawk

# Run full recon (no pip install needed — stdlib only)
python osinthawk.py -d example.com

# Run specific modules only
python osinthawk.py -d example.com -m whois dns subdomains

# Save JSON report
python osinthawk.py -d target.com -o recon_report.json

# High-speed subdomain scan with 100 threads
python osinthawk.py -d company.com -t 100
```

---

## 📋 CLI Options

```
  -d DOMAIN   --domain    Target domain (required)
  -m MODULES  --modules   Modules to run: whois dns subdomains ip ports emails tech
  -t THREADS  --threads   Threads for subdomain scan (default: 50)
  -o OUTPUT   --output    JSON report output path
```

---

## 📊 Sample Output

```
  ██████╗ ███████╗██╗███╗   ██╗████████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
  ...
  OSINT Reconnaissance Framework v1.0

[*] Target: example.com

[+] WHOIS Lookup...
    Registrar:       ICANN
    Creation Date:   1995-08-14

[+] Subdomain Enumeration (75 wordlist)...
    ✓ www.example.com              → 93.184.216.34
    ✓ mail.example.com             → 93.184.216.35
    ✓ api.example.com              → 93.184.216.36

[+] Common Port Scan...
    ✓ 80     HTTP
    ✓ 443    HTTPS

══════════════════════════════════════════
  SUMMARY — example.com
══════════════════════════════════════════
  Subdomains found : 3
  Open ports       : 2
  Emails found     : 1
  Tech detected    : Nginx, Cloudflare
```

---

## ⚠️ Legal Notice

> Use OsintHawk only on domains you own or have explicit authorization to test.  
> All data collected is from public sources. Respect rate limits and laws.

---

## 📄 License

MIT License © 2024 [Srinivasan S](https://github.com/SRINIVASAN55)
