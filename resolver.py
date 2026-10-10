import random
import socket
import sys
import ipaddress
from DNSStarter import (
    DNSHeader, DNSQuestion, DNSDatagram, write_datagram, read_datagram,
    )


# DNS server used by this resolver.
# Change this value if a different DNS server should be used.
DNS_SERVER = "8.8.8.8"


def build_query(domain, qtype):
    labels = domain.split(".")

    transaction_id = random.randint(0, 65535)

    header = DNSHeader(
        ident=transaction_id,
        qr=0,
        opcode=0,
        aa=0,
        tc=0,
        rd=1,
        ra=0,
        z=0,
        rcode=0,
        qdcount=1,
        ancount=0,
        nscount=0,
        arcount=0
    )

    question = DNSQuestion(
        name=labels,
        qtype=qtype,
        qclass=1
    )

    return DNSDatagram(
        header=header,
        questions=[question],
        answers=[]
    
    )


def send_query(query):
    raw_query = write_datagram(query)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(raw_query, (DNS_SERVER, 53))

    response, _ = sock.recvfrom(512)

    sock.close()

    return response


def format_ipv4(rdata):
    return ".".join(str(byte) for byte in rdata)


def format_ipv6(rdata):
    return str(ipaddress.IPv6Address(bytes(rdata)))


#not required by the assignment, added for testing purposes
#check that exactly one domain was provided
if len(sys.argv) != 2:
    print("Usage: python resolver.py <domain>")
    sys.exit(1)

domain = sys.argv[1]

query = build_query(domain, 1)

response = send_query(query)

datagram = read_datagram(response)

if datagram.header.rcode != 0:
    print("DNS lookup failed. Response code:", datagram.header.rcode)
    sys.exit(1)

cname_answers = [
    answer for answer in datagram.answers
    if answer.type == 5
]

ipv4_answers = [
    answer for answer in datagram.answers
    if answer.type == 1
]

if cname_answers:
    print("\nCanonical names for", domain, ":")

    for answer in cname_answers:
        cname_labels = answer.cname_as_array_list(datagram)
        cname = ".".join(cname_labels)
        print("CNAME:", cname)

if ipv4_answers:
    print("\nIPv4 addresses for", domain, ":")

    for answer in ipv4_answers:
        print("IPv4:", format_ipv4(answer.rdata))



ipv6_query = build_query(domain, 28)

ipv6_response = send_query(ipv6_query)

ipv6_datagram = read_datagram(ipv6_response)

if ipv6_datagram.header.rcode != 0:
    print("IPv6 DNS lookup failed. Response code:", ipv6_datagram.header.rcode)

ipv6_answers = [
    answer for answer in ipv6_datagram.answers
    if answer.type == 28
]

if ipv6_answers:
    print("\nIPv6 addresses for", domain, ":")

    for answer in ipv6_answers:
        print("IPv6:", format_ipv6(answer.rdata))