import random as rd
from tkinter import CENTER, Tk
import PySimpleGUI as sg
import string
sg.theme("Dark Teal 6")
sg.set_options(font=("Verdana", 12))


lowercase_letters = string.ascii_lowercase
uppercase_letters = string.ascii_uppercase
numbers = string.digits
symbols = string.punctuation
possible_chars = " "
lowercases_enabled, uppercases_enabled, numbers_enabled, symbols_enabled = True, True, True, False
repeateds_disabled = False
pwd_limit = [*range(8,25)]
pwd_lenght = 8

def make_pwd_win():
    layout = [  [sg.T("Senha gerada:"),\
                 sg.In("", justification=CENTER, readonly=True, size=(28 , 1), k=("password"), text_color="Black"),\
                 sg.Spin(pwd_limit, size=(2, 1), tooltip=("Tamanho da senha gerada"), readonly=True, k=("lenght"),\
                        enable_events=True, text_color="Black")],
                [sg.B("Gerar senha"), sg.B("Copiar"), sg.B("Configurações"), sg.B("Cancelar")] ]
    return sg.Window("Gerador de Senhas", layout, finalize=True)
def make_cfg_win():

    layout_l = [    [sg.CB("Incluir letras minúsculas.", default=lowercases_enabled, k="lowercase_enabled", enable_events=True)],
                    [sg.CB("Incluir letras maiúsculas.", default=uppercases_enabled, k="uppercase_enabled", enable_events=True)],
                    [sg.CB("Incluir números.", default=numbers_enabled, k="number_enabled", enable_events=True)],
                    [sg.CB("Incluir símbolos.", default=symbols_enabled, k="symbol_enabled", enable_events=True)],
                    [sg.CB("Não usar caracteres repetidos.", default=repeateds_disabled, k="repeated_disabled", enable_events=True)] ]
    layout_r = [    [sg.T("(Ex. a, b, c, d)", pad=(None, 5))],
                    [sg.T("(Ex. A, B, C, D)", pad=(None, 5))],
                    [sg.T("(Ex. 1, 2, 3, 4)", pad=(None, 5))],
                    [sg.T("(Ex. $, @, #, %)", pad=(None, 5))],
                    [sg.T("(Ex. 111, aaa, $$$)", pad=(None, 5))] ]
    layout = [      [sg.Column(layout_l), sg.Column(layout_r)],
                    [sg.B("Salvar"), sg.B("Padrão")]]
    return sg.Window("Configurações", layout, finalize=True) 
def set_chars():
    enabled_chars =""
    if lowercases_enabled:
        enabled_chars += lowercase_letters
    if uppercases_enabled:
        enabled_chars += uppercase_letters
    if numbers_enabled:
        enabled_chars += numbers
    if symbols_enabled:
        enabled_chars += symbols
    return enabled_chars
def generate_password():
    if len(possible_chars) < 1:
        return ""
    password = ""
    set_chars()
    possible_chars_list = list(possible_chars)
    for i in range(pwd_lenght+1):
        random = rd.randint(0, len(possible_chars_list)-1)
        password += possible_chars_list[random]
        if repeateds_disabled:
            possible_chars_list.pop(random)
        if len(possible_chars_list) == 0:
            return password
    return password
def copy_to_clipboard():
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(values["password"])
    r.update()
    r.destroy()
def save_settings(values):
    global lowercases_enabled
    global uppercases_enabled
    global numbers_enabled
    global symbols_enabled
    global repeateds_disabled
    lowercases_enabled = values["lowercase_enabled"]
    uppercases_enabled = values["uppercase_enabled"]
    numbers_enabled = values["number_enabled"]
    symbols_enabled = values["symbol_enabled"]
    repeateds_disabled = values["repeated_disabled"]
def default_settings(window):
    window["lowercase_enabled"].update(True)
    window["uppercase_enabled"].update(True)
    window["number_enabled"].update(True)
    window["symbol_enabled"].update(False)
    window["repeated_disabled"].update(False)

pwd_window, cfg_window = make_pwd_win(), None

while True:
    window, event, values = sg.read_all_windows()
    possible_chars = set_chars()
    if event == sg.WIN_CLOSED or event == "Cancelar":
        window.close()
        if window == cfg_window:
            window = None
        elif window == pwd_window:
            break
    elif event == "lenght":
        pwd_lenght = values["lenght"]
    elif event == "Gerar senha":
        window["password"].update(generate_password())
    elif event == "Copiar":
        copy_to_clipboard()
    elif event == "Configurações":
        window = make_cfg_win()
    elif event == "Salvar":
        save_settings(values)
        possible_chars = set_chars()
        window.close()
    elif event == "Padrão":
        default_settings(window)
