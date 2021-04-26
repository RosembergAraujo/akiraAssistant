#!/usr/bin/python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3
import os
import subprocess
import glob
import time

fromNone = False #Global variable that needs to be global


art = '█──██████────██████──█\n█─██────██──██────██─█\n─███─██─██████─██─███\n──██────██──██────██\n───██████────██████' #ASCii Art

engine = pyttsx3.init() 
engine.setProperty('voice', 'brazil')
engine.setProperty('rate', 230)

# Comandos \/ ============================

pPlaySongsCommands = ['musica', 'ouvir', 'playlist', 'tocar', 'toque'] #Commands with more than one possibility
pFilesCommands = ['arquivos', 'pastas', 'nautilus', 'nautilu', 'nautilo']

pGeneralCommands = ['chrome', 'terminal', 'atualizar', 'code', 'calculadora'] #Simple commands that have no variation
pPossibleCommands = [pPlaySongsCommands, pFilesCommands, pGeneralCommands] #Commands array, to make all together
pAllValideCommands = ['sair'] #I have to start this array, so "exit", is a good choice :)
for options in pPossibleCommands:
    pAllValideCommands.extend(options) #Extend all the others commands arrays in just one



pOpeningCommands = ['abra', 'abrir'] # BTW "p" means possibilities :)
pClosingCommands = ['fechar', 'feche', 'sair']
# Fim Comandos /\ ============================


# Reused functions \/ ============================
def stringTreatament(param): #A way to treat some useless exceptions and take off portuguese prepositions 
    removeList = [',', '', 'o', 'a', 'na', 'no', 'nos', 'nas', 'um', 'uma', 'akira', 'com', 'diretório', 'diretorio', 'diretor', 'gestor']
    for i in range(len(param) -1, -1, -1): #Run the array backward and remove all words on remove list
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
    os.system('cls' if os.name == 'nt' else 'clear') #Maybe its can run in windows ? who knows, right ?


def vOutput(resposta): #Voice output
    global engine
    engine.say(resposta)
    engine.runAndWait()

def vInput(vAudio, fromNone): #Voice input
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
# End of reused functions /\ ============================

# Akira functions \/ ============================

def dontGetIt(param):
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
        dontGetIt(param)
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
    atualSong = -1 #Need to be in a upper scope
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
        chosedSong = int(input("\nEntrada => ")) # Place holder keyboard input
        #chosedSong = int(vInput('Opções de 0 até {}'.format(songCounter -1), fromNone))
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
            #playInput = vInput('PlaylistMode ligado', fromNone)
            # Place holder keyboard input
            playInput = str(input("\n\n-1 PARA SAIR\n0.PARA LISTAR\n1.PARA PLAY\n2.PARA STOP \n3.Para proxima musica\n4.Para musica anterior\n5.PARA REMOVER UMA MUSICA\n>> "))
            playInputAsArray = playInput.lower().split(" ")
            playInput = stringTreatament(playInputAsArray)
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
                        quit()
                    fromNone = False
                    mainLoop()
                else:
                    fromNone = True
                    mainLoop()
        else:
            playInput = str(input(">")) #QUANDO COLOCAR INPUT DE VOZ COLOCAR O FROM NONE
    mainLoop()
# End of akira functions /\ ============================ 


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

            if inputAfterTreatment[0] in pAllValideCommands:
                for word in inputAfterTreatment:
                    if word != inputAfterTreatment[0]:
                        allParameter += word #Remove the already validate command and concatenate all the rest as a parammeter
                if inputAfterTreatment[0] == 'chrome':
                    try:
                        openChrome(allParameter)#Try to send this parammeter
                    except:
                        openChrome('')#Or just a empty string
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
                        updateSystem(allParameter)
                    except:
                        updateSystem('')
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
                dontGetIt(voiceInput)
    else: #If don't have any voice input, akira tries to get again but without voice output
        vOutput('none')
        fromNone = True
        start()


start()
