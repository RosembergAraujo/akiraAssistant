#!/usr/bin/python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3
import os
import subprocess
import glob
import time

fromNone = False #Variavel que precisa ser global, caso não diga nada, ele só espera


art = '█──██████────██████──█\n█─██────██──██────██─█\n─███─██─██████─██─███\n──██────██──██────██\n───██████────██████'

engine = pyttsx3.init()
engine.setProperty('voice', 'brazil')
engine.setProperty('rate', 230)

# Comandos \/ ============================

pPlaySongsCommands = ['musica', 'ouvir', 'playlist', 'tocar', 'toque'] #todos os comandos com mais de uma possibilidade
pFilesCommands = ['arquivos', 'pastas', 'nautilus', 'nautilu', 'nautilo']

pGeneralCommands = ['chrome', 'terminal', 'atualizar', 'code', 'calculadora'] #Comandos com uma só possibilidade
pPossibleCommands = [pPlaySongsCommands, pFilesCommands, pGeneralCommands] #Array de comandos
pAllValideCommands = ['sair'] #Precisa iniciar um array com algo, 'sair' é uma boa opção
for options in pPossibleCommands:
    pAllValideCommands.extend(options) #extende todos os comandos dos outros arrays



pOpeningCommands = ['abra', 'abrir']
pClosingCommands = ['fechar', 'feche', 'sair']
# Fim Comandos /\ ============================


# Funções reutilizadas \/ ============================
def stringTreatament(param): #nunca enviar parametro sem splitar antes para n 'comer' os 'os' 'nos'
    removeList = [',', '', 'o', 'a', 'na', 'no', 'nos', 'nas', 'um', 'uma', 'akira', 'com', 'diretório', 'diretorio', 'diretor', 'gestor']
    for i in range(len(param) -1, -1, -1): #TEM Q RODAR ESSA DESGRAÇA DE TRAS PRA FRENTE
        if param[i] in removeList:
            param.remove(param[i])
    return param

def displayArt(param):
    if param == True: cleanConsole() 
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
        displayArt(True)
        displayFig('Escutando...')
        if fromNone == False:
            vOutput(vAudio)
        r.adjust_for_ambient_noise(source)
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

# Funções ddo assistente \/ ============================

def naoEntendi(param):
    displayArt(True)
    print('\n\n🤔 Desculpe, \'{}\' não é um comando valido...' .format(param))
    vOutput('🤔 Desculpe, {} não é um comando valido... ' .format(param))
    start()

def openChrome(param):
    displayArt(True)
    displayFig('Abrindo chrome...')
    vOutput('Abrindo chrome')
    if param == '':
        os.system('xdg-open https://google.com/')
    elif param == 'youtube':
        os.system('xdg-open http://youtube.com')
    elif param == 'notion':
        os.system('xdg-open http://notion.so')

def openFiles(param):
    if param == 'atual':
        os.system('xdg-open ./')
        start()
    elif param == 'inicial' or param == '':
        os.system('xdg-open $HOME')
        start()
    elif param == None or param == 'voltar':
        start()
    else:
        naoEntendi(param)
        openFiles()

def openTerminal(param):
    displayArt(True)
    displayFig('Abrindo terminal...')
    vOutput('Abrindo terminal...')
    if param == '' or param == 'atual':
        os.system('gnome-terminal ./')
    elif param == 'inicial':
        os.system('gnome-terminal $HOME')

def openWithCode(param):
    displayArt(True)
    displayFig('Abrindo com o vscode...')
    vOutput('Abrindo com o code')
    os.system('code -n .')

def updateSystem(param):
    displayArt(True)
    displayFig('Atualizando...')
    vOutput('Atualizando')
    if param == 'somenteupdate':
        os.system('sudo apt-get update')
    elif param == 'somenteupgrade':
        os.system('sudo apt-get upgrade')
    else:
        os.system('sudo apt-get update')
        os.system('sudo apt-get upgrade')

def openCalculator(param):
    displayArt(True)
    displayFig('Abrindo calculadora...')
    vOutput('Abrindo calculadora')
    os.system('gnome-calculator')

def exit():
    displayArt(True)
    displayFig('Saindo...')
    vOutput('saindo')
    quit()




def playlistMode(param):
    atualSong = -1 #TEM Q SER VAR DE ESCOPO ACIMA DAS FUNÇÕES 
    songsMainPath = '/home/berg/Música/'
    songList = []
    songCounter = 0
    playSongProgram = 'vlc'

    def playSubProcess(audio_file_path):
        subprocess.call(["xdg-open", audio_file_path])

    def stopSubProcess(program):
        subprocess.call(["killall", program])

    def playSongFunc():
        global atualSong
        global songList
        global songCounter
        os.chdir(songsMainPath)
        for file in glob.glob("*.mp3"):
            songList.append(file)
        for i in songList:
            print("Arquivo ({0}) => {1}" .format(songCounter, i))
            songCounter+=1
        chosedSong = int(input("\nEntrada => ")) # ESCOLHA DA MUSICA
        if chosedSong < len(songList) -1 and chosedSong >= 0:
            atualSong = chosedSong
            playSubProcess("{0}{1}" .format(songsMainPath,songList[chosedSong]))
            time.sleep(0.7)
        else:
            print("FORA DO RANGE DAS MSCS")
            mainLoop()

    def listSongs():
        global atualSong
        global songList
        global songCounter
        os.chdir(songsMainPath)
        for file in glob.glob("*.mp3"):
            songList.append(file)
        for i in songList:
            print("Arquivo ({0}) => {1}" .format(songCounter, i))
            songCounter+=1

    def nextSongFunc():
        global atualSong
        global songList
        global songCounter

        print(atualSong)
        os.chdir(songsMainPath)
        for file in glob.glob("*.mp3"):
            songList.append(file)
        for songName in songList:
            print("Arquivo ({0}) => {1}" .format(songCounter, songName))
            songCounter+=1
        if atualSong +1 <= len(songList) -1 and atualSong != -1:
            atualSong += 1
            stopSubProcess(playSongProgram)
            time.sleep(0.7)
            playSubProcess("{0}{1}" .format(songsMainPath,songList[atualSong]))
        else:
            if atualSong != -1:
                print("\n\nULTIMO\n\n")
            else:
                print("\n\nNECESSARIO PLAY\n\n")

    def prevSongFunc():
        global atualSong
        global songList
        global songCounter
        os.chdir(songsMainPath)
        for file in glob.glob("*.mp3"):
            songList.append(file)
        for songName in songList:
            print("Arquivo ({0}) => {1}" .format(songCounter, songName))
            songCounter+=1
        if atualSong -1 >= 0 and atualSong != -1:
            atualSong -= 1
            stopSubProcess(playSongProgram)
            time.sleep(0.7)
            playSubProcess("{0}{1}" .format(songsMainPath,songList[atualSong]))
        else:
            if atualSong != -1:
                print("\n\nPRIMEIRA\n\n")
            else:
                print("\n\nNECESSARIO PLAY\n\n")

    def stopSongfunc():
        global atualSong
        stopSubProcess(playSongProgram)
        time.sleep(0.7)
        atualSong = -1

    def deleteSong():
        global songList
        global songCounter
        os.chdir(songsMainPath)
        for file in glob.glob("*.mp3"):
            songList.append(file)
        for i in songList:
            print("Arquivo ({0}) => {1}" .format(songCounter, i))
            songCounter+=1
        chosedSong = int(input("\Qual deseja apagar ? => "))
        os.system("mv {0}{1} trash" .format(songsMainPath,songList[chosedSong]))

    def mainLoop ():

        pListSongs = ['listar', 'lista', '0']
        pPlaySong = ['tocar', 'começar', 'play', '1']
        pStopSong = ['parar', '2']
        pNextSong = ['proximo', 'passar', '3']
        pPreviousSong = ['anterior', 'voltar', '4']
        pDeleSong = ['delete', 'apagar', '5']

        global songList
        global songCounter
        global fromNone
        songList = []
        songCounter = 0
        
        if fromNone == False:
            #playInput = vInput('Como posso ajudar ?', fromNone)
            playInput = str(input("\n\n-1 PARA SAIR\n0.PARA LISTAR\n1.PARA PLAY\n2.PARA STOP \n3.Para proxima musica\n4.Para musica anterior\n5.PARA REMOVER UMA MUSICA\n>> "))
            playInputAsArray = playInput.lower().split(" ")
            playInput = stringTreatament(playInputAsArray)
            print(playInput)
            if playInput[0] in pClosingCommands:
                exit()
            else:
                if playInput[0] != None:  
                    if playInput[0] in pListSongs:
                        listSongs()
                    elif playInput[0] in pPlaySong:
                        playSongFunc()
                    elif playInput[0] in pStopSong:
                        stopSongfunc()
                    elif playInput[0] in pNextSong:
                        nextSongFunc()
                    elif playInput[0] in pPreviousSong:
                        prevSongFunc()
                    elif playInput[0] in pDeleSong:
                        deleteSong()
                    elif playInput[0] in pClosingCommands:
                        exit()
                    fromNone = False
                    mainLoop()
                else:
                    fromNone = True
                    mainLoop()
        else:
            playInput = str(input(">")) #QUANDO COLOCAR INPUT DE VOZ COLOCAR O FROM NONE
    mainLoop()
# Fim das funções do assistente /\ ============================ 


def start():
    global fromNone
    firstCommand = ''
    allParameter = ''
    
    voiceInput = vInput(
       'Como posso ajudar ?', fromNone)   
    if voiceInput != None:
        if voiceInput in pClosingCommands:
            exit()
        else:
            fromNone = False

            inputAsArray = voiceInput.lower().split(' ') 
            inputAfterTreatment = stringTreatament(inputAsArray)
            
            if inputAfterTreatment[0] in pOpeningCommands:
                firstCommand = inputAfterTreatment[0]
                inputAfterTreatment.remove(firstCommand)

            if inputAfterTreatment[0] in pAllValideCommands: #Caso o comando for um dos comandos validos
                for word in inputAfterTreatment:
                    if word != inputAfterTreatment[0]:
                        allParameter += word #Tira o comando ja validado e concatena todo o resto como um parametro a ser enviado
                if inputAfterTreatment[0] == 'chrome':
                    try:
                        openChrome(allParameter)#tenta enviar com esse parametro
                    except:
                        openChrome('')#Se n conseguir, ele envia sem parametro
                elif inputAfterTreatment[0] in pFilesCommands:
                    try:
                        openFiles(allParameter)
                    except:
                        openFiles('')
                elif inputAfterTreatment[0] == 'terminal':
                    try:
                        openTerminal(allParameter)
                    except:
                        openTerminal('')
                elif inputAfterTreatment[0] == 'atualizar':
                    try:
                        openTerminal(allParameter)
                    except:
                        openTerminal('')
                elif inputAfterTreatment[0] == 'code':
                    try:
                        openWithCode(allParameter)
                    except:
                        openWithCode('')
                elif inputAfterTreatment[0] == 'calculadora':
                    try:
                        openCalculator(allParameter)
                    except:
                        openCalculator('')
                elif inputAfterTreatment[0] in pPlaySongsCommands:
                    try:
                        playlistMode(allParameter)
                    except:
                        playlistMode('')
            else:
                naoEntendi(voiceInput)
    else:
        vOutput('none')
        fromNone = True
        start()


start()
