import socket

loop = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
sock.connect((host, 12345))

while (loop):
    mensagem = input("Digitar mensagem: ")

    sock.sendall(mensagem.encode())

    print(sock.recv(1024))

    loop = not(input("Continuar? S/N ").lower() == 'n')

print("Conexão fechada.")
sock.close()