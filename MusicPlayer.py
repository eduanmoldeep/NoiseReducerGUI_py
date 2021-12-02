from tkinter import *
from tkinter import filedialog
from pygame import mixer
from pygame.sndarray import use_arraytype

class MusicPlayer:
    def __init__(self):
        self.music_file = False
        self.playing_state = False
    def __init__(self, filename:str ):
        self.music_file = filename
        self.playing_state = False
        use_arraytype('numpy')

    def get_state(self):
        return self.playing_state
    def load(self):
        self.music_file = filedialog.askopenfilename()
    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
            self.playing_state = True
    def pause(self):
        if self.playing_state:
            mixer.music.pause()
            self.playing_state=False
        else:
            mixer.music.unpause()
            self.playing_state = True
    def stop(self):
        mixer.music.stop()

# root = Tk()
# app= MusicPlayer(root)
# root.mainloop()
