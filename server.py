import socket
import sys
import threading
import time
from queue import Queue

import pickle


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []
file = open('candidate.txt', 'rb+')
Dict = {"A": 0, "B": 0, "C": 0}

# Create a Socket (connect two computers)


def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9990
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def start_turtle():

    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        # elif cmd == 'newvoter':
        #    new_voter()
        elif cmd == 'stat':
            show_stat()
        elif cmd == 'startelection':
            startelec()
        else:
            print("Command not recognized")


# Display all current active connections with client

def list_connections():
    results = ''
    print('Checking..')
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))  # 101
            conn.recv(20480)  # 201480
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(
            i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):

    Dict = pickle.load(file)

    try:
        askVID = "Enter Voter ID: "
        conn.send(str.encode(askVID))
        vid = str(conn.recv(20480), "utf-8")
    except:
        print("\n Error sending commands1")
    try:
        askVOTE = "Enter candidate (A or B or C): "
        conn.send(str.encode(askVOTE))
        vote = str(conn.recv(20480), "utf-8")

        if vote in Dict:
            count = Dict[vote]
            count = count + 1

        Dict[vote] = count
        print("\nPolling Statistic: ")
        print(Dict)
        pickle.dump(Dict, file)

    except:
        print("\n Error sending commands2")


def show_stat():

    try:
        Dict = pickle.load(file)
        print(Dict)
    except EOFError:
        Dict = dict()


def startelec():

    pickle.dump(Dict, file)


# Create worker threads


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
file.close()
