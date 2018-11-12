# pwned password checker

Checks passwords stored in BitWarden against pwned password database.

Requires the BitWarden CLI `bw`:

https://help.bitwarden.com/article/cli/#download--install

Uses the database from haveibeenpwned:

https://haveibeenpwned.com/API/v2#PwnedPasswords

The script has intentionally been kept short so that it is easy to audit - you should read it before running it!

## Dependencies

Uses the 3rd party `requests` library for HTTP requests to haveibeenpwned

## Usage

Unlock your BitWarden vault:

```
bw unlock
```

Enter your password and then copy the session token into the `BW_SESSION` environment variable:

```
export BW_SESSION="SECRETKEYWILLBEHERE"
```

Then run the Python script:

```
python pwned.py
```

Any compromised passwords will be reported:

```
aninsecurewebsite.com HAS BEEN PWNED!!!
```