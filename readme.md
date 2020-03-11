# MultiClient-Sever

## About Project

This is a basic implemetnation of multiclient server model. I have used this to develop my system of voting.
In this project, a voter can cast the vote at the client side. At the server side, the real time statistics of votes can be viewed using a simple few command.

## Environment

I ran this on Windows Home but I think it can be run on any operating system. It can even run on MACOS but may require a few installation.

## Software Used

I used Visual Studio Code to write my codes and used terminal to run the programs. The version for Visual studio Code is 1.43.0.

## Requirements

This requires Python 3.8.2 . To install python3

```shell
$ python -m pip install --upgrade pip
```

## Run the programs

We have two files here server.py and client.py
Open two terminal tabs
Use cd command to get into the directory where these files are stored.
Then on

### Server

Run

```shell
$ python3 server.py
```

Now, our server is live

### Client

Run

```shell
$ python3 client.py
```

Client is counnected to server now.

## Sample Test of system

### Server

Start by showing the list of connections established.

```shell
list
```

Then start elections, that is to initialize all the candidates' votes to zero

```shell
startelection
```

Now see, the statistics, by

```shell
stat
```

This will show

```
{'A':0,'B':0,'C':0}
```

Now, conect to the client using

```shell
select 0
```

This will make connection to client 0
Move to client tab
Coming back from client
Check whether vote has been added by

```shell
stat
```

### Client

Now at client Enter input

```
123456789
```

press enter or return key

```
A
```

Back at server tab
