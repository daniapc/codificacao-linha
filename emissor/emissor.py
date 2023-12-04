import socket

loop = True

print("Conectando ao receptor...")

# Procurando endereços existentes no host
sock = socket.socket()
for i in range(0,255):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.05)
    result = sock.connect_ex(("192.168.1."+str(i), 12345))

    if result == 0:
        host = "192.168.1."+str(i)
        sock.sendall('Conexao estabelecida'.encode())
        print(sock.recv(1024))
        break
    else:
        sock.close()

socket.setdefaulttimeout(600)

# Loop de comunicação
while (loop):
    mensagem = input("Digitar mensagem: ")

    sock.sendall(mensagem.encode())
    print(sock.recv(1024))

    loop = not(input("Continuar? S/N ").lower() == 'n')

print("Conexão fechada.")
sock.close()