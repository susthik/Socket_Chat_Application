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
                if msg.lower() == "exit" :
                    client.close()
                    exitmsg = f"{clients.get(client, 'unkownUser')} has disconnected"
                    cast(exitmsg ,client)
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
        print("msg not sended\n")

# Handle the Multiple client at Time          
def client_handler(client, addr):
    
    buffer = ""
    print(f"\nconnected with{addr}")
    client.send("you are conneccted with our server :\n)".encode())# server side msg to client>>
    client.send("UserName :\n".encode())# server side msg to client>>
 
    
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
 
        except ConnectionResetError:
            print("error!")
            break


 
    #creating a thread for get the msg 
    t1 = threading.Thread(target= recv_msg, args=(client,))
    t1.start()
    
   

#Socket Configaration
def start_server():

    host="0.0.0.0"
    port=12345
    
    #socket connection init__
    socket_server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    socket_server.bind((host , port))
    socket_server.listen(2)
    print(f"server listion on {host}:{port}")
    
    while True:
        try:
            
            client , addr = socket_server.accept()# accept the  incoming connection<<  
            #creating a thread for accept the user
            t = threading.Thread(target=client_handler, args=(client, addr))
            t.start()
        except RuntimeError as e:
            print(e,"??")
            
                               
start_server()

    
 
