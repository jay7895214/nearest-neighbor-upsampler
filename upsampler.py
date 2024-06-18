import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime
from tkinterdnd2 import TkinterDnD, DND_FILES

class NearestNeighborUpsamplingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nearest Neighbor Upsampling App")

        self.images = []
        self.current_image_index = 0
        self.input_image = None
        self.output_image = None
        self.scale_factor = tk.DoubleVar(value=1.0)  # Default scale factor is 1.0
        self.width_var = tk.StringVar(value="")
        self.height_var = tk.StringVar(value="")
        self.bg_color = tk.StringVar(value="gray")
        self.always_on_top = False

        # Create GUI elements
        self.create_widgets()

        # Enable drag-and-drop functionality
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.on_drop)

    def create_widgets(self):
        # Frame for buttons and input fields
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Buttons and labels
        self.load_button = tk.Button(self.control_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=5, pady=10)

        self.prev_button = tk.Button(self.control_frame, text="<", command=self.prev_image)
        self.prev_button.grid(row=0, column=1, padx=5, pady=10)

        self.next_button = tk.Button(self.control_frame, text=">", command=self.next_image)
        self.next_button.grid(row=0, column=2, padx=5, pady=10)

        self.process_button = tk.Button(self.control_frame, text="Process Image", command=self.process_image)
        self.process_button.grid(row=0, column=3, padx=5, pady=10)

        self.save_button = tk.Button(self.control_frame, text="Save Image", command=self.save_image)
        self.save_button.grid(row=0, column=4, padx=5, pady=10)

        self.topmost_button = tk.Button(self.control_frame, text="Toggle Always on Top", command=self.toggle_always_on_top)
        self.topmost_button.grid(row=0, column=5, padx=5, pady=10)

        # Scale factor input
        self.scale_label = tk.Label(self.control_frame, text="Scale Factor:")
        self.scale_label.grid(row=1, column=0, padx=5, pady=10)

        self.scale_entry = tk.Entry(self.control_frame, textvariable=self.scale_factor)
        self.scale_entry.grid(row=1, column=1, padx=5, pady=10)
        self.scale_entry.bind("<Up>", self.increment_scale)
        self.scale_entry.bind("<Down>", self.decrement_scale)
        self.scale_entry.bind("<Return>", lambda event: self.update_dimensions_by_scale())

        # Width and height input fields (editable)
        self.width_label = tk.Label(self.control_frame, text="Width:")
        self.width_label.grid(row=1, column=2, padx=5, pady=10)

        self.width_entry = tk.Entry(self.control_frame, textvariable=self.width_var)
        self.width_entry.grid(row=1, column=3, padx=5, pady=10)
        self.width_entry.bind("<Return>", lambda event: self.update_dimensions_by_width())

        self.height_label = tk.Label(self.control_frame, text="Height:")
        self.height_label.grid(row=1, column=4, padx=5, pady=10)

        self.height_entry = tk.Entry(self.control_frame, textvariable=self.height_var)
        self.height_entry.grid(row=1, column=5, padx=5, pady=10)
        self.height_entry.bind("<Return>", lambda event: self.update_dimensions_by_height())

        # Canvas background color selection
        self.bg_color_label = tk.Label(self.control_frame, text="Canvas BG Color:")
        self.bg_color_label.grid(row=2, column=0, padx=5, pady=10)

        self.bg_color_combobox = ttk.Combobox(self.control_frame, textvariable=self.bg_color, values=["black", "gray", "white"])
        self.bg_color_combobox.grid(row=2, column=1, padx=5, pady=10)
        self.bg_color_combobox.bind("<<ComboboxSelected>>", self.change_bg_color)

        # Canvas to display the image
        self.canvas = tk.Canvas(self.root, bg=self.bg_color.get())
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

    def load_image(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_paths:
            self.images = [Image.open(file_path) for file_path in file_paths]
            self.current_image_index = 0
            self.display_image()

    def on_drop(self, event):
        file_paths = self.root.tk.splitlist(event.data)
        self.images = [Image.open(file_path) for file_path in file_paths]
        self.current_image_index = 0
        self.display_image()

    def display_image(self):
        if self.images:
            self.input_image = self.images[self.current_image_index]
            self.process_image()

    def prev_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.display_image()

    def next_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.display_image()

    def process_image(self, event=None):
        if self.input_image:
            try:
                scale_factor = float(self.scale_factor.get())
                new_width = int(self.input_image.width * scale_factor)
                new_height = int(self.input_image.height * scale_factor)
                self.output_image = self.input_image.resize((new_width, new_height), Image.NEAREST)

                output_photo = ImageTk.PhotoImage(self.output_image)
                self.canvas.config(width=self.output_image.width, height=self.output_image.height)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=output_photo)
                self.canvas.image = output_photo

                self.width_var.set(str(new_width))
                self.height_var.set(str(new_height))

            except ValueError:
                tk.messagebox.showerror("Error", "Invalid scale factor. Please enter a valid number.")

    def save_image(self):
        if self.images:
            try:
                scale_factor = self.scale_factor.get()
                time_stamp = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')

                for image in self.images:
                    original_filename = image.filename.split("/")[-1]
                    new_filename = f"{original_filename}_{scale_factor}_{time_stamp}.png"
                    original_path = image.filename
                    save_path = original_path.replace(original_filename, new_filename)

                    new_width = int(image.width * scale_factor)
                    new_height = int(image.height * scale_factor)
                    output_image = image.resize((new_width, new_height), Image.NEAREST)
                    output_image.save(save_path)

                tk.messagebox.showinfo("Success", "All images saved successfully.")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error saving images: {e}")

    def increment_scale(self, event):
        current_scale = self.scale_factor.get()
        self.scale_factor.set(current_scale + 0.5)
        self.process_image()

    def decrement_scale(self, event):
        current_scale = self.scale_factor.get()
        self.scale_factor.set(max(0.5, current_scale - 0.5))
        self.process_image()

    def change_bg_color(self, event):
        self.canvas.config(bg=self.bg_color.get())

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        if self.always_on_top:
            self.topmost_button.config(text="Disable Always on Top")
        else:
            self.topmost_button.config(text="Enable Always on Top")

    def update_dimensions_by_scale(self):
        if self.input_image:
            try:
                scale_factor = float(self.scale_factor.get())
                new_width = int(self.input_image.width * scale_factor)
                new_height = int(self.input_image.height * scale_factor)
                self.width_var.set(str(new_width))
                self.height_var.set(str(new_height))
                self.process_image()
            except ValueError:
                pass

    def update_dimensions_by_width(self, event=None):
        if self.input_image:
            try:
                new_width = float(self.width_var.get())
                if new_width > 0:
                    scale_factor = new_width / self.input_image.width
                    new_height = int(self.input_image.height * scale_factor)
                    self.scale_factor.set(scale_factor)
                    self.height_var.set(str(new_height))
                    self.process_image()
            except ValueError:
                pass

    def update_dimensions_by_height(self, event=None):
        if self.input_image:
            try:
                new_height = float(self.height_var.get())
                if new_height > 0:
                    scale_factor = new_height / self.input_image.height
                    new_width = int(self.input_image.width * scale_factor)
                    self.scale_factor.set(scale_factor)
                    self.width_var.set(str(new_width))
                    self.process_image()
            except ValueError:
                pass

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = NearestNeighborUpsamplingApp(root)
    root.mainloop()