import tkinter as tk

def say_hi():
    print("hi")

root = tk.Tk()
root.title("Say Hi")

hi_button = tk.Button(root, text="hi", command=say_hi)
hi_button.pack()

root.mainloop()