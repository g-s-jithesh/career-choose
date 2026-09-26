import customtkinter as ctk
from tkinter import messagebox
from theme import THEME

class ClassSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=THEME["bg_color"])
        self.controller = controller
        self.selected_class = None

        # Container Card
        card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=18,
            border_width=2,
            border_color=THEME["card_border"]
        )
        card.pack(pady=40, padx=60, fill="both", expand=True)

        # Header Title
        title_label = ctk.CTkLabel(
            card,
            text="Select Your Class",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=THEME["text_title"]
        )
        title_label.pack(pady=(40, 8))

        subtitle_label = ctk.CTkLabel(
            card,
            text="Choose your grade level to tailor your career pathway assessment.",
            font=ctk.CTkFont(size=16),
            text_color=THEME["text_body"]
        )
        subtitle_label.pack(pady=(0, 30))

        # Buttons Grid Frame
        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(pady=10, padx=40)

        self.class_buttons = {}
        classes_info = [
            ("9th", "Class 9", "Secondary School (Foundations)"),
            ("10th", "Class 10", "Secondary School (Board Exam Year)"),
            ("11th", "Class 11", "Senior Secondary (Stream Specialization)"),
            ("12th", "Class 12", "Senior Secondary (Higher Secondary)")
        ]

        for idx, (code, title, desc) in enumerate(classes_info):
            row = idx // 2
            col = idx % 2

            btn_box = ctk.CTkFrame(
                grid_frame,
                fg_color=THEME["surface_color"],
                corner_radius=12,
                border_width=2,
                border_color=THEME["card_border"]
            )
            btn_box.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            btn = ctk.CTkButton(
                btn_box,
                text=title,
                font=ctk.CTkFont(size=20, weight="bold"),
                height=50,
                width=240,
                corner_radius=10,
                fg_color=THEME["secondary"],
                hover_color=THEME["secondary_hover"],
                text_color=THEME["secondary_text"],
                command=lambda c=code: self.select_class(c)
            )
            btn.pack(pady=(15, 6), padx=15)

            sub_lbl = ctk.CTkLabel(
                btn_box,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color=THEME["text_muted"]
            )
            sub_lbl.pack(pady=(0, 12), padx=10)

            self.class_buttons[code] = {
                "button": btn,
                "box": btn_box
            }

        # Status / Feedback label
        self.status_lbl = ctk.CTkLabel(
            card,
            text="Please select your class to proceed.",
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color=THEME["text_muted"]
        )
        self.status_lbl.pack(pady=(20, 10))

        # Bottom Navigation
        nav_frame = ctk.CTkFrame(card, fg_color="transparent")
        nav_frame.pack(pady=(10, 30))

        back_button = ctk.CTkButton(
            nav_frame,
            text="← Back",
            font=ctk.CTkFont(size=15),
            height=40,
            width=130,
            corner_radius=8,
            fg_color=THEME["secondary"],
            hover_color=THEME["secondary_hover"],
            text_color=THEME["secondary_text"],
            command=self.on_back
        )
        back_button.pack(side="left", padx=15)

        self.continue_button = ctk.CTkButton(
            nav_frame,
            text="Continue →",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            width=150,
            corner_radius=8,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            text_color=THEME["text_light"],
            command=self.on_continue
        )
        self.continue_button.pack(side="right", padx=15)

    def select_class(self, class_code):
        self.selected_class = class_code

        # Update button visuals to show active selection
        for code, items in self.class_buttons.items():
            btn = items["button"]
            box = items["box"]
            if code == class_code:
                btn.configure(
                    fg_color=THEME["primary"],
                    text_color=THEME["text_light"],
                    hover_color=THEME["primary_hover"]
                )
                box.configure(border_color=THEME["primary"], border_width=2)
            else:
                btn.configure(
                    fg_color=THEME["secondary"],
                    text_color=THEME["secondary_text"],
                    hover_color=THEME["secondary_hover"]
                )
                box.configure(border_color=THEME["card_border"], border_width=1)

        display_name = f"Class {class_code.replace('th', '')}"
        if class_code in ["9th", "10th"]:
            self.status_lbl.configure(
                text=f"Selected: {display_name} (Direct to questionnaire - no subjects required)",
                text_color=THEME["primary"]
            )
        else:
            self.status_lbl.configure(
                text=f"Selected: {display_name} (Next step: Stream selection for 11th/12th)",
                text_color=THEME["primary"]
            )

    def on_continue(self):
        if not self.selected_class:
            messagebox.showinfo("Select Class", "Please click one of the class buttons above to continue.")
            return

        self.controller.user_data["class_level"] = self.selected_class

        # Routing:
        # Classes 9 & 10: No stream or subjects required -> Go straight to Questionnaire
        # Classes 11 & 12: Stream is only for 11/12 -> Go to Stream Selection
        if self.selected_class in ["11th", "12th"]:
            self.controller.show_frame("StreamSelectionScreen")
        else:
            self.controller.user_data["stream"] = None
            self.controller.user_data["strict_stream"] = False
            self.controller.show_frame("QuestionnaireScreen")

    def on_back(self):
        self.controller.show_frame("WelcomeScreen")

    def on_show(self):
        # Refresh or keep selection
        pass
