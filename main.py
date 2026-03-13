import tkinter as tk
from gui.main_window import MainWindow
from services.weather_api import getData, getTemperature 

def main():
    root = tk.Tk()
    app = MainWindow(root)
    print("App running")
    root.mainloop()         

if __name__ == "__main__":
    main()