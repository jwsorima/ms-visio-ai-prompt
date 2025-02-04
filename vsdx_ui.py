import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from vsdx import VisioFile
import os

# -------------------------------
# Backend function to extract details from a VSDX file
# -------------------------------
def extract_vsdx_details(file_path):
    with VisioFile(file_path) as vis:
        details = "Extracted Visio Diagram Data:\n"
        for page in vis.pages:
            details += f"\nPage: {page.name}\n"
            for shape in page.child_shapes:
                shape_id = shape.ID
                shape_text = shape.text.strip() if shape.text else ""
                shape_type = shape.universal_name if shape.universal_name else "Unknown"
                if shape_text.endswith("?"):
                    shape_type = "Decision"
                shape_x = shape.x
                shape_y = shape.y
                shape_width = shape.width
                shape_height = shape.height
                details += (
                    f"Shape ID {shape_id}:\n"
                    f"   • Is Connector: {True if shape.end_arrow and shape.end_arrow != 0 else False}\n"
                    f"   • Text: '{shape_text}'\n"
                    f"   • Type: {shape_type}\n"
                    f"   • Position: (X: {shape_x}, Y: {shape_y})\n"
                    f"   • Dimensions: (Width: {shape_width}, Height: {shape_height})\n"
                )
                if shape.connects:
                    details += "\n"
                    for conn in shape.connects:
                        connected_shape = conn.shape
                        from_shape = conn.from_id
                        from_cell = conn.from_rel
                        if connected_shape and connected_shape.ID == shape.ID:
                            continue
                        if from_shape and connected_shape:
                            if from_cell == 'BeginX':
                                details += f"   • From '{connected_shape.text.strip()}' to this arrow\n"
                            elif from_cell == 'EndX':
                                details += f"   • This arrow to '{connected_shape.text.strip()}'\n"
        return details

# -------------------------------
# Tkinter UI Application
# -------------------------------
class VSDXAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visio Diagram Analyzer")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Create a scrolled text widget for the conversation display
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Arial", 11))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure text tags for styling messages
        self.chat_display.tag_config("user", background="#d1e7dd", foreground="black", spacing1=5, spacing3=5)
        self.chat_display.tag_config("bot", background="#f8d7da", foreground="black", spacing1=5, spacing3=5)

        # Create a frame for the buttons at the bottom
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, fill=tk.X)

        # Upload File button
        self.upload_btn = tk.Button(button_frame, text="Upload VSDX File", command=self.upload_file, bg="#0d6efd", fg="white", padx=10, pady=5)
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        # Optionally, a Clear Chat button
        self.clear_btn = tk.Button(button_frame, text="Clear Chat", command=self.clear_chat, bg="#dc3545", fg="white", padx=10, pady=5)
        self.clear_btn.pack(side=tk.RIGHT, padx=5)

    def append_message(self, sender, message):
        """
        Append a message to the chat display.
        """
        self.chat_display.configure(state='normal')
        # Insert sender label (capitalize first letter)
        self.chat_display.insert(tk.END, f"{sender.capitalize()}:\n", sender)
        self.chat_display.insert(tk.END, message + "\n\n", sender)
        self.chat_display.configure(state='disabled')
        # Auto-scroll to the bottom
        self.chat_display.see(tk.END)

    def upload_file(self):
        """
        Open a file dialog to select a VSDX file, process it, and display the results.
        """
        file_path = filedialog.askopenfilename(
            title="Select a VSDX File",
            filetypes=[("Visio Files", "*.vsdx")]
        )
        if file_path:
            file_name = os.path.basename(file_path)
            self.append_message("user", f"Uploaded file: {file_name}")

            try:
                # Process the file and extract details
                details = extract_vsdx_details(file_path)
            except Exception as e:
                details = f"Error processing file: {str(e)}"
                messagebox.showerror("Processing Error", details)

            self.append_message("bot", details)

    def clear_chat(self):
        """
        Clear the chat display.
        """
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')

# -------------------------------
# Run the Application
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VSDXAnalyzerApp(root)
    root.mainloop()