import customtkinter as ctk
from database import get_careers
from theme import THEME

class ResultsScreen(ctk.CTkFrame):
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
        card.pack(pady=30, padx=50, fill="both", expand=True)

        # Header Title
        self.title_label = ctk.CTkLabel(
            card,
            text="Your Recommended Careers",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=THEME["text_title"]
        )
        self.title_label.pack(pady=(30, 6))

        self.subtitle_label = ctk.CTkLabel(
            card,
            text="Based on your profile, here are the best matches for you:",
            font=ctk.CTkFont(size=15),
            text_color=THEME["text_body"]
        )
        self.subtitle_label.pack(pady=(0, 15))

        # Scrollable Frame for Results
        self.results_frame = ctk.CTkScrollableFrame(
            card,
            width=680,
            height=380,
            fg_color=THEME["surface_color"],
            corner_radius=12,
            border_width=1,
            border_color=THEME["card_border"],
            scrollbar_button_color=THEME["secondary_hover"],
            scrollbar_button_hover_color=THEME["primary"]
        )
        self.results_frame.pack(pady=10, padx=25, fill="both", expand=True)

        # Navigation Buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(pady=(15, 25))

        retake_button = ctk.CTkButton(
            button_frame,
            text="← Retake Assessment",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=180,
            corner_radius=8,
            fg_color=THEME["secondary"],
            hover_color=THEME["secondary_hover"],
            text_color=THEME["secondary_text"],
            command=self.on_retake
        )
        retake_button.pack(side="left", padx=10)

        change_class_button = ctk.CTkButton(
            button_frame,
            text="Change Class",
            font=ctk.CTkFont(size=14),
            height=40,
            width=140,
            corner_radius=8,
            fg_color=THEME["surface_color"],
            hover_color=THEME["secondary"],
            text_color=THEME["text_title"],
            border_width=1,
            border_color=THEME["card_border"],
            command=self.on_change_class
        )
        change_class_button.pack(side="left", padx=10)

        exit_button = ctk.CTkButton(
            button_frame,
            text="Exit Application",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=150,
            corner_radius=8,
            fg_color=THEME["danger"],
            hover_color=THEME["danger_hover"],
            text_color=THEME["text_light"],
            command=self.controller.destroy
        )
        exit_button.pack(side="right", padx=10)

    def on_show(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        user_data = self.controller.user_data
        class_level = user_data.get("class_level", "9th")
        display_class = f"Class {class_level.replace('th', '')}"

        stream_filter = None
        if class_level in ["11th", "12th"] and user_data.get("strict_stream", True):
            stream_filter = user_data.get("stream")

        if stream_filter:
            self.subtitle_label.configure(
                text=f"Personalized matches for {display_class} ({stream_filter} Stream):"
            )
        else:
            self.subtitle_label.configure(
                text=f"Personalized matches for {display_class} (Foundational Pathways):"
            )

        filters = user_data.get("answers", {})

        # Fetch from database
        try:
            results = get_careers(stream_filter=stream_filter, filters=filters)
        except Exception as e:
            results = []
            error_lbl = ctk.CTkLabel(
                self.results_frame,
                text=f"Notice: {e}\nPlease check your database configuration.",
                text_color=THEME["danger"]
            )
            error_lbl.pack(pady=20)
            return

        if not results:
            no_result_box = ctk.CTkFrame(
                self.results_frame,
                fg_color=THEME["card_bg"],
                corner_radius=12,
                border_width=1,
                border_color=THEME["card_border"]
            )
            no_result_box.pack(fill="x", padx=20, pady=30)

            no_result_lbl = ctk.CTkLabel(
                no_result_box,
                text="No exact matches found for that specific combination.\nTry choosing 'Select' for one or both questions to explore wider options!",
                font=ctk.CTkFont(size=15),
                text_color=THEME["text_body"]
            )
            no_result_lbl.pack(pady=25, padx=20)
            return

        for career in results:
            card = ctk.CTkFrame(
                self.results_frame,
                fg_color=THEME["card_bg"],
                corner_radius=12,
                border_width=1.5,
                border_color=THEME["card_border"]
            )
            card.pack(fill="x", pady=8, padx=10)

            # Dictionary access
            if isinstance(career, dict):
                c_title = career.get("title", "")
                c_desc = career.get("description", "")
                c_streams = career.get("allowed_streams", "All")
                c_field = career.get("career_interest", "") or career.get("primary_strength", "")
            else:
                c_title = career[1]
                c_desc = career[2]
                c_streams = career[3]
                c_field = career[5]

            # Header with title and stream badge
            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=16, pady=(14, 4))

            title_lbl = ctk.CTkLabel(
                top_row,
                text=c_title,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=THEME["text_title"]
            )
            title_lbl.pack(side="left")

            stream_badge = ctk.CTkLabel(
                top_row,
                text=f"Streams: {c_streams}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=THEME["tag_text"],
                fg_color=THEME["tag_bg"],
                corner_radius=6,
                padx=8,
                pady=2
            )
            stream_badge.pack(side="right")

            # Description
            desc_lbl = ctk.CTkLabel(
                card,
                text=c_desc,
                font=ctk.CTkFont(size=14),
                text_color=THEME["text_body"],
                wraplength=600,
                justify="left"
            )
            desc_lbl.pack(anchor="w", padx=16, pady=4)

            # Field info tag
            if c_field:
                field_lbl = ctk.CTkLabel(
                    card,
                    text=f"✨ Recommended Field: {c_field}",
                    font=ctk.CTkFont(size=12, slant="italic"),
                    text_color=THEME["text_muted"]
                )
                field_lbl.pack(anchor="w", padx=16, pady=(2, 12))

    def on_retake(self):
        self.controller.show_frame("QuestionnaireScreen")

    def on_change_class(self):
        self.controller.show_frame("ClassSelectionScreen")
