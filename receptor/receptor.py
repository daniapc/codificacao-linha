import socket

loop = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
sock.bind((host, 12345))
sock.listen(5)

print("Aguardando conexão.")
con, addr = sock.accept()

while (loop):

    mensagem = con.recv(1024)

    con.sendall(mensagem)

    print(mensagem)

    loop = not(input("Continuar? S/N ").lower() == 'n')

print("Conexão fechada.")
sock.close()