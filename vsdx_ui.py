import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class HoverButton(tk.Canvas):
    def __init__(self, master, text, command=None, **kw):
        tk.Canvas.__init__(self, master, **kw)
        self.command = command
        self.text = text

        self.button_bg = "#3B82F6"
        self.button_hover = "#2563EB"
        self.text_color = "#FFFFFF"
        self.font = ("Segoe UI", 14, "bold")

        self.width = 180
        self.height = 50
        self.radius = 20  

        self.configure(width=self.width, height=self.height, highlightthickness=0, bg=master["bg"])
        self.draw_rounded_rectangle()
        
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=self.font, fill=self.text_color)

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def draw_rounded_rectangle(self):
        self.create_rounded_rectangle(0, 0, self.width, self.height, self.radius, fill=self.button_bg, outline="")

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        self.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, **kwargs)
        self.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, **kwargs)
        self.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, **kwargs)
        self.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, **kwargs)
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_hover(self, event):
        self.delete("all")
        self.button_bg = self.button_hover
        self.draw_rounded_rectangle()
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=self.font, fill=self.text_color)

    def on_leave(self, event):
        self.delete("all")
        self.button_bg = "#3B82F6"
        self.draw_rounded_rectangle()
        self.create_text(self.width / 2, self.height / 2, text=self.text, font=self.font, fill=self.text_color)

class VisioDiagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visio Diagram Manager")
        self.root.geometry("800x500")
        self.root.configure(bg='#FFFFFF')

        self.bg_color = '#FFFFFF'
        self.text_color = '#333333'
        self.desc_color = '#666666'

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=50)
        content_frame.columnconfigure(0, weight=1)

        welcome_label = tk.Label(content_frame, 
                                 text="Visio Diagram Manager", 
                                 font=('Segoe UI', 24, 'bold'),
                                 fg=self.text_color, 
                                 bg=self.bg_color)
        welcome_label.grid(row=0, column=0, pady=(0, 20), sticky="n")

        desc_text = ("Easily manage and analyze your Visio diagrams.\n"
                     "Upload your VSDX files, extract details, and visualize your workflows effortlessly.")
        desc_label = tk.Label(content_frame, 
                              text=desc_text, 
                              font=('Segoe UI', 14),
                              fg=self.desc_color, 
                              bg=self.bg_color, 
                              justify="center")
        desc_label.grid(row=1, column=0, pady=10, sticky="n")

        upload_btn = HoverButton(content_frame, text="Upload File", command=self.upload_file)
        upload_btn.grid(row=2, column=0, pady=30)

    def upload_file(self):
        print("File upload initiated")

def main():
    root = tk.Tk()
    app = VisioDiagramApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
