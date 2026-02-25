import sqlite3
import socket
import json
import threading
from datetime import datetime
import time

CONNECTIONS_DB = "configs/connections.db"
CHAT_DB = "configs/chat.db"

class ConnectionManager:
    def __init__(self, username, host='localhost', port=5000):
        self.username = username
        self.host = host
        self.port = port
        self.server_socket = None
        self.connected_peers = {}  # {username: socket}
        self.is_running = False
        
    def start_server(self):
        """Start listening for incoming connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True
        print(f'Server started on {self.host}:{self.port}')
        
        # Accept connections in background thread
        threading.Thread(target=self._accept_connections, daemon=True).start()
    
    def _accept_connections(self):
        """Accept incoming peer connections"""
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                # Receive username from connecting peer
                data = client_socket.recv(1024).decode('utf-8')
                peer_username = data.strip()
                
                self.connected_peers[peer_username] = client_socket
                print(f'Connection accepted from {peer_username} at {address}')
                
                # Listen for messages from this peer
                threading.Thread(target=self._receive_messages, args=(peer_username, client_socket), daemon=True).start()
            except Exception as e:
                print(f'Error accepting connection: {e}')
    
    def connect_to_peer(self, peer_username, peer_host, peer_port):
        """Connect to another peer"""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            # Send our username
            peer_socket.send(self.username.encode('utf-8'))
            self.connected_peers[peer_username] = peer_socket
            print(f'Connected to {peer_username}')
            
            # Listen for messages from this peer
            threading.Thread(target=self._receive_messages, args=(peer_username, peer_socket), daemon=True).start()
            return True
        except Exception as e:
            print(f'Error connecting to {peer_username}: {e}')
            return False
    
    def send_message(self, peer_username, message):
        """Send a message to a connected peer"""
        try:
            if peer_username not in self.connected_peers:
                print(f'Not connected to {peer_username}')
                return False
            
            msg_data = {
                'sender': self.username,
                'recipient': peer_username,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            self.connected_peers[peer_username].send(json.dumps(msg_data).encode('utf-8'))
            return True
        except Exception as e:
            print(f'Error sending message to {peer_username}: {e}')
            return False
    
    def _receive_messages(self, peer_username, peer_socket):
        """Receive messages from a connected peer"""
        while self.is_running:
            try:
                data = peer_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                msg_data = json.loads(data)
                self._save_message_to_db(msg_data)
                print(f"Message from {peer_username}: {msg_data['message']}")
                
            except Exception as e:
                print(f'Error receiving from {peer_username}: {e}')
                break
        
        # Remove disconnected peer
        if peer_username in self.connected_peers:
            del self.connected_peers[peer_username]
        peer_socket.close()
    
    def _save_message_to_db(self, msg_data):
        """Save received message to chat database"""
        try:
            con = sqlite3.connect(CHAT_DB)
            cur = con.cursor()
            cur.execute(
                "INSERT INTO chat_log(user, time, msg) VALUES(?,?,?)",
                (msg_data['sender'], msg_data['timestamp'], msg_data['message'])
            )
            con.commit()
            con.close()
        except Exception as e:
            print(f'Error saving message to DB: {e}')
    
    def add_connection(self, other_username, other_host, other_port, status='connected'):
        """Add a connection to the connections database"""
        try:
            con = sqlite3.connect(CONNECTIONS_DB)
            cur = con.cursor()
            cur.execute(
                """INSERT INTO connections(user1, user2, user2_host, user2_port, status) VALUES(?,?,?,?,?)""",
                (self.username, other_username, other_host, other_port, status)
            )
            con.commit()
            con.close()
            print(f'Connection with {other_username} saved')
            return True
        except Exception as e:
            print(f'Error saving connection: {e}')
            return False
    
    def get_connections(self):
        """Get all saved connections for this user"""
        try:
            con = sqlite3.connect(CONNECTIONS_DB)
            cur = con.cursor()
            cur.execute(
                "SELECT user2, status FROM connections WHERE user1 = ?",
                (self.username,)
            )
            connections = cur.fetchall()
            con.close()
            return connections
        except Exception as e:
            print(f'Error retrieving connections: {e}')
            return []
    
    def update_connection_status(self, other_username, status):
        """Update connection status"""
        try:
            con = sqlite3.connect(CONNECTIONS_DB)
            cur = con.cursor()
            cur.execute(
                """UPDATE connections SET status = ?, updated_at = CURRENT_TIMESTAMP 
                   WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)""",
                (status, self.username, other_username, other_username, self.username)
            )
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f'Error updating connection: {e}')
            return False
    
    def stop_server(self):
        """Stop the server and close all connections"""
        self.is_running = False
        for peer_socket in self.connected_peers.values():
            try:
                peer_socket.close()
            except:
                pass
        if self.server_socket:
            self.server_socket.close()
        print('Server stopped')
