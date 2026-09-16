import customtkinter as ctk
from tkinter import messagebox

class QuestionnaireScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        title_label = ctk.CTkLabel(self, text="Career Assessment", font=ctk.CTkFont(size=30, weight="bold"))
        title_label.pack(pady=(40, 10))

        subtitle_label = ctk.CTkLabel(self, text="Tell us about your preferences to find the best match.", font=ctk.CTkFont(size=16))
        subtitle_label.pack(pady=(0, 20))

        # Scrollable Frame for Questions
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=400, fg_color="transparent")
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.questions = [
            {
                "key": "work_environment",
                "text": "What type of work environment do you prefer?",
                "options": ["Introvert (Quiet, Independent)", "Extrovert (Social, Team-oriented)", "Don't Care"]
            },
            {
                "key": "primary_strength",
                "text": "What is your primary strength or interest?",
                "options": ["Logic", "Art", "Math", "Science", "Nature", "Communication", "Leadership", "Empathy", "Organization", "Don't Care"]
            },
            {
                "key": "education_length",
                "text": "How long are you willing to study after high school?",
                "options": ["Short-term (1-2 yrs / Diplomas)", "Medium-term (3-4 yrs / Bachelor's)", "Long-term (5+ yrs / Master's, Medicine)", "Any"]
            },
            {
                "key": "hands_on",
                "text": "Do you prefer a desk job or a hands-on/field job?",
                "options": ["Desk Job", "Hands-on", "Both", "Don't Care"]
            }
        ]

        self.variables = {}

        for q in self.questions:
            q_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            q_frame.pack(fill="x", pady=10)
            
            lbl = ctk.CTkLabel(q_frame, text=q["text"], font=ctk.CTkFont(size=16, weight="bold"))
            lbl.pack(anchor="w", pady=(0, 5))
            
            var = ctk.StringVar(value=q["options"][-1]) # Default to last option (usually Don't Care/Any)
            self.variables[q["key"]] = var
            
            dropdown = ctk.CTkOptionMenu(q_frame, values=q["options"], variable=var, width=400)
            dropdown.pack(anchor="w")

        # Navigation Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        back_button = ctk.CTkButton(button_frame, text="Back", font=ctk.CTkFont(size=16), height=40, width=150, fg_color="gray", hover_color="darkgray", command=self.on_back)
        back_button.pack(side="left", padx=20)

        finish_button = ctk.CTkButton(button_frame, text="See My Results", font=ctk.CTkFont(size=16, weight="bold"), height=40, width=150, command=self.on_finish)
        finish_button.pack(side="right", padx=20)
        
    def on_show(self):
        pass # Optional: Reset or update fields if needed

    def on_back(self):
        # Go back based on class level
        class_level = self.controller.user_data.get("class_level", "9th")
        if class_level in ["11th", "12th"]:
            self.controller.show_frame("StreamSelectionScreen")
        else:
            self.controller.show_frame("WelcomeScreen")

    def on_finish(self):
        answers = {}
        for key, var in self.variables.items():
            val = var.get()
            # Map complex UI strings back to database strings
            if "Introvert" in val: val = "Introvert"
            elif "Extrovert" in val: val = "Extrovert"
            elif "Short-term" in val: val = "Short-term"
            elif "Medium-term" in val: val = "Medium-term"
            elif "Long-term" in val: val = "Long-term"
            elif val == "Any": val = "Don't Care"
            
            answers[key] = val

        self.controller.user_data["answers"] = answers
        self.controller.show_frame("ResultsScreen")
