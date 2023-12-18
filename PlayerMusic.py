import tkinter as tk
from tkinter import filedialog
import pygame
import threading
import time

class LecteurAudio:
    def __init__(self, master):
        self.master = master
        master.title("Lecteur Audio")

        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False

        # Créer les widgets
        self.label = tk.Label(master, text="Bienvenue dans le Lecteur Audio", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE, font=("Helvetica", 12))
        self.listbox.pack(pady=10)

        self.btn_add = tk.Button(master, text="Ajouter une piste", command=self.ajouter_piste)
        self.btn_add.pack()

        self.btn_remove = tk.Button(master, text="Supprimer la piste sélectionnée", command=self.supprimer_piste)
        self.btn_remove.pack()

        self.btn_play = tk.Button(master, text="Lire", command=self.lire)
        self.btn_play.pack()

        self.btn_pause = tk.Button(master, text="Pause", command=self.pause)
        self.btn_pause.pack()

        self.btn_stop = tk.Button(master, text="Arrêter", command=self.arreter)
        self.btn_stop.pack()

        self.btn_volume_up = tk.Button(master, text="Augmenter le volume", command=self.augmenter_volume)
        self.btn_volume_up.pack()

        self.btn_volume_down = tk.Button(master, text="Diminuer le volume", command=self.diminuer_volume)
        self.btn_volume_down.pack()

        self.progress_bar = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, length=200, showvalue=False, command=self.change_position)
        self.progress_bar.pack(pady=10)

        # Créer un thread pour la lecture audio
        self.audio_thread = threading.Thread(target=self.lire_audio_thread)

    def ajouter_piste(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3;*.wav")])
        if file_path:
            self.playlist.append(file_path)
            self.listbox.insert(tk.END, file_path)

    def supprimer_piste(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.playlist.pop(selected_index[0])
            self.listbox.delete(selected_index)

    def lire(self):
        if not self.is_playing and self.playlist:
            if not self.audio_thread.is_alive():
                self.audio_thread = threading.Thread(target=self.lire_audio_thread)
                self.audio_thread.start()
                self.is_playing = True
                self.update_progress_bar()

    def lire_audio_thread(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.playlist[self.current_track_index])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.master.after(100, self.check_audio_end)

    def check_audio_end(self):
        if pygame.mixer.music.get_busy():
            self.master.after(100, self.check_audio_end)
        else:
            self.is_playing = False

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def arreter(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

    def augmenter_volume(self):
        current_volume = pygame.mixer.music.get_volume()
        if current_volume < 1.0:
            pygame.mixer.music.set_volume(current_volume + 0.1)

    def diminuer_volume(self):
        current_volume = pygame.mixer.music.get_volume()
        if current_volume > 0.0:
            pygame.mixer.music.set_volume(current_volume - 0.1)

    def update_progress_bar(self):
        if self.is_playing:
            current_position = pygame.mixer.music.get_pos() / 1000  # en secondes
            total_duration = pygame.mixer.Sound(self.playlist[self.current_track_index]).get_length()
            progress_percent = (current_position / total_duration) * 100
            self.progress_bar.set(progress_percent)
            self.master.after(1000, self.update_progress_bar)

    def change_position(self, value):
        if self.is_playing:
            total_duration = pygame.mixer.Sound(self.playlist[self.current_track_index]).get_length()
            new_position = (float(value) / 100) * total_duration
            pygame.mixer.music.set_pos(new_position)

if __name__ == "__main__":
    root = tk.Tk()
    lecteur_audio = LecteurAudio(root)
    root.mainloop()
