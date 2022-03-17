import speech_recognition as sr
import pyautogui
import pyttsx3
import time

r = sr.Recognizer()
maquina  = pyttsx3.init()

def falar (fala):
    maquina.say(fala)
    maquina.runAndWait

def digitar (texto):
    pyautogui.write(str(texto))

def clicar (botao):
    pyautogui.press(botao)

def comandos(comando):
    if 'fale' in comando:
        comando = comando.replace('fale ','')
        falar(comando)
    elif 'digitar' in comando:
        comando = comando.replace('digitar ','')
        digitar(comando)
    else:
        falar('Diga um comando corretamente')



with sr.Microphone() as s:
    r.adjust_for_ambient_noise(s)

    while True:
        audio = r.listen(s)
        comando = r.recognize_google(audio, language ='pt-BR',show_all=True)
        if comando == []:
            print(comando)
        else:
            comando = r.recognize_google(audio, language ='pt-BR')
            if 'xerife' in comando:
                comando = comando.replace('xerife ','')
                falar('Olá')
                comandos(comando)
            else:
             print (comando)

