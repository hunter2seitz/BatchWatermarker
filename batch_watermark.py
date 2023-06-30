import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Batch Image Watermarking")
        self.geometry("500x300")

        # Center the window on the screen
        window_width = 500
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.directory = ""
        self.watermark_path = ""
        self.quality = 75

        self.directory_var = tk.StringVar()
        self.directory_var.set("No directory selected")

        self.watermark_var = tk.StringVar()
        self.watermark_var.set("No watermark selected")

        self.create_widgets()

    def create_widgets(self):
        # Directory Selection
        directory_frame = tk.Frame(self)
        directory_frame.pack(pady=10)

        directory_label = tk.Label(directory_frame, textvariable=self.directory_var)
        directory_label.pack(side=tk.LEFT)

        directory_button = tk.Button(directory_frame, text="Browse", command=self.select_directory)
        directory_button.pack(side=tk.LEFT, padx=10)

        # Watermark Selection
        watermark_frame = tk.Frame(self)
        watermark_frame.pack(pady=10)

        watermark_label = tk.Label(watermark_frame, textvariable=self.watermark_var)
        watermark_label.pack(side=tk.LEFT)

        watermark_button = tk.Button(watermark_frame, text="Browse", command=self.select_watermark)
        watermark_button.pack(side=tk.LEFT, padx=10)

        # Quality Selection
        quality_frame = tk.Frame(self)
        quality_frame.pack(pady=10)

        quality_label = tk.Label(quality_frame, text="Compression Quality (1-95):")
        quality_label.pack(side=tk.LEFT)

        quality_entry = tk.Entry(quality_frame, width=10)
        quality_entry.pack(side=tk.LEFT)
        quality_entry.insert(tk.END, str(self.quality))
        
        # Apply Watermark Button
        apply_button = tk.Button(self, text="Apply Watermark", command=lambda: self.apply_watermark(quality_entry.get()))
        apply_button.pack(pady=10)

        # Cancel Button
        cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        cancel_button.pack(pady=10)

    def select_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.directory_var.set(self.directory)

    def select_watermark(self):
        self.watermark_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if self.watermark_path:
            self.watermark_var.set(self.watermark_path)

    def apply_watermark(self, quality):
        if not self.directory:
            messagebox.showerror("Error", "Please select a directory!")
            return

        if not self.watermark_path:
            messagebox.showerror("Error", "Please select a watermark image!")
            return

        try:
            self.quality = int(quality)
            if self.quality < 1 or self.quality > 95:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid compression quality!")
            return

        watermark = Image.open(self.watermark_path).convert("RGBA")

        for filename in os.listdir(self.directory):
            if filename.lower().endswith(".jpg"):
                image_path = os.path.join(self.directory, filename)
                with Image.open(image_path).convert("RGB") as image:
                    watermarked_image = self.apply_watermark_to_image(image, watermark)
                    watermarked_image.save(image_path, "JPEG", quality=self.quality)

        messagebox.showinfo("Success", "Watermark applied to images!")

    def apply_watermark_to_image(self, image, watermark):
        image_width, image_height = image.size
        watermark_width, watermark_height = watermark.size

        # Calculate the position to center the watermark
        x = (image_width - watermark_width) // 2
        y = (image_height - watermark_height) // 2

        watermarked_image = image.copy()
        watermarked_image.paste(watermark, (x, y), mask=watermark)

        return watermarked_image

if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
