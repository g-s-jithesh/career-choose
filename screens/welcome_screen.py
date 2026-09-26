import customtkinter as ctk
from theme import THEME

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=THEME["bg_color"])
        self.controller = controller

        # Center Hero Card
        hero_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=18,
            border_width=2,
            border_color=THEME["card_border"]
        )
        hero_card.pack(pady=50, padx=60, fill="both", expand=True)

        # Decorative Top Icon / Header
        icon_label = ctk.CTkLabel(
            hero_card,
            text="🎓",
            font=ctk.CTkFont(size=56)
        )
        icon_label.pack(pady=(45, 10))

        # Main Title
        title_label = ctk.CTkLabel(
            hero_card,
            text="Welcome to Career Chooser",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=THEME["text_title"]
        )
        title_label.pack(pady=(0, 12))

        # Subtitle / Welcome Message
        subtitle_label = ctk.CTkLabel(
            hero_card,
            text="Find the perfect career path tailored to your interests and passions.",
            font=ctk.CTkFont(size=17),
            text_color=THEME["text_body"]
        )
        subtitle_label.pack(pady=(0, 25))

        # Highlights Box
        highlights_frame = ctk.CTkFrame(
            hero_card,
            fg_color=THEME["surface_color"],
            corner_radius=12,
            border_width=1,
            border_color=THEME["card_border"]
        )
        highlights_frame.pack(pady=(0, 35), padx=50, fill="x")

        highlights = [
            ("✨ Quick & Simple", "Answer just 2 questions about your hobbies and career interests."),
            ("🎯 Tailored Guidance", "Curated stream-specific pathways for senior students."),
            ("🚀 Explore Opportunities", "Discover in-demand careers across Science, Commerce & Arts.")
        ]

        for title, desc in highlights:
            item_frame = ctk.CTkFrame(highlights_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=8)

            t_lbl = ctk.CTkLabel(
                item_frame,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=THEME["text_title"],
                anchor="w"
            )
            t_lbl.pack(anchor="w")

            d_lbl = ctk.CTkLabel(
                item_frame,
                text=desc,
                font=ctk.CTkFont(size=13),
                text_color=THEME["text_muted"],
                anchor="w"
            )
            d_lbl.pack(anchor="w")

        # Next Button
        next_button = ctk.CTkButton(
            hero_card,
            text="Next →",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=44,
            width=220,
            corner_radius=10,
            fg_color=THEME["primary"],
            hover_color=THEME["primary_hover"],
            text_color=THEME["text_light"],
            command=self.on_next
        )
        next_button.pack(pady=(0, 40))

    def on_next(self):
        # Move directly to Class Selection
        self.controller.show_frame("ClassSelectionScreen")
