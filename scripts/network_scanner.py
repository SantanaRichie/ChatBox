#!/usr/bin/env python
"""Network Scanner - Discover IP addresses on local network"""

import socket
import subprocess
import platform
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to connect to an external address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def get_network_range(local_ip):
    """Generate network range from local IP"""
    parts = local_ip.split('.')
    print(f'parts: {parts}')
    if len(parts) != 4:
        return []
    
    network_base = f"{parts[0]}.{parts[1]}.{parts[2]}"
    return [f"{network_base}.{i}" for i in range(1, 255)]

def check_port(ip, port=5000, timeout=1):
    """Check if a specific port is open on an IP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def ping_host(ip, timeout=1):
    """Ping a host to check if it's online"""
    try:
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
        else:
            cmd = ["ping", "-c", "1", "-W", str(timeout), ip]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 1)
        return result.returncode == 0
    except Exception:
        return False

def scan_network(port=5000, timeout=1, max_threads=50):
    """Scan the network for hosts with open ChatBox port"""
    local_ip = get_local_ip()
    print(f'local_ip: {local_ip}')
    network_range = get_network_range(local_ip)
    print(f'network_range: {network_range}')
    
    print(f"Scanning network for ChatBox instances on port {port}...")
    print(f"Your IP: {local_ip}")
    print(f"Network range: {network_range[0]} - {network_range[-1]}")
    print("=" * 60)
    
    online_hosts = []
    chatbox_hosts = []
    
    def scan_ip(ip):
        """Scan a single IP"""
        if ping_host(ip, timeout):
            online_hosts.append(ip)
            if check_port(ip, port, timeout):
                chatbox_hosts.append(ip)
                return f"✓ {ip} - ChatBox running!"
            else:
                return f"• {ip} - Online (no ChatBox)"
        return None
    
    # Use ThreadPoolExecutor for faster scanning
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_ip, ip): ip for ip in network_range}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)
    
    print("\n" + "=" * 60)
    print(f"Scan Complete!")
    print(f"Online hosts: {len(online_hosts)}")
    print(f"ChatBox instances found: {len(chatbox_hosts)}")
    
    if chatbox_hosts:
        print(f"\nChatBox IPs you can connect to:")
        for ip in chatbox_hosts:
            print(f"  - {ip}:5000")
    else:
        print("\nNo ChatBox instances found. Make sure ChatBox is running on other machines.")
    
    return chatbox_hosts

def quick_scan():
    """Quick scan for ChatBox instances"""
    print("Quick Network Scan for ChatBox")
    print("=" * 40)
    return scan_network(port=5000, timeout=0.5, max_threads=100)

def get_network_info():
    """Display detailed network information"""
    local_ip = get_local_ip()
    hostname = socket.gethostname()
    
    print("Network Information")
    print("=" * 30)
    print(f"Hostname: {hostname}")
    print(f"Local IP: {local_ip}")
    print(f"ChatBox Port: 5000")
    print(f"Network Range: {'.'.join(local_ip.split('.')[:3])}.1-254")
    print()
    print("Other users should connect to your IP address above.")

if __name__ == '__main__':
    print("ChatBox Network Scanner")
    print("1. Quick Scan (fast)")
    print("2. Full Scan (thorough)")
    print("3. Show My Network Info")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            quick_scan()
        elif choice == '2':
            scan_network()
        elif choice == '3':
            get_network_info()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select 1-4.")
