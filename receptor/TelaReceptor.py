import PySimpleGUI as sg
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt
import socket

CHAVE = "v3oK2y7pLpkodK374oVZ_we6cNp4qseOwfOCcSOq1mg="

class TelaReceptor:
    def __init__(self):

        # Coleta o endereço do receptor
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.host = s.getsockname()[0]

        self.layout = [
            [sg.Text("Aguardando conexão com o endereço do receptor " + self.host + "...")],
            # [sg.Text('Mensagem Escrita'), sg.Input(key='escrita')],
            [sg.Button('Receber'), sg.Button('Gráfico Binário'), sg.Button('Gráfico HDB3')],
            [sg.Output(size=(200,30), key='impressao')],
            [sg.Text('Conexão fechada')]
        ]
        
        self.estado = 'Carregando'

        self.fernet = Fernet(CHAVE.encode())

    def Iniciar(self):

        janela = sg.Window(title="Carregando Receptor").layout(self.layout[:1])
        self.button, self.values = janela.Read(timeout=0)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, 12345))
        sock.listen(5)
        con, addr = sock.accept()
        
        socket.setdefaulttimeout(600)

        janela.close()

        janela = sg.Window("Receptor").layout(self.layout[1:-1])

        self.button, self.values = janela.Read()
        hdb3 = ''
        binaria = ''
        criptografada = ''
        escrita = ''

        try:

            while (not(janela.is_closed())):
                janela.FindElement('impressao').Update('')
                    
                if (self.button == 'Receber'):

                    hdb3 = con.recv(2048).decode()

                    binaria = hdb3.replace('B00V','0000').replace('000V', '0000')

                    criptografada = self.desbinarizar(binaria)

                    escrita = self.fernet.decrypt(criptografada.encode()).decode()

                if (self.button == 'Gráfico Binário'):
                    self.fazer_grafico(binaria, "Gráfico Binário")
                if (self.button == 'Gráfico HDB3'):
                    self.fazer_grafico(hdb3, "Gráfico HDB3")

                print(f'Mensagem Em HDB3:\n{hdb3}\n')
                print(f'Mensagem Em Binário:\n{binaria}\n')
                print(f'Mensagem Criptografada:\n{criptografada}\n')
                print(f'Mensagem Escrita:\n{escrita}\n')

                self.button, self.values = janela.Read()
            sock.close()
            
        except:
            sock.close()
        # janela = sg.Window("Fim").layout(self.layout[-1:])
            

    def desbinarizar(self, binaria):
        criptografada = ''
        i = 0
        while i < len(binaria):
            criptografada += chr(int(binaria[i:i+8],2))
            i += 8

        return criptografada

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


tela = TelaReceptor()
tela.Iniciar()