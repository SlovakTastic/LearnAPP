import os
import tkinter as tk
from tkinter import font
import customtkinter as ctk
from PIL import Image
import random, sqlite3, importlib, requests

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LearnAPP")
        self.geometry("800x525")
        self.minsize(800,525)
        ctk.set_appearance_mode("dark")

        self.create_variables()
        self.run()

    def create_variables(self):
        self.mainpath = os.path.dirname(os.path.abspath(__file__))
        print(self.mainpath)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    App() 
