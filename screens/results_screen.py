import customtkinter as ctk
from database import get_careers

class ResultsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        self.title_label = ctk.CTkLabel(self, text="Your Recommended Careers", font=ctk.CTkFont(size=30, weight="bold"))
        self.title_label.pack(pady=(40, 10))

        self.subtitle_label = ctk.CTkLabel(self, text="Based on your profile, here are the best matches:", font=ctk.CTkFont(size=16))
        self.subtitle_label.pack(pady=(0, 20))

        # Scrollable Frame for Results
        self.results_frame = ctk.CTkScrollableFrame(self, width=650, height=400, fg_color="transparent")
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Navigation Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        back_button = ctk.CTkButton(button_frame, text="Retake Questionnaire", font=ctk.CTkFont(size=16), height=40, width=200, fg_color="gray", hover_color="darkgray", command=self.on_back)
        back_button.pack(side="left", padx=20)

        exit_button = ctk.CTkButton(button_frame, text="Exit Application", font=ctk.CTkFont(size=16, weight="bold"), height=40, width=200, fg_color="#c0392b", hover_color="#e74c3c", command=self.controller.destroy)
        exit_button.pack(side="right", padx=20)
        
    def on_show(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        user_data = self.controller.user_data
        
        stream_filter = None
        if user_data.get("class_level") in ["11th", "12th"] and user_data.get("strict_stream"):
            stream_filter = user_data.get("stream")
            
        filters = user_data.get("answers", {})
        
        # Fetch from database
        try:
            results = get_careers(stream_filter=stream_filter, filters=filters)
        except Exception as e:
            results = []
            error_lbl = ctk.CTkLabel(self.results_frame, text=f"Database error: {e}\nPlease check if MySQL is running.", text_color="red")
            error_lbl.pack(pady=20)
            return

        if not results:
            no_result_lbl = ctk.CTkLabel(self.results_frame, text="No exact matches found. Try relaxing some of your preferences!", font=ctk.CTkFont(size=16, slant="italic"))
            no_result_lbl.pack(pady=40)
            return

        for career in results:
            card = ctk.CTkFrame(self.results_frame, corner_radius=10)
            card.pack(fill="x", pady=10, padx=10)
            
            # Handle both dictionary and tuple returns safely based on cursor type
            if isinstance(career, dict):
                c_title = career['title']
                c_desc = career['description']
                c_env = career['work_environment']
                c_str = career['primary_strength']
            else:
                c_title = career[1]
                c_desc = career[2]
                c_env = career[4]
                c_str = career[5]

            title = ctk.CTkLabel(card, text=c_title, font=ctk.CTkFont(size=20, weight="bold"))
            title.pack(anchor="w", padx=15, pady=(15, 5))
            
            desc = ctk.CTkLabel(card, text=c_desc, font=ctk.CTkFont(size=14), wraplength=550, justify="left")
            desc.pack(anchor="w", padx=15, pady=5)
            
            tags = ctk.CTkLabel(card, text=f"Environment: {c_env} | Strength: {c_str}", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray")
            tags.pack(anchor="w", padx=15, pady=(5, 15))


    def on_back(self):
        self.controller.show_frame("QuestionnaireScreen")
