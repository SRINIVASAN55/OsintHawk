# OsintHawk

> "Give me a domain. I'll give you its attack surface."

OsintHawk is an open-source intelligence gathering tool that aggregates public data across DNS, subdomains, WHOIS, certificate transparency logs, email breach databases, and more — building a structured recon profile from a single domain name.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Python | 3.8 or higher |
| OS | Linux, macOS, Windows |
| Internet | Required (queries public DNS, crt.sh, WHOIS servers) |

```bash
python3 --version    # must be 3.8+
```

---

## Installation

```bash
git clone https://github.com/SRINIVASAN55/OsintHawk.git
cd OsintHawk
pip install -r requirements.txt
```

---

## Running It

### Basic recon — point at any domain
```bash
python3 osinthawk.py --domain example.com
python3 osinthawk.py -d tesla.com
python3 osinthawk.py -d target.org
```
Runs all default modules: subdomain enumeration, DNS records, WHOIS, certificate transparency search.

### Run specific modules only
```bash
# Only subdomains and DNS
python3 osinthawk.py -d example.com --modules subdomains dns

# Only WHOIS info
python3 osinthawk.py -d example.com --modules whois

# Only SSL/TLS certificate recon
python3 osinthawk.py -d example.com --modules certs
```

Available modules: `subdomains`, `dns`, `whois`, `certs`, `emails`, `ports`

### Control scan speed with threads
```bash
# Faster scan — more threads (default is 50)
python3 osinthawk.py -d example.com --threads 100

# Slower, quieter scan
python3 osinthawk.py -d example.com --threads 10
```

### Save results to a JSON file
```bash
python3 osinthawk.py -d example.com --output results.json
python3 osinthawk.py -d example.com -o /tmp/osint_report.json
```

---

## All CLI Flags

| Flag | Short | Description | Default | Example |
|------|-------|-------------|---------|---------|
| `--domain` | `-d` | Target domain **(required)** | — | `-d example.com` |
| `--modules` | `-m` | Specific modules to run (space-separated) | all | `-m subdomains dns` |
| `--threads` | `-t` | Threads for subdomain scan | `50` | `-t 100` |
| `--output` | `-o` | Save results to JSON file | — | `-o out.json` |

---

## Sample Output

```
[DOMAIN] example.com
─────────────────────────────────────────────────
[DNS]
  A      → 93.184.216.34
  MX     → 0 mail.example.com
  NS     → a.iana-servers.net, b.iana-servers.net
  TXT    → v=spf1 -all

[WHOIS]
  Registrar  : IANA
  Created    : 1995-08-14
  Expires    : 2024-08-13
  Registrant : (redacted for privacy)

[SUBDOMAINS — 6 found]
  www.example.com       → 93.184.216.34
  mail.example.com      → 93.184.216.34
  dev.example.com       → 93.184.216.34  ⚠ exposed dev env
  staging.example.com   → 93.184.216.34
  api.example.com       → 93.184.216.34
  cdn.example.com       → 93.184.216.34

[CERTS — via crt.sh]
  *.example.com  — issued 2024-01-10, expires 2025-01-10
  dev.example.com — issued 2023-06-15 (may reveal internal names)
```

---

## Troubleshooting

**`Required argument --domain missing`**
→ OsintHawk always needs a target: `python3 osinthawk.py -d yourtarget.com`

**Scan is slow**
→ Increase threads: `--threads 100`. Or your internet/DNS is rate-limiting — try `--threads 20`.

**Connection errors / timeouts**
→ Some public WHOIS/DNS servers rate-limit. Wait 30s and retry, or lower thread count.

---

## Ethics

OsintHawk only accesses public information through legitimate channels (public DNS, crt.sh, WHOIS). Use it on your own domains, with explicit permission, or for authorized security assessments. Misuse is your responsibility.

---

**Author:** S. Srinivasan · [GitHub](https://github.com/SRINIVASAN55) · [LinkedIn](https://linkedin.com/in/srinivasan132)
