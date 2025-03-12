import os
import platform
import tkinter as tk
import json
from tkinter import messagebox
from PIL import ImageTk, Image

# Configurações
PASTA_HINOS = "hinos"
ARQUIVO_HINOS_JSON = "hinos.json"

def carregar_hinos():
    """Carrega o dicionário de hinos a partir do arquivo JSON"""
    try:
        with open(ARQUIVO_HINOS_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Erro Crítico", "Arquivo hinos.json não encontrado!")
        exit()
    except json.JSONDecodeError:
        messagebox.showerror("Erro Crítico", "Erro na formatação do arquivo hinos.json!")
        exit()

def verificar_pasta_hinos():
    """Cria a pasta de hinos se não existir"""
    if not os.path.exists(PASTA_HINOS):
        try:
            os.makedirs(PASTA_HINOS)
            messagebox.showinfo("Informação", f'Pasta "{PASTA_HINOS}" criada com sucesso!')
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar pasta: {str(e)}")
            exit()

# Inicialização
hinos = carregar_hinos()
verificar_pasta_hinos()

def open_video(event=None):
    entrada = entry.get()
    numero = ''.join(filter(str.isdigit, entrada))
    
    if not numero:
        messagebox.showerror('Erro', 'Digite um número de hino válido')
        entry.delete(0, tk.END)
        return
    
    # Caminho completo do arquivo
    filename = os.path.join(PASTA_HINOS, f"{numero}.mp4")
    
    if not os.path.isfile(filename):
        messagebox.showerror('Erro', f'Hino {numero} não encontrado na pasta "{PASTA_HINOS}"')
    else:
        try:
            sistema = platform.system()
            if sistema == 'Windows':
                os.startfile(filename)
            elif sistema == 'Darwin':
                os.system(f'open "{filename}"')
            else:
                os.system(f'xdg-open "{filename}"')
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao abrir: {str(e)}')
    
    entry.delete(0, tk.END)

def atualizar_sugestoes(event):
    texto = entry.get().lower()
    lista_sugestoes.delete(0, tk.END)
    
    if texto:
        for num, nome in hinos.items():
            busca = f"{num} - {nome}".lower()
            if texto in busca or texto in num or texto in nome.lower():
                lista_sugestoes.insert(tk.END, f"{num} - {nome}")
        
        if lista_sugestoes.size() > 0:
            lista_sugestoes.place(relx=0.5, rely=0.55, anchor=tk.N, width=400, height=120)
        else:
            lista_sugestoes.place_forget()
    else:
        lista_sugestoes.place_forget()

def selecionar_sugestao(event):
    if lista_sugestoes.curselection():
        index = lista_sugestoes.curselection()[0]
        entrada = lista_sugestoes.get(index)
        entry.delete(0, tk.END)
        entry.insert(0, entrada)
        lista_sugestoes.place_forget()

# Configuração da janela
janela = tk.Tk()
janela.title('Hinário Adventista - 2025')

# Configurar ícone personalizado
try:
    logo_img = Image.open("logo.png")
    photo_icon = ImageTk.PhotoImage(logo_img)
    janela.iconphoto(True, photo_icon)
except FileNotFoundError:
    messagebox.showwarning("Ícone não encontrado", "Arquivo logo.png não encontrado. Usando ícone padrão.")
except Exception as e:
    messagebox.showwarning("Erro no ícone", f"Não foi possível carregar o ícone: {str(e)}")

janela.geometry("800x600")
janela.resizable(False, False)

# Carregar imagem de fundo
try:
    img = Image.open("background.png")
    photo = ImageTk.PhotoImage(img)
    background_label = tk.Label(janela, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    janela.config(background='#FFFFFF')
    messagebox.showwarning('Aviso', 'Imagem de fundo não encontrada!')

# Container principal
input_container = tk.Frame(janela, bg='#282C34')
input_container.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Campo de entrada estilizado
entry = tk.Entry(
    input_container,
    font=('Helvetica', 12),
    width=30,
    bg='#3C4048',
    fg='white',
    insertbackground='white',
    relief=tk.FLAT,
    highlightthickness=3,
    highlightcolor='#FFC107',
    highlightbackground='#3C4048',
    justify='left'
)
entry.pack(side=tk.LEFT, padx=(0, 10), ipady=2)
entry.insert(0, 'Digite o número ou nome...')
entry.bind('<FocusIn>', lambda e: entry.delete(0, tk.END) if entry.get() == 'Digite o número ou nome...' else None)

# Botão estilizado
btn_abrir = tk.Button(
    input_container,
    text='▶ Tocar Hino',
    command=open_video,
    bg='#FFC107',
    fg='black',
    activebackground='#FFD54F',
    font=('Helvetica', 12, 'bold'),
    relief=tk.FLAT,
    padx=15,
    pady=2,
    cursor='hand2'
)
btn_abrir.pack(side=tk.LEFT)

# Lista de sugestões
lista_sugestoes = tk.Listbox(
    janela,
    bg='#3C4048',
    fg='white',
    font=('Helvetica', 12),
    selectbackground='#FFC107',
    selectforeground='black',
    relief=tk.FLAT,
    activestyle='none',
    bd=2
)

# Barra de rolagem
scrollbar = tk.Scrollbar(lista_sugestoes, orient=tk.VERTICAL)
scrollbar.config(command=lista_sugestoes.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
lista_sugestoes.config(yscrollcommand=scrollbar.set)

# Configuração de eventos
janela.bind('<Return>', open_video)
janela.bind('<Escape>', lambda e: lista_sugestoes.place_forget())
entry.bind('<KeyRelease>', atualizar_sugestoes)
lista_sugestoes.bind('<Double-Button-1>', selecionar_sugestao)
lista_sugestoes.bind('<Return>', selecionar_sugestao)

janela.mainloop()