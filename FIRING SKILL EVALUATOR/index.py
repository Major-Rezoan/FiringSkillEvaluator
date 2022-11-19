from pathlib import Path
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from window1 import index_items

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Firing Skill Evaluator")
window.attributes('-fullscreen', True)
window.configure(bg = "#2DD32C")
window = index_items(window, relative_to_assets)
window.mainloop()