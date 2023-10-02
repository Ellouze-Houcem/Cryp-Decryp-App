from tkinter import *
from tkinter.font import Font
from pathlib import Path
import subprocess
from subprocess import run

import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from tkinter.messagebox import askokcancel, askyesno, askquestion
from tkinter.messagebox import askretrycancel, showwarning, showinfo, showerror


window = Tk()

window.title(
    "Application de mesure de temps d'éxecution d'un algorithme de chiffrement et déchiffrement")

window.iconbitmap(Path("files/logo.ico"))

window.minsize(width=800, height=500)

window.config(background="#B8D8FA")

police_btn = Font(family='Baskerville', size=16,
                  weight='normal', slant='italic')

police_text = Font(family='Baskerville', size=20,
                   weight='normal', slant='italic')

police = Font(family='Baskerville', size=14, weight='normal', slant='italic')


def size(u, t):
    if (u == "KO"):
        taille = t*1024
    elif (u == "MO"):
        taille = t*1024*1024
    return taille


def courbe():
    plt.figure(2, figsize=(18, 7))
    data = pd.read_csv(os.path.abspath(Path("files/statistique_ch.csv")))
    x = []
    y = []
    z = []
    for i in data.taille:
        x.append(i)
    for i in data.temps_ch:
        y.append(i)
    for i in data.temps_dech:
        z.append(i)

    plt.subplot(211)
    plt.xticks(x)
    plt.yticks(y)
    plt.title("La Courbe de Chiffrement", color="red")
    plt.xlabel("La taille (octet)", color="purple")
    plt.ylabel("Le temps (m-seconde)", color="purple")
    plt.plot(x, y, color='green', linewidth=3,
             marker="o", markersize=15, linestyle='--')

    plt.subplot(212)
    plt.xticks(x)
    plt.yticks(z)
    plt.title("La Courbe de Dechiffrement", color="red")
    plt.xlabel("La taille (octet)", color="purple")
    plt.ylabel("Le temps (m-seconde)", color="purple")
    plt.plot(x, z, color='red', linewidth=3,
             marker="x", markersize=10, linestyle=':')

    plt.show()


def alert():
    pathfile = Path("files/statistique_ch.csv")
    pathlist = Path("files_chiff").glob('*')
    rep = askokcancel("Quitter",
                      " Voulez-vous terminer ?")
    if rep:
        for path in pathlist:
            subprocess.call("del "+os.path.abspath(path), shell=True)
        subprocess.call("del "+os.path.abspath(pathfile), shell=True)
        window.quit()


def chiffrement_aes(taille, u_min, t_min, u_max, t_max):
    taille_min = size(u_min, t_min)
    taille_max = size(u_max, t_max)

    t = taille_min
    liste = []
    while (t <= taille_max):
        liste.append(t)
        t = t*2

    pathlist = Path("files").glob('**/*.txt')
    pathfile = Path("files_chiff")
    statiq = open(os.path.abspath(Path("files/statistique_ch.csv")), "a")
    statiq.write('"taille","temps_ch","temps_dech"')
    for path in pathlist:
        for item in liste:
            if (os.path.getsize(path) == item):

                subprocess.call(
                    "openssl rand -out "+os.path.abspath(pathfile)+"/cle.key "+str(taille), shell=True)

                depart_chf = time.perf_counter()
                subprocess.call("openssl aes-"+str(taille)+"-cbc -in "+os.path.abspath(path) + " -out "+os.path.abspath(
                    pathfile)+"/chiffre.txt -e -k "+os.path.abspath(pathfile)+"/cle.key ", shell=True)
                fin_chf = time.perf_counter()
                diff_chf = (fin_chf-depart_chf)*1000

                depart_dch = time.perf_counter()
                subprocess.call("openssl aes-256-cbc -in "+os.path.abspath(pathfile)+"/chiffre.txt -d -out " +
                                os.path.abspath(pathfile)+"/fich_dechf.txt -k "+os.path.abspath(pathfile)+"/cle.key ", shell=True)
                fin_dch = time.perf_counter()
                diff_dch = (fin_dch-depart_dch)*1000

                statiq = open(os.path.abspath(
                    Path("files/statistique_ch.csv")), "a")
                statiq.write("\n"+'"'+str(os.path.getsize(path)) +
                             '","'+str(diff_chf)+'","'+str(diff_dch)+'"')
                statiq.close()

    Label(window, text=" ", font=police_text, bg="#B8D8FA",
          height=5, padx=8, pady=0).pack()

    Button(window, text="  Accueil ", font=police_btn, bg='#C8FCEA',
                        foreground='#364B44', padx=25, pady=10,
           command=lambda: bienvenue()).pack()
    Label(window, text=" ", font=police_text, bg="#B8D8FA",
          padx=2, pady=0).pack()

    Button(window, text="La courbe", font=police_btn, bg='#C8FCEA',
                        foreground='#364B44', padx=20, pady=10,
           command=lambda: courbe()).pack()
    Label(window, text=" ", font=police_text, bg="#B8D8FA",
          padx=2, pady=0).pack()
    Button(window, text="   Quitter   ",  font=police_btn, bg='#C8FCEA',
                        foreground='#364B44', padx=20, pady=10,
           command=lambda: alert()).pack()


def chiffrement_rsa(taille, u_min, t_min, u_max, t_max):
    taille_min = size(u_min, t_min)
    taille_max = size(u_max, t_max)
    t = taille_min
    liste = []
    while (t <= taille_max):
        liste.append(t)
        t = t*2
    pathlist = Path("files").glob('**/*.txt')
    pathfile = Path("files_chiff")
    statiq = open(os.path.abspath(Path("files/statistique_ch.csv")), "a")
    statiq.write('"taille","temps_ch","temps_dech"')
    for path in pathlist:
        for item in liste:
            if (os.path.getsize(path) == item):

                subprocess.call(
                    "openssl genrsa -out "+os.path.abspath(pathfile)+"/cle.priv " + str(taille), shell=True)

                subprocess.call("openssl rsa -in "+os.path.abspath(pathfile)+"/cle.priv -out " +
                                os.path.abspath(pathfile)+" fichier-sans-password.key", shell=True)

                subprocess.call("openssl rsa -in " + os.path.abspath(pathfile)+"/fichier-sans-password.key -des3 -out " +
                                os.path.abspath(pathfile)+"/clechiffre.priv  ", shell=True)

                subprocess.call("openssl rsa -in " + os.path.abspath(pathfile) +
                                "/cle.priv -pubout -out " + os.path.abspath(pathfile)+"/cle.pub ", shell=True)

                depart_chf = time.perf_counter()
                subprocess.call("openssl rsautl -encrypt -in "+os.path.abspath(path)+" -pubin -inkey "+os.path.abspath(
                    pathfile)+"/cle.pub -out "+os.path.abspath(pathfile)+"/chiffre.txt ", shell=True)
                fin_chf = time.perf_counter()
                diff_chf = (fin_chf-depart_chf)*1000

                depart_dch = time.perf_counter()
                subprocess.call("openssl rsautl -decrypt -in "+os.path.abspath(pathfile)+"/chiffre.txt -inkey "+os.path.abspath(
                    pathfile)+"/clechiffre.priv -out "+os.path.abspath(pathfile)+"/fich_dechf.txt ", shell=True)
                fin_dch = time.perf_counter()
                diff_dch = (fin_dch-depart_dch)*1000

                statiq = open(os.path.abspath(
                    Path("files/statistique_ch.csv")), "a")
                statiq.write("\n"+'"'+str(os.path.getsize(path)) +
                             '","'+str(diff_chf)+'","'+str(diff_dch)+'"')
                statiq.close()

    Label(window, text=" ", font=police_text, bg="#B8D8FA",
          height=5, padx=8, pady=0).pack()

    Button(window, text="  Accueil ", font=police_btn, bg='#C8FCEA',
                        foreground='#364B44', padx=25, pady=10,
           command=lambda: bienvenue()).pack()

    Label(window, text=" ", font=police_text, bg="#B8D8FA",
          padx=2, pady=0).pack()

    Button(window, text="La courbe", font=police_btn, bg='#C8FCEA',
                        foreground='#364B44', padx=25, pady=10,
           command=lambda: courbe()).pack()

    Label(window, text=" ", font=police_text, bg="#B8D8FA",
          padx=2, pady=0).pack()
    Button(window, text="   Quitter   ", font=police_btn, bg='#C8FCEA',
                        foreground='#364B44', padx=25, pady=10,
           command=lambda: alert()).pack()


def aes(taille, u_min, t_min, u_max, t_max):
    if (taille == 0):
        rep = showinfo("Attention", "Il faut choisir la dimension du clé!")
    else:
        for w in window.winfo_children():
            w.destroy()
        window.pack_propagate(0)

        chiffrement_aes(taille, u_min, t_min, u_max, t_max)


def rsa(taille, u_min, t_min, u_max, t_max):
    if (taille == 0):
        rep = showinfo("Attention", "Il faut choisir la dimension du clé!")
    else:
        for w in window.winfo_children():
            w.destroy()
        window.pack_propagate(0)
        chiffrement_rsa(taille, u_min, t_min, u_max, t_max)


def cle(algo, u_min, t_min, u_max, t_max):
    if (t_min > t_max):
        rep = showinfo(
            "Attention", "La taille minimale doit etre inferieur a la taille maximale")
    else:
        for w in window.winfo_children():
            w.destroy()
        window.pack_propagate(0)
        Label(window, text="SVP choisissez la taille de la clé", font=police_text, bd=3, bg="#B8D8FA",
              fg="#070C34", height=5, padx=2, pady=2).pack()

        taille = IntVar()
        taille.get()

        if (algo == "AES"):

            Radiobutton(window, text="128", variable=taille, value=128, bg="#B8D8FA",
                        fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()
            Radiobutton(window, text="192", variable=taille, value=192, bg="#B8D8FA",
                        fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()
            Radiobutton(window, text="256", variable=taille, value=256, bg="#B8D8FA",
                        fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()

            Label(window, text=" ", font=police_text, bg="#B8D8FA",
                  padx=2, pady=0).pack()

            submit = Button(window, text="Suivant", command=lambda: aes(
                taille.get(), u_min, t_min, u_max, t_max), font=police_btn, bg='#C8FCEA',
                foreground='#364B44', padx=15)
            submit.pack()
        elif (algo == "RSA"):

            Radiobutton(window, text="1024", variable=taille, value=1024, bg="#B8D8FA",
                        fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()
            Radiobutton(window, text="2048", variable=taille, value=2048, bg="#B8D8FA",
                        fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()
            Radiobutton(window, text="4096", variable=taille, value=4096, bg="#B8D8FA",
                        fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()

            Label(window, text=" ", font=police_text, bg="#B8D8FA",
                  padx=2, pady=0).pack()

            submit = Button(window, text="Suivant >", command=lambda: rsa(
                taille.get(), u_min, t_min, u_max, t_max), font=police_btn, bg='#C8FCEA',
                foreground='#364B44', padx=15)
            submit.pack()


def choixcle(algo):

    Label(window, text="Veuillez choisir l'intervale de la taille du fichier", font=police_text, bd=3, bg="#B8D8FA",
          fg="#070C34", height=5, padx=2, pady=2).pack()

    unite = [
        "KO", "MO"
    ]
    taille = [
        1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024
    ]

    choix_taille_min = IntVar()
    choix_taille_max = IntVar()
    choix_unite_min = StringVar()
    choix_unite_max = StringVar()
    choix_unite_min.set(unite[0])
    choix_unite_max.set(unite[0])
    choix_taille_min.set(taille[0])
    choix_taille_max.set(taille[0])

    frame = Frame(window, padx=100, pady=40, bg="#B8D8FA")
    frame.pack()

    frame1 = LabelFrame(
        frame, text="La taille minimale du fichier", font=police, padx=50, pady=50, bg="#82A1C1")
    frame1.grid(row=0, column=1)
    unite_option = OptionMenu(frame1, choix_unite_min, *unite)
    unite_option.grid(row=0, column=1)
    mininmum = OptionMenu(frame1, choix_taille_min, *taille)
    mininmum.grid(row=0, column=2)

    frame2 = LabelFrame(
        frame, text="La taille maximale du fichier", font=police, padx=50, pady=50, bg="#82A1C1")
    frame2.grid(row=0, column=3)
    unite_option = OptionMenu(frame2, choix_unite_max, *unite)
    unite_option.grid(row=0, column=1)
    mininmum = OptionMenu(frame2, choix_taille_max, *taille)
    mininmum.grid(row=0, column=2)

    #donnee = [algo,choix_unite_min.get(),choix_taille_min.get(),choix_unite_max.get(),choix_taille_max.get()]
    frame = Frame(window, padx=50, pady=10, bg="#B8D8FA")
    frame.pack()

    Button(frame, text="Suivant >", command=lambda: cle(algo, choix_unite_min.get(
    ), choix_taille_min.get(), choix_unite_max.get(), choix_taille_max.get()), font=police_btn, bg='#C8FCEA',
        foreground='#364B44', padx=15).grid(row=2, column=2)


def radio(value):
    if (value == 0):
        rep = showinfo("Attention", "Il faut choisir un algorithme!")
    else:
        for w in window.winfo_children():
            w.destroy()
        window.pack_propagate(0)
        if (value == 1):
            choix = "AES"
        elif (value == 2):
            choix = "RSA"
        choixcle(choix)


def algorithme():

    text = Label(window, text="Veuillez choisir un algorithme!", font=police_text, bd=3, bg="#B8D8FA",
                 fg="#070C34", height=8, padx=2, pady=0)
    text.pack()
    algo = IntVar()
    algo.get()

    Radiobutton(window, text="AES", variable=algo, value=1, bg="#B8D8FA",
                fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()
    Radiobutton(window, text="RSA", variable=algo, value=2, bg="#B8D8FA",
                fg="#364B44", font=police_btn, activebackground="#B8D8FA").pack()

    Label(window, text=" ", font=police_text, bg="#B8D8FA",
          padx=2, pady=0).pack()
    submit = Button(window, text="Suivant >", command=lambda: radio(algo.get()), font=police_btn, bg='#C8FCEA',
                    foreground='#364B44', padx=15)
    submit.pack()


def start():
    for w in window.winfo_children():
        w.destroy()
    window.pack_propagate(0)
    algorithme()


def bienvenue():
    pathfile = Path("files/statistique_ch.csv")
    subprocess.call("del "+os.path.abspath(pathfile), shell=True)
    pathlist = Path("files_chiff").glob('*')
    for path in pathlist:
        subprocess.call("del "+os.path.abspath(path), shell=True)

    for w in window.winfo_children():
        w.destroy()
    window.pack_propagate(0)
    label = Label(window, text="Bienvenue", font=police_text, bd=3, bg="#B8D8FA",
                  fg="#070C34", height=10, padx=8, pady=2)
    label.pack()

    commencer = Button(window, text="Commencer", command=start, font=police_btn, bg='#C8FCEA',
                       foreground='#364B44', padx=15)
    commencer.pack(padx=10, pady=10)


bienvenue()

window.mainloop()
