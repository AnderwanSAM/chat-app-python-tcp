import socket
import threading
import pickle 

host = '127.0.0.1'
port = 3333

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make sur we can reuse the port later 
server.bind((host, port))

server.listen()

# Lists For Clients , Their Nicknames and their targets (receivers)
clients = []
nicknames = []
receivers = [] 

# default - to send messages to all clients 
def broadcast(message):
    for client in clients:
        client.send(message)



# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Receive  Message from a client 
            message = client.recv(1024)
            # find the receiver 
            client_index  = clients.index(client)
            receiver_name = receivers[client_index]
            # if the receiver is connected 
            if receiver_name in nicknames: 
                receiver_index  = nicknames.index(receiver_name)
                # send the message to the receiver 
                clients[receiver_index].send(message)
            else : 
                # let the client know its target is offline
                client.send('This user is offline or  disconnected from the server!'.encode('ascii'))
        except:
            # Removing And Closing Clients when something goes wrong  - the client left 
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

       
        # Request And Store Nickname and target (receiver)
        client.send('NICK'.encode('ascii'))
        communication_info = client.recv(1024)
        d = pickle.loads(communication_info)
        nickname = d[1]
        receiver = d[2]
        nicknames.append(nickname)
        clients.append(client)
        receivers.append(receiver)
        # in  the server console, log the communication information 
        print("{} wishes to talk to {}".format(nickname,receiver))

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        
        
        
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()