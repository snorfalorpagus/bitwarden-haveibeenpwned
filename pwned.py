import subprocess
import json
import hashlib
import re
import requests


def get_hash(password):
    m = hashlib.sha1()
    m.update(password)
    password_hash = m.hexdigest().upper()
    return password_hash


def get_pwned(key):
    assert len(key) == 5
    res = requests.get(f"https://api.pwnedpasswords.com/range/{key}")
    assert res.status_code
    results = {key+l[0]: int(l[1]) for l in [line.split(":") for line in res.text.split("\r\n")]}
    return results


def get_hostname(uri):
    try:
        hostname = re.search("://([^/]*)/", uri).group(1)
    except AttributeError:
        hostname = uri
    return hostname


result = subprocess.run(["bw", "list", "items"], capture_output=True)
items = json.loads(result.stdout)

for item in items:
    if not "login" in item:
        continue
    password = item["login"]["password"].encode("utf-8")
    password_hash = get_hash(password)
    results = get_pwned(password_hash[0:5])
    pwned = password_hash in results
    if not pwned:
        continue
    hostname = get_hostname(item["login"]["uris"][0]["uri"])
    print(f"{hostname} HAS BEEN PWNED!!!")
    

