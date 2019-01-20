import subprocess
import json
import hashlib
import re
import requests
from typing import Dict, Any
import sys


def get_hash(password: str) -> str:
    m = hashlib.sha1()
    m.update(password)
    password_hash = m.hexdigest().upper()
    return password_hash


def get_pwned(password_hash: str) -> Dict[str, int]:
    key = password_hash[0:5]
    res = requests.get(f"https://api.pwnedpasswords.com/range/{key}")
    assert res.status_code == 200
    lines = res.text.splitlines()
    pairs = [line.split(":") for line in lines]
    results = {f"{key}{ending}": int(count) for ending, count in pairs}
    return results


def get_credentials() -> Dict[str, Any]:
    result = subprocess.run(["bw", "list", "items"], capture_output=True)
    items = json.loads(result.stdout)
    return [item for item in items if "login" in item]


def main():
    count_pwned = 0
    credentials = get_credentials()
    for item in credentials:
        password = item["login"]["password"].encode("utf-8")
        password_hash = get_hash(password)
        results = get_pwned(password_hash)
        pwned = password_hash in results
        if not pwned:
            continue
        count_pwned += 1
        print(f"{item['name']} has been pwned!")

    print(f"{count_pwned} of {len(credentials)} logins have been pwned.")

if __name__ == "__main__":
    sys.exit(main())
