import customtkinter as ctk
import tkinter as tk

def labeledScale(master, text, default, from_, to, row, column, step, padx=0, pady=0, label_sticky='w', fg_color="transparent"):
    container = ctk.CTkFrame(master, fg_color=fg_color)
    container.grid(row=row, column=column, padx=padx, pady=pady)
    label_text = tk.StringVar(value=f"{text}: {default}")
    slider = ctk.CTkSlider(container, from_=from_, to=to, number_of_steps=step, command = lambda v: label_text.set(f"{text}: {int(v)}"))
    slider.grid(row=1, column=0)
    slider.set(default)
    label = ctk.CTkLabel(container, textvariable=label_text)
    label.grid(row=0, column=0, sticky=label_sticky, padx=5)
    return slider