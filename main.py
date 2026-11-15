import tkinter as tk
from tkinter import ttk
root= tk.Tk()

root.title("Virtual Oscilloscope")
root.geometry("1200x760")
root.configure(bg ="#1E1E1E")





generator_title = tk.Label(root,
                            text = "Signal generator ",
                            font = ("Arial",18),
                            fg="yellow",
                            bg= "#1E1E1E"
                            )
generator_title.pack(pady=100)





title = tk.Label(root, 
                text = "Virtual Oscilloscope",
                font= ("Arial",24,"bold"),
                fg="white",
                bg="#1E1E1E"
                )
title.pack(pady=20)

frequency_label = tk.Label(
    root,
    text ="Frequency (Hz)",
    fg="white",
    bg = "#1E1E1E"
)

frequency_label.pack (pady=5)

frequency_entry = tk.Entry(root,width = 20)
frequency_entry.pack()
frequency_entry.insert(0,"50")

amplitude_label = tk.Label(
    root,
    text ="Amplitude (V)",
    fg ="red",
    background= "#1E1E1E"
)
amplitude_label.pack (pady= 20)
amplitude_entry = tk.Entry(root, width= 20)
amplitude_entry.pack()
amplitude_entry.insert(0,"5")

wave_label= tk.Label(
    root,
    text = "Wave type",
    fg = "white",
    bg = "#1E1E1E"
)

wave_label.pack(pady=10)

wave_box = ttk.Combobox(
    root,
    values = ["Sine","Square", "Triangle"],
    state = "readonly",
    width= 20
)
wave_box.pack()
wave_box.current(0)




def generate_signal():
    frequency = float(frequency_entry.get())
    amplitude = float(amplitude_entry.get())
    wave_type = wave_box.get()
    print("Frequency:", frequency)
    print("Amplitude:", amplitude)
    print("Wave Type:", wave_type)


generate_button = tk.Button(
    root,
    text= "Generate signal",
    font=("Arial",12),
    bg="green",
    fg = "white",
    command=generate_signal
)
generate_button.pack(pady=20)


root.mainloop()