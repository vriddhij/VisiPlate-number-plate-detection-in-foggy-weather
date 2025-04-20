# gui_interface.py
import tkinter as tk
import subprocess

def run_and_close(script):
    root.destroy()
    subprocess.run(["python", script])

root = tk.Tk()
root.title("VISIPLATE")
root.geometry("600x300")
root.configure(bg="white")

title = tk.Label(root, text="Number plate recognition", font=("Georgia", 16), bg="white")
title.pack(pady=(20, 5))

subtitle = tk.Label(root, text="VISIPLATE", font=("Arial", 28, "bold"), fg="#9b59b6", bg="white")
subtitle.pack(pady=(0, 40))

button_frame = tk.Frame(root, bg="white")
button_frame.pack()

style = {"font": ("Helvetica", 12), "bg": "black", "fg": "white", "width": 20, "height": 2}

btn1 = tk.Button(button_frame, text="Capture in Real time",
                 command=lambda: run_and_close("realtime_defog.py"), **style)
btn1.grid(row=0, column=0, padx=30)

btn2 = tk.Button(button_frame, text="Capture",
                 command=lambda: run_and_close("msbdn2.py"), **style)
btn2.grid(row=0, column=1, padx=30)

root.mainloop()
