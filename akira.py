#!/usr/bin/python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3
import os

engine = pyttsx3.init()
engine.setProperty('voice', 'brazil')
engine.setProperty('rate', 230)
fromNone = False #Variavel que precisa ser global, caso não diga nada, ele só espera
art = '█──██████────██████──█\n█─██────██──██────██─█\n─███─██─██████─██─███\n──██────██──██────██\n───██████────██████'
# Comandos \/ ============================

pCommands = ['chrome', 'terminal', 'nautilus', 'atualizar', 'code', 'sair', 'calculadora', 'print']
pOpeningCommands = ['abra', 'abrir']
pClosingCommands = ['fechar', 'feche']
# Fim Comandos /\ ============================


# Funções reutilizadas \/ ============================
def stringTreatament(param): #nunca enviar parametro sem splitar antes para n 'comer' os 'os' 'nos'
    removeList = [',', 'o', 'a', 'na', 'no', 'nos', 'nas', 'akira', 'com', 'diretório', 'diretorio', 'diretor']
    for i in range(len(param) -1, -1, -1): #TEM Q RODAR ESSA DESGRAÇA DE TRAS PRA FRENTE
        if param[i] in removeList:
            param.remove(param[i])
    return param

def displayArt():
    cleanConsole()
    print(art + '\n')
    os.system('figlet -f pagga A K I R A')

def displayFig(param):
    os.system('\n\n\nfiglet -f future {}'.format(param))

def cleanConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def vOutput(resposta):
    global engine
    engine.say(resposta)
    engine.runAndWait()

def vInput(vAudio, fromNone):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        displayArt()
        displayFig('Escutando...')
        if (fromNone == False):
            vOutput(vAudio)
        audio = r.listen(source)
    try:
        input = r.recognize_google(audio, language='pt-br')
        return input.lower()
    except sr.UnknownValueError:
        print('Aguardando...')
    except sr.ResquestError as e:
        print(
            'Ero ao chamar Google speech Recognition service; {0}' .format(e))
# Fim das funções reutilizadas /\ ============================

# Funções da IA \/ ============================

'''
def closeTerminal():
    cleanConsole()
    print('Fechado terminal...')
    vOutput('Fechando terminal')

def openWithCode():
    cleanConsole()
    print('Abrindo com o code o diretorio atual...')
    vOutput('Abrindo com o code')
    os.system('code .')


def openCalculator():
    cleanConsole()
    print('Abrindo calculadora...')
    vOutput('Abrindo calculadora')
    os.system('gnome-calculator')


def tirarPrint():
    cleanConsole()
    displayArt()
    print('Tirando print... SALVO EM IMAGENS')
    vOutput('Tirando print')
    os.system('gnome-screenshot')

def abrirScrcpy():
    cleanConsole()
    print('Abrindo tela do celular...')
    vOutput('Abrindo tela do celular')
    os.system('scrcpy')


def config():
    os.system('code $HOME/.local/bin')

def sair():
    cleanConsole()
    displayArt()
    print('\n\nSaindo...')
    vOutput('Saindo')
    cleanConsole()
    quit()

# Fim das funções da IA /\ ============================ 
'''
def naoEntendi(param):
    displayArt()
    print('\n\n🤔 Desculpe, \'{}\' não é um comando valido...' .format(param))
    vOutput('🤔 Desculpe, {} não é um comando valido... ' .format(param))
    start()

def openChrome(param):
    displayArt()
    displayFig('Abrindo chrome...')
    vOutput('Abrindo chrome')
    if (param == ''):
        os.system('xdg-open https://google.com/')
    elif(param == 'youtube'):
        os.system('xdg-open http://youtube.com')
    elif(param == 'notion'):
        os.system('xdg-open http://notion.so')

def openNautilus(param):
    if (param == 'atual'):
        os.system('xdg-open ./')
        start()
    elif (param == 'inicial' or param == ''):
        os.system('xdg-open $HOME')
        start()
    elif (param == None or param == 'voltar'):
        start()
    else:
        naoEntendi(param)
        openNautilus()

def openTerminal(param):
    displayArt()
    displayFig('Abrindo terminal...')
    vOutput('Abrindo terminal...')
    if(param == '' or param == 'atual'):
        os.system('gnome-terminal ./')
    elif(param == 'inicial'):
        os.system('gnome-terminal $HOME')

def updateSystem(param):
    displayArt()
    displayFig('Atualizando...')
    vOutput('Atualizando')
    if param == 'somenteupdate':
        os.system('sudo apt-get update')
    elif param == 'somenteupgrade':
        os.system('sudo apt-get upgrade')
    else:
        os.system('sudo apt-get update')
        os.system('sudo apt-get upgrade')

def start():

    global fromNone
    firstCommand = ''
    allParameter = ''

    voiceInput = vInput(
        'Como posso ajudar ?', fromNone)
    if (voiceInput != None):
        fromNone = False

        inputAsArray = voiceInput.lower().split(' ')
        inputAfterTreatment = stringTreatament(inputAsArray)

        if(inputAfterTreatment[0] in pOpeningCommands or inputAfterTreatment[0] in pClosingCommands):
            firstCommand = inputAfterTreatment[0]
            inputAfterTreatment.remove(firstCommand)

        if(inputAfterTreatment[0] in pCommands): #Caso o comando for um dos comandos validos
            if(firstCommand in pOpeningCommands): #Apenas para comandos de abertura de 'programas'
                for i in inputAfterTreatment:
                    if (i != inputAfterTreatment[0]):
                        allParameter += i #Tira o comando ja validado e concatena todo o resto como um parametro a ser enviado
                if(inputAfterTreatment[0] == 'chrome'):
                    try:
                        openChrome(allParameter)#tenta enviar com esse parametro
                    except:
                        openChrome('')#Se n conseguir, ele envia sem parametro
                elif(inputAfterTreatment[0] == 'nautilus'):
                    try:
                        openNautilus(allParameter)
                    except:
                        openNautilus('')
                elif(inputAfterTreatment[0] == 'terminal'):
                    try:
                        openTerminal(allParameter)
                    except:
                        openTerminal('')
                elif(inputAfterTreatment[0] == 'atualizar'):
                    try:
                        openTerminal(allParameter)
                    except:
                        openTerminal('')
        else:
            print('NOT IN COMMANDS')
    else:
        vOutput('none')
        fromNone = True
        start()


start()
