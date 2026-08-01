<div align="center">

```
  ██████╗ ███████╗██╗███╗  ██╗████████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
 ██╔═══██╗██╔════╝██║████╗ ██║╚══██╔══╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝
 ██║   ██║███████╗██║██╔██╗██║   ██║   ███████║███████║██║ █╗ ██║█████╔╝ 
 ██║   ██║╚════██║██║██║╚████║   ██║   ██╔══██║██╔══██║██║███╗██║██╔═██╗ 
 ╚██████╔╝███████║██║██║ ╚███║   ██║   ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
```

**🦅 Automated OSINT Reconnaissance Framework**

[![Python](https://img.shields.io/badge/Python_3.8+-orange?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Modules](https://img.shields.io/badge/7_Recon_Modules-FF8C00?style=flat-square)]()
[![Zero_Deps](https://img.shields.io/badge/Zero_Dependencies-stdlib_only-success?style=flat-square)]()
[![License](https://img.shields.io/badge/MIT-gray?style=flat-square)](LICENSE)

*Hunt from the sky. See everything. Leave no trace.*

</div>

---

## 🎯 Mission

OsintHawk is a single-file OSINT reconnaissance tool that chains 7 intelligence-gathering modules into one clean CLI workflow. No API keys required for core features. No pip install needed.

```
$ python osinthawk.py -d target.com

[whois]      → Registrar, creation date, expiry, nameservers
[dns]        → A, AAAA, MX, NS, TXT, CNAME, SOA records  
[subdomains] → 75-word multithreaded brute-force → 12 live found
[ip]         → IP: 93.184.216.34 | US | Edgecast | AS15133
[ports]      → 80/HTTP ✓  443/HTTPS ✓  22/SSH ✗  3306 ✗
[emails]     → Found via crt.sh: admin@target.com
[tech]       → Nginx 1.24, Cloudflare, React
```

---

## 🚀 One-Line Start

```bash
git clone https://github.com/SRINIVASAN55/OsintHawk && cd OsintHawk

python osinthawk.py -d example.com                   # Full recon
python osinthawk.py -d example.com -m whois dns      # Pick modules
python osinthawk.py -d example.com -t 100 -o out.json # 100 threads, save JSON
```

---

## 🧩 Module Map

```
OsintHawk
├── whois       ── Socket-based WHOIS via whois.iana.org
├── dns         ── dig fallback → socket for A records  
├── subdomains  ── ThreadPoolExecutor, 75-word wordlist
├── ip          ── ip-api.com: geo, ISP, ASN, timezone
├── ports       ── 20 common ports, 1.5s timeout each
├── emails      ── Certificate Transparency via crt.sh
└── tech        ── Header + body signature fingerprinting
```

---

## 📦 Output

All results saved as structured JSON — pipe into other tools or SIEMs:

```json
{
  "target": "example.com",
  "subdomains": [{"subdomain": "api.example.com", "ip": "93.184.216.35"}],
  "ports": [{"port": 443, "service": "HTTPS"}],
  "tech_hints": ["Nginx", "Cloudflare", "React"]
}
```

---

> ⚠️ Use only on domains you own or have authorization to test. Respect rate limits.

<p align="center">
  <a href="https://github.com/SRINIVASAN55">SRINIVASAN55</a> ·
  <a href="https://linkedin.com/in/srinivasan132">LinkedIn</a>
</p>
