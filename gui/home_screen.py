import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from pathlib import Path
from services.weather_api import getData, getLocation, getTemperature, getHumidity

BG         = "#2B2D3A"
PANEL_BG   = "#2B2D3A"
BTN_FG     = "#000000"
BTN_BG     = "#313447"
BTN_ACTIVE = "#3C4059"
TITLE_FG   = "#DDD8EE"
SUBTITLE_FG= "#7E7A96"
DIVIDER    = "#3E4159"
WEATHER_BG = "#2B2D3A"
WEATHER_FG = "#DDD8EE"
WEATHER_SUB= "#8A849E"

FONT_TITLE    = ("Georgia", 28, "bold")
FONT_SUBTITLE = ("Georgia", 11, "italic")
FONT_BTN      = ("Georgia", 13)
FONT_TEMP     = ("Georgia", 52, "bold")
FONT_CITY     = ("Georgia", 15, "italic")
FONT_FEELS    = ("Georgia", 13, "italic")
FONT_HUMIDITY = ("Georgia", 13, "italic")


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

        tk.Frame(left_panel, bg=DIVIDER, height=1).grid(
            row=0, column=0, sticky="sew", padx=40
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

        right_panel = tk.Frame(self, bg="#252736")
        right_panel.grid(row=0, column=1, rowspan=4, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=0)

        self.image_label = tk.Label(
            right_panel, bg="#252736",
            padx=0, pady=0, borderwidth=0, highlightthickness=0
        )
        self.image_label.grid(row=0, column=0, rowspan=2, sticky="nsew")

        tk.Frame(right_panel, bg=DIVIDER, height=1).grid(row=1, column=0, sticky="new")

        weather_bar = tk.Frame(right_panel, bg=WEATHER_BG, pady=20)
        weather_bar.grid(row=1, column=0, sticky="sew")
        weather_bar.columnconfigure(0, weight=1)
        weather_bar.columnconfigure(1, weight=0)

        left_weather = tk.Frame(weather_bar, bg=WEATHER_BG)
        left_weather.grid(row=0, column=0, sticky="w", padx=28)

        self.lbl_city = tk.Label(
            left_weather,
            text="—",
            font=FONT_CITY,
            fg=WEATHER_SUB,
            bg=WEATHER_BG,
            anchor="w"
        )
        self.lbl_city.pack(anchor="w")

        self.lbl_temp = tk.Label(
            left_weather,
            text="--°C",
            font=FONT_TEMP,
            fg=WEATHER_FG,
            bg=WEATHER_BG,
            anchor="w"
        )
        self.lbl_temp.pack(anchor="w")

        self.lbl_feels = tk.Label(
            left_weather,
            text="Feels like --°C",
            font=FONT_FEELS,
            fg=WEATHER_SUB,
            bg=WEATHER_BG,
            anchor="w"
        )
        self.lbl_feels.pack(anchor="w")

        right_weather = tk.Frame(weather_bar, bg=WEATHER_BG)
        right_weather.grid(row=0, column=1, sticky="e", padx=28)

        self.lbl_humidity = tk.Label(
            right_weather,
            text="Humidity\n--",
            font=FONT_HUMIDITY,
            fg=WEATHER_SUB,
            bg=WEATHER_BG,
            justify="right"
        )
        self.lbl_humidity.pack(anchor="e")

        self.after(1, self.load_image)
        self.after(100, self.load_weather)

    def load_image(self):
        w = self.image_label.winfo_width()
        h = self.image_label.winfo_height()
        if w < 2 or h < 2:
            self.after(50, self.load_image)
            return
        img = Image.open(self.image_path)
        img = ImageOps.fit(img, (w, h))
        image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=image, width=w, height=h)
        self.image_label.image = image

    def load_weather(self):
        try:
            data = getData("london")
            city, country = getLocation(data)
            temp, feels_like = getTemperature(data)
            humidity = getHumidity(data)

            self.lbl_city.configure(text=f"{city}, {country}")
            self.lbl_temp.configure(text=f"{round(temp)}°C")
            self.lbl_feels.configure(text=f"Feels like {round(feels_like)}°C")
            self.lbl_humidity.configure(text=f"Humidity\n{humidity}%")
        except Exception as e:
            self.lbl_city.configure(text="Weather unavailable")
            self.lbl_temp.configure(text="--°C")
            print(f"Weather error: {e}")