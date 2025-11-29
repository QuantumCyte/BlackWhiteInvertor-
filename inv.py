import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
import os

def browse_file():
    try:
        filepath = filedialog.askopenfilename(title="select a file",
                    filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), 
                               ("Python Files", "*.py"), ("Png files", "*.png")])
        if filepath:
            entry_var.set(filepath)
            status_var.set(f"Selected: {os.path.basename(filepath)}")
            load_preview(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def choose_output_folder():
    try:
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            output_dir_var.set(folder)
            status_var.set(f"Output folder set: {folder}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def convert_file():
    filepath = entry_var.get()
    output_dir = output_dir_var.get()
    file = os.path.basename(filepath)

    if not filepath:
        messagebox.showwarning("No File", "Please select a file first.")
        return

    if not output_dir:
        messagebox.showwarning("No Output Folder", "Please choose a save location.")
        return

    try:
        status_var.set(f"Converting {file}…")
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

        _, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        biggest_contour = max(contours, key=cv2.contourArea)

        mask = np.zeros_like(img)
        cv2.drawContours(mask, [biggest_contour], -1, 255, thickness=-1)

        inverted = cv2.bitwise_not(img)
        result = np.where(mask == 255, inverted, img)

        # Save to selected output folder
        finalResultFile = os.path.join(output_dir, f'inverted_{file}')
        cv2.imwrite(finalResultFile, result)

        status_var.set(f"Saved: {finalResultFile}")
        messagebox.showinfo("Success", f"File converted and saved to:\n{finalResultFile}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during conversion: {e}")


root = tk.Tk()
root.title("Image Inverter")
root.geometry('740x460+50+50')
root.resizable(False, False)

entry_var = tk.StringVar()
output_dir_var = tk.StringVar()
status_var = tk.StringVar(value="Ready")

# Try to import Pillow for nicer preview handling; if unavailable we'll skip thumbnail.
have_pillow = False
try:
    from PIL import Image, ImageTk
    have_pillow = True
except Exception:
    have_pillow = False


# Top frame for controls
top = ttk.Frame(root, padding=10)
top.pack(fill=tk.X)

ttk.Label(top, text="Input Image:", width=12).grid(row=0, column=0, sticky=tk.W)
entry = ttk.Entry(top, textvariable=entry_var, width=56)
entry.grid(row=0, column=1, padx=(0, 8))

browse_btn = ttk.Button(top, text="Browse…", command=browse_file)
browse_btn.grid(row=0, column=2)

ttk.Label(top, text="Output Folder:", width=12).grid(row=1, column=0, sticky=tk.W, pady=(8, 0))
output_entry = ttk.Entry(top, textvariable=output_dir_var, width=56)
output_entry.grid(row=1, column=1, padx=(0, 8), pady=(8, 0))

output_btn = ttk.Button(top, text="Choose…", command=choose_output_folder)
output_btn.grid(row=1, column=2, pady=(8, 0))

# Middle: preview + controls
middle = ttk.Frame(root, padding=10)
middle.pack(fill=tk.BOTH, expand=True)

preview_frame = ttk.LabelFrame(middle, text="Preview", width=420, height=320)
preview_frame.grid(row=0, column=0, padx=(0, 10), sticky="n")

preview_label = ttk.Label(preview_frame)
preview_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

control_frame = ttk.Frame(middle)
control_frame.grid(row=0, column=1, sticky="n")

convert_btn = ttk.Button(control_frame, text="Convert", command=convert_file)
convert_btn.grid(row=0, column=0, pady=(8, 4), sticky="ew")

quit_btn = ttk.Button(control_frame, text="Quit", command=root.destroy)
quit_btn.grid(row=1, column=0, pady=(4, 4), sticky="ew")

# Bottom status bar
status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


def load_preview(path):
    try:
        if not have_pillow:
            status_var.set("Pillow not installed — install pillow to enable preview")
            return
        img = Image.open(path)
        img.thumbnail((400, 300))
        photo = ImageTk.PhotoImage(img)
        preview_label.image = photo
        preview_label.configure(image=photo)
    except Exception as e:
        status_var.set(f"Preview error: {e}")


root.mainloop()