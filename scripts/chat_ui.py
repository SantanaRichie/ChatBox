import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime as dt
import sqlite3
import time
import threading
from manage_connections import ConnectionManager

path = r'C:\Users\santa\Documents\Projects\ChatBox\configs\chat.db'
connections_path = r'C:\Users\santa\Documents\Projects\ChatBox\configs\connections.db'

def refresh_chat(path, peer_filter=None):
    """Fetch chat log. Returns (full_log, message_count, messages)
    If peer_filter is provided, only shows messages from/to that peer"""
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('Select time, user, msg From chat_log Order by time asc')
    res = cur.fetchall()
    conn.close()
    
    # Filter by peer if specified
    if peer_filter:
        res = [msg for msg in res if msg[1] == peer_filter]
    
    msg_count = len(res)
    log = ''.join([f'{entry[0]}: {entry[1]}- {entry[2]}\n' for entry in res])
    return log, msg_count, res

def append_new_messages(chat_display, res, last_count):
    """Append only new messages to the display"""
    if last_count < len(res):
        new_messages = res[last_count:]
        new_text = ''.join([f'{entry[0]}: {entry[1]}- {entry[2]}\n' for entry in new_messages])
        chat_display.configure(state="normal")
        chat_display.insert('end', new_text)
        chat_display.configure(state="disabled")
        chat_display.see('end')

def open_chatbox(user_name, host='localhost', port=5000):
    status = 'Online'
    
    # Track appearance mode
    appearance_mode = {'current': 'Light'}
    ctk.set_appearance_mode("Light")
    
    # Initialize connection manager
    conn_manager = ConnectionManager(user_name, host, port)
    conn_manager.start_server()
    
    root = ctk.CTk()
    root.title(f'ChatBox - {user_name} - Status: {status}')
    root.geometry("900x750")
    
    # Main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Header with user info
    header_frame = ctk.CTkFrame(main_frame)
    header_frame.pack(fill="x", padx=5, pady=5)
    ctk.CTkLabel(header_frame, text=f"User: {user_name}", text_color="gray", font=("Arial", 12, "bold")).pack(side="left", padx=5)
    ctk.CTkLabel(header_frame, text="Connected Users:", text_color="gray").pack(side="left", padx=20)
    connected_label = ctk.CTkLabel(header_frame, text="None", text_color="green")
    connected_label.pack(side="left", padx=5)
    
    # Dark mode toggle button
    def toggle_dark_mode():
        """Toggle between light and dark mode"""
        if appearance_mode['current'] == 'Light':
            appearance_mode['current'] = 'Dark'
            ctk.set_appearance_mode("Dark")
            dark_mode_btn.configure(text="☀️ Light Mode")
        else:
            appearance_mode['current'] = 'Light'
            ctk.set_appearance_mode("Light")
            dark_mode_btn.configure(text="🌙 Dark Mode")
    
    dark_mode_btn = ctk.CTkButton(
        header_frame,
        text="🌙 Dark Mode",
        command=toggle_dark_mode,
        width=150
    )
    dark_mode_btn.pack(side="right", padx=5)
    
    # Connection toggle panel
    conn_header_frame = ctk.CTkFrame(main_frame)
    conn_header_frame.pack(fill="x", padx=5, pady=5)
    
    # Toggle button for connection panel
    toggle_states = {'expanded': False}
    
    def toggle_connection_panel():
        """Toggle the connection panel visibility"""
        toggle_states['expanded'] = not toggle_states['expanded']
        if toggle_states['expanded']:
            conn_panel.pack(fill="x", padx=5, pady=5, after=conn_header_frame)
            toggle_btn.configure(text="▼ Connect to Peer")
        else:
            conn_panel.pack_forget()
            toggle_btn.configure(text="► Connect to Peer")
    
    toggle_btn = ctk.CTkButton(
        conn_header_frame, 
        text="► Connect to Peer", 
        command=toggle_connection_panel,
        text_color="blue",
        fg_color="transparent",
        hover_color=("gray", "gray"),
        anchor="w"
    )
    toggle_btn.pack(fill="x", padx=5)
    
    # Connection panel (hidden by default)
    conn_panel = ctk.CTkFrame(main_frame)
    
    # Function to load saved connections
    def load_saved_connections():
        """Load saved connections from database"""
        try:
            conn = sqlite3.connect(connections_path)
            cur = conn.cursor()
            cur.execute(
                "SELECT user2, status, user2_host, user2_port FROM connections WHERE user1 = ? ORDER BY user2",
                (user_name,)
            )
            saved = cur.fetchall()
            conn.close()
            return [f"{u[0]} ({u[1]})" for u in saved]
        except Exception as e:
            print(f"Error loading connections: {e}")
            return []
    
    # Function to get connection details
    def get_connection_details(selection):
        """Extract username, host, port from saved connection"""
        try:
            if selection and selection != "No saved connections":
                username = selection.split(" (")[0]
                conn = sqlite3.connect(connections_path)
                cur = conn.cursor()
                cur.execute(
                    "SELECT user2_host, user2_port FROM connections WHERE user1 = ? AND user2 = ?",
                    (user_name, username)
                )
                result = cur.fetchone()
                conn.close()
                if result:
                    return username, result[0], result[1]
        except Exception as e:
            print(f"Error getting connection details: {e}")
        return None, None, None
    
    # Saved connections frame
    saved_conn_frame = ctk.CTkFrame(conn_panel)
    saved_conn_frame.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkLabel(saved_conn_frame, text="Connections:").pack(side="left", padx=5)
    
    # Track current selected peer
    current_peer = {'name': None}
    
    # Load initial saved connections
    saved_connections = load_saved_connections()
    saved_conn_dropdown = ctk.CTkComboBox(
        saved_conn_frame, 
        values=saved_connections if saved_connections else ["No saved connections"],
        state="readonly",
        width=250
    )
    saved_conn_dropdown.pack(side="left", padx=5)
    if saved_connections:
        saved_conn_dropdown.set(saved_connections[0])
        # Set initial peer from first connection
        first_peer = saved_connections[0].split(" (")[0]
        current_peer['name'] = first_peer
    
    # Connection input frame
    conn_input_frame = ctk.CTkFrame(conn_panel)
    conn_input_frame.pack(fill="x", padx=5, pady=5)
    
    # Peer username
    ctk.CTkLabel(conn_input_frame, text="Username:").pack(side="left", padx=5)
    peer_username_entry = ctk.CTkEntry(conn_input_frame, placeholder_text="Peer username", width=120)
    peer_username_entry.pack(side="left", padx=5)
    
    # Peer host
    ctk.CTkLabel(conn_input_frame, text="Host:").pack(side="left", padx=5)
    peer_host_entry = ctk.CTkEntry(conn_input_frame, placeholder_text="localhost or IP", width=150)
    peer_host_entry.pack(side="left", padx=5)
    
    # Peer port
    ctk.CTkLabel(conn_input_frame, text="Port:").pack(side="left", padx=5)
    peer_port_entry = ctk.CTkEntry(conn_input_frame, placeholder_text="5000", width=80)
    peer_port_entry.pack(side="left", padx=5)
    
    # Function to handle dropdown selection
    def on_connection_selected(choice):
        """Populate fields and update chat when a saved connection is selected"""
        if choice and choice != "No saved connections":
            username, host, port = get_connection_details(choice)
            if username and host and port:
                current_peer['name'] = username
                peer_username_entry.delete(0, 'end')
                peer_username_entry.insert(0, username)
                peer_host_entry.delete(0, 'end')
                peer_host_entry.insert(0, host)
                peer_port_entry.delete(0, 'end')
                peer_port_entry.insert(0, str(port))
                # Refresh chat display to show messages from this peer
                update_chat_display()
    
    saved_conn_dropdown.configure(command=on_connection_selected)
    
    # Connect button
    def connect_to_peer():
        peer_user = peer_username_entry.get().strip()
        peer_h = peer_host_entry.get().strip()
        peer_p = peer_port_entry.get().strip()
        
        if not peer_user or not peer_h or not peer_p:
            messagebox.showerror("Error", "Please fill in all connection fields")
            return
        
        try:
            peer_port_num = int(peer_p)
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return
        
        # Connect in background thread
        def _connect():
            if conn_manager.connect_to_peer(peer_user, peer_h, peer_port_num):
                conn_manager.add_connection(peer_user, peer_h, peer_port_num, status='connected')
                messagebox.showinfo("Success", f"Connected to {peer_user}")
                # Clear fields on success
                peer_username_entry.delete(0, 'end')
                peer_host_entry.delete(0, 'end')
                peer_port_entry.delete(0, 'end')
                # Refresh the dropdown with updated connections
                updated_connections = load_saved_connections()
                saved_conn_dropdown.configure(values=updated_connections if updated_connections else ["No saved connections"])
                if updated_connections:
                    saved_conn_dropdown.set(updated_connections[-1])  # Select the newly added connection
            else:
                messagebox.showerror("Error", f"Failed to connect to {peer_user}")
        
        threading.Thread(target=_connect, daemon=True).start()
    
    # Save connection function
    def save_connection():
        """Save connection without connecting"""
        peer_user = peer_username_entry.get().strip()
        peer_h = peer_host_entry.get().strip()
        peer_p = peer_port_entry.get().strip()
        
        if not peer_user or not peer_h or not peer_p:
            messagebox.showerror("Error", "Please fill in all connection fields")
            return
        
        try:
            peer_port_num = int(peer_p)
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return
        
        # Save connection to database
        try:
            conn_manager.add_connection(peer_user, peer_h, peer_port_num, status='saved')
            messagebox.showinfo("Success", f"Connection saved for {peer_user}")
            # Clear fields
            peer_username_entry.delete(0, 'end')
            peer_host_entry.delete(0, 'end')
            peer_port_entry.delete(0, 'end')
            # Refresh dropdown
            updated_connections = load_saved_connections()
            saved_conn_dropdown.configure(values=updated_connections if updated_connections else ["No saved connections"])
            if updated_connections:
                saved_conn_dropdown.set(updated_connections[-1])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save connection: {e}")
    
    # Button frame for Connect and Save buttons
    button_frame = ctk.CTkFrame(conn_input_frame)
    button_frame.pack(side="right", padx=5)
    
    connect_btn = ctk.CTkButton(button_frame, text="Connect", command=connect_to_peer, width=100)
    connect_btn.pack(side="left", padx=5)
    
    save_connection_btn = ctk.CTkButton(button_frame, text="Save Connection", command=save_connection, width=120)
    save_connection_btn.pack(side="left", padx=5)
    
    # Chat display area
    chat_display = ctk.CTkTextbox(main_frame, height=350, wrap="word")
    chat_display.pack(fill="both", expand=True, padx=5, pady=5)
    chat_display.configure(state="disabled")
    
    # Input frame for sending messages
    input_frame = ctk.CTkFrame(main_frame)
    input_frame.pack(fill="x", padx=5, pady=5)
    
    ctk.CTkLabel(input_frame, text="Send Message:", text_color="blue", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=3)
    
    # Message input row
    msg_input_frame = ctk.CTkFrame(input_frame)
    msg_input_frame.pack(fill="x", padx=5, pady=5)
    
    # Recipient selection
    ctk.CTkLabel(msg_input_frame, text="To:").pack(side="left", padx=5)
    recipient_entry = ctk.CTkEntry(msg_input_frame, placeholder_text="Username or 'all'", width=120)
    recipient_entry.pack(side="left", padx=5)
    
    # Message input
    message_entry = ctk.CTkEntry(msg_input_frame, placeholder_text="Type your message...")
    message_entry.pack(side="left", fill="x", expand=True, padx=5)
    
    # Send button
    send_button = ctk.CTkButton(msg_input_frame, text="SEND", command=lambda: send_message(), width=100)
    send_button.pack(side="right", padx=5)
    
    # Track message count for incremental updates
    msg_tracker = {'count': 0, 'messages': []}
    
    def update_chat_display():
        """Update display - only appends new messages for speed, filtered by selected peer"""
        peer_filter = current_peer['name']
        log, msg_count, res = refresh_chat(path, peer_filter=peer_filter)
        
        # If first load or chat was cleared, do full rebuild
        if msg_tracker['count'] == 0 or msg_count < msg_tracker['count']:
            chat_display.configure(state="normal")
            chat_display.delete('1.0', 'end')
            chat_display.insert('1.0', log)
            chat_display.configure(state="disabled")
        else:
            # Append only new messages
            append_new_messages(chat_display, res, msg_tracker['count'])
        
        msg_tracker['count'] = msg_count
        msg_tracker['messages'] = res
        
        # Update connected users display
        connected_users = ', '.join(conn_manager.connected_peers.keys())
        connected_label.configure(text=connected_users or 'None')
    
    def send_message():
        query = message_entry.get().strip()
        recipient = recipient_entry.get().strip() or 'all'
        
        if query:
            ts = dt.now().isoformat()
            
            # Save to local database
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute(f"""INSERT INTO chat_log(user, time, msg) VALUES(?,?,?)""", (user_name, ts, query))
            conn.commit()
            conn.close()
            
            # Send through network
            if recipient == 'all':
                # Send to all connected peers
                for peer_username in conn_manager.connected_peers.keys():
                    conn_manager.send_message(peer_username, query)
            else:
                # Send to specific user
                conn_manager.send_message(recipient, query)
            
            # Update display immediately
            message_entry.delete(0, 'end')
            update_chat_display()
    
    # Bind Enter key to send message
    message_entry.bind('<Return>', lambda event: send_message())
    
    # Poll for new messages from network
    def poll_updates():
        while root.winfo_exists():
            update_chat_display()
            time.sleep(1)
    
    threading.Thread(target=poll_updates, daemon=True).start()
    
    # Initial chat display update
    update_chat_display()
    
    # Handle window close
    def on_closing():
        conn_manager.stop_server()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()