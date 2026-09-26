import customtkinter as ctk
from theme import THEME

class QuestionnaireScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=THEME["bg_color"])
        self.controller = controller

        # Main Card Container
        card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=18,
            border_width=2,
            border_color=THEME["card_border"]
        )
        card.pack(pady=35, padx=60, fill="both", expand=True)

        # Header Title
        title_label = ctk.CTkLabel(
            card,
            text="Career Assessment",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=THEME["text_title"]
        )
        title_label.pack(pady=(35, 8))

        self.subtitle_label = ctk.CTkLabel(
            card,
            text="Answer these 2 simple questions to find your matching career paths.",
            font=ctk.CTkFont(size=16),
            text_color=THEME["text_body"]
        )
        self.subtitle_label.pack(pady=(0, 25))

        # Scrollable / Form Frame for Questions
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # EXACTLY 2 Questions:
        # Question 1: Hobbies/interest
        # Question 2: Career interest
        # With "Select" instead of "Don't care"
        self.questions = [
            {
                "key": "hobby_interest",
                "icon": "🎨",
                "title": "Question 1: Hobbies & Interests",
                "hint": "What do you enjoy doing most in your free time or school projects?",
                "options": [
                    "Select",
                    "Coding & Technology",
                    "Art, Drawing & Design",
                    "Mathematics & Problem Solving",
                    "Science & Experiments",
                    "Nature, Animals & Outdoors",
                    "Writing, Reading & Media",
                    "Business, Stocks & Finance",
                    "Leadership & Event Organizing",
                    "Helping People & Social Service",
                    "Building, Mechanics & Robotics"
                ]
            },
            {
                "key": "career_interest",
                "icon": "💼",
                "title": "Question 2: Career Interest",
                "hint": "Which professional industry or career field sparks your curiosity?",
                "options": [
                    "Select",
                    "Computer Science & IT",
                    "Healthcare & Medicine",
                    "Engineering & Architecture",
                    "Business, Finance & Banking",
                    "Design, Animation & Arts",
                    "Law, Journalism & Public Policy",
                    "Marketing & Entrepreneurship",
                    "Ecology & Wildlife Sciences",
                    "Psychology & Social Sciences"
                ]
            }
        ]

        self.variables = {}

        for q in self.questions:
            q_box = ctk.CTkFrame(
                form_frame,
                fg_color=THEME["surface_color"],
                corner_radius=12,
                border_width=1.5,
                border_color=THEME["card_border"]
            )
            q_box.pack(fill="x", pady=12, padx=15)

            # Header row with icon and title
            hdr_row = ctk.CTkFrame(q_box, fg_color="transparent")
            hdr_row.pack(fill="x", padx=16, pady=(12, 4))

            q_lbl = ctk.CTkLabel(
                hdr_row,
                text=f"{q['icon']}  {q['title']}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=THEME["text_title"]
            )
            q_lbl.pack(anchor="w")

            hint_lbl = ctk.CTkLabel(
                q_box,
                text=q["hint"],
                font=ctk.CTkFont(size=13),
                text_color=THEME["text_muted"]
            )
            hint_lbl.pack(anchor="w", padx=16, pady=(0, 10))

            var = ctk.StringVar(value="Select")
            self.variables[q["key"]] = var

            dropdown = ctk.CTkOptionMenu(
                q_box,
                values=q["options"],
                variable=var,
                width=380,
                height=38,
                corner_radius=8,
                fg_color=THEME["dropdown_fg"],
                button_color=THEME["dropdown_button"],
                button_hover_color=THEME["dropdown_hover"],
                dropdown_fg_color=THEME["menu_bg"],
                dropdown_text_color=THEME["menu_text"],
                dropdown_hover_color=THEME["menu_hover"],
                font=ctk.CTkFont(size=14, weight="bold"),
                dropdown_font=ctk.CTkFont(size=13)
            )
            dropdown.pack(anchor="w", padx=16, pady=(0, 14))

        # Bottom Navigation Buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(pady=(15, 30))

        back_button = ctk.CTkButton(
            button_frame,
            text="← Back",
            font=ctk.CTkFont(size=15),
            height=40,
            width=140,
            corner_radius=8,
            fg_color=THEME["secondary"],
            hover_color=THEME["secondary_hover"],
            text_color=THEME["secondary_text"],
            command=self.on_back
        )
        back_button.pack(side="left", padx=15)

        finish_button = ctk.CTkButton(
            button_frame,
            text="See My Results →",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            width=180,
            corner_radius=8,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            text_color=THEME["text_light"],
            command=self.on_finish
        )
        finish_button.pack(side="right", padx=15)

    def on_show(self):
        class_level = self.controller.user_data.get("class_level", "9th")
        stream = self.controller.user_data.get("stream")
        display_class = f"Class {class_level.replace('th', '')}"
        if stream:
            self.subtitle_label.configure(
                text=f"{display_class} ({stream} Stream) • Select your interests to find best matching careers"
            )
        else:
            self.subtitle_label.configure(
                text=f"{display_class} • Select your interests to find best matching careers"
            )

    def on_back(self):
        # Go back based on class level:
        # 11th & 12th go back to StreamSelectionScreen
        # 9th & 10th go back to ClassSelectionScreen (no subjects/stream)
        class_level = self.controller.user_data.get("class_level", "9th")
        if class_level in ["11th", "12th"]:
            self.controller.show_frame("StreamSelectionScreen")
        else:
            self.controller.show_frame("ClassSelectionScreen")

    def on_finish(self):
        answers = {
            "hobby_interest": self.variables["hobby_interest"].get(),
            "career_interest": self.variables["career_interest"].get()
        }
        self.controller.user_data["answers"] = answers
        self.controller.show_frame("ResultsScreen")
