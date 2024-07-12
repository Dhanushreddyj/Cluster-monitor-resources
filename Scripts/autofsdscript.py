import yaml
import nmap
import logging
import netifaces
import threading
import time

# Configure logging
logging.basicConfig(filename='/Users/dhanushreddyjanagama/Developer/Scripts/autofsdscript2.log',
                    format='%(asctime)s - %(message)s',
                    level=logging.INFO)

def get_local_network_range():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if_addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in if_addresses:
            ipv4_info = if_addresses[netifaces.AF_INET][0]
            ip_address = ipv4_info['addr']
            netmask = ipv4_info['netmask']
            if not ip_address.startswith("127."):  # Skip loopback addresses
                ip_parts = ip_address.split('.')
                netmask_parts = netmask.split('.')
                network_parts = [str(int(ip_parts[i]) & int(netmask_parts[i])) for i in range(4)]
                network_address = '.'.join(network_parts)
                cidr_suffix = sum(bin(int(part)).count('1') for part in netmask_parts)
                return f"{network_address}/{cidr_suffix}"
    raise ValueError("Unable to determine the local network range")

def get_active_nodes(network):
    nm = nmap.PortScanner()
    try:
        start_time = time.time()
        nm.scan(hosts=network, arguments='-sP')  # Ping scan to detect active nodes
        end_time = time.time()
        logging.info(f"Network scan took {end_time - start_time:.2f} seconds.")
    except nmap.PortScannerError as e:
        logging.error(f"Error during network scan: {str(e)}")
        raise
    nodes = [host for host in nm.all_hosts() if nm[host].state() == 'up']
    logging.info(f"Active nodes found: {nodes}")
    return nm, nodes

def service_running(nm, host, port):
    try:
        start_time = time.time()
        nm.scan(hosts=host, arguments=f'-p {port}')
        end_time = time.time()
        logging.info(f"Port scan for {host}:{port} took {end_time - start_time:.2f} seconds.")
        if nm[host]['tcp'][int(port)]['state'] == 'open':
            logging.info(f"Port {port} is open on {host}")
            return True
        else:
            logging.info(f"Port {port} is closed on {host}")
            return False
    except KeyError:
        logging.warning(f"No scan results found for host {host} on port {port}")
        return False

def update_targets_file(file_path):
    network = get_local_network_range()
    logging.info(f"Determined local network range: {network}")

    unix_targets = []
    windows_targets = []

    nm, active_nodes = get_active_nodes(network)
    logging.info("Started scanning network for active nodes")

    threads = []
    for host in active_nodes:
        t = threading.Thread(target=scan_host, args=(nm, host, unix_targets, windows_targets))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    data = unix_targets + windows_targets

    try:
        with open(file_path, 'w') as f:
            yaml.dump(data, f)
        logging.info(f"Updated targets.yml successfully with {len(data)} entries")
    except Exception as e:
        logging.error(f"Failed to update targets.yml: {str(e)}")

def scan_host(nm, host, unix_targets, windows_targets):
    if service_running(nm, host, 9100):
        unix_targets.append({
            'targets': [f"{host}:9100"],
            'labels': {
                'job': 'UNIX'
            }
        })
        logging.info(f"Added {host}:9100 to UNIX targets")
    elif service_running(nm, host, 9182):
        windows_targets.append({
            'targets': [f"{host}:9182"],
            'labels': {
                'job': 'WINDOWS'
            }
        })
        logging.info(f"Added {host}:9182 to WINDOWS targets")
    else:
        logging.warning(f"No suitable service found on host {host}")

if __name__ == "__main__":
    TARGETS_FILE_PATH = '/opt/homebrew/etc/targets.yml'
    update_targets_file(TARGETS_FILE_PATH)
