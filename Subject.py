import customtkinter as ctk

ctk.set_default_color_theme("blue")


class App:

    APP_NAME = "Select Subject"
    WIDTH = 580
    HEIGHT = 260

    def __init__(self, master=None, subject_var=None, callable_func=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        self.top = ctk.CTkToplevel(self.master)
        
        # Bring the window to the top
        self.top.lift()
        self.top.grab_set()
        self.top.title(App.APP_NAME)
        self.top.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.top.minsize(App.WIDTH, App.HEIGHT)

        self.label = ctk.CTkLabel(self.top, text="Select a subject:")
        self.label.place(relx=0.06, rely=0.2)
        self.subject_var = subject_var
        self.selected_subject = self.subject_var[0]
        self.option_menu = ctk.CTkOptionMenu(self.top, values=self.subject_var, command=self.get_subject)
        self.option_menu.place(relx=0.25, rely=0.2)
        self.button = ctk.CTkButton(self.top, text="Enter", command=callable_func)
        self.top.bind("<Return>", lambda event: callable_func())
        self.button.place(relx=0.45, rely=0.6)

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.top.bind("<Command-q>", self.on_closing) # type: ignore
    
        self.appearance_mode_label = ctk.CTkLabel(self.top, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.place(relx=0.04, rely=0.7)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.top, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.place(relx=0.04, rely=0.8)
        self.appearance_mode_optionemenu.set("System")
    
    def get_subject(self, selected_subject=None):
        if selected_subject is None:
            selected_subject = self.option_menu.get()
        subject_index = self.subject_var.index(selected_subject)
        self.selected_subject = self.subject_var[subject_index]
        return self.selected_subject
    
    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def on_closing(self, event=0):
        self.top.destroy()

    def start(self):
        self.top.mainloop()
        