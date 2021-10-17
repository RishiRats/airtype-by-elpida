from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

import webbrowser


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def core():
    window.destroy()
    import main.py


webbrowser.open("https://dev-elpida.netlify.app/")

window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    320.0,
    360.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    320.0,
    360.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    961.0,
    212.0,
    image=image_image_3
)

canvas.create_text(
    917.0,
    685.0,
    anchor="nw",
    text="Mail us:",
    fill="#00CFFF",
    font=("Comfortaa Bold", 18 * -1)
)

canvas.create_text(
    1005.0,
    685.0,
    anchor="nw",
    text=" dev.elpida@gmail.com",
    fill="#000000",
    font=("Comfortaa Bold", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: core(),
    relief="flat"
)
button_1.place(
    x=810.0,
    y=474.0,
    width=312.0,
    height=94.0
)
window.resizable(False, False)
window.title('AIRTYPE By Elpida')
window.mainloop()
