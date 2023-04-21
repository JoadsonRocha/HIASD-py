import os
from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image


def open_video(event=None):
    # obtém o nome do arquivo digitado pelo usuário
    video_name = entry.get()
    filename = f"{video_name}.mp4"
    
    if video_name == "":
        messagebox.showerror('Atenção', 'Digite um Hino')
        entry.delete(0, tk.END)
    elif not os.path.isfile(filename):
        messagebox.showerror('Atenção', 'Hino Não Encontrado')
        entry.delete(0, tk.END)
    else:
        # executa o comando no terminal para abrir o arquivo no player padrão
        os.system(f'xdg-open "{filename}"')
        # Apagar texto apos o click
        entry.delete(0, tk.END)


# cria a janela principal
janela = tk.Tk()
janela.title('Hinário Adventista - 2023')
janela.geometry("800x600")
janela.resizable(False, False)
# fundo do hinario
img = Image.open("background.png")
photo = ImageTk.PhotoImage(img)
# Cria um widget Canvas com a imagem como plano de fundo
canvas = Canvas(janela, width=photo.width(), height=photo.height())
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack()

# cria a entrada de texto para o nome do arquivo
entry = tk.Entry(janela)
entry.pack(padx=10, pady=10)
entry.place(relx=0.5, rely=0.5, anchor=CENTER)
entry.insert(0, 'Digite um Hino!')
entry.bind('<FocusIn>', lambda event: entry.delete(0, 'end'))
button = tk.Button(janela, text='Abrir', command=open_video)
button.place(relx=0.5, rely=0.56, anchor=CENTER)  # centraliza os blocos
# Configuração de componetes
janela.config(background='#fff')
entry.config(justify='center', font='fontes')
button.config(background='#E6AA00', bd='0',
              activebackground='#fff', fg='#fff', font='fontes')


# conecta a função open_video à entrada de texto
entry.bind("<Return>", open_video)


# exibe a janela principal
janela.mainloop()
