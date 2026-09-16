import customtkinter as ctk
from tkinter import messagebox

class StreamSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        title_label = ctk.CTkLabel(self, text="Stream Selection", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(pady=(60, 20))

        self.subtitle_label = ctk.CTkLabel(self, text="Since you're in high school, tell us about your stream.", font=ctk.CTkFont(size=18))
        self.subtitle_label.pack(pady=(0, 40))

        # Form Frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Stream Input
        stream_label = ctk.CTkLabel(form_frame, text="Which stream have you taken?", font=ctk.CTkFont(size=16))
        stream_label.pack(pady=(10, 5))
        
        self.stream_var = ctk.StringVar(value="Science")
        self.stream_dropdown = ctk.CTkOptionMenu(
            form_frame, 
            values=["Science", "Commerce", "Arts"],
            variable=self.stream_var,
            width=300
        )
        self.stream_dropdown.pack(pady=(0, 30))

        # Strict Stream Question
        strict_label = ctk.CTkLabel(form_frame, text="Do you want to strictly follow careers related to your stream?", font=ctk.CTkFont(size=16))
        strict_label.pack(pady=(10, 5))
        
        self.strict_var = ctk.BooleanVar(value=True)
        self.radio_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.radio_frame.pack(pady=(0, 40))
        
        radio_yes = ctk.CTkRadioButton(self.radio_frame, text="Yes, stream specific only", variable=self.strict_var, value=True)
        radio_yes.pack(side="left", padx=20)
        
        radio_no = ctk.CTkRadioButton(self.radio_frame, text="No, show me all options", variable=self.strict_var, value=False)
        radio_no.pack(side="left", padx=20)

        # Navigation Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        back_button = ctk.CTkButton(button_frame, text="Back", font=ctk.CTkFont(size=16), height=40, width=150, fg_color="gray", hover_color="darkgray", command=self.on_back)
        back_button.pack(side="left", padx=20)

        next_button = ctk.CTkButton(button_frame, text="Continue", font=ctk.CTkFont(size=16, weight="bold"), height=40, width=150, command=self.on_next)
        next_button.pack(side="right", padx=20)
        
    def on_show(self):
        # Update text based on user name
        name = self.controller.user_data.get("name", "Student")
        self.subtitle_label.configure(text=f"Hi {name}! Since you're in high school, tell us about your stream.")

    def on_back(self):
        self.controller.show_frame("WelcomeScreen")

    def on_next(self):
        # Save to controller
        self.controller.user_data["stream"] = self.stream_var.get()
        self.controller.user_data["strict_stream"] = self.strict_var.get()

        # Go to questionnaire
        self.controller.show_frame("QuestionnaireScreen")
