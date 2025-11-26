import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import os

def browse_file():
    try:
        filepath = filedialog.askopenfilename(title="select a file",
                    filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), 
                               ("Python Files", "*.py"), ("Png files", "*.png")])
        if filepath:
            messagebox.showinfo("Selected File", f"You selected: {filepath}")
            entry_var.set(filepath)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def choose_output_folder():
    try:
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            output_dir_var.set(folder)
            messagebox.showinfo("Output Folder", f"Files will be saved to:\n{folder}")
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
        messagebox.showinfo("Conversion", f"Converting file: {file}")
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

        messagebox.showinfo("Success", f"File converted and saved to:\n{finalResultFile}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during conversion: {e}")


root = tk.Tk()
root.title("RGB Colour Changer")
root.geometry('600x400+50+50')

entry_var = tk.StringVar()
output_dir_var = tk.StringVar() 

entry = tk.Entry(root, textvariable=entry_var, width=50)
entry.pack(side=tk.LEFT, padx=5, pady=10)

browse_btn = tk.Button(root, text="Browse", command=browse_file)
browse_btn.pack(side=tk.LEFT, padx=5)

# NEW BUTTON (placed in the middle)
output_btn = tk.Button(root, text="Save To...", command=choose_output_folder)
output_btn.pack(side=tk.LEFT, padx=5)

convert_btn = tk.Button(root, text="Convert", command=convert_file)
convert_btn.pack(side=tk.RIGHT, padx=5)

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()
