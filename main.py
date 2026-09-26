import customtkinter as ctk
from database import init_db
from theme import THEME
from screens.welcome_screen import WelcomeScreen
from screens.class_selection import ClassSelectionScreen
from screens.stream_selection import StreamSelectionScreen
from screens.questionnaire import QuestionnaireScreen
from screens.results_screen import ResultsScreen

ctk.set_appearance_mode("Light")

class CareerChooserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Career Chooser Platform")
        self.geometry("860x660")
        self.minsize(820, 620)
        self.configure(fg_color=THEME["bg_color"])
        
        # User profile state
        self.user_data = {
            "class_level": "9th",
            "stream": None,
            "strict_stream": True,
            "answers": {}
        }
        
        # Container to hold all frames
        self.container = ctk.CTkFrame(self, fg_color=THEME["bg_color"])
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Initialize database (MySQL with SQLite automatic fallback)
        init_db()

        # Add all frames to the dictionary
        screens = (
            WelcomeScreen,
            ClassSelectionScreen,
            StreamSelectionScreen,
            QuestionnaireScreen,
            ResultsScreen
        )

        for F in screens:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            
            # Put all frames in the same location; the active one is raised
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

if __name__ == "__main__":
    app = CareerChooserApp()
    app.mainloop()
