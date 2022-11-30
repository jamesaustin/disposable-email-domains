#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor, as_completed as futures_as_completed

from dns.resolver import resolve as domain_resolve
from dns.exception import DNSException

FILENAME = "disposable-email-domains.txt"
DOMAINS = set()
INPUTS = set()

with open(FILENAME) as f:
    for d in f:
        d = d.strip()
        d = d.strip(".")
        INPUTS.add(d)


def test_domain(d):
    try:
        for _ in domain_resolve(d, "MX"):
            DOMAINS.add(d)
            return True
    except DNSException:
        pass
    return False


with ThreadPoolExecutor(max_workers=100) as executor:
    futures = {executor.submit(test_domain, d): d for d in INPUTS}
    for f in futures_as_completed(futures):
        d = futures[f]
        try:
            success = f.result()
        except Exception as e:
            error(f"# Failed: {d} -> {e}")
        else:
            if success:
                print(f"+ {d}")
            else:
                print(f"\033[31m- {d}\033[0m")

with open(FILENAME, "w") as f:
    f.write("\n".join(sorted(DOMAINS)))
