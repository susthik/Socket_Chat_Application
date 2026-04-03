import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("\n" + msg)
        except:
            print("Disconnected from server.")
            sock.close()
            break

def send_messages(sock, username):
    while True:
        msg = input("\n you:")
        sock.send(msg.encode())
        if msg == "exit" or msg == "quit" :
            sock.close()
            sexit(0)

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.30.17.163", 12345))

username = input("Enter your username: ")
client.send(username.encode())

print(f"Connected as {username}")

# Start threads
threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
threading.Thread(target=send_messages, args=(client, username), daemon=True).start()

# Keep main thread alive
while True:
    pass
