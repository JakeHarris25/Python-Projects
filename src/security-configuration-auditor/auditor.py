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
    try:
        command = ("Get-NetFirewallProfile | "
                "Select-Object Name, Enabled | "
                "ConvertTo-Json")
        
        result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check=True)
        firewall_profiles = json.loads(result.stdout)

        json_is_dict = isinstance(firewall_profiles, dict)
        if json_is_dict:
            json_list = []
            json_list.append(firewall_profiles)
            return json_list
        else:
            return firewall_profiles
    
    except subprocess.CalledProcessError as error:
        print("Failed to retrieve firewall profiles.\n")
        print(f"Powershell error: {error.stderr}")
        return None
    except json.JSONDecodeError as error:
        print("Failed to convert data to Json.")
        print(f"Powershell error: {error}")
        return None

def get_firewall_status_check(firewall_profiles):
    all_profiles_enabled = all(
        profile["Enabled"] == 1 for profile in firewall_profiles
    )

    if all_profiles_enabled:
        return "Firewall check: PASS"
    else:
        return "Firewall check: FAIL"

def get_tcp_ports():
    try:
        process_name = "@{ Name = 'ProcessName'; Expression = {( Get-Process -Id $_.OwningProcess).ProcessName }}"
        command = ("Get-NetTCPConnection -State Listen | "
                    f"Select-Object LocalAddress, LocalPort, OwningProcess, {process_name} | "
                    "Sort-Object LocalPort | "
                    "ConvertTo-Json")

        result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check=True)
        tcp_ports = json.loads(result.stdout)
        
        json_is_dict = isinstance(tcp_ports, dict)
        if json_is_dict:
            json_list = []
            json_list.append(tcp_ports)
            return json_list
        else:
            return tcp_ports

    except subprocess.CalledProcessError as error:
        print("Failed to retrieve listener information.")
        print(f"Powershell error: {error.stderr}")
        return None
    except json.JSONDecodeError as error:
        print("Failed to convert data to Json.")
        print(f"Powershell error: {error}")
        return None

def classify_net_address(local_address):
    
    if local_address == "127.0.0.1" or local_address == "::1":
        return "Local only"
    elif local_address == "0.0.0.0" or local_address == "::":
        return "All interfaces"
    else:
        return "Specific interface"
        
def classify_listener(local_port, exposure):
    if local_port in approved_ports:
        return "Approved"
    elif exposure == "Local only":
        return "Local only"
    elif exposure == "All interfaces":
        return "High-priority review"
    else:
        return "Review"

def completeness_check(approved_count, review_count, local_only_count, high_priority_count, total_listeners):

    sum_of_counts = approved_count + review_count + local_only_count + high_priority_count

    if total_listeners == sum_of_counts:
        return "PASS!"
    else:
        return "FAIL. Verify listener count."

def get_service_name():
    try:
        
        service_map = ("Get-CimInstance -ClassName Win32_Service | "
                      f"Select-Object ProcessId, Name | "
                      "Where-Object { $_.ProcessID -gt 0} | "
                      "Group-Object ProcessId | "
                      "ConvertTo-Json -Depth 4")

        services = subprocess.run(["powershell.exe", "-NoProfile", "-Command", service_map], capture_output=True, text=True, check=True)
        services_result = json.loads(services.stdout)

        json_is_dict = isinstance(services_result, dict)
        if json_is_dict:
            json_list = []
            json_list.append(services_result)
            services_result = json_list      

        service_map_dict = {}

        for outer_pid in services_result:
            pid = outer_pid["Name"]
            pid_integer = int(pid)
            group = outer_pid["Group"]
            service_list = []
            for service in group:
                service_name = service["Name"]
                service_list.append(service_name)
            service_map_dict[pid_integer] = service_list
        return service_map_dict
    
    except subprocess.CalledProcessError as error:
        print(f"Powershell error: {error.stderr}")
        return None
    except json.JSONDecodeError as error:
        print("Failed to convert data to Json.")
        print(f"Powershell error: {error}")
        return None

def get_process_map():
    try:
        command = ("Get-CimInstance -ClassName Win32_Process | "
                   "Select-Object ProcessId, Name, ExecutablePath | "
                   "ConvertTo-Json")

        result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check=True)
        exe_result = json.loads(result.stdout)

        json_is_dict = isinstance(exe_result, dict)
        if json_is_dict:
            json_list = []
            json_list.append(exe_result)
            exe_result = json_list
        
        exe_pid_dict = {}

        for var in exe_result:
            pid = var["ProcessId"]
            pid_int = int(pid)
            exe_path = var["ExecutablePath"] or "Path unavailable"
            exe_pid_dict[pid_int] = exe_path

        return exe_pid_dict
            
    except subprocess.CalledProcessError as error:
        print(f"Powershell error: {error.stderr}")
        return None
    except json.JSONDecodeError as error:
        print("Failed to convert data to Json.")
        print(f"Powershell error: {error}")
        return None

def main():
    hostname = get_hostname()
    audit_time = get_audit_time()
    firewall_profiles = get_firewall_profiles()
    if firewall_profiles is None:
        return

    firewall_status_check = get_firewall_status_check(firewall_profiles)
    tcp_ports = get_tcp_ports()
    if tcp_ports is None:
        return
    
    approved_count = 0
    review_count = 0
    local_only_count = 0
    high_priority_count = 0
    total_listeners = len(tcp_ports)
    windows_service_names = get_service_name()

    print("~" * 28)
    print("SECURITY CONFIGURATION AUDIT")
    print("~" * 28)
    print(
    f"{'HOSTNAME':<18}"
    f"{'AUDIT TIME':<8}"
    )

    print(f"{hostname:<18}"
          f"{audit_time:<8}\n")

    print("Firewall Profile Status")
    print("-" * 23)
    for profile in firewall_profiles:
        name = profile["Name"]
        enabled = profile["Enabled"]

        if enabled:
            status = "Enabled"
        else:
            status = "Disabled"

        print(f"{name}: {status}")

    print("-" * 15)
    print(firewall_status_check)

    print("\nListening TCP Ports:")
    print("-" * 105)

    print(
    f"{'ADDRESS':<18}"
    f"{'PORT':<8}"
    f"{'PROCESS':<26}"
    f"{'PID':<10}"
    f"{'SERVICE':<27}"
    f"{'EXPOSURE':<20}"
    f"{'STATUS':<25}"
    f"{'EXE PATH':<20}"
    )

    process_map = get_process_map()

    for port in tcp_ports:
        exposure = classify_net_address(port["LocalAddress"])
        approval_status = classify_listener(port['LocalPort'], exposure)
        process_name = port['ProcessName'] or "Unknown"
        pid_lookup = port['OwningProcess']
        service_to_pid = windows_service_names.get(pid_lookup, ["No Windows service"])
        service_string = ", ".join(service_to_pid)
        exe_path = process_map.get(pid_lookup, "Path unavailable")
        
       
        if approval_status == "Approved":
            approved_count += 1
        elif approval_status == "Local only":
            local_only_count += 1
        elif approval_status == 'High-priority review':
            high_priority_count += 1
        else:
            review_count += 1

        print(
            f"{port['LocalAddress']:<18}"
            f"{port['LocalPort']:<8}"
            f"{process_name[:24]:<26}"
            f"{port['OwningProcess']:<10}"
            f"{service_string[:24]:<27}"
            f"{exposure:<20}"
            f"{approval_status:<25}"
            f"{exe_path[:50]:<20}"
        )

    print("-" * 105)
    print(f"Approved listeners: {approved_count}")
    print(f"High-priority listeners to review: {high_priority_count}")
    print(f"Listeners to review: {review_count}")
    print(f"Local only listeners: {local_only_count}")
    print("-" * 25)
    print(f"Total listener count: {total_listeners}")

    result = completeness_check(
    approved_count,
    review_count,
    local_only_count,
    high_priority_count,
    total_listeners
    )

    print("Completeness verification:", result)


    print("~" * 50)
    
   
    
    

   





if __name__ == "__main__":
    main()