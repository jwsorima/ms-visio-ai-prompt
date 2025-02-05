import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class VisioChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visio AI Assistant")
        self.geometry("900x600")
        self.configure(bg="#F4F4F4")

        self.chat_frame = ctk.CTkFrame(self, corner_radius=15)
        self.chat_frame.grid(row=0, column=0, padx=40, pady=20, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.chat_frame, text="Visio AI Assistant 🤖",
            font=("Segoe UI", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.chat_output = ctk.CTkTextbox(self, height=400, width=800, font=("Segoe UI", 14), wrap="word")
        self.chat_output.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.chat_output.insert("1.0", "🤖 Hello! Upload a Visio file, and I will analyze it for you.\n\n")
        self.chat_output.configure(state="disabled")

        self.upload_btn = ctk.CTkButton(
            self.chat_frame, text="Upload Visio File 📂",
            font=("Segoe UI", 16, "bold"),
            command=self.upload_file
        )
        self.upload_btn.grid(row=2, column=0, pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a Visio (.vsdx) File", filetypes=[("Visio Files", "*.vsdx")]
        )

        if file_path:
            file_name = file_path.split("/")[-1]
            self.chat_output.configure(state="normal")
            self.chat_output.insert("end", f"📂 User uploaded: {file_name}\n")
            self.chat_output.insert("end", f"🤖 AI is analyzing the diagram...\n\n")
            self.chat_output.insert("end", "🤖 (Backend processing will go here...)\n\n")
            self.chat_output.see("end")
            self.chat_output.configure(state="disabled")

if __name__ == "__main__":
    app = VisioChatbotApp()
    app.mainloop()


#test12345