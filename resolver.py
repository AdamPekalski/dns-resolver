import random

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


query = build_query("google.com", 1)

raw_query = write_datagram(query)

print(query.header.ident)
print(query.questions[0].name)
print(query.questions[0].qtype)
print(raw_query)
