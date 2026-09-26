import customtkinter as ctk
from theme import THEME

class StreamSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=THEME["bg_color"])
        self.controller = controller

        # Main Container Card
        card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=18,
            border_width=2,
            border_color=THEME["card_border"]
        )
        card.pack(pady=40, padx=60, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            card,
            text="Stream Selection",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=THEME["text_title"]
        )
        title_label.pack(pady=(35, 10))

        self.subtitle_label = ctk.CTkLabel(
            card,
            text="Since you are in Class 11/12, tell us about your academic stream.",
            font=ctk.CTkFont(size=16),
            text_color=THEME["text_body"]
        )
        self.subtitle_label.pack(pady=(0, 25))

        # Stream Selection Area
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(pady=10, padx=50, fill="both", expand=True)

        stream_lbl = ctk.CTkLabel(
            form_frame,
            text="Which stream are you studying in?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=THEME["text_title"]
        )
        stream_lbl.pack(pady=(10, 8))

        self.stream_var = ctk.StringVar(value="Science")
        
        # Interactive Stream Cards
        self.stream_buttons = {}
        stream_box = ctk.CTkFrame(form_frame, fg_color="transparent")
        stream_box.pack(pady=(0, 25))

        streams = [
            ("Science", "🔬 Science", "PCM, PCB, Computer Science"),
            ("Commerce", "📊 Commerce", "Accounts, Economics, Business"),
            ("Arts", "🎨 Arts / Humanities", "Psychology, History, Fine Arts")
        ]

        for s_val, s_title, s_desc in streams:
            box = ctk.CTkFrame(
                stream_box,
                fg_color=THEME["surface_color"],
                corner_radius=10,
                border_width=2,
                border_color=THEME["card_border"]
            )
            box.pack(side="left", padx=10, pady=5)

            btn = ctk.CTkButton(
                box,
                text=s_title,
                font=ctk.CTkFont(size=16, weight="bold"),
                height=42,
                width=170,
                corner_radius=8,
                fg_color=THEME["secondary"] if s_val != "Science" else THEME["primary"],
                hover_color=THEME["primary_hover"],
                text_color=THEME["secondary_text"] if s_val != "Science" else THEME["text_light"],
                command=lambda v=s_val: self.select_stream(v)
            )
            btn.pack(pady=(10, 4), padx=10)

            lbl = ctk.CTkLabel(
                box,
                text=s_desc,
                font=ctk.CTkFont(size=11),
                text_color=THEME["text_muted"]
            )
            lbl.pack(pady=(0, 10), padx=8)

            self.stream_buttons[s_val] = {
                "button": btn,
                "box": box
            }

        # Strict Stream Question
        strict_lbl = ctk.CTkLabel(
            form_frame,
            text="Do you want to focus strictly on careers within this stream?",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=THEME["text_title"]
        )
        strict_lbl.pack(pady=(10, 8))

        self.strict_var = ctk.BooleanVar(value=True)
        radio_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        radio_frame.pack(pady=(0, 25))

        radio_yes = ctk.CTkRadioButton(
            radio_frame,
            text="Yes, show stream-specific careers only",
            variable=self.strict_var,
            value=True,
            fg_color=THEME["primary"],
            border_color=THEME["secondary_hover"],
            text_color=THEME["text_title"],
            font=ctk.CTkFont(size=14)
        )
        radio_yes.pack(side="left", padx=15)

        radio_no = ctk.CTkRadioButton(
            radio_frame,
            text="No, include interdisciplinary & open options",
            variable=self.strict_var,
            value=False,
            fg_color=THEME["primary"],
            border_color=THEME["secondary_hover"],
            text_color=THEME["text_title"],
            font=ctk.CTkFont(size=14)
        )
        radio_no.pack(side="left", padx=15)

        # Navigation Buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(pady=(10, 30))

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

        next_button = ctk.CTkButton(
            button_frame,
            text="Continue →",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            width=160,
            corner_radius=8,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            text_color=THEME["text_light"],
            command=self.on_next
        )
        next_button.pack(side="right", padx=15)

    def select_stream(self, stream_val):
        self.stream_var.set(stream_val)
        for s_val, items in self.stream_buttons.items():
            btn = items["button"]
            box = items["box"]
            if s_val == stream_val:
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

    def on_show(self):
        class_level = self.controller.user_data.get("class_level", "11th")
        display_class = f"Class {class_level.replace('th', '')}"
        self.subtitle_label.configure(
            text=f"As a {display_class} student, choose your stream to tailor your career pathway."
        )

    def on_back(self):
        self.controller.show_frame("ClassSelectionScreen")

    def on_next(self):
        self.controller.user_data["stream"] = self.stream_var.get()
        self.controller.user_data["strict_stream"] = self.strict_var.get()
        self.controller.show_frame("QuestionnaireScreen")
