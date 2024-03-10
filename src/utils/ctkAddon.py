from typing import Callable, Sequence
import customtkinter as ctk
import tkinter as tk

def labeledScale(master, text: str, value: float, from_: int, to: int, row: int, column: int, step: int, 
    padx: tuple[float, float]=(0, 0), pady: tuple[float, float]=(0, 0), label_sticky: str='w', 
    fg_color: str="transparent", command: Callable | None=None
) -> ctk.CTkSlider:

    container = ctk.CTkFrame(master, fg_color=fg_color)
    container.grid(row=row, column=column, padx=padx, pady=pady)

    label_text = tk.StringVar(value=f"{text}: {value}")

    slider = ctk.CTkSlider(container, from_=from_, to=to, number_of_steps=step, 
        command=lambda v: __fxnExecuter(label_text.set(f"{text}: {int(v)}"), command)
    ) # test pending for command
    slider.grid(row=1, column=0)
    slider.set(value)

    label = ctk.CTkLabel(container, textvariable=label_text)
    label.grid(row=0, column=0, sticky=label_sticky, padx=5)

    return slider

def labeledRadioButton(master, label_text: str, row: int, column: int, options: Sequence[str], value: int=0, 
    padx: tuple[float, float]=(0, 0), pady: tuple[float, float]=(0, 0), label_sticky: str='w', 
    fg_color: str="transparent", label_font_size: int=15, option_font_size: int=12, indent: float=15, 
    command: Callable | None=None
) -> tk.IntVar:

    container = ctk.CTkFrame(master, fg_color=fg_color)
    container.grid(row=row, column=column, padx=padx, pady=pady)

    label = ctk.CTkLabel(container, text=label_text, font=ctk.CTkFont(size=label_font_size))
    label.grid(row=0, column=0, sticky=label_sticky, padx=5)

    select_var = tk.IntVar(value=value)
    for i, v in enumerate(options):
        radio_button = ctk.CTkRadioButton(container, text=v, variable=select_var, value=i, 
            radiobutton_height=15, radiobutton_width=15, border_width_checked=11, border_width_unchecked=1, 
            corner_radius=1, font=ctk.CTkFont(size=option_font_size), command=command
        )
        radio_button.grid(row=i + 1, column=0, padx=(indent, 0), pady=(5, 0))

    return select_var

def __fxnExecuter(*args: Callable | None) -> None:
    for i in args:
        if i is not None:
            i()