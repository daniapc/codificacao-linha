# TESTES SEM INTERFACE GRÁFICA, IGNORAR

import socket

# Coleta o endereço do receptor
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host = s.getsockname()[0]

# Criando porta e aguardando conexão
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, 12345))
sock.listen(5)
print("Aguardando conexão com o endereço do receptor " + host + "...")
con, addr = sock.accept()
mensagem = con.recv(1024)
con.sendall(mensagem)

socket.setdefaulttimeout(600)

# Loop de comunicação
loop = True
while (loop):

    print(mensagem)

    mensagem = con.recv(1024)
    con.sendall(mensagem)

    loop = not(mensagem == b'')

print("Conexão fechada.")
sock.close()