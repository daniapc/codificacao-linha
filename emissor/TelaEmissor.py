import PySimpleGUI as sg
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt
import socket

CHAVE = "v3oK2y7pLpkodK374oVZ_we6cNp4qseOwfOCcSOq1mg="

class TelaEmissor:
    def __init__(self):

        self.layout = [
            [sg.Text('Realizando conexão com o receptor...')],
            [sg.Text('Mensagem Escrita'), sg.Input(key='escrita')],
            [sg.Button('Enviar'), sg.Button('Gráfico Binário'), sg.Button('Gráfico HDB3')],
            [sg.Output(size=(200,30), key='impressao')],
            [sg.Text('Conexão fechada')]
        ]
        
        self.estado = 'Carregando'

        self.fernet = Fernet(CHAVE.encode())

    def Iniciar(self):
        janela = sg.Window("Carregando Emissor").layout(self.layout[:1])

        self.button, self.values = janela.Read(timeout=0)

        while (self.estado == 'Carregando'):
            sock = socket.socket()
            for i in range(0,255):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.05)
                result = sock.connect_ex(("192.168.1."+str(i), 12345))

                if result == 0:
                    self.estado = 'Conexao estabelecida'
                    # sock.sendall((self.estado).encode())
                    # print(sock.recv(1024))
                    break
                else:
                    sock.close()
        
        socket.setdefaulttimeout(600)

        janela.close()

        janela = sg.Window("Emissor").layout(self.layout[1:-1])

        self.button, self.values = janela.Read()
        # print(f'Conectando ao receptor...')
        escrita = ''
        criptografada = ''
        binaria = ''
        hdb3 = ''

        while (not(janela.is_closed())):
            janela.FindElement('impressao').Update('')
                
            if (self.button == 'Enviar'):

                escrita = self.values['escrita']

                criptografada = self.fernet.encrypt(escrita.encode()).decode()

                codigoascii = criptografada.encode('utf-8')

                binaria = ''.join([str(int(str(bin(bit))[2:])+100000000)[1:] for bit in codigoascii])
                # binaria = bin(int.from_bytes(criptografada.encode(), "big"))[2:]

                hdb3 = self.hdb3(binaria)

                sock.sendall(hdb3.encode())
                # print(sock.recv(1024))

            if (self.button == 'Gráfico Binário'):
                self.fazer_grafico(binaria, "Gráfico Binário")
            if (self.button == 'Gráfico HDB3'):
                self.fazer_grafico(hdb3, "Gráfico HDB3")

            print(f'Mensagem Escrita:\n{escrita}\n')
            print(f'Mensagem Criptografada:\n{criptografada}\n')
            print(f'Mensagem Em Binário:\n{binaria}\n')
            print(f'Mensagem Em HDB3:\n{hdb3}\n')

            self.button, self.values = janela.Read()

        sock.close()
        # janela = sg.Window("Fim").layout(self.layout[-1:])
            

    def hdb3(self, binario):
        substituido = list(binario)
        
        index = 0
        
        pulsos_high = 0

        size = len(binario)-3

        while index < size:

            if binario[index] == '1':
                pulsos_high += 1

            sequencia = binario[index:index+4]

            if sequencia == '0000':
                if pulsos_high%2 == 0:
                    substituido[index]   = 'B'
                    substituido[index+1] = '0'
                    substituido[index+2] = '0'
                    substituido[index+3] = 'V'
                else:
                    substituido[index]   = '0'
                    substituido[index+1] = '0'
                    substituido[index+2] = '0'
                    substituido[index+3] = 'V'

                pulsos_high = 0
                index += 3
            
            index += 1
        
        
        return ''.join(substituido)

    def fazer_grafico(self, binario, titulo):
        if binario == '':
            return

        tam = len(binario)

        binario = binario.replace('B', '1').replace('V', '1')

        fig = plt.figure(titulo)

        plt.plot((0, 0+1), (int(binario[0]), int(binario[0])), color = 'b')

        for i in range(1, tam -1):
            value = int(binario[i])

            if binario[i - 1] == '0':
                plt.plot((i, i), (0, value), color = 'b')
            plt.plot((i, i+1), (value, value), color = 'b')
            if binario[i + 1] == '0':
                plt.plot((i+1, i+1), (value, 0), color = 'b')
        
        if binario[tam - 1] == '0':
            plt.plot((tam-1, tam-1), (0, int(binario[tam-1])), color = 'b')
        plt.plot((tam-1, tam-1), (int(binario[tam-1]), int(binario[tam-1])), color = 'b')

        ax = plt.gca() 
        ax.set_ylim([0, 2])
        plt.xlabel("X")
        plt.ylabel("y")
        plt.title(titulo)

        plt.draw()
        plt.show()


tela = TelaEmissor()
tela.Iniciar()