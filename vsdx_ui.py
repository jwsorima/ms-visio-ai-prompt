import customtkinter as ctk
from tkinter import filedialog
import time

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class VisioChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visio Diagram")
        self.geometry("1000x700")
        self.configure(bg="#ffffff")
        
        self.header_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=80)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="📊",
            font=("Segoe UI", 24)
        )
        self.logo_label.pack(side="left", padx=(20, 5))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Visio Diagram",
            font=("Segoe UI", 24, "bold"),
            text_color="#1a1a1a"
        )
        self.title_label.pack(side="left")

        self.header_upload_btn = ctk.CTkButton(
            self.header_frame,
            text="Upload New File",
            font=("Segoe UI", 13, "bold"),
            command=self.upload_file,
            width=140,
            height=35,
            corner_radius=8,
            fg_color="#000000",
            hover_color="#333333"
        )
        
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.welcome_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")
        self.welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.welcome_title = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome to Visio Diagram",
            font=("Segoe UI", 28, "bold"),
            text_color="#1a1a1a"
        )
        self.welcome_title.pack(pady=(100, 20))

        self.welcome_text = ctk.CTkLabel(
            self.welcome_frame,
            text="Visio Diagram is here to assist you with your diagram analysis needs.\n"
                 "Whether you need to analyze, extract, or understand your diagrams,\n"
                 "we're ready to help make your diagram analysis effortless and efficient.",
            font=("Segoe UI", 14),
            text_color="#666666"
        )
        self.welcome_text.pack(pady=(0, 40))

        self.upload_btn = ctk.CTkButton(
            self.welcome_frame,
            text="Upload Your File",
            font=("Segoe UI", 14, "bold"),
            command=self.upload_file,
            width=200,
            height=40,
            corner_radius=8,
            fg_color="#000000",
            hover_color="#333333"
        )
        self.upload_btn.pack(pady=20)

        self.chat_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")
        
        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_frame,
            fg_color="#ffffff",
            corner_radius=0,
            height=520
        )
        self.messages_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.separator = ctk.CTkFrame(
            self.chat_frame,
            height=1,
            fg_color="#e0e0e0"
        )

    def create_message_bubble(self, sender, message):
        msg_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color="#ffffff",
            corner_radius=0
        )
        msg_frame.pack(fill="x", pady=8, padx=10)

        if sender == "system":
            avatar_label = ctk.CTkLabel(
                msg_frame,
                text="🤖",
                font=("Segoe UI", 20),
                width=40
            )
            bubble_color = "#f0f4f9"
            align = "left"
        else:
            avatar_label = ctk.CTkLabel(
                msg_frame,
                text="👤",
                font=("Segoe UI", 20),
                width=40
            )
            bubble_color = "#e9ecef"
            align = "right"
        
        message_bubble = ctk.CTkFrame(
            msg_frame,
            corner_radius=15,
            fg_color=bubble_color,
            border_width=1,
            border_color="#e0e0e0" if sender == "system" else "#d1d1d1"
        )
        
        message_text = ctk.CTkLabel(
            message_bubble,
            text=message,
            font=("Segoe UI", 13),
            text_color="#1a1a1a",
            wraplength=600,
            justify="left"
        )
        message_text.pack(padx=20, pady=15)

        if align == "left":
            avatar_label.pack(side="left", padx=(5, 10))
            message_bubble.pack(side="left", fill="x", expand=True, padx=(0, 80))
        else:
            avatar_label.pack(side="right", padx=(10, 5))
            message_bubble.pack(side="right", fill="x", expand=True, padx=(80, 0))

    def add_file_separator(self):
        separator = ctk.CTkFrame(
            self.messages_frame,
            height=1,
            fg_color="#e0e0e0"
        )
        separator.pack(fill="x", pady=20, padx=10)

    def smooth_transition(self):
        if self.welcome_frame.winfo_viewable():
            self.welcome_frame.pack_forget()
            self.chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.header_upload_btn.pack(side="right", padx=20)
        self.update()

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a Visio (.vsdx) File",
            filetypes=[("Visio Files", "*.vsdx")]
        )

        if file_path:
            self.smooth_transition()
            file_name = file_path.split("/")[-1]
            
            if not self.welcome_frame.winfo_viewable():
                self.add_file_separator()
            
            messages = [
                ("user", f"Uploaded: {file_name}"),
                ("system", f"Got it! I'll start analyzing this Visio diagram for you. Give me a moment to process its contents..."),
                ("system", "I've completed my initial analysis. This appears to be a detailed Visio file with multiple components. Let me break down what I found:"),
                ("system", "Key findings from the diagram:\n\n"
                          "• Structure: I've identified a network of interconnected elements and their relationships\n"
                          "• Components: The diagram contains multiple shapes and connectors forming a workflow\n"
                          "• Relationships: There are clear connections showing how components interact\n"
                          "• Properties: I've extracted metadata that provides additional context\n\n"
                          "Would you like me to elaborate on any of these aspects?")
            ]

            for sender, message in messages:
                self.create_message_bubble(sender, message)
                self.update()
                time.sleep(0.8)
                self.messages_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = VisioChatbotApp()
    app.mainloop()