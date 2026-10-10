# DNS Resolver

CMPU 4050 Systems Integration Assignment 1.

This project implements a DNS resolver in Python using the provided
DNS starter code.

## Current Progress

- Project setup complete
- DNS query construction implemented
- DNS query serialization implemented
- UDP DNS communication implemented
- DNS response parsing implemented
- IPv4 A record resolution implemented
- Command-line domain input implemented
- IPv6 AAAA record resolution implemented
- CNAME record handling implemented

## Current Output

The resolver currently displays:

- Canonical names from CNAME records
- IPv4 addresses from A records
- IPv6 addresses from AAAA records
- Basic DNS error message upon a failed lookup

### Example

```text
Canonical names for www.tudublin.ie :
CNAME: tudublinie-lb01-production.terminalfour.net

IPv4 addresses for www.tudublin.ie :
IPv4: 52.17.166.15
IPv4: 63.32.192.231

## Supported Record Types

- A
- AAAA
- CNAME


## Usage

Run the resolver with:

```bash
python resolver.py <domain>
