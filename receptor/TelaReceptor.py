import PySimpleGUI as sg
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt

CHAVE = "v3oK2y7pLpkodK374oVZ_we6cNp4qseOwfOCcSOq1mg="
ESCRITA = ""

class TelaReceptor:
    def __init__(self):

        layout = [
            [sg.Text('Mensagem Escrita'), sg.Input(key='escrita')],
            [sg.Button('Enviar')],
            [sg.Output(size=(100,15), key='impressao')]
        ]

        self.fernet = Fernet(CHAVE.encode())

        self.janela = sg.Window("Receptor").layout(layout)


    def Iniciar(self):
        self.button, self.values = self.janela.Read()

        while (not(self.janela.is_closed())):
            self.janela.FindElement('impressao').Update('')

            escrita = self.values['escrita']

            criptografada = self.fernet.encrypt(escrita.encode()).decode()

            binaria = bin(int.from_bytes(criptografada.encode(), "big"))[2:]

            hdb3 = self.hdb3(binaria)

            print(f'Mensagem Em HDB3: {hdb3}')
            print(f'Mensagem Em Binário: {binaria}')
            print(f'Mensagem Criptografada: {criptografada}')
            print(f'Mensagem Escrita: {escrita}')
            
            self.fazer_grafico(hdb3, "Gráfico HDB3")
            self.fazer_grafico(binaria, "Gráfico Binário")

            self.button, self.values = self.janela.Read()
            

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
        plt.show()


tela = TelaReceptor()
tela.Iniciar()