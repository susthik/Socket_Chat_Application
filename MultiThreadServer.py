import socket
import threading


clients={}

#Recive msg Form Client       
def recv_msg(client):
    buffer=""
    
    while True:
        try:
            msg = client.recv(1024).decode()
            buffer +=msg
            if "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)  # split at first newline
                msg = msg.strip()
                m = f"{clients.get(client, 'unkownUser')}:{msg}\n"
                print(m,end="")
                cast(m, client) # Boadcast To Another User's
                if msg.lower() == "exit" or  msg.lower() == "quit":
                    client.close()
                    exitmsg = f"{clients.get(client, 'unkownUser')} has disconnected"
                    cast(exitmsg ,client)
                    clients.pop(client,0)
                    break
        except ConnectionResetError:
            print("recv_verror!")
            break

# Recive the Msg Boadcast to connected User's
def cast(msg, sender=None):
    try:
        for client in clients:
            if client != sender:
                client.sendall(msg.encode())
    except :
        print("cast!=\n")

# Handle the Multiple client at Time          
def client_handler(client, addr):
    
    buffer = ""
    print(f"\nconnected with{addr}") 
    while True:
        try:
            uname = client.recv(1024).decode()
            buffer +=uname
            if "\n" in buffer:
                uname, buffer = buffer.split("\n", 1)  # split at first newline
                uname = uname.strip()
                print(f"Wellcome,{uname}❤\n")
                clients[client] = uname
                joinmsg = f"{uname} jion on chat\n"
                cast(joinmsg ,client)
                break
            else:
                print("null")
 
        except ConnectionResetError:
            print("error!")
            break
    #creating a thread for get the msg 
    t1 = threading.Thread(target= recv_msg, args=(client,))
    t1.start()
      

#Socket Configaration
def main():

    host="127.168.0.0"
    port=4343
    
    #socket connection init__
    socket_server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    socket_server.bind((host , port))
    socket_server.listen(5)
    print(f"server listion on {host}:{port}")
    
    while True:
        try:
            
            client , addr = socket_server.accept()# accept the  incoming connection<< 
            client.send("\nyou are conneccted with our server :\n".encode())# server side msg to client>>
            #creating a thread for accept the user
            t = threading.Thread(target=client_handler, args=(client, addr))
            t.start()
        except RuntimeError as e:
            print(e,"??")
            
if __name__ == "__main__" :
    main()

    
 
