import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2 as cv
import numpy as np
import os
from math import sqrt
import shutil

global pasta_selecionada, salvar_pasta, c, q, I, graphic, h, w, video, imgs, el, caminho_video
#c = False

color1 = "#FFFFFF"

class SA:
    def matrizdn(heigth, width):
        m = [0] * (heigth * width)
        return m
    
    def set_folder(caminho):
        global c, q, el
        c = caminho
        el = os.listdir(c)
        q = int(len(el) + 1)
    
    def colorPicture(RED, GREEN, BLUE):
        a1 = q // 2 + q // 3
        a2 = a1 // 2 + a1//4
        a3 = a2 // 2

        rr = RED / (q - 1)
        gg = GREEN / (q - 1)
        bb = BLUE / (q - 1)

        #print('a1 {} a2 {} a3 {}'.format(a1, a2, a3))
        #print('rr {} gg {} bb {}'.format(rr, gg, bb))
        i = 0
        for y in range(0, h):
            for x in range(0, w):
                if I[i] >= a1:
                    r = I[i] * rr
                    g = 0
                    b = 0
                elif I[i] >= a2:
                    r = I[i] * rr
                    g = I[i]/2 * gg
                    b = 0
                elif I[i] >= a3:
                    r = 0
                    g = I[i] * gg
                    b = 0
                else:
                    r = 0
                    g = 0
                    b = I[i] * bb
                    #print(b)
                    #print(g)
                    #print(r)
                graphic[y, x] = b, g, r
                #label_colorir.config(text="Processando: {} de {}".format(i, len(I)), foreground="green")
                #label_colorir.update()
                i += 1

def apenas_numeros(n):
    return n.isdigit() or n == ""

def selecionar_pasta():
    global pasta_selecionada
    label_colorir.config(text= "")
    label_salvar.config(text="")
    pasta_selecionada = filedialog.askdirectory(title="Selecione uma pasta")
    try:
        SA.set_folder(pasta_selecionada)
        print(pasta_selecionada)
        label_prog.config(text="Pasta Selecionada, Execute.", foreground="green")
    except:
        label_prog.config(text="Pasta não encontrada.", foreground="red")

def executar():
    global c, I, graphic, h, w
    label_colorir.config(text= "")
    label_salvar.config(text="")

    try:
        img  = cv.imread(c + '/imagem1.png')
        h, w, _ = img.shape
        imga = img
        del (img)

        I = SA.matrizdn(h,w)

        graphic = np.zeros((h, w, 3), dtype='uint8')

        for i in range(1, q):
                #print(f'lendo imagem {i}')
                label_prog.config(text="Processando: {} de {}".format(i,q-1))
                label_prog.update()
                img = cv.imread(c + '/imagem{}.png'.format(i))

                j = 0
                for y in range(0, h):
                    for x in range(0, w):
                        if not all(img[y, x] == imga[y, x]):
                            I[j] += 1
                        j += 1

                imga = img

        label_prog.config(text="Processamento Concluído.", foreground="green")
    except:
       label_prog.config(text="Pasta não encontrada.", foreground="red") 

def colorir():
    label_salvar.config(text="")
    if red.get() == '':
        RED = 0   
    else:
        RED = int(red.get())
        if RED > 255:
            RED = 255

    if green.get() == '':
        GREEN = 0
    else:
        GREEN = int(green.get())
        if GREEN > 255:
            GREEN = 255

    if blue.get() == '':
        BLUE = 0
    else:
        BLUE = int(blue.get())
        if BLUE > 255:
            BLUE = 255
    
    print('RED {} GREEN {} BLUE {}'.format(RED, GREEN, BLUE))
    print(type(RED))

    SA.colorPicture(RED, GREEN, BLUE)
    label_colorir.config(text= "Concluído", foreground = "green")
    
    
def salvar():
    global salvar_pasta
    salvar_pasta = filedialog.askdirectory(title="Selecione uma pasta")
    try:
        save = f'{salvar_pasta}/'
        s = int(int(len(os.listdir(save))))
        name = f'{save}grafico{s+1}.png'
        cv.imwrite(name, graphic)
        label_salvar.config(text="Concluído.", foreground="green")
        label_prog.config(text="")
        label_colorir.config(text="")
    except:
        label_salvar.config(text="Pasta não encontrada.", foreground="red")


def selecionar_pasta_video():
    global pasta_selecionada
    pasta_selecionada = filedialog.askdirectory(title="Selecione uma pasta")
    try:
        SA.set_folder(pasta_selecionada)
        label_salvar2.config(text="")
        label_video.config(text="Pasta Selecionada, Execute.", foreground="green")
    except:
        label_salvar2.config(text="")
        label_video.config(text="Pasta não encontrada.", foreground="red")
        

def executar_video():
    global c, q, video, imgs, h, w, I, graphic, el, caminho_video
    imgs = []
    label_salvar2.config(text="")

    try:
        average = int(sqrt(len(el)))
        average_2 = average
        
        img = cv.imread(c + '/imagem1.png')
        h, w, _ = img.shape
        imga = img
        del (img)

        I = SA.matrizdn(h, w)

        graphic = np.zeros((h, w, 3), dtype='uint8')

        n = 0
        ll = 1
        for u in range (1, average + 1):
            for i in range(1, average + 1):
                label_video.config(text="Processando: {} de {}".format(ll, q-1))
                label_video.update()
                print(f'lendo imagem {n + i}')
                img = cv.imread(c + '/imagem{}.png'.format(i))

                j = 0
                for y in range(0, h):
                    for x in range(0, w):
                        if not all(img[y, x] == imga[y, x]):
                            I[j] += 1
                        j += 1

                imga = img
                ll += 1

            n = average_2
            average_2 += average

            SA.colorPicture(255,127,63)
            imgs.append(graphic.copy())
            
        name = 'videoSpeckle.avi'
        fps = 1
        height, width, layers = imgs[0].shape
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        video = cv.VideoWriter(name, fourcc, fps, (width, height))

        for img in imgs:
            video.write(img)

        video.release()
        caminho_video = os.path.abspath(name)
        label_video.config(text="Processamento Concluído.", foreground="green")
    except:
        label_salvar2.config(text="")
        label_video.config(text="Pasta não encontrada.",foreground="red")
    
##

def salvar_video():
    global salvar_pasta, caminho_video
    salvar_pasta = filedialog.askdirectory(title="Selecione uma pasta")
    try:
        origem = caminho_video
        destino = salvar_pasta
        if os.path.exists(destino):
            base, ext = os.path.splitext(destino)
            destino = base + "_novo" + ext

        shutil.move(origem, destino)
        label_salvar2.config(text="Salvo com Sucesso.", foreground="green")
        label_video.config(text="")
    except:
        label_salvar2.config(text="Pasta não encontrada.", foreground="red")

# #

def salvar_video():
    global salvar_pasta, caminho_video
    salvar_pasta = filedialog.askdirectory(title="Selecione uma pasta")

    try:
        nome_arquivo = os.path.basename(caminho_video)
        destino = os.path.join(salvar_pasta, nome_arquivo)

        if os.path.exists(destino):
            base, ext = os.path.splitext(nome_arquivo)
            contador = 1
            novo_destino = os.path.join(salvar_pasta, f"{base}_{contador}{ext}")

            while os.path.exists(novo_destino):
                contador += 1
                novo_destino = os.path.join(salvar_pasta, f"{base}_{contador}{ext}")

            destino = novo_destino

        shutil.move(caminho_video, destino) 
        label_salvar2.config(text="Salvo com Sucesso.", foreground="green")
        label_video.config(text="")
    except:
        label_salvar2.config(text="Pasta não encontrada.", foreground="red")


# config janela

window  = tk.Tk()
window.title("Speclke Analysis")
window.config(bg=color1)
window.geometry("340x400")
window.resizable(width=False, height=False)

notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")

aba1 = ttk.Frame(notebook)
aba2 = ttk.Frame(notebook)

# abas notebook
notebook.add(aba1, text="Imagem")
notebook.add(aba2, text="Vídeo")

label1 = ttk.Label(aba1, text="Speclke Analysis - Analisador de Atividade de Speclke")
label1.place(x=7, y=15)

label2 = ttk.Label(aba1, text="Análise de Fotos:")
label2.place(x=20, y=50)

botao1 = ttk.Button(aba1, text="Selecionar Pasta de Arquivos", command=selecionar_pasta)
botao1.place(x=25, y=80)

botao2 = ttk.Button(aba1, text="Executar", command=executar)
botao2.place(x=190, y=80)

label3 = ttk.Label(aba1, text="Progresso: ")
label3.place(x=40, y=120)

label_prog = ttk.Label(aba1, text = "Selecione uma pasta e Execute.", foreground = "red")
label_prog.place(x=120, y=120)

label4 = ttk.Label(aba1, text="Nível de Cores (1 a 255): ")
label4.place(x=40, y=150)

#

valor1 = tk.StringVar()
valor2 = tk.StringVar()
valor3 = tk.StringVar()
valor1.set("255")
valor2.set("127")
valor3.set("63")

vcmd = (window.register(apenas_numeros), "%P")

#entrada vermelho
label_r = ttk.Label(aba1, text="Vermelho:")
label_r.place(x=50 , y= 180)

red = ttk.Entry(aba1, validate="key", validatecommand=vcmd, textvariable=valor1)
red.place(x=130 , y= 180)

#entrada verde
label_g = ttk.Label(aba1, text="Verde:")
label_g.place(x=50 , y= 210)

green = ttk.Entry(aba1, validate="key", validatecommand=vcmd, textvariable=valor2)
green.place(x=130 , y= 210)

#entrada azul
label_b = ttk.Label(aba1, text="Azul:")
label_b.place(x=50 , y= 240)

blue = ttk.Entry(aba1, validate="key", validatecommand=vcmd, textvariable=valor3)
blue.place(x=130 , y= 240)

botao3 = ttk.Button(aba1, text="Colorir", command=colorir)
botao3.place(x=25 , y= 280)

label_colorir = ttk.Label(aba1, text = "")
label_colorir.place(x=110, y=285)

botao4 = ttk.Button(aba1, text="Salvar", command=salvar)
botao4.place(x=25 , y= 320)

label_salvar = ttk.Label(aba1, text = "")
label_salvar.place(x=110, y=325)

# video

label5 = ttk.Label(aba2, text="Speclke Analysis - Analisador de Atividade de Speclke")
label5.place(x=7, y=15)

label6 = ttk.Label(aba2, text="Análise em Vídeo")
label6.place(x=20, y=50)

botao5 = ttk.Button(aba2, text="Selecionar Pasta de Arquivos", command=selecionar_pasta_video)
botao5.place(x=25, y=80)

botao6 = ttk.Button(aba2, text="Executar", command=executar_video)
botao6.place(x=190, y=80)

label7 = ttk.Label(aba2, text="Progresso: ")
label7.place(x=40, y=120)


label_video = ttk.Label(aba2, text = "Selecione uma pasta e Execute.", foreground = "red")
label_video.place(x=120, y=120)

botao7 = ttk.Button(aba2, text="Salvar", command=salvar_video)
botao7.place(x=25, y=160)

label_salvar2 = ttk.Label(aba2, text = "")
label_salvar2.place(x=120, y=160)

window.mainloop()
