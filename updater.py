import customtkinter as ctk
import requests, os

window = window

class Updater(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("250x100")
        self.resizable(False, False)
        self.api_url = f'https://api.github.com/repos/SlovakTastic/LearnAPP/contents'
        self.currentverfilename = os.listdir(__file__)[-1]
        self.create_widgets()
        self.update_logic()

    def update_logic(self):
        if self.get_latest_release_info()[-1]["name"] != self.currentverfilename:
            window.Label1 = ctk.CTkLabel(window, text="1 Update found. Commencing update...")
            window.Label1.pack(before=window.UpdateButton)
            window.after(1000, self.run)
        else:
            window.Label = ctk.CTkLabel(window, text="No update available.")
            window.Label.pack(before=window.UpdateButton)

    def create_widgets(self):
        self.Label = ctk.CTkLabel(self, text="Updating...")
        self.Label.place(relx=0.5,rely=0.2, relwidth=0.5, relheight=0.2, anchor = "n")

        self.ProgressBar = ctk.CTkProgressBar(self, maximum=100)
        self.ProgressBar.place(relx=0.5, rely=0.5, anchor="n")

    def check_modified_files(self):
        versionfile = requests.get(self.api_url)
        versionfile.raise_for_status()
        versionfilename = versionfile.json()[-1]["name"]
        versionfile = versionfile.json()[-1]["download_url"]
        versionfile = requests.get(versionfile)
        versionfile.raise_for_status()

        with open(f"{os.path.join(__file__, versionfilename)}") as file:
            file.write(versionfile.content)

        os.remove(os.path.join(__file__, self.currentverfilename))

    def run(self):
        window.destroy()
        self.check_modified_files()
        # self.download_modified_files()
        self.mainloop()


Updater()