#!/usr/bin/env python
from dns.resolver import query as domain_query
from dns.exception import DNSException

FILENAME = 'disposable-email-domains.txt'
DOMAINS = [ ]

with open(FILENAME) as f:
    for domain in f:
        d = domain.strip()
        d = d.strip('.')

        try:
            for _ in domain_query(d, 'MX'):
                DOMAINS.append(domain)
                print '+', d
                break
        except DNSException:
            print '-', d

with open(FILENAME, 'w') as f:
    f.write(''.join(DOMAINS))
