#-*- coding:utf-8 -*-
"""
GUI Command functions for the assistant.
These functions handle GUI interactions, keyboard/mouse automation, and speech.
"""
from pynput.keyboard import Controller
import pyautogui
import pyttsx3


# Initialize text-to-speech engine
maquina = pyttsx3.init()


def falar(fala):
    """Speak the given text using text-to-speech."""
    maquina.say(fala)
    maquina.runAndWait()


def digitar(texto):
    """Type the given text using keyboard controller."""
    Controller().type(texto)


def aperta(botao):
    """Press the specified key(s) using pyautogui."""
    pyautogui.press(botao)


def abrirgaveta(teste):
    """Open drawer using keyboard shortcut."""
    pyautogui.hotkey('ctrl', 'shift', 'g')


def clicarNaNet(comando):
    """
    Click on element in browser by searching for text.
    Uses Ctrl+F to search and then clicks on the result.
    """
    falar('procurando')
    comando = comando.replace('clicar em ', '')
    pyautogui.hotkey('ctrl', 'f')
    digitar(comando)
    # Note: clicarNeste() would need to be imported or implemented here
    # For now, this is a simplified version
    pyautogui.hotkey('ctrl', 'enter')


def abrirInternet(teste):
    """Open internet browser using keyboard shortcut."""
    pyautogui.hotkey('ctrl', 'shift', 'c')
