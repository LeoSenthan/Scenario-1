import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from pathlib import Path

# Palette
BG         = "#1A1E2E"   
PANEL_BG   = "#1F2435"   
BTN_FG     = "#000000"   
BTN_BG     = "#1F2435"   
BTN_ACTIVE = "#2A3348"  
TITLE_FG   = "#D6E8F5"  
SUBTITLE_FG= "#6B8499"  
DIVIDER    = "#2E3D52"  

FONT_TITLE    = ("Georgia", 28, "bold")
FONT_SUBTITLE = ("Georgia", 11, "italic")
FONT_BTN      = ("Georgia", 13)

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.grid_propagate(False)
        self.image_path = Path(__file__).parent.parent / "static" / "thumbnail.jpg"

        self.columnconfigure(0, weight=2, uniform="equal")
        self.columnconfigure(1, weight=3, uniform="equal")
        self.rowconfigure(0, weight=2)  
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        left_panel = tk.Frame(self, bg=PANEL_BG)
        left_panel.grid(row=0, column=0, rowspan=4, sticky="nsew")
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=2)
        left_panel.rowconfigure(1, weight=1)
        left_panel.rowconfigure(2, weight=1)
        left_panel.rowconfigure(3, weight=1)

        title_block = tk.Frame(left_panel, bg=PANEL_BG)
        title_block.grid(row=0, column=0, sticky="nsew", padx=40, pady=(50, 10))

        tk.Label(
            title_block,
            text="MindfulDesk",
            font=FONT_TITLE,
            fg=TITLE_FG,
            bg=PANEL_BG,
            anchor="w"
        ).pack(anchor="w")

        tk.Label(
            title_block,
            text="Tools for focus, calm & healthy habits",
            font=FONT_SUBTITLE,
            fg=SUBTITLE_FG,
            bg=PANEL_BG,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))

        tk.Frame(left_panel, bg="#C8C0B0", height=1).grid(
            row=0, column=0, sticky="sew", padx=40, pady=(0, 0)
        )

        buttons = [
            ("Meditation", "MeditationScreen"),
            ("Timers",     "TimerScreen"),
            ("Hydration",  "HydrationScreen"),
        ]

        for i, (label, screen) in enumerate(buttons):
            btn = tk.Button(
                left_panel,
                text=label,
                font=FONT_BTN,

                fg=BTN_FG,
                bg=BTN_BG,
                activebackground=BTN_ACTIVE,
                activeforeground=BTN_FG,
                relief="flat",
                bd=0,
                pady=14,
                anchor="w",
                padx=30,
                command=lambda s=screen: controller.show_frame(s)
            )
            btn.grid(row=i + 1, column=0, sticky="ew", padx=40, pady=6)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=BTN_ACTIVE))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BTN_BG))

        self.image_label = tk.Label(self, bg="#2C2C2C", padx=0, pady=0, borderwidth=0, highlightthickness=0)
        self.image_label.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.after(1, self.load_image)

    def load_image(self):
        w = self.image_label.winfo_width()
        h = self.image_label.winfo_height()
        img = Image.open(self.image_path)
        img = ImageOps.fit(img, (w, h))
        image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=image, width=w, height=h)
        self.image_label.image = image