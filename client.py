import socket
import threading
import pickle

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 3333))


# Choosing Nickname and target 
nickname = input("Choose your nickname: ")
receiver = input("Please tell me with who you would like to talk : ")
dic = { 1 : nickname, 2 : receiver}
communication_info = pickle.dumps(dic)



def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send communication info (nickname + receiver)
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(communication_info)
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()