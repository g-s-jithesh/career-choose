import customtkinter as ctk
from tkinter import messagebox

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        title_label = ctk.CTkLabel(self, text="Welcome to Career Chooser", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(pady=(60, 20))

        subtitle_label = ctk.CTkLabel(self, text="Let's find the perfect career path for you!", font=ctk.CTkFont(size=18))
        subtitle_label.pack(pady=(0, 40))

        # Form Frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Name Input
        name_label = ctk.CTkLabel(form_frame, text="What is your name?", font=ctk.CTkFont(size=16))
        name_label.pack(pady=(10, 5))
        self.name_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter your name")
        self.name_entry.pack(pady=(0, 20))

        # Class Input
        class_label = ctk.CTkLabel(form_frame, text="Which class are you in?", font=ctk.CTkFont(size=16))
        class_label.pack(pady=(10, 5))
        
        self.class_var = ctk.StringVar(value="9th")
        self.class_dropdown = ctk.CTkOptionMenu(
            form_frame, 
            values=["9th", "10th", "11th", "12th"],
            variable=self.class_var,
            width=300
        )
        self.class_dropdown.pack(pady=(0, 40))

        # Next Button
        next_button = ctk.CTkButton(self, text="Start Journey", font=ctk.CTkFont(size=16, weight="bold"), height=40, width=200, command=self.on_next)
        next_button.pack(pady=20)

    def on_next(self):
        name = self.name_entry.get().strip()
        class_level = self.class_var.get()

        if not name:
            messagebox.showerror("Error", "Please enter your name to continue.")
            return

        # Save to controller
        self.controller.user_data["name"] = name
        self.controller.user_data["class_level"] = class_level

        # Logic based on class level
        if class_level in ["11th", "12th"]:
            self.controller.show_frame("StreamSelectionScreen")
        else:
            self.controller.show_frame("QuestionnaireScreen")
