import random
import socket
from DNSStarter import DNSHeader, DNSQuestion, DNSDatagram, write_datagram


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


query = build_query("google.com", 1)

response = send_query(query)

print(response)
