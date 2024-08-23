import customtkinter as ctk
import requests, os

class Updater(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry("250x100")
        self.resizable(False, False)
        self.mainpath = os.path.dirname(os.path.abspath(__file__))
        self.repo_owner = 'SlovakTastic'
        self.repo_name = 'LearnAPP'
        self.api_url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest'
        self.token = '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'
        self.create_widgets()
        self.update_app()
        self.mainloop()

    def create_widgets(self):
        self.Label = ctk.CTkLabel(self, text="Updating...")
        self.Label.place(relx=0.5,rely=0.2, relwidth=0.5, relheight=0.2, anchor = "n")

        self.ProgressBar = ctk.CTkProgressBar(self)
        self.ProgressBar.place(relx=0.5, rely=0.5, anchor="n")

    def get_latest_release_info(self):
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(self.api_url, headers=headers)
        response.raise_for_status()
        latest_release = response.json()
        return latest_release
    
    def update_app(self):
        release_info = self.get_latest_release_info()
        version = release_info["tag_name"]
        assets = release_info["assets"]
        print(assets)
Updater()