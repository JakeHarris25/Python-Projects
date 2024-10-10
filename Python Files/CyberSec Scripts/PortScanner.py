import socket
import threading
import os


# limiting multi-threading
thread_limit = 100
sephamore = threading.BoundedSemaphore(value=thread_limit)

# function to scan ports
def scan_port(ip_address, port, file_name):
    with sephamore:
        try:
            # create a new socket with each iteration
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # one second timeout limit
            s.settimeout(3)

            # attempt connection with specified IP and port in range
            connect_status = s.connect_ex((ip_address, port))

            # if socket returns 0, this means successful
            if connect_status == 0:
                result = (f"{port} is open!")
            else:
                result = (f"{port} is closed or unreachable.")
 
            # write results to a log file
            with open(file_name, 'a') as f:
                f.write(result) 

            # closes socket
            s.close()

        except socket.error as e:
            print(f"Error with port {port}: {str(e)}")

# user input for IPv4 address
ip_address = input("Enter the IPv4 address to scan: ")

# specifying file name and file save path
file_name = input("Please enter the name of the log files: (new files start as .txt files!)")
save_path = input("Enter the file path you want to save the log file to: ")

# verifying file path exists and joins together with file name
if not os.path.exists(save_path):
    print("The provided path is invalid.")
else:
    file_path_joined = os.path.join(save_path, file_name)
    full_file_path = file_path_joined + '.txt'


# list to keep track of running threads
threads = []

# multi-threading instance of scan_port function
try:
    for port in range(18, 1000):
        thread = threading.Thread(target=scan_port, args=(ip_address, port, full_file_path))
        threads.append(thread)
        thread.start()
except Exception as e:
    print(f"Error: {e}")

# waiting for threads to join for sychronicity
for thread in threads:
    thread.join()


# final print statement
print(f"\n{full_file_path} has been saved to {save_path}")

