import socket
import threading
import os
import argparse
import ipaddress
from datetime import datetime


# limiting multi-threading
thread_limit = 100
sephamore = threading.BoundedSemaphore(value=thread_limit)

# function to scan ports
def scan_port(ip_address, port, file_name):
    with sephamore:
        try:
            # create a new socket with each iteration
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # three second timeout limit
            s.settimeout(3)

            # attempt connection with specified IP and port
            connect_status = s.connect_ex((ip_address, port))

            # if socket returns 0, this means successful
            if connect_status == 0:
                result = (f"{port} is open!\n")
            else:
                result = (f"{port} is closed or unreachable.\n")
                
            print(result.strip())
 
            # write results to a log file
            with open(file_name, 'a') as f:
                f.write(result)
                

            # closes socket
            s.close()

        except socket.error as e:
            print(f"Error with port {port}: {str(e)}")


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        
        return True
    except ValueError:
        return False

# adds command line arguments to be used in a CLI
def main():
    parser = argparse.ArgumentParser(description='A rudimentary multi-threaded port scanner')
    parser.add_argument("--ip", required=True, help="The IPv4 address to scan.")
    parser.add_argument("--start-port", type=int, default=1, help="The starting port to scan.")
    parser.add_argument("--end-port", type=int, default=1024, help="The last port to scan.")
    parser.add_argument("--log", required=True, help="The file path to save the scan log to.")

    args = parser.parse_args()

    if not validate_ip(args.ip):
        print(f"{args.ip} is not a valid IP address. Exiting.")
        return


    log_dir = os.path.dirname(args.log)
    if log_dir and not os.path.exists(log_dir):
        print(f"The directory {log_dir} does not exist.")
        return
    
    with open(args.log, 'w') as f:
        f.write(f"Port Scan Results\n")
        f.write(f"Target IP: {args.ip}\n")
        f.write(f"Port Range: {args.start_port} - {args.end_port}\n")
        f.write(f"Scan Start Time: {datetime.now()}\n")
        f.write(f"{'-' * 40}\n")

    print(f"Port Scan Results")
    print(f"Target IP: {args.ip}")
    print(f"Port Range: {args.start_port} - {args.end_port}")
    print(f"Scan Start Time: {datetime.now()}")
    print(f"{'-' * 40}")
    
    threads = []
    
    # multi-threading instance of scan_port function
    try:
        for port in range(args.start_port, args.end_port+1):
            thread = threading.Thread(target=scan_port, args=(args.ip, port, args.log))
            threads.append(thread)
            thread.start()
    except Exception as e:
        print(f"Error: {e}")

    # waiting for threads to join for sychronicity
    for thread in threads:
        thread.join()
    
    print(f"\nScan complete. Log saved at {args.log}")

if __name__ == "__main__":
    main()





