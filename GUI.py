import tkinter as tk

HEIGHT = 400
WIDTH = 800


root = tk.Tk()


def main(HEIGHT, WIDTH):
    #root = tk.Tk()

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    background_image = tk.PhotoImage(file='./Files/pics/hog.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(relheight=1, relwidth=1)

    frame = tk.Frame(root, bg='#80c1ff', bd=5)  # can use color hex codes
    frame.place(relx=0.5, rely=0.1, relwidth=0.75,
                relheight=0.1, anchor='n')

    data = tk.Button(frame, text="View Data", bg='grey',
                     fg='blue', font=40, command=lambda: data_page(HEIGHT, WIDTH))
    data.place(relx=0.75, relwidth=0.25, relheight=1)

    slaughter = tk.Button(frame, text="Slaughter", bg='grey',
                          fg='blue', font=40, command=lambda: slaughter_page(HEIGHT, WIDTH))
    slaughter.place(relx=0.5, relwidth=0.25, relheight=1)

    consumable = tk.Button(frame, text="Consumables", bg='grey',
                           fg='blue', font=40, command=lambda: consumables_page(HEIGHT, WIDTH))
    consumable.place(relx=0.25, relwidth=0.25, relheight=1)

    piglet = tk.Button(frame, text="Piglet", bg='grey',
                       fg='blue', font=40, command=lambda: piglet_page(HEIGHT, WIDTH))
    piglet.place(relx=0, relwidth=0.25, relheight=1)

    # root.mainloop()


def piglet_page(HEIGHT, WIDTH):

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(root, bg="#80c1ff")
    frame.place(relheight=1, relwidth=1)

    home = tk.Button(frame, text="Home", bg="yellow",
                     command=lambda: print(piglet_price.get(), piglet_age.get()))
    home.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

    pigId = tk.Label(frame, text="piglet")
    pigId.place(relheight=0.1, relwidth=1)

    piglet_age = tk.Entry(frame)
    piglet_age.place(relx=0, rely=0.1)

    piglet_price = tk.Entry(frame)
    piglet_price.place(relx=0, rely=0.2)


def consumables_page(HEIGHT, WIDTH):

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(root, bg="#80c1ff")
    frame.place(relheight=1, relwidth=1)

    home = tk.Button(frame, text="Home", bg="yellow",
                     command=lambda: main(HEIGHT, WIDTH))
    home.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

    pigId = tk.Label(frame, text="consumables")
    pigId.place(relheight=0.1, relwidth=1)


def slaughter_page(HEIGHT, WIDTH):

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(root, bg="#80c1ff")
    frame.place(relheight=1, relwidth=1)

    home = tk.Button(frame, text="Home", bg="yellow",
                     command=lambda: main(HEIGHT, WIDTH))
    home.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

    pigId = tk.Label(frame, text="slaughter_page")
    pigId.place(relheight=0.1, relwidth=1)


def data_page(HEIGHT, WIDTH):

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(root, bg="#80c1ff")
    frame.place(relheight=1, relwidth=1)

    home = tk.Button(frame, text="Home", bg="yellow",
                     command=lambda: main(HEIGHT, WIDTH))
    home.place(relx=0, rely=0.95, relwidth=0.1, relheight=0.05)

    pigId = tk.Label(frame, text="data_page")
    pigId.place(relheight=0.1, relwidth=1)


def check():
    print(piglet_page(HEIGHT, WIDTH).a)

main(HEIGHT, WIDTH)

root.mainloop()
