import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import *
from tkinter import filedialog
import pygame
import shutil
from os import scandir



class screen():
    def __init__(self):
        self.minute = 25
        self.second = 0
        self.create_btn = 0
        self.cancel = 0
        self.again=0
        self.again1 = 0
        self.select_music_copy = ""
        self.rest = 0

        self.screen = tk.Tk()
        self.screen.title("Pomodora")
        self.screen.geometry("550x392")
        self.screen.configure(background="blue")
        self.screen.resizable(width=False , height=False)

        self.text = tk.Label(text="00:00", font="Andada 45", bg="blue")
        self.text.place(x=170, y=142)

        self.text1 = tk.Label(text="Hoşgeldiniz", font="Andada 20", bg="blue",fg="green")
        self.text1.place(x=170, y=0)

        self.stop_btn = tk.Button(text="Cancel", bg="blue", width=15, height=3,bd=5, command=self.stop_kontroller)
        self.stop_btn.place(x=190, y=222)

        self.start_btn = tk.Button(text="Start", bg="blue", width=15, height=3,bd=5, command=self.start_fonction)
        self.start_btn.place(x=190, y=222)

        self.scroll = tk.Scrollbar(self.screen)


        self.listbox = Listbox(self.screen, yscrollcommand=self.scroll.set,width=19,height=15,bd=5,
                               font="serif 12 bold",bg="grey",fg="white",
                               relief="raised",selectmode="browse")
        self.list_add()
        self.listbox.place(x=350,y=30)

        self.scroll.config(command=self.listbox.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.height= 342

        self.list_play = tk.Button(text="Play",bg="blue",bd=3,command=self.music_start)
        self.list_play.place(x=456,y=self.height)
        pygame.init()
        pygame.mixer.init()

        self.list_stop = tk.Button(text="Stop",bg="blue",bd=3,command=self.music_stop)
        self.list_stop.place(x=414,y=self.height)

        self.list_next = tk.Button(text="Next",bg="blue",bd=3,command=self.music_next)
        self.list_next.place(x=495,y=self.height)

        self.list_previous = tk.Button(text="Pervious",bg="blue",bd=3,command=self.music_previous)
        self.list_previous.place(x=350,y=self.height)

        self.add_btn = tk.Button(text="Music add",bg="blue",bd=3,command=self.music_add)
        self.add_btn.place(x=350,y=0,width=180)
        self.screen.mainloop()



    def start_fonction(self):

        self.cancel = 0
        self.start()
        self.text1.config(text="Başlayabilirsiniz")
        self.text1.place(x=140, y=0)

    def start(self):
        self.start_btn.destroy()
        if (self.second == 0 and self.minute == 0):
            if self.rest == 0:

                self.minute = 5
                self.text1.config(text="Mola Zamanı")
                self.text1.place(x=170, y=0)
                self.screen.after(1000, self.start)
                self.rest = 1
            else:
                self.minute = 25
                self.screen.after(1000, self.start)
                self.text1.config(text="Başlayabilirsiniz")
                self.text1.place(x=140, y=0)
                self.rest = 0
        elif self.cancel == 1:
            pygame.mixer.music.pause()
            pass
        elif self.second == 0:
            self.second = 60
            self.minute -= 1
            self.screen.after(0, self.start)
        else:
            self.second-=1
            self.time =  str(self.minute).zfill(2)+":"+str(self.second).zfill(2)
            self.text.config(text=self.time)
            self.screen.after(1000,self.start)

    def stop_kontroller(self):
        self.request = mbox.askquestion("Question", "Are you sure to quit?")
        if self.request == "yes":
            self.again1 = 0
            self.stop()

    def stop(self):
        if self.again1 == 0:
            self.again = 0
        self.cancel = 1
        self.start_btn = tk.Button(text="Start", bg="blue", width=15, height=3,bd=5,command=self.start_fonction)
        self.start_btn.place(x=190, y=222)
        if self.again == 0:
            self.start_btn.destroy()
            self.screen.after(750,self.stop)
            self.again = 1
            self.again1 = 1

    def list_add(self):
        self.add_number = 1
        self.klasor = "pomodora/music/"

        self.onlyfiles = []
        with scandir(self.klasor) as tarama:
            for belge in tarama:
                if belge.name.endswith(".mp3"):
                    ekle = "music/"+belge.name
                    self.onlyfiles.append(ekle)

        for i in self.onlyfiles:
            self.listbox.insert(self.add_number, i)

            self.add_number+=1




    def music_start(self):

        self.copy_list = self.onlyfiles.copy()


        self.select_music = self.listbox.get(ACTIVE)
        self.index_copy = self.onlyfiles.index(self.select_music)
        del self.copy_list[0:self.index_copy]
        if self.select_music != self.select_music_copy:

            clock = pygame.time.Clock()
            pygame.mixer.music.load(self.select_music)
            pygame.mixer.music.play()
            self.select_music_copy = self.select_music
        else:
            pygame.mixer.music.unpause()
            pause = True

    def music_stop(self):
        pygame.mixer.music.pause()
        pause = False

    def music_add(self):
        self.screen.filename = filedialog.askopenfilename(initialdir="music/",title="select a file",
                                                      filetypes=(("music","*.mp3"),("all files","*.*")),)
        self.file_name = self.screen.filename
        shutil.copy2(self.file_name, "music")


    def music_next(self):

        self.index = self.onlyfiles.index(self.select_music) +1
        if self.index == 70:
            self.copy_list = self.onlyfiles.copy()
            self.select_music = self.copy_list[0]
        else:

            self.copy_list = self.onlyfiles.copy()
            del self.copy_list[0:self.index]
            self.select_music = self.copy_list[0]
            clock = pygame.time.Clock()
            pygame.mixer.music.load(self.select_music)
            pygame.mixer.music.play()


    def music_previous(self):
        self.index = self.onlyfiles.index(self.select_music)-1

        self.copy_list = self.onlyfiles.copy()
        del self.copy_list[0:self.index]
        self.select_music = self.copy_list[0]
        clock = pygame.time.Clock()
        pygame.mixer.music.load(self.select_music)
        pygame.mixer.music.play()
        

screen()