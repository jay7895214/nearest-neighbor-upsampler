import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime
from tkinterdnd2 import TkinterDnD, DND_FILES

class NearestNeighborUpsamplingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nearest Neighbor Upsampling App")

        self.input_image = None
        self.output_image = None
        self.scale_factor = tk.DoubleVar(value=1.0)  # Default scale factor is 1.0
        self.width_var = tk.StringVar(value="")
        self.height_var = tk.StringVar(value="")
        self.bg_color = tk.StringVar(value="gray")
        self.always_on_top = False

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons and input fields
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Buttons and labels
        self.load_button = tk.Button(self.control_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=5, pady=10)

        self.process_button = tk.Button(self.control_frame, text="Process Image", command=self.process_image)
        self.process_button.grid(row=0, column=1, padx=5, pady=10)

        self.save_button = tk.Button(self.control_frame, text="Save Image", command=self.save_image)
        self.save_button.grid(row=0, column=2, padx=5, pady=10)

        self.topmost_button = tk.Button(self.control_frame, text="Toggle Always on Top", command=self.toggle_always_on_top)
        self.topmost_button.grid(row=0, column=3, padx=5, pady=10)

        # Scale factor input
        self.scale_label = tk.Label(self.control_frame, text="Scale Factor:")
        self.scale_label.grid(row=1, column=0, padx=5, pady=10)

        self.scale_entry = tk.Entry(self.control_frame, textvariable=self.scale_factor)
        self.scale_entry.grid(row=1, column=1, padx=5, pady=10)
        self.scale_entry.bind("<Up>", self.increment_scale)
        self.scale_entry.bind("<Down>", self.decrement_scale)
        self.scale_entry.bind("<Return>", lambda event: self.process_image())

        # Width and height input fields (editable)
        self.width_label = tk.Label(self.control_frame, text="Width:")
        self.width_label.grid(row=1, column=2, padx=5, pady=10)

        self.width_entry = tk.Entry(self.control_frame, textvariable=self.width_var)
        self.width_entry.grid(row=1, column=3, padx=5, pady=10)
        self.width_var.trace_add('write', lambda *args: self.update_dimensions_by_width())

        self.height_label = tk.Label(self.control_frame, text="Height:")
        self.height_label.grid(row=1, column=4, padx=5, pady=10)

        self.height_entry = tk.Entry(self.control_frame, textvariable=self.height_var)
        self.height_entry.grid(row=1, column=5, padx=5, pady=10)
        self.height_var.trace_add('write', lambda *args: self.update_dimensions_by_height())

        # Canvas background color selection
        self.bg_color_label = tk.Label(self.control_frame, text="Canvas BG Color:")
        self.bg_color_label.grid(row=2, column=0, padx=5, pady=10)

        self.bg_color_combobox = ttk.Combobox(self.control_frame, textvariable=self.bg_color, values=["black", "gray", "white"])
        self.bg_color_combobox.grid(row=2, column=1, padx=5, pady=10)
        self.bg_color_combobox.bind("<<ComboboxSelected>>", self.change_bg_color)

        # Canvas to display the image
        self.canvas = tk.Canvas(self.root, bg=self.bg_color.get())
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

        # Enable drag-and-drop functionality
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.on_drop)

    def load_image(self):
        # Open file dialog to select input image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            # Open input image and display it on the canvas
            self.input_image = Image.open(file_path)
            photo = ImageTk.PhotoImage(self.input_image)
            self.canvas.config(width=self.input_image.width, height=self.input_image.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

            # Update width and height input fields
            self.width_var.set(str(self.input_image.width))
            self.height_var.set(str(self.input_image.height))

    def process_image(self):
        if self.input_image:
            try:
                # Get user input scale factor
                scale_factor = float(self.scale_factor.get())

                # Perform nearest neighbor upsampling
                new_width = int(self.input_image.width * scale_factor)
                new_height = int(self.input_image.height * scale_factor)
                self.output_image = self.input_image.resize((new_width, new_height), Image.NEAREST)

                # Display output image on the canvas
                output_photo = ImageTk.PhotoImage(self.output_image)
                self.canvas.config(width=self.output_image.width, height=self.output_image.height)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=output_photo)
                self.canvas.image = output_photo

                # Update width and height input fields
                self.width_var.set(str(new_width))
                self.height_var.set(str(new_height))

            except ValueError:
                tk.messagebox.showerror("Error", "Invalid scale factor. Please enter a valid number.")

    def save_image(self):
        if self.output_image:
            try:
                # Get original image filename (without path)
                original_filename = self.input_image.filename.split("/")[-1]

                # Get scale factor value
                scale_factor = self.scale_factor.get()

                # Generate timestamp
                time_stamp = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')

                # Construct new filename
                new_filename = f"{original_filename}_{scale_factor}_{time_stamp}.png"

                # Get original image path
                original_path = self.input_image.filename

                # Save the upsampled image
                save_path = original_path.replace(original_filename, new_filename)
                self.output_image.save(save_path)

                tk.messagebox.showinfo("Success", f"Image saved as {new_filename}")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error saving image: {e}")

    def increment_scale(self, event):
        current_scale = self.scale_factor.get()
        self.scale_factor.set(current_scale + 0.5)

    def decrement_scale(self, event):
        current_scale = self.scale_factor.get()
        self.scale_factor.set(max(0.5, current_scale - 0.5))

    def change_bg_color(self, event):
        self.canvas.config(bg=self.bg_color.get())

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        if self.always_on_top:
            self.topmost_button.config(text="Disable Always on Top")
        else:
            self.topmost_button.config(text="Enable Always on Top")

    def on_drop(self, event):
        # Get the dropped file path
        file_paths = event.widget.tk.splitlist(event.data)

        if file_paths:
            # Load the first dropped image file
            self.input_image = Image.open(file_paths[0])
            photo = ImageTk.PhotoImage(self.input_image)
            self.canvas.config(width=self.input_image.width, height=self.input_image.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

            # Update width and height input fields
            self.width_var.set(str(self.input_image.width))
            self.height_var.set(str(self.input_image.height))

    def update_dimensions_by_scale(self):
        if self.input_image:
            try:
                scale_factor = float(self.scale_factor.get())
                new_width = int(self.input_image.width * scale_factor)
                new_height = int(self.input_image.height * scale_factor)
                self.width_var.set(str(new_width))
                self.height_var.set(str(new_height))
            except ValueError:
                pass

    def update_dimensions_by_width(self, *args):
        if self.input_image:
            try:
                new_width = float(self.width_var.get())
                if new_width > 0:
                    scale_factor = new_width / self.input_image.width
                    new_height = int(self.input_image.height * scale_factor)
                    self.scale_factor.set(scale_factor)
                    self.height_var.set(str(new_height))
            except ValueError:
                pass

    def update_dimensions_by_height(self, *args):
        if self.input_image:
            try:
                new_height = float(self.height_var.get())
                if new_height > 0:
                    scale_factor = new_height / self.input_image.height
                    new_width = int(self.input_image.width * scale_factor)
                    self.scale_factor.set(scale_factor)
                    self.width_var.set(str(new_width))
            except ValueError:
                pass

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = NearestNeighborUpsamplingApp(root)
    root.mainloop()