# DNS Resolver

CMPU 4050 Systems Integration Assignment 1.

## Student Details

**Name:** Adam Pekalski  
**Student Number:** C23475872

## Project Description

This project implements a DNS resolver in Python using the provided DNS starter code.

The resolver accepts a domain name from the command line and performs:

- IPv4 A record lookups
- IPv6 AAAA record lookups
- CNAME record handling

The resolver sends DNS requests using UDP and displays the returned results in human-readable form.

## Usage

Run the resolver with:

```bash
python resolver.py <domain>
```

### Example

```bash
python resolver.py google.com
```

## DNS Server

The resolver currently uses Google Public DNS:

```text
8.8.8.8
```

The DNS server is configured near the top of `resolver.py` using:

```python
DNS_SERVER = "8.8.8.8"
```

This value can be changed if a different DNS server needs to be used.

## Supported Record Types

- A
- AAAA
- CNAME

## Current Output

The resolver displays:

- Canonical names from CNAME records
- IPv4 addresses from A records
- IPv6 addresses from AAAA records
- Basic DNS error messages when a lookup fails

Empty record sections are not displayed.

## Implementation

### Implemented in `resolver.py`

The following resolver logic was implemented as part of this project:

- Reading the domain from the command line
- Splitting the domain into DNS labels
- Generating a random transaction ID
- Creating DNS queries using the starter code classes
- Sending DNS requests using UDP sockets
- Receiving DNS responses
- Requesting both A and AAAA records
- Detecting A, AAAA and CNAME answers
- Formatting IPv4 addresses
- Formatting IPv6 addresses
- Displaying CNAME records
- Basic DNS response code checking
- Formatting the final output

### Reused from `DNSStarter.py`

The provided starter code is used for DNS message creation and parsing.

The main starter code components used are:

- `DNSHeader`
- `DNSQuestion`
- `DNSDatagram`
- `DNSAnswer`
- `write_datagram()`
- `read_datagram()`
  
The starter code also uses the following internally when encoding and
decoding DNS packets:

- `DNSAnswer`
- `ByteArray`
- DNS name encoding and decoding
- Compressed DNS name handling

The resolver logic decides what DNS queries to make and how to display the answers, while the starter code handles DNS packet serialization and deserialization.

## Limitations and Special Notes

- The DNS server is hardcoded rather than discovered automatically.
- Recursive DNS resolution is handled by the configured DNS server.
- DNSSEC validation is not implemented.
- CNAME chains are not followed manually.
- Only basic error handling is implemented.
- DNS responses may differ between separate requests because DNS records can change due to caching and load balancing.

## Testing Summary

The resolver was tested using Google Public DNS at `8.8.8.8`.

### `google.com`

The resolver was run with:

```bash
python resolver.py google.com
```

Example output:

```text
IPv4 addresses for google.com :
IPv4: 74.125.193.101
IPv4: 74.125.193.100
IPv4: 74.125.193.138
IPv4: 74.125.193.102
IPv4: 74.125.193.113
IPv4: 74.125.193.139

IPv6 addresses for google.com :
IPv6: 2a00:1450:400b:c02::66
IPv6: 2a00:1450:400b:c02::71
IPv6: 2a00:1450:400b:c02::8b
IPv6: 2a00:1450:400b:c02::8a
```

The results were compared with:

```bash
$ dig @8.8.8.8 +short google.com A
209.85.203.139
209.85.203.102
209.85.203.101
209.85.203.100
209.85.203.138
209.85.203.113
$ dig @8.8.8.8 +short google.com AAAA
2a00:1450:400b:c02::66
2a00:1450:400b:c02::8b
2a00:1450:400b:c02::71
2a00:1450:400b:c02::8a
```

The resolver returned valid IPv4 A records and IPv6 AAAA records.

The IPv6 results matched the `dig` output, although the order of the addresses was different.

The IPv4 results differed between some queries. DNS responses may vary between requests due to caching, load balancing, and different responses over time.

### `www.tudublin.ie`

Command:

```bash
python resolver.py www.tudublin.ie
```

Example output:

```text
Canonical names for www.tudublin.ie :
CNAME: tudublinie-lb01-production.terminalfour.net

IPv4 addresses for www.tudublin.ie :
IPv4: 52.17.166.15
IPv4: 63.32.192.231
```

This test confirmed that CNAME records are detected and displayed.

### `ipv6.google.com`

Command:

```bash
python resolver.py ipv6.google.com
```

Example output:

```text
Canonical names for ipv6.google.com :
CNAME: ipv6.l.google.com

IPv6 addresses for ipv6.google.com :
IPv6: 2a00:1450:400b:c03::64
IPv6: 2a00:1450:400b:c03::65
IPv6: 2a00:1450:400b:c03::66
IPv6: 2a00:1450:400b:c03::8b
```

This test confirmed that AAAA records are correctly requested and formatted.

### Non-existent Domain

Command:

```bash
python resolver.py this-domain-does-not-exist.invalid
```

Output:

```text
DNS lookup failed. Response code: 3
```

This test confirmed that the resolver checks the DNS response code and reports a failed lookup.