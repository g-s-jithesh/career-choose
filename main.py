import customtkinter as ctk
from database import init_db
from screens.welcome_screen import WelcomeScreen
from screens.stream_selection import StreamSelectionScreen
from screens.questionnaire import QuestionnaireScreen
from screens.results_screen import ResultsScreen

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CareerChooserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Career Chooser Platform")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # User data collected throughout the app
        self.user_data = {
            "name": "",
            "class_level": "",
            "stream": None,
            "strict_stream": False,
            "answers": {}
        }
        
        # Container to hold all frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Initialize database
        init_db()

        # Add all frames to the dictionary
        for F in (WelcomeScreen, StreamSelectionScreen, QuestionnaireScreen, ResultsScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            
            # Put all frames in the same location; the one on top will be visible
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
        # Call an update method if the frame needs to refresh its data
        if hasattr(frame, "on_show"):
            frame.on_show()

if __name__ == "__main__":
    app = CareerChooserApp()
    app.mainloop()
