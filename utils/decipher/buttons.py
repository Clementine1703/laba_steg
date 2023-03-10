import tkinter

def create_button(window, text, command):
    btn = tkinter.Button(window , text=text, command=command)
    btn.pack()
    
