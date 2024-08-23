import os, sys, requests
import customtkinter as ctk
from tkinter import messagebox, font

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LearnAPP")
        self.geometry("800x525")
        self.minsize(800, 525)
        ctk.set_appearance_mode("dark")

        self.create_variables()
        self.create_widgets()
        self.run()

    def create_variables(self):
        self.mainpath = os.path.dirname(os.path.abspath(__file__))
        self.api_url = 'https://api.github.com/repos/SlovakTastic/LearnAPP/contents'
        self.currentverfilename = os.listdir(self.mainpath)[-1]

    def create_widgets(self):
        self.SettingsBtn = ctk.CTkButton(self, text="Settings", command=self.showsettings)
        self.SettingsBtn.place(relx=0.9,rely=0.1, anchor="ne")

        self.SettingsFrame = ctk.CTkFrame(self)
        # self.UpdateProgressBar = ctk.CTkProgressBar(self.SettingsFrame)
        self.CheckForUpdatesBtn = ctk.CTkButton(self.SettingsFrame, text="Check for updates", command=self.check_update)
        self.UpdatesLabel = ctk.CTkLabel(self.SettingsFrame, text="No updates yet...")

    def showsettings(self):
        self.SettingsBtn.place_forget()
        
        self.SettingsFrame.place(relx=0.5,rely=0.5, anchor = "center", relwidth=0.5, relheight=0.9)
        # self.UpdateProgressBar.place(relx=0.5,rely=0.5, anchor = "center", relwidth=0.5, relheight=0.9)
        self.CheckForUpdatesBtn.place(relx=0.5,rely=0.5, anchor = "center")
        self.UpdatesLabel.place(relx=0.5,rely=0.3, anchor = "center")

    def check_update(self):
        if self.get_latest_release_info()[-1]["name"] != self.currentverfilename:
            self.showsettings()
            self.UpdatesLabel.configure(text="Updating...")
            self.check_modified_files()
        else:
            self.showsettings()
            self.UpdatesLabel.configure(text="No updates available!")

    def get_latest_release_info(self):
        response = requests.get(self.api_url)
        response.raise_for_status()
        latest_release = response.json()
        return latest_release
    
    def check_modified_files(self):
        data = requests.get(self.api_url)
        data.raise_for_status()
        versionfilename = data.json()[-1]["name"]
        versionfile = data.json()[-1]["download_url"]
        versionfile = requests.get(versionfile)
        versionfile.raise_for_status()

        with open(f"{os.path.join(self.mainpath, versionfilename)}", "wb") as file:
            file.write(versionfile.content)

        os.remove(os.path.join(self.mainpath, self.currentverfilename))
        os.remove(os.path.join(self.mainpath, "mdf.txt"))

        mdffile = data.json()[3]["download_url"]
        mdffile = requests.get(mdffile)
        mdffile.raise_for_status()

        with open(f"{os.path.join(self.mainpath, "mdf.txt")}", "wb") as file:
            file.write(mdffile.content)

        self.fetch_update_files()
    
    def fetch_update_files(self):
        with open(os.path.join(self.mainpath, "mdf.txt"), "r") as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines if line.strip()]
        for line in lines:
            apppathformat = self.mainpath + line.replace("/", "\\\\")
            filelink = self.api_url + line
            filelink = requests.get(filelink)
            filelink.raise_for_status()
            filelink = filelink.json()["download_url"]
            filelink = requests.get(filelink)

            if os.path.exists(apppathformat):
                os.remove(apppathformat)
            with open(apppathformat, "wb") as file:
                file.write(filelink.content)
                print("Success!")

    def prompt_restart(self):
        restart = messagebox.showinfo("Restart Required", "Update complete. Restart is necessary.")
        if restart:
            self.restart_application()
        else:
            self.destroy()

    def restart_application(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def run(self):
        self.check_update()
        self.mainloop()

if __name__ == "__main__":
    App()
