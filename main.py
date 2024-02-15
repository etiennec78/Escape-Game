from tkinter.messagebox import *
from tkinter import *
from tkinter.ttk import *
import vlc
import time
import subprocess
import os

enterpriseNameFound = False
radioUsed = []
radioStep = 0
lowTimeMode = False


def refreshTimer():
    global windowTimer
    global lowTimeMode
    if timerEnd - int(time.time()) == 0:
        endGame()
    if timerEnd - int(time.time()) < 360 and not lowTimeMode:
        windowTimer.config(style="Notime.TLabel")
        lowTimeMode = True

    if ((timerEnd - int(time.time())) % 60) < 10:
        windowTimer.config(text=str(int((timerEnd - int(time.time())) / 60)) + ":0" + str(
            ((timerEnd - int(time.time())) % 60)))
    else:
        windowTimer.config(text=str(int((timerEnd - int(time.time())) / 60)) + ":" + str(
            ((timerEnd - int(time.time())) % 60)))


def on_closing():
    print("Fermeture de la fenêtre tentée")


def start_game():
    window.bind_all("<Key-Return>")
    clear_frame()
    start_global_timer(3600)
    timer = time.time() + 10
    timerText = Label(window, text="Lancement de la vidéo des maîtres dans : x secondes.", style="Title.TLabel")
    timerText.place(relx=0.5, rely=0.5, anchor=CENTER)
    while timer - time.time() > 0:
        timerText.config(
            text="Lancement de la vidéo des maîtres dans : " + str(round(timer - time.time(), 1)) + " secondes.")
        window.update()
    video()
    hack()


def start_global_timer(timeToAdd):
    global timerEnd
    timerEnd = int(time.time()) + timeToAdd


def replay_video():
    global replayButton
    nextAnimation = int(time.time() + 2)
    replayButton.config(state="disabled", command=lambda: [audio("button.mp3"), video()])
    while int(time.time()) < nextAnimation:
        replayButton.config(text="Êtes-vous sûr ? " + str(round(nextAnimation - time.time(), 1)))
        refreshTimer()
        window.update()
    replayButton.config(text="Êtes-vous sûr ?", state="normal")

    nextAnimation = int(time.time() + 5)
    while int(time.time()) < nextAnimation:
        refreshTimer()
        window.update()
    replayButton.config(text="Revoir la vidéo d'intro", command=lambda: [audio("button.mp3"), replay_video()])


def video():
    global bgplayer
    if bgplayer is not None:
        bgplayer.kill()
    video = vlc.MediaPlayer(os.getcwd() + "/Data/video.mp4")
    video.set_fullscreen(True)
    video.play()
    time.sleep(1.5)
    duration = video.get_length() / 1000
    time.sleep(duration)
    video.stop()
    bgplayer = subprocess.Popen(
        '"C:/Program Files/VideoLAN/VLC/vlc.exe" /Data/background.m4a --qt-start-minimized --loop -I null')


def audio(file):
    global player
    player = vlc.MediaPlayer(os.getcwd() + "/Data/" + file)
    player.play()


def clear_frame():
    for widgets in window.winfo_children():
        widgets.destroy()


def plug_USB_Linux():
    global USB
    USB = True


def hack():
    global alertPlayer
    global alertProgressBar
    global styleAlert
    global deleteButton
    global alertText
    global alert
    global entryHack
    global hackState
    global USB
    global alertPlayer
    clear_frame()

    Label(window, text="Session Login", style="Title.TLabel").place(relx=0.5, rely=0.055, anchor=CENTER)

    Label(window, text="Username :").place(relx=0.395, rely=0.27)
    usernameEntry = Entry(window, style="Label.TEntry",
                          font="Helvetica " + str(int(20 * window.winfo_screenheight() / 1080)))
    usernameEntry.insert(0, "Administrator")
    usernameEntry.config(state="disabled")
    usernameEntry.place(relx=0.5, rely=0.35, relwidth=0.21875, relheight=0.065, anchor=CENTER)

    Label(window, text="Password :").place(relx=0.395, rely=0.42)
    entryHack = Entry(window, state="focus", font="Helvetica " + str(int(20 * window.winfo_screenheight() / 1080)))
    entryHack.place(relx=0.5, rely=0.5, relwidth=0.21875, relheight=0.065, anchor=CENTER)
    hackState = Label(window, text="")
    hackState.place(relx=0.5, rely=0.56, anchor=CENTER)

    hackLogin = Button(window, text="Login", command=login)
    hackLogin.place(relx=0.5, rely=0.52 + 0.15, relwidth=0.1823, relheight=0.0926, anchor=CENTER)

    window.bind_all("<Key-Return>", lambda void: login())
    USB = False
    if os.name == "posix":
        Button(window, text="Brancher la clé USB (Linux)", command=plug_USB_Linux).place(relx=0.5, rely=0.8,
                                                                                         relwidth=0.2604,
                                                                                         relheight=0.0926,
                                                                                         anchor=CENTER)
    while not USB:
        window.update()
        if os.name != "posix":
            for drive in str(
                    subprocess.check_output("wmic logicaldisk get  DriveType, caption", shell=True)).strip().split(
                "\\r\\r\\n"):
                if '2' in drive:
                    USB = True
        if USB:
            alertPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/alert.mp3")
            alertPlayer.play()
            alert = Tk()
            largeur = int(600 * alert.winfo_screenwidth() / 1920)
            hauteur = int(200 * alert.winfo_screenheight() / 1080)
            posLargeur = int((alert.winfo_screenwidth() - largeur) / 2)
            posHauteur = int((alert.winfo_screenheight() - hauteur) / 2)

            alert.protocol("WM_DELETE_WINDOW", on_closing)
            alert.attributes("-topmost", True)
            alert.geometry(str(largeur) + "x" + str(hauteur) + "+" + str(posLargeur) + "+" + str(posHauteur))
            alert.resizable(False, False)
            alert.title("Windows Defender")
            alert.iconbitmap(os.getcwd() + "/Data/defender.ico")
            alert.configure(bg='white')
            styleAlert = Style(alert)
            styleAlert.configure("TProgressbar", troughcolor="red", background="white")
            styleAlert.configure("Alert.TLabel", foreground="red", background="white",
                                 font="Helvetica " + str(int(26 * window.winfo_screenheight() / 1080)))
            styleAlert.configure("AlertETA.TLabel", foreground="white", background="red")
            styleAlert.configure("TButton", foreground="white", background="red")
            global virusDeleted
            virusDeleted = False
            alertText = Label(alert, text="Alerte : Logiciel malveillant détecté !", style="Alert.TLabel")
            alertText.place(relx=0.5, rely=0.25, anchor=CENTER)
            deleteButton = Button(alert, text="Ok", command=lambda: [audio("button.mp3"), delete_virus()])
            deleteButton.place(relx=0.5, rely=0.65, relwidth=0.4167, relheight=0.25, anchor=CENTER)
            nextAnimation = int(time.time()) + 6
            animationStep = 0
            animationNext = int(time.time() + 1)
            styleAlert.configure("Alert.TLabel", foreground="red", background="white")
            while nextAnimation != int(time.time()) and not virusDeleted:
                if round(animationNext, 1) == round(time.time(), 1):
                    if animationStep == 0:
                        styleAlert.configure("Alert.TLabel", foreground="white", background="red")
                        styleAlert.configure("TButton", foreground="red", background="white")
                        alert.configure(bg="red")
                    if animationStep == 1:
                        styleAlert.configure("Alert.TLabel", foreground="red", background="white")
                        styleAlert.configure("TButton", foreground="white", background="red")
                        alert.configure(bg="white")
                        animationStep = -1
                    animationStep += 1
                    animationNext += 0.5
                alert.update()
            if not virusDeleted:
                delete_virus()
            if os.name == "posix":
                osdir = "/bin/"
            else:
                osdir = "C:/Windows/System32"
            terminal = Tk()
            largeur = int(600 * terminal.winfo_screenwidth() / 1920)
            hauteur = int(350 * terminal.winfo_screenheight() / 1080)
            terminal.protocol("WM_DELETE_WINDOW", on_closing)
            terminal.attributes("-topmost", True)
            terminal.title("Terminal")
            terminal.iconbitmap(os.getcwd() + "/Data/terminal.ico")
            terminal.geometry(str(largeur) + "x" + str(hauteur) + "+0+0")
            terminal.resizable(False, False)
            terminalStyle = Style(terminal)
            terminal.configure(bg="black")
            terminalStyle.configure("TLabel", foreground="green", background="black",
                                    font="hack " + str(int(14 * window.winfo_screenheight() / 1080)))
            terminalText = Label(terminal)
            terminalText.pack(fill=X)
            terminal.update()
            text = "sudo apt install hack-tool"
            display = "Guest@PC-BUNKER : ~$ "
            terminalPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/radio.mp3")
            terminalPlayer.play()
            for letter in range(len(text)):
                display = display + text[letter]
                terminalText.config(text=display)
                terminal.update()
                time.sleep(0.1)
            terminalPlayer.stop()
            time.sleep(1)
            terminalRemovingDefender = Label(terminal)
            terminalRemovingDefender.pack(fill=X)
            terminal.update()
            progressBar = ""
            for animationStep in range(11):
                terminalPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/step.mp3")
                terminalPlayer.play()
                progressBarSpaces = ""
                progressBar = progressBar + "="
                for i in range(10 - animationStep):
                    progressBarSpaces = progressBarSpaces + "   "
                terminalRemovingDefender.config(
                    text="Disabling Windows Defender" + " [" + progressBar + progressBarSpaces + "]" + str(
                        animationStep * 10) + "%")
                terminal.update()
            alert.destroy()
            terminalExtractingPercentage = Label(terminal)
            terminalExtractingPercentage.pack(fill=X)
            terminal.update()
            progressBar = ""
            for animationStep in range(11):
                terminalPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/step.mp3")
                terminalPlayer.play()
                progressBarSpaces = ""
                progressBar = progressBar + "="
                for i in range(10 - animationStep):
                    progressBarSpaces = progressBarSpaces + "   "
                terminalExtractingPercentage.config(
                    text="Extracting files... " + " [" + progressBar + progressBarSpaces + "]" + str(
                        animationStep * 10) + "%")
                terminal.update()
                time.sleep(0.5)
            terminalCopyingPercentage = Label(terminal)
            terminalCopyingPercentage.pack(fill=X)
            terminalCopyingFiles = Label(terminal)
            terminalCopyingFiles.pack(fill=X)
            terminalPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/bruteforce.mp3")
            terminalPlayer.play()
            oldProgressBar = ""
            for animationStep in range(int(len(os.listdir(osdir)) / 10)):
                oldProgressBar = progressBar
                progressBar = ""
                progressBarSpaces = ""
                terminalCopyingFiles.config(text=os.listdir(osdir)[animationStep])
                for i in range(int((animationStep + 1) * 10 / int(len(os.listdir(osdir)) / 10))):
                    progressBar = progressBar + "="
                for i in range(10 - int((animationStep + 1) * 10 / int(len(os.listdir(osdir)) / 10))):
                    progressBarSpaces = progressBarSpaces + "   "
                if oldProgressBar != progressBar:
                    terminalPlayer2 = vlc.MediaPlayer(os.getcwd() + "/Data/step.mp3")
                    terminalPlayer2.play()
                terminalCopyingPercentage.config(
                    text="Copying files... " + " [" + progressBar + progressBarSpaces + "] " + str(int(
                        (animationStep + 1) * 100 / int(len(os.listdir(osdir)) / 10))) + "%")
                terminal.update()
            terminalPlayer.stop()
            terminalExploitingPercentage = Label(terminal)
            terminalExploitingPercentage.pack(fill=X)
            terminal.update()
            progressBar = ""
            for animationStep in range(11):
                terminalPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/step.mp3")
                terminalPlayer.play()
                progressBarSpaces = ""
                progressBar = progressBar + "="
                for i in range(10 - animationStep):
                    progressBarSpaces = progressBarSpaces + "   "
                terminalExploitingPercentage.config(
                    text="Exploiting zero-day breach " + " [" + progressBar + progressBarSpaces + "]" + str(
                        animationStep * 10) + "%")
                terminal.update()
                time.sleep(0.3)
            Label(terminal, text="Starting bruteforcer").pack(fill=X)
            terminal.update()
            time.sleep(2)

            hack = Tk()
            largeur = int(500 * hack.winfo_screenwidth() / 1920)
            hauteur = int(250 * hack.winfo_screenheight() / 1080)
            posLargeur = int(hack.winfo_screenwidth() - 650 * hack.winfo_screenwidth() / 1920)
            posHauteur = int(hack.winfo_screenheight() - 780 * hack.winfo_screenheight() / 1080)

            hack.protocol("WM_DELETE_WINDOW", on_closing)
            hack.attributes('-topmost', True)
            hack.geometry(str(largeur) + "x" + str(hauteur) + "+" + str(posLargeur) + "+" + str(posHauteur))
            hack.resizable(False, False)
            hack.title("Hack-tool")
            hack.iconbitmap(os.getcwd() + "/Data/hack.ico")

            styleHack = Style(hack)
            styleHack.configure("TLabel", font="Helvetica " + str(int(24 * window.winfo_screenheight() / 1080)))
            styleHack.configure("Red.TLabel",
                                font="Helvetica " + str(int(24 * window.winfo_screenheight() / 1080)) + " bold",
                                foreground="red")
            styleHack.configure("Green.TLabel",
                                font="Helvetica " + str(int(24 * window.winfo_screenheight() / 1080)) + " bold",
                                foreground="green")
            styleHack.configure("TButton", font="Helvetica " + str(int(24 * window.winfo_screenheight() / 1080)) + "")

            hackText = Label(hack, text="Hacking en cours...")
            hackText.place(relx=0.5, rely=0.15, anchor=CENTER)
            hackProgressBar = Progressbar(hack, orient=HORIZONTAL, length=200, mode="determinate", maximum=3672)
            hackProgressBar.place(relx=0.5, rely=0.3, relwidth=0.7, relheight=0.12, anchor=CENTER)

            hackFrame = Frame(hack, borderwidth=1, relief="groove", padding=1)
            hackFrame.place(relx=0.5, rely=0.65, relwidth=0.84, relheight=0.34, anchor=CENTER)

            hackTry = Label(hackFrame, text="Essai du mot de passe :")
            hackTry.pack(fill=X)
            hackPass = Label(hackFrame, text="ECHEC", style="Red.TLabel")
            hackPass.pack()

            passwordBruteforce = [97]
            tried = 0
            animationStep = 0
            nextAnimation = int(time.time()) + 1
            countTime = int(time.time())
            bruteforcePlayer = vlc.MediaPlayer(os.getcwd() + "/Data/bruteforce.mp3")
            bruteforcePlayer.play()
            while not "".join(map(chr, passwordBruteforce)) == "ekg":
                if nextAnimation <= int(time.time()):
                    if animationStep == 0:
                        hackText.config(text="Hacking en cours")
                    if animationStep == 1:
                        hackText.config(text="Hacking en cours.")
                    if animationStep == 2:
                        hackText.config(text="Hacking en cours..")
                    if animationStep == 3:
                        hackText.config(text="Hacking en cours...")
                        animationStep = -1
                    animationStep += 1
                    nextAnimation += 1
                tried += 1
                for lettre in reversed(range(len(passwordBruteforce))):
                    # Si la lettre est différente de z, l'augmente de 1 et arrête la boucle
                    if passwordBruteforce[lettre] != 122:
                        passwordBruteforce[lettre] += 1
                        break
                    else:
                        # Si la lettre est un z, la transforme en a
                        passwordBruteforce[lettre] = 97
                        # Si le z est le tout premier de la liste, rajoute une nouvelle lettre dans la liste (a)
                        if lettre == 0:
                            passwordBruteforce.append(97)
                        # La lettre était un z, donc le programme continue pour modifier la prochaine lettre
                hackProgressBar.config(value=tried)
                entryHack.delete(0, len(entryHack.get()))
                entryHack.insert(0, "".join(map(chr, passwordBruteforce)))
                hackTry.config(text="Essai du mot de passe : " + entryHack.get())
                styleHack.configure("Red.TLabel", foreground="black")
                hack.update()
                styleHack.configure("Red.TLabel", foreground="red")
                hack.update()
            bruteforcePlayer.stop()
            print("Mot de passe trouvé en", tried, "essais, en", int(time.time() - countTime), "secondes")
            hackText.config(text="Hacking achevé")
            hack.protocol("WM_DELETE_WINDOW", hack.destroy)
            hackPass.config(text="RÉUSSITE", style="Green.TLabel")
            bruteforcePlayer = vlc.MediaPlayer(os.getcwd() + "/Data/done.mp3")
            bruteforcePlayer.play()
            Label(terminal, text="Bruteforce done. Exiting...").pack(fill=X)
            nextAnimation = int(time.time()) + 3
            Button(hack, text="Fermer", command=lambda: [audio("button.mp3"), hack.destroy()]).place(relx=0.5,
                                                                                                     rely=0.65,
                                                                                                     relwidth=0.84,
                                                                                                     relheight=0.34,
                                                                                                     anchor=CENTER)

            while int(time.time()) != nextAnimation:
                terminal.update()
            terminal.destroy()


def delete_virus():
    global alertProgressBar
    global virusDeleted
    global deleteButton
    global alertText
    global alert
    global styleAlert
    global alertPlayer

    alertPlayer.stop()

    deleteButton.destroy()
    alert.configure(bg="red")
    alertProgressBar = Progressbar(alert, orient=HORIZONTAL, length=200, mode="determinate", maximum=100)
    alertProgressBar.place(relx=0.5, rely=0.5, relwidth=0.4167, relheight=0.125, anchor=CENTER)
    styleAlert.configure("Alert.TLabel", foreground="white", background="red")
    alertText.config(text="Suppression du virus...")
    ETA = Label(alert, text="Temps restant: environ x secondes", style="AlertETA.TLabel")
    ETA.place(relx=0.293, rely=0.57)
    progressBarPercent = 0
    speed = 0
    alertPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/loading.mp3")
    alertPlayer.play()

    while progressBarPercent != 70:
        alertProgressBar.config(value=progressBarPercent)
        ETA.config(text="Temps restant: environ " + str(int(speed * (100 - progressBarPercent))) + " secondes")
        alert.update()
        progressBarPercent += 1
        time.sleep(speed)
        speed += 0.001
    alertPlayer.stop()
    while int(speed * (100 - progressBarPercent)) < 60:
        alertProgressBar.config(value=progressBarPercent)
        ETA.config(text="Temps restant: environ " + str(int(speed * (100 - progressBarPercent))) + " secondes")
        alert.update()
        progressBarPercent += 1
        time.sleep(speed)
        speed += 0.6
    ETA.config(text="Temps restant: environ 1 heure")
    virusDeleted = True


def main():
    global enterpriseNameFound
    global vlcBackground
    global replayButton
    global lowTimeMode
    global timer
    global windowTimer
    window.bind_all("<Key-Return>")
    clear_frame()
    window.grid_rowconfigure(5, weight=1)
    window.grid_columnconfigure(3, weight=1)

    windowFrame = Frame(window)
    windowFrame.grid(row=0, column=3, sticky=NE)

    Label(window, text="Choisissez une option", style="Title.TLabel").place(relx=0.5, rely=0.055, anchor=CENTER)
    replayButton = Button(window, text="Revoir la vidéo d'intro", command=lambda: [audio("button.mp3"), replay_video()])
    replayButton.place(relx=0.5, rely=0.3, relwidth=0.224, relheight=0.0926, anchor=CENTER)
    Button(window, text="Chiffrer un message", command=lambda: [audio("button.mp3"), coder("coding")]).place(relx=0.5,
                                                                                                             rely=0.4,
                                                                                                             relwidth=0.224,
                                                                                                             relheight=0.0926,
                                                                                                             anchor=CENTER)
    Button(window, text="Déchiffrer un message", command=lambda: [audio("button.mp3"), coder("decoding")]).place(
        relx=0.5, rely=0.5, relwidth=0.224, relheight=0.0926, anchor=CENTER)
    Button(window, text="Utiliser la radio", command=lambda: [audio("button.mp3"), radio()]).place(relx=0.5, rely=0.6,
                                                                                                   relwidth=0.224,
                                                                                                   relheight=0.0926,
                                                                                                   anchor=CENTER)
    windowTimer = Label(window, text="", style="Title.TLabel")
    windowTimer.place(relx=1, rely=0.01, relwidth=0.1145, relheight=0.0926, anchor=NE)

    while True:
        refreshTimer()
        window.update()


def error(msg):
    showerror("Erreur !", msg)


def info(msg):
    showinfo("Information", msg)


def login():
    if entryHack.get() != "ekg":
        hackState.config(text="Invalid password !", style="TLabel")
        window.update()
        hackState.config(style="Refused.TLabel")
        audio("error.wav")
        window.update()
    else:
        hackState.config(text="Access granted!", style="Valid.TLabel")
        audio("login.mp3")
        window.update()
        time.sleep(1)
        main()


def coder(coderMethod):
    global titleLabel
    global entryCoder
    global entryKey
    global textCoder
    global buttonCoder
    global textKey
    global method
    global backButton
    global windowTimer
    method = coderMethod
    clear_frame()

    titleLabel = Label(window, style="Title.TLabel")
    textCoder = Label(window)
    entryCoder = Entry(window, font="Helvetica " + str(int(30 * window.winfo_screenheight() / 1080)))
    textKey = Label(window)
    entryKey = Entry(window, font="Helvetica " + str(int(30 * window.winfo_screenheight() / 1080)))
    buttonCoder = Button(window)

    coder_texts()

    backButton = Button(window, text="< Retour", command=lambda: [audio("button.mp3"), main()])
    backButton.place(relx=0, rely=0.01, relwidth=0.1146, relheight=0.0926)
    titleLabel.place(relx=0.5, rely=0.055, anchor=CENTER)
    textCoder.place(relx=0.395, rely=0.27)
    textKey.place(relx=0.395, rely=0.42)
    entryKey.place(relx=0.5, rely=0.5, relwidth=0.21875, relheight=0.065, anchor=CENTER)
    buttonCoder.place(relx=0.5, rely=0.52 + 0.15, relwidth=0.21875, relheight=0.0926, anchor=CENTER)
    window.bind_all("<Key-Return>", lambda void: coder_check())

    window.bind_all("<Key-Return>")

    windowTimer = Label(window, text="", style="Title.TLabel")
    windowTimer.place(relx=1, rely=0.01, relwidth=0.1145, relheight=0.0926, anchor=NE)

    while True:
        if 420 * window.winfo_screenwidth() / 1920 < 18 * len(entryCoder.get()) * window.winfo_screenwidth() / 1920:
            entryCoder.place(relx=0.5, rely=0.35, width=18 * len(entryCoder.get()) * window.winfo_screenwidth() / 1920)
        else:
            entryCoder.place(relx=0.5, rely=0.35, width=420 * window.winfo_screenwidth() / 1920, relheight=0.065,
                             anchor=CENTER)
        refreshTimer()
        window.update()


def coder_check():
    global method
    global backButton
    message = entryCoder.get()
    if entryCoder.get() == "":
        error("Aucun message n'a été inséré.")
    try:
        key = int(entryKey.get())
    except ValueError:
        error("La clé spécifiée est invalide. Veuillez insérer un nombre.")
    else:
        if 0 < key <= 25:
            if message == "":
                error("Veuillez entrer un texte.")
            wrongChar = ""
            for letter in range(len(message)):
                if 65 <= ord(message[letter]) <= 90 or 97 <= ord(message[letter]) <= 122 or ord(
                        message[letter]) == 32 or ord(message[letter]) == 39:
                    print("Le caractère", ord(message[letter]), "est valide.")
                else:
                    wrongChar += message[letter] + " "
            if wrongChar != "":
                error("Le texte entré est incorrect!\nLes caractères suivants sont invalides : " + wrongChar)
                print("Les caractères", wrongChar, "sont invalides.")
                coder(method)
            animationTime = int(time.time())
            animationStep = 0
            display = ""
            textCoder.config(text=display)
            sortiePasse = ""
            buttonCoder.config(state="disabled")
            textKey.config(state="disabled")
            entryKey.config(state="disabled")
            window.bind_all("<Key-Return>")
            print("----------------------- Démarrage de la modification du message --------------------------")
            coderPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/bruteforce.mp3")
            coderPlayer.play()
            for letter in range(len(message)):
                refreshTimer()
                display = ""
                print("---- travaille sur la lettre", letter, "----")
                print("La lettre de base est:", message[letter], "avec le numéro", ord(message[letter]))
                sortieFin = ""
                for i in range(letter + 1, len(message)):
                    sortieFin = sortieFin + message[i]
                for bruteforce in range(1, key + 1):
                    print("La clé de bruteforce est à", bruteforce)
                    if 65 <= ord(message[letter]) <= 90:
                        if method == "decoding":
                            if ord(message[letter]) - bruteforce < 65:
                                print("descend trop bas, va a la fin")
                                display = chr(ord(message[letter]) - bruteforce + 26)
                            else:
                                print("recule de", bruteforce)
                                display = chr(ord(message[letter]) - bruteforce)
                        else:
                            if ord(message[letter]) + bruteforce > 90:
                                print("monte trop haut, va au début")
                                display = chr(ord(message[letter]) + bruteforce - 26)
                            else:
                                print("avance de", bruteforce)
                                display = chr(ord(message[letter]) + bruteforce)
                    elif 97 <= ord(message[letter]) <= 122:
                        if method == "decoding":
                            if ord(message[letter]) - bruteforce < 97:
                                print("descend trop bas, va a la fin")
                                display = chr(ord(message[letter]) - bruteforce + 26)
                            else:
                                print("recule de", bruteforce)
                                display = chr(ord(message[letter]) - bruteforce)
                        else:
                            if ord(message[letter]) + bruteforce > 122:
                                print("monte trop haut, va au début")
                                display = chr(ord(message[letter]) + bruteforce - 26)
                            else:
                                print("avance de", bruteforce)
                                display = chr(ord(message[letter]) + bruteforce)
                    else:
                        print("c'est un caractère spécial donc pas de modif")
                        display = message[letter]
                        continue
                    print("la lettre sortie est :", display)
                    print()
                    entryCoder.delete(letter)
                    entryCoder.insert(letter, display)
                    if animationTime == int(time.time()):
                        animationStep += 1
                        animationTime = int(time.time()) + 1
                        if animationStep == 4:
                            animationStep = 0
                    if method == "coding":
                        if animationStep == 0:
                            textCoder.config(text="Chiffrement du message en cours")
                        if animationStep == 1:
                            textCoder.config(text="Chiffrement du message en cours.")
                        if animationStep == 2:
                            textCoder.config(text="Chiffrement du message en cours..")
                        if animationStep == 3:
                            textCoder.config(text="Chiffrement du message en cours...")
                    else:
                        if animationStep == 0:
                            textCoder.config(text="Déchiffrement du message en cours")
                        if animationStep == 1:
                            textCoder.config(text="Déchiffrement du message en cours")
                        if animationStep == 2:
                            textCoder.config(text="Déchiffrement du message en cours")
                        if animationStep == 3:
                            textCoder.config(text="Déchiffrement du message en cours")
                    time.sleep(0.05)
                    textCoder.update()
                sortiePasse = sortiePasse + display
            coderPlayer.stop()
            if method == "decoding":
                textCoder.config(text="Message déchiffré avec succès!", style="Valid.TLabel")
            else:
                textCoder.config(text="Message chiffré avec succès!", style="Valid.TLabel")
            if method == "coding" and "nkvxzt" in sortiePasse.lower() and not enterpriseNameFound:
                backButton.config(state="disabled")
                buttonCoder.config(state="normal", text="Envoyer à l'infiltré",
                                   command=lambda: [audio("button.mp3"), send_enterprise_name()])
            else:
                buttonCoder.config(state="normal", text="Ok", command=coder_texts)
        else:
            error("La clé spécifiée est invalide.")


def coder_texts():
    global titleLabel
    global entryCoder
    global entryKey
    global textCoder
    global buttonCoder
    global textKey
    if method == "decoding":
        titleLabel.config(text="Déchiffrer un message")
        textCoder.config(text="Message à déchiffrer", style="TLabel")
        textKey.config(text="Clé de déchiffrement", state="normal")
        buttonCoder.config(text="Lancer le déchiffrement", command=lambda: [audio("button.mp3"), coder_check()],
                           state="normal")
    else:
        titleLabel.config(text="Chiffrer un message")
        textCoder.config(text="Message à chiffrer", style="TLabel")
        textKey.config(text="Clé de chiffrement", state="normal")
        buttonCoder.config(text="Lancer le chiffrement", command=lambda: [audio("button.mp3"), coder_check()])
    entryKey.config(state="normal")


def send_enterprise_name():
    global textCoder
    global entryCoder
    global animationHistory
    global titleLabel
    global enterpriseNameFound
    global radioLabel
    global entryRadio
    Button(window, text="< Retour", command=lambda: [audio("button.mp3"), radio()]).place(relx=0, rely=0.01,
                                                                                          width=220,
                                                                                          relheight=0.0926)
    if not enterpriseNameFound:
        enterpriseNameFound = True
        percent = 0
        buttonCoder.config(state="disabled")
        textKey.config(text="Envoi sur la fréquence 104.0 Mhz...", state="normal")
        sendingProgressBar = Progressbar(window, orient=HORIZONTAL, mode="determinate", maximum=100)
        sendingProgressBar.place(relx=0.5, rely=0.5, relwidth=0.21875, relheight=0.065, anchor=CENTER)
        while percent < 100:
            refreshTimer()
            percent += 1
            sendingProgressBar.config(value=percent)
            window.update()
            time.sleep(0.05)
        textCoder.destroy()
        entryCoder.destroy()
        titleLabel.config(text="Réponse reçue de l'infiltré")
        animationHistory = True
    else:
        radioLabel.destroy()
        entryRadio.destroy()
    printRadioMessage(None, "Réponse de l'infiltré", "Cela confirme nos soupçons sur cette entreprise...\nVotre "
                                                     "mission n'aura finalement pas été vaine.\nEssayez de vous "
                                                     "échapper d'ici pendant que nous intervenons chez Spacey.\n\nJ'ai caché un objet précieux dans la seconde partie du sac à dos.\nCependant, elle est verrouillée par un cadenas à 3 chiffres.\nNormalement, vous avez trouvé deux de ces chiffres grâce à mes anciens messages.\nLe dernier qu'il vous manque est simplement le chiffre de notre district.\n\nLorsque vous aurez récupéré les 3 chiffres, essayez les 6 combinaisons possibles du\ncadenas.\nVotre cher collègue,\nL'infiltré")


def radio():
    global entryRadio
    global radioLabel
    global enterpriseNameFound
    global windowTimer
    clear_frame()

    Button(window, text=">").place(relx=0.63, rely=0.35, relheight=0.065, relwidth=0.03646, anchor=CENTER)

    Button(window, text="< Retour", command=lambda: [audio("button.mp3"), main()]).place(relx=0, rely=0.01,
                                                                                         relwidth=0.1146,
                                                                                         relheight=0.0926)
    Label(window, text="Radio", style="Title.TLabel").place(relx=0.5, rely=0.055, anchor=CENTER)
    radioLabel = Label(window, text="Entrez la fréquence radio :")
    radioLabel.place(relx=0.395, rely=0.27)
    entryRadio = Entry(window, font="Helvetica " + str(int(20 * window.winfo_screenheight() / 1080)), state="focus")
    entryRadio.place(relx=0.5, rely=0.35, relwidth=0.21875, relheight=0.065, anchor=CENTER)
    Button(window, text=">", command=lambda: [audio("button.mp3"), radio_connect(entryRadio.get())]).place(relx=0.63,
                                                                                                           rely=0.35,
                                                                                                           relheight=0.065,
                                                                                                           width=70,
                                                                                                           anchor=CENTER)
    if radioStep > 0:
        Button(window, text="Historique des messages",
               command=lambda: [audio("button.mp3"), radio_history(radioStep)]).place(relx=0.5, rely=0.5,
                                                                                      relwidth=0.2396,
                                                                                      relheight=0.0926, anchor=CENTER)
    if enterpriseNameFound:
        Button(window, text="Réponse de l'infiltré",
               command=lambda: [audio("button.mp3"), send_enterprise_name()]).place(relx=0.5, rely=0.6, relwidth=0.2396,
                                                                                    relheight=0.0926, anchor=CENTER)
    window.bind_all("<Key-Return>", lambda void: radio_connect(entryRadio.get()))

    windowTimer = Label(window, text="", style="Title.TLabel")
    windowTimer.place(relx=1, rely=0.01, relwidth=0.1145, relheight=0.0926, anchor=NE)

    while True:
        refreshTimer()
        window.update()


def radio_connect(tempFrequency):
    clear_frame()
    global frequency
    global radioLabel
    global radioStep
    global entryRadio
    global animationHistory
    global radioUsed
    frequency = tempFrequency
    if "9" not in frequency and "1" not in frequency:
        error("Merci d'entrer une fréquence valide.")
        radio()
    if frequency in radioUsed:
        error("Cette fréquence radio est déjà dans l'historique.")
        radio()
    elif ("96.2" in frequency or "96,2" in frequency) and 96.2 not in radioUsed:
        radioStep += 1
        animationHistory = True
        radioUsed.append(96.2)
        radio_history(radioStep)
    elif ("137.7" in frequency or "137,7" in frequency) and 137.7 not in radioUsed:
        radioStep += 1
        animationHistory = True
        radioUsed.append(137.7)
        radio_history(radioStep)
    elif ("91.3" in frequency or "91,3" in frequency) and 91.3 not in radioUsed:
        radioStep += 1
        animationHistory = True
        radioUsed.append(91.3)
        radio_history(radioStep)
    elif ("85.1" in frequency or "85,1" in frequency) and 85.1 not in radioUsed:
        radioStep += 1
        animationHistory = True
        radioUsed.append(85.1)
        radio_history(radioStep)
    elif ("104" in frequency or "104.0" in frequency or "104,0" in frequency) and 104 not in radioUsed:
        radioStep += 1
        animationHistory = True
        radioUsed.append(104)
        radio_history(radioStep)
    else:
        animationHistory = True
        printRadioMessage(None, "Message",
                          '\nDésolé mais il ne semble pas y avoir de message sur la fréquence radio ''"' + frequency + '".\n\nVeuillez réessayer.')


def radio_history(page):
    global animationHistory
    global previousButton
    global nextButton
    clear_frame()
    previousButton = Button(window, text="<", state="disabled")
    previousButton.place(relx=0.385, rely=0.2, relheight=0.065, relwidth=0.03646, anchor=CENTER)
    nextButton = Button(window, text=">", state="disabled")
    nextButton.place(relx=0.615, rely=0.2, relheight=0.065, relwidth=0.03646, anchor=CENTER)
    if page == 1:
        printRadioMessage(page, "Premier message", "\nBonjour, je vois que vous avez trouvé la clé USB et la première "
                                                   "fréquence radio.\nJe suis l'infiltré, et comme vous l’ont expliqué les "
                                                   "chefs, je serai là tout le long de\nvotre séjour dans le "
                                                   "bunker.\n\nJ’ai caché de nombreux objets et fréquences radio dans la "
                                                   "salle pour communiquer\net vous aider à vous échapper d’ici.\n\nBonne "
                                                   "chance collègues.\n\nTrouvez une autre fréquence radio pour continuer.")
    elif page == 2:
        printRadioMessage(page, "Deuxième message",
                          "\nJe vous ai laissé un de mes gadgets sur la table du bunker pour que "
                          "vous puissiez\nobtenir un chiffre qui vous servira pour votre "
                          "fuite.\nVous devrez placer votre main entre 40 et 60 centimètres des cercles pour "
                          "actionner\nle mécanisme.\n\nTrouvez un moyen pour déchiffrer le "
                          "message lumineux.\n\nVotre cher collègue,\nL'infiltré")
    elif page == 3:
        printRadioMessage(page, "Troisième message",
                          "\nJe vous ai laissé un message codé dans l'annuaire à la page de l'initiale de mon\n"
                          "surnom. J'ai aussi caché le numéro de la CLÉ de déchiffrement dans la "
                          "salle.\n\nVous devrez utiliser l'ordinateur de surveillance pour le "
                          "déchiffrer puis tentez de\ncomprendre l'énigme.\n\n\nVotre cher collègue,\nL'infiltré")
    elif page == 4:
        printRadioMessage(page, "Quatrième message",
                          "\nCher collègue, je suis désolé de vous décevoir mais vos chances de "
                          "survie dans\nce bunker sont évaluées à « très faibles ».\nVous "
                          "n’aurez peut-être pas la possibilité de vous échapper.\nAvant "
                          "d’arriver à votre dernier souffle, nous vous demandons de collecter "
                          "le plus\nd’informations possible sur l’arme secrète de l’ennemi afin "
                          "de réussir la mission.\n\nTentez de retrouver le fournisseur de "
                          "l’arme secrète qui a trahi la nation.\nSi vous parvenez à le trouver, "
                          "chiffrez-le avec une clé de 21.\n\nVotre cher collègue,\nL'infiltré")
    elif page == 5:
        printRadioMessage(page, "Cinquième message",
                          "\n\nJ'ai caché la clé dans le grand coffre de l'armoire, mais pour "
                          "l'ouvrir, vous devrez\nallumer les 2 voyants verts de la face "
                          "avant.\n\nPour ce faire, actionnez les 2 mécanismes "
                          "simultanément.\n\n\nVotre cher collègue,\nL'infiltré")
    else:
        error("Impossible d'afficher le message.")


def printRadioMessage(index, subtitle, text):
    global animationHistory
    global previousButton
    global nextButton
    global pageToDisplay
    global windowTimer
    if index is None:
        clear_frame()
    backButton = Button(window, text="< Retour", state="disabled", command=lambda: [audio("button.mp3"), radio()])
    backButton.place(relx=0, rely=0.01, relwidth=0.1146, relheight=0.0926)
    Label(window, text="Messages reçus de l'infiltré", style="Title.TLabel").place(relx=0.5, rely=0.055, anchor=CENTER)
    indexFrame = Frame(window, borderwidth=1, relief="solid")
    indexFrame.place(relx=0.5, rely=0.2, relheight=0.065, relwidth=0.1927, anchor=CENTER)
    indexText = Label(indexFrame, text=subtitle, style="Frame.TLabel")
    indexText.place(relx=0.5, rely=0.5, anchor=CENTER)
    textFrame = Frame(window, borderwidth=1, relief="solid", style="TFrame")
    textFrame.place(relx=0.5, rely=0.6, relwidth=0.78125, relheight=0.5556, anchor=CENTER)
    radioMessage = Label(textFrame, style="Frame.TLabel")
    radioMessage.pack(fill=X)

    windowTimer = Label(window, text="", style="Title.TLabel")
    windowTimer.place(relx=1, rely=0.01, relwidth=0.1145, relheight=0.0926, anchor=NE)

    if animationHistory:
        radioProgressBar = Progressbar(window, orient=HORIZONTAL, mode="determinate", maximum=len(text))
        radioProgressBar.place(relx=0.5, rely=0.27, relheight=0.0463, relwidth=0.1927, anchor=CENTER)
        radioPlayer = vlc.MediaPlayer(os.getcwd() + "/Data/radio.mp3")
        radioPlayer.play()
        for letter in range(len(text) + 1):
            refreshTimer()
            radioProgressBar.config(value=letter)
            radioMessage.config(text=text[0:letter])
            window.update()
            time.sleep(0.035)
        radioProgressBar.destroy()
        radioPlayer.stop()
        animationHistory = False
    else:
        radioMessage.config(text=text)
    backButton.config(state="normal")
    if index is not None:
        if 1 <= index <= 5:
            if index - 1 > 0:
                previousButton.config(text="< " + str(index - 1), state="normal",
                                      command=lambda: [audio("button.mp3"), radio_history(index - 1)])
            if index + 1 <= radioStep:
                nextButton.config(text=str(index + 1) + " >", state="normal",
                                  command=lambda: [audio("button.mp3"), radio_history(index + 1)])
    while True:
        window.update()
        refreshTimer()


def endGame():
    global timerDisplay
    clear_frame()
    Label(window, text="Fin de jeu", style="Title.TLabel").place(relx=0.5, rely=0.055, anchor=CENTER)
    timerFrame = Frame(window, borderwidth=2, relief="solid")
    timerFrame.place(relx=0.5, rely=0.2, relheight=0.0741, relwidth=0.1146, anchor=CENTER)
    timerDisplay = Label(timerFrame, text="00 : 00", style="EndGame.TLabel")
    timerDisplay.place(relx=0.5, rely=0.5, anchor=CENTER)
    textFrame = Frame(window, borderwidth=1, relief="solid")
    textFrame.place(relx=0.5, rely=0.5, relwidth=0.78125, relheight=0.45, anchor=CENTER)
    textFrame.place()
    Label(textFrame,
          text="\nMalheureusement, vous êtes arrivés à court de temps…\nJe suis désolé de ne pas avoir été assez"
               " rapide et clair dans mes instructions pour\nvous aider à vous échapper du bunker.\nVous serez "
               "bientôt tous exécutés par nos ennemis.\nJ'ai été heureux de connaître chacun de "
               "vous.\n\nAdieu,\n- Votre cher collègue, l’infiltré", style="Frame.TLabel").pack(fill=X)
    window.bind_all("<Key-Home>", lambda void: endGameCheat())
    window.mainloop()


def endGameCheat():
    global upButton
    global timerAdd
    global returnMain
    timerAdd = 0
    window.bind_all("<Key-Home>")

    upButton = Button(window, text="^", command=lambda: [audio("button.mp3"), moreTime()])
    upButton.place(relx=0.42, rely=0.2, relheight=0.0741, relwidth=0.04427, anchor=CENTER)
    returnMain = Button(window, text=">", state="disabled",
                        command=lambda: [audio("button.mp3"), start_global_timer(timerAdd), main()])
    returnMain.place(relx=0.58, rely=0.2, relheight=0.0741, relwidth=0.04427, anchor=CENTER)


def moreTime():
    global returnMain
    global timerDisplay
    global timerAdd
    global upButton
    returnMain.config(state="normal")
    timerAdd += 300
    timerDisplay.config(text=str(int(timerAdd / 60)) + " : 00")
    if timerAdd == 3600:
        upButton.config(state="disabled")


window = Tk()
window.attributes("-fullscreen", True)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.title("Script Etienne Escape game I3 - Bunker russe")
style = Style()

style.configure("Start.TButton", font="Helvetica " + str(int(60 * window.winfo_screenheight() / 1080)))

style.configure("Notime.TLabel", font="Helvetica " + str(int(50 * window.winfo_screenheight() / 1080)) + " bold",
                foreground="red")
style.configure("EndGame.TLabel", font="Helvetica " + str(int(50 * window.winfo_screenheight() / 1080)) + " bold",
                foreground="red", background="white")
style.configure("Title.TLabel", font="Helvetica " + str(int(50 * window.winfo_screenheight() / 1080)) + " bold")
style.configure("Title.TButton", font="Helvetica " + str(int(30 * window.winfo_screenheight() / 1080)))

style.configure("TLabel", font="Helvetica " + str(int(30 * window.winfo_screenheight() / 1080)))
style.configure("TButton", font="Helvetica " + str(int(30 * window.winfo_screenheight() / 1080)))

style.map("Label.TEntry", fieldbackground=[("disabled", "white")], foreground=[("disabled", "black")])
style.configure("TFrame", background="white")
style.configure("Frame.TLabel", background="white")
style.configure("Valid.TLabel", foreground="green")
style.configure("Refused.TLabel", foreground="red")

Label(window, text="CONDAMNÉS", style="Title.TLabel").place(relx=0.5, rely=0.1, anchor=CENTER)
Label(window, text="Escape Game").place(relx=0.5, rely=0.145, anchor=CENTER)
startButton = Button(window, text="Démarrer le jeu", style="Start.TButton",
                     command=lambda: [audio("button.mp3"), start_game()])
startButton.place(relx=0.5, rely=0.45, relwidth=0.4167, relheight=0.2778, anchor=CENTER)
window.bind_all("<Key-Return>", lambda void: start_game())

if os.name == "nt":
    bgplayer = subprocess.Popen(
        '"C:/Program Files/VideoLAN/VLC/vlc.exe" /Data/background.m4a --qt-start-minimized --loop -I null')

################
# PAS TOUCHE, RESERVÉ AU DEV (ETIENNE)
# timerEnd = 10**10
# radio()
# hack()
# main()
# radioStep = 5
# endGame()
################

window.mainloop()
