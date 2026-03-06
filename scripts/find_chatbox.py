#!/usr/bin/env python
"""Find ChatBox instances on your network"""

from scripts.chatNet_utils import get_local_ip, scan_for_chatbox_hosts, show_network_info

def main():
    print("ChatBox Network Discovery")
    print("=" * 40)
    
    # Show your network info
    my_ip = show_network_info()
    print()
    
    # Scan for other ChatBox instances
    print("Scanning for other ChatBox instances...")
    print("This may take a moment...")
    
    hosts = scan_for_chatbox_hosts(port=5000, timeout=2)
    
    print("\nScan Results:")
    print("=" * 40)
    
    if hosts:
        print(f"Found {len(hosts)} ChatBox instance(s):")
        for host in hosts:
            if host != my_ip:  # Don't show our own IP
                print(f"  • {host}:5000")
    else:
        print("No other ChatBox instances found on your network.")
        print("Make sure ChatBox is running on other machines.")
    
    print(f"\nYour ChatBox is running on: {my_ip}:5000")
    print("Other users can connect to this IP address.")

if __name__ == '__main__':
    main()
