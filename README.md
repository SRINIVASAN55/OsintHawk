# OsintHawk

> "Give me a username. I'll give you a person."

OsintHawk is an open-source intelligence gathering tool that aggregates public data across platforms — social media, DNS records, email breach databases, WHOIS, certificate transparency logs — and builds a structured profile from a single starting point: a username, email, domain, or IP.

---

## Starting points

| Input | What OsintHawk finds |
|-------|----------------------|
| Username | Matching accounts across 50+ platforms, profile metadata, activity patterns |
| Email | Breach history, associated accounts, domain ownership, MX records |
| Domain | WHOIS, DNS records, subdomains, SSL cert history, linked IPs, tech stack |
| IP | ASN, geolocation, reverse DNS, open ports, hosting provider, abuse reports |
| Phone | Country/carrier, linked accounts (where public), formatting variants |

---

## How it works

OsintHawk doesn't scrape. It queries APIs and public records that are meant to be queried — DNS resolvers, WHOIS servers, certificate transparency logs (crt.sh), HaveIBeenPwned, Shodan (with key), and platform-specific public endpoints.

Results are correlated. If a username appears on GitHub and a matching email appears in a breach, OsintHawk links them in the output graph.

---

## Usage

```bash
git clone https://github.com/SRINIVASAN55/OsintHawk
cd OsintHawk
pip install -r requirements.txt

# Investigate a username
python osinthawk.py --username johndoe

# Investigate a domain
python osinthawk.py --domain example.com

# Investigate an email
python osinthawk.py --email user@example.com

# Full report (all modules) → HTML output
python osinthawk.py --target johndoe --full --report
```

---

## Sample output

```
[USERNAME] johndoe
  ✓ GitHub        → github.com/johndoe (joined 2019, 47 repos, last active 3d ago)
  ✓ Twitter/X     → @johndoe (12k followers, location: "SF")
  ✓ HackerNews    → johndoe (karma: 4,231)
  ✓ Reddit        → u/johndoe (5y account, r/netsec regular)
  ✗ Instagram     → not found
  ✗ TikTok        → not found

[EMAIL CORRELATION]
  johndoe@gmail.com → found in 3 breaches (LinkedIn 2012, Adobe 2013, Dropbox 2012)
  Associated domains: johndoe.dev (registered 2021, WHOIS matches SF timezone)
```

---

## Ethics

OsintHawk only accesses public information through legitimate channels. Use it for your own accounts, with explicit consent, or for authorized security assessments. Misuse is your responsibility.

---

**Author:** S. Srinivasan · [GitHub](https://github.com/SRINIVASAN55) · [LinkedIn](https://linkedin.com/in/srinivasan132)
