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
if len(sys.argv) != 2:
    print("Usage: python resolver.py <domain>")
    sys.exit(1)

domain = sys.argv[1]

query = build_query(domain, 1)

response = send_query(query)

datagram = read_datagram(response)

print("Transaction ID:", datagram.header.ident)
print("QR:", datagram.header.qr)
print("Response code:", datagram.header.rcode)
print("Answer count:", datagram.header.ancount)

print("\nList of IPv4 addresses for", domain, ":")
for answer in datagram.answers:
    if answer.type == 1:
        print("IPv4:", format_ipv4(answer.rdata))


ipv6_query = build_query(domain, 28)

ipv6_response = send_query(ipv6_query)

ipv6_datagram = read_datagram(ipv6_response)

print("\nList of IPv6 addresses for", domain, ":")
for answer in ipv6_datagram.answers:
    if answer.type == 28:
        print("IPv6:", format_ipv6(answer.rdata))