import PySimpleGUI as sg
from cryptography.fernet import Fernet

CHAVE = "v3oK2y7pLpkodK374oVZ_we6cNp4qseOwfOCcSOq1mg="

class TelaEmissor:
    def __init__(self):

        layout = [
            [sg.Text('Mensagem Escrita'), sg.Input(key='escrita')],
            [sg.Button('Enviar')],
            [sg.Output(size=(100,15), key='impressao')]
        ]

        self.fernet = Fernet(CHAVE.encode())

        self.janela = sg.Window("Emissor").layout(layout)


    def Iniciar(self):
        self.button, self.values = self.janela.Read()

        while (not(self.janela.is_closed())):
            self.janela.FindElement('impressao').Update('')

            escrita = self.values['escrita']

            criptografada = self.fernet.encrypt(escrita.encode()).decode()

            binaria = bin(int.from_bytes(criptografada.encode(), "big"))[2:]

            print(f'Mensagem Escrita: {escrita}')
            print(f'Mensagem Criptografada: {criptografada}')
            print(f'Mensagem Em Binário: {binaria}')

            self.button, self.values = self.janela.Read()


tela = TelaEmissor()
tela.Iniciar()