# first, get the computer/host name
# retrieve the current date and time
# check enabled Windows firewall profiles (domain, private, public)
# display results in a readable audit report (PDF will work)

import socket
from datetime import datetime
import subprocess
import json

approved_ports = [135, 445]

def get_hostname():
    return socket.gethostname()

def get_audit_time():
    current_time = datetime.now()
    return current_time.strftime("%B %d, %Y at %I:%M %p")

def get_firewall_profiles():
    command = ("Get-NetFirewallProfile | "
               "Select-Object Name, Enabled | "
               "ConvertTo-Json")
    
    result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check= True)
    firewall_profiles = json.loads(result.stdout)

    return firewall_profiles

def get_firewall_status_check(firewall_profiles):
    all_profiles_enabled = all(
        profile["Enabled"] == 1 for profile in firewall_profiles
    )

    if all_profiles_enabled:
        return "Firewall check: PASS"
    else:
        return "Firewall check: FAIL"


def get_tcp_ports():
    process_name = "@{ Name = 'ProcessName'; Expression = {(Get-Process -Id $_.OwningProcess).ProcessName }}"
    command = ("Get-NetTCPConnection -State Listen | "
                f"Select-Object LocalAddress, LocalPort, OwningProcess, {process_name} | "
                "Sort-Object LocalPort | "
                "ConvertTo-Json")

    result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check= True)
    tcp_ports = json.loads(result.stdout)

    return tcp_ports


def classify_net_address(local_address):
    
    if local_address == "127.0.0.1" or local_address == "::1":
        return "Local only"
    elif local_address == "0.0.0.0" or local_address == "::":
        return "All interfaces"
    else:
        return "Bound interface"
        


def main():
    hostname = get_hostname()
    audit_time = get_audit_time()
    firewall_profiles = get_firewall_profiles()
    firewall_status_check = get_firewall_status_check(firewall_profiles)
    tcp_ports = get_tcp_ports()
    approved_count = 0
    review_count = 0

    print("Security Configuration Audit")
    print(f"Computer hostname: {hostname}\n"
          f"Current audit time: {audit_time}\n")

    for profile in firewall_profiles:
        name = profile["Name"]
        enabled = profile["Enabled"]

        if enabled:
            status = "Enabled"
        else:
            status = "Disabled"

        print(f"{name}: {status}")

    print(firewall_status_check)

    tcp_ports = get_tcp_ports()

    print("\nListening TCP Ports:")
    print("-" * 105)

    print(
    f"{'ADDRESS':<18}"
    f"{'PORT':<8}"
    f"{'PROCESS':<26}"
    f"{'PID':<10}"
    f"{'EXPOSURE':<20}"
    f"{'STATUS':<12}"
    )


    for port in tcp_ports:
        exposure = classify_net_address(port["LocalAddress"])

        if port["LocalPort"] in approved_ports:
            approval_status = "Approved"
            approved_count += 1
        else:
            approval_status = "Review"
            review_count += 1

        print(
            f"{port['LocalAddress']:<18}"
            f"{port['LocalPort']:<8}"
            f"{port['ProcessName']:<26}"
            f"{port['OwningProcess']:<10}"
            f"{exposure:<20}"
            f"{approval_status:<12}"
        )



    print("-" * 105)
    print(f"Approved listeners: {approved_count}")
    print(f"Listeners to review: {review_count}")

   

if __name__ == "__main__":
    main()