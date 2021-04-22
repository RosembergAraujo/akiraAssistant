#!/usr/bin/python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3
import os

fromNone = False #Variavel que precisa ser global, caso não diga nada, ele só espera
art = "█──██████────██████──█\n█─██────██──██────██─█\n─███─██─██████─██─███\n──██────██──██────██\n───██████────██████"
# Comandos \/ ============================

pAtualizar = ["atualizar", "atualizar o sistema",
              "procurar atualização", "abrir atualização"]
pNautilus = ["abrir nautilus", "abrir arquivos",
             "abrir pastas", "abrir pastas", "nautilus", "arquivos", "pastas"]
pCode = ["code", "abrir code", "abrir com o code",
         "abrir com code", "abrir no code", "abrir o code"]
pAbrirTerminal = ["abrir terminal", "terminal", "abrir o terminal"]
pSair = ["sair", "saindo", "fechar", "tchau", "tchau akira", "fechar akira", "fechando"]
pCalculadora = ["abrir calculadora", "abrir a calculadora", "calculadora"]
pPrint = ["print", "tirar print", "capturar tela"]
pChrome = ["abrir chrome", "chrome", "abrir o chrome"]
pAbrirCelular = ["abrir celular", "abrir tela do celular", "tela do celular", "me mostre meu celular", "me mostre a tela do meu celular"]

# Fim Comandos /\ ============================


# Funções de Fala \/ ============================
def exibirArt():
    print(art + "\n")
    os.system("figlet -f future A K I R A")

def limparConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

engine = pyttsx3.init()
engine.setProperty('voice', 'brazil')
engine.setProperty('rate', 230)
def vOutput(resposta):
    global engine
    engine.say(resposta)
    engine.runAndWait()

def vInput(write, vAudio, fromNone):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        limparConsole()
        exibirArt()
        print("\n\n\n{}\n\n\n" .format(write))
        os.system("figlet -f pagga Escutando...")
        if (fromNone == False):
            vOutput(vAudio)
        audio = r.listen(source)
    try:
        input = r.recognize_google(audio, language="pt-br")
        return input.lower()
    except sr.UnknownValueError:
        print("Aguardando...")
    except sr.ResquestError as e:
        print(
            "Ero ao chamar Google speech Recognition service; {0}" .format(e))
# Fim das funções de Fala /\ ============================

# Funções da IA \/ ============================


def naoEntendi(param):
    limparConsole()
    exibirArt()
    print("🤔 Desculpe, \"{}\" não é um comando valido..." .format(param))
    vOutput("🤔 Desculpe, {} não é um comando valido... " .format(param))


def atualizar():
    limparConsole()
    print("Atualizando...")
    vOutput("Atualizando")
    os.system('sudo apt-get update')
    os.system('sudo apt-get upgrade')


def abrirTerminal():
    limparConsole()
    print("Abrindo terminal...")
    vOutput("Abrindo terminal")
    os.system('gnome-terminal ./')


def abrirNoCode():
    limparConsole()
    print("Abrindo com o code o diretorio atual...")
    vOutput("Abrindo com o code")
    os.system('code .')


def abrirCalculadora():
    limparConsole()
    print("Abrindo calculadora...")
    vOutput("Abrindo calculadora")
    os.system('gnome-calculator')


def tirarPrint():
    limparConsole()
    exibirArt()
    print("Tirando print... SALVO EM IMAGENS")
    vOutput("Tirando print")
    os.system('gnome-screenshot')


def abrirNautilus():

    pAtual = ["atual", "no atual", "diretório atual",
              "no diretório atual", "o diretório atual"]
    pInicial = ["inicial", "no inicial",
                "diretório inicial", "o diretório inicial"]

    choice = vInput("Onde deseja abrir?\n\nOpções:\n\n*INICIAL\n*ATUAL\n*VOLTAR\n*SAIR",
                    "diretorio atual ou no inicial ?", False)
    if (choice in pAtual):
        os.system('xdg-open ./')
        fromNone = False
        start()
    elif (choice in pInicial):
        os.system('xdg-open $HOME')
        fromNone = False
        start()
    elif (choice == None or choice == "voltar"):
        start()
    elif (choice in pSair):
        sair()
    else:
        naoEntendi(choice)
        abrirNautilus()


def abrirChrome():
    limparConsole()
    print("Abrindo chrome...")
    vOutput("Abrindo chrome")
    os.system('google-chrome')

def abrirScrcpy():
    limparConsole()
    print("Abrindo tela do celular...")
    vOutput("Abrindo tela do celular")
    os.system("scrcpy")


def config():
    os.system('code $HOME/.local/bin')

def sair():
    limparConsole()
    exibirArt()
    print("\n\nSaindo...")
    vOutput("Saindo")
    limparConsole()
    quit()
# Fim das funções da IA /\ ============================


def start():
    global fromNone

    firstInput = vInput(
        "Olá, eu sou o akira 👾, como posso te ajudar?", "Como posso ajudar ?", fromNone)

    if (firstInput in pAtualizar):
        fromNone = False
        atualizar()
    elif (firstInput in pAbrirTerminal):
        fromNone = False
        abrirTerminal()
    elif (firstInput in pNautilus):
        limparConsole()
        fromNone = False
        abrirNautilus()
    elif (firstInput == "config"):
        fromNone = False
        config()
    elif (firstInput in pCode):
        fromNone = False
        abrirNoCode()
    elif (firstInput in pCalculadora):
        fromNone = False
        abrirCalculadora()
    elif (firstInput in pPrint):
        fromNone = False
        tirarPrint()
    elif (firstInput in pChrome):
        fromNone = False
        abrirChrome()
    elif (firstInput in pAbrirCelular):
        fromNone = False
        abrirScrcpy()
    elif (firstInput in pSair):
        sair()
    elif (firstInput == None): #Caso n tenha um input, ele "espera"
        fromNone = True
    else:
        fromNone = False
        naoEntendi(firstInput)
    start()


start()
