from tkinter import Tk, Label, Button
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox as mb

from noise_reduce import reduce_noise
import soundfile as sf
from MusicPlayer import MusicPlayer

from pygame import mixer
import pygame
import numpy as np

class NoiseReduceApp():

    def get_audio_file(self, label):
        label.config(text=askopenfilename(filetypes=(("WAV File", "*.wav"),)))

    def isFile(self, filename):

        try:
            f = open(filename)
        except IOError:
            print("File not accessible", filename)
            return False
        f.close()
        return True

    def reduce_noise_clicked(self):
        print("Reduce Noise Clicked")
        input_ok = False
        noise_ok = False
        print("Reduce Noise Button Clicked")
        if self.isFile(self.input_fileloc_label.cget("text")):
            print("Input File is Valid")
            input_ok = True

        else:
            print("Input File is Invalid")
            mb.showwarning(
                'Invalid File Path', 'Please specify a valid file path for Input Audio File')

        if self.isFile(self.noise_fileloc_label.cget("text")):
            print("Input File is Valid")
            noise_ok = True
        else:
            print("Input File is Invalid")
            mb.showwarning(
                'Invalid File Path', 'Please specify a valid file path for Noise Audio File')

        if input_ok and noise_ok:
            self.noise_reduced, self.rate = reduce_noise(self.input_fileloc_label.cget(
                "text"), self.noise_fileloc_label.cget("text"))
            self.outputfile_label.place(x=450, y=390)
            self.save_output_btn.place(x=450, y=360)
            mixer.init()
            sf.write('temp.wav', self.noise_reduced, self.rate)
            self.player = MusicPlayer('temp.wav')
            self.play_output_btn.place(x=300, y=360)
            self.output_gen_lbl.place(x=300, y=340)
        else:
            self.outputfile_label.place_forget()
            self.save_output_btn.place_forget()
            self.play_output_btn.place_forget()
            self.output_gen_lbl.place_forget()

  
    def save_output_file(self):
        print("Save Output Button Clicked")
        filetypes = [("Wav Files", "*.wav"),]
        filename = asksaveasfilename(filetypes=filetypes,defaultextension=filetypes)
        print(filename)
        sf.write(filename, self.noise_reduced, self.rate, 'PCM_24')
        self.outputfile_label.config(text=('File saved at '+ filename))
        mb.showinfo("File Saved", "File Saved Successfully")


    def play_music(self, playbtn):
        if self.player is not None:
            if self.player.get_state() == True and playbtn['text'] == 'Stop':
                self.player.pause()
                playbtn.config(text="Play")
            else:
                self.player.play()
                playbtn.config(text="Stop")
        
    
    def stop_music(self):
        if self.player is not None:
            self.player.stop()

    def check_event(self, playbtn):
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                print('music end event')
                playbtn.config(text="Play")

        self.root.after(100, lambda: self.check_event(playbtn))


    def on_closing(self):
        pygame.quit()
        self.root.destroy() 

    def __init__(self):

        pygame.init()
        self.root = Tk()
        self.root.title("NoiseReduction App")
        self.root.geometry("400x400")
        Label(self.root, text="").pack()
        self.heading = Label(self.root,
                             text="Welcome to Noise Reduction App",
                             font=("Helvetica", 20))
        self.heading.pack()

        self.noise_reduced = None
        self.rate = None
        self.player = None

        # input audio file section
        self.label_audiofile = Label(
            self.root, text="Noisy Audio file Input:", font=("Helvetica", 14))
        self.label_audiofile.place(x=260, y=100)

        self.input_fileloc_label = Label(self.root, text="Not_Chosen")
        self.input_fileloc_label.place(x=500, y=125)

        self.audiofile_btn = Button(
            self.root, text="Choose File", command=lambda: self.get_audio_file(self.input_fileloc_label))
        self.audiofile_btn.place(x=500, y=95)

        # noise file input section

        self.label_audiofile = Label(
            self.root, text="Noise file Input:", font=("Helvetica", 14))
        self.label_audiofile.place(x=260, y=200)

        self.noise_fileloc_label = Label(self.root, text="Not_Chosen")
        self.noise_fileloc_label.place(x=500, y=225)

        self.audiofile_btn = Button(
            self.root, text="Choose File", command=lambda: self.get_audio_file(self.noise_fileloc_label))
        self.audiofile_btn.place(x=500, y=195)

        # reduce noise button
        self.reduce_noise_btn = Button(
            self.root, text="Reduce Noise", command=self.reduce_noise_clicked)
        self.reduce_noise_btn.place(x=400, y=280)

        # output file section
        self.play_output_btn = Button(
            self.root, text="Play", command=lambda: self.play_music(self.play_output_btn))
       
        
        # save output file 
        self.save_output_btn = Button(
            self.root, text="Save Output", command=self.save_output_file)
        
        # output file loc
        self.outputfile_label = Label(self.root, text="Not_Chosen")
        

        self.output_gen_lbl = Label(self.root, text="Output Generated!", font=("Helvetica", 12))
        self.MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        self.check_event(self.play_output_btn)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry('1000x500')
        self.root.mainloop()


