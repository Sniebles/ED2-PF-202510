import socket as sk

client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
client.connect(('localhost', 10000))
client.sendall(bytes("Hello from Client", 'UTF-8'))
while True:
    in_data = client.recv(1024)
    if not in_data:
        break
    print("From Server:", in_data.decode())
    out_data = input("Reply to Server: ")
    client.sendall(bytes(out_data, 'UTF-8'))
    if out_data.lower() == 'bye':
        break