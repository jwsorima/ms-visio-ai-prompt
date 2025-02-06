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
    
    # Enhanced header with subtle shadow
    self.header_frame = ctk.CTkFrame(
      self,
      fg_color="#ffffff",
      corner_radius=0,
      height=80,
      border_width=1,
      border_color="#e8e8e8"
    )
    self.header_frame.pack(fill="x", pady=(0, 20))
    
    # Logo and title container
    self.brand_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
    self.brand_frame.pack(side="left", padx=30, pady=15)
    
    self.logo_label = ctk.CTkLabel(
      self.brand_frame,
      text="📊",
      font=("Segoe UI", 28)
    )
    self.logo_label.pack(side="left", padx=(0, 10))
    
    self.title_label = ctk.CTkLabel(
      self.brand_frame,
      text="Visio Diagram",
      font=("Segoe UI Semibold", 26),
      text_color="#1a1a1a"
    )
    self.title_label.pack(side="left")

    # Refined upload button in header
    self.header_upload_btn = ctk.CTkButton(
      self.header_frame,
      text="Upload New File",
      font=("Segoe UI", 13, "bold"),
      command=self.upload_file,
      width=140,
      height=38,
      corner_radius=8,
      fg_color="#2d3436",
      hover_color="#1e2224",
      border_width=1,
      border_color="#1e2224"
    )
    
    # Main content area with subtle background
    self.main_frame = ctk.CTkFrame(self, fg_color="#f8f9fa", corner_radius=12)
    self.main_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    # Welcome screen with improved layout
    self.welcome_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
    self.welcome_frame.pack(fill="both", expand=True, padx=40, pady=40)

    self.welcome_title = ctk.CTkLabel(
      self.welcome_frame,
      text="Welcome to Visio Diagram",
      font=("Segoe UI Semibold", 32),
      text_color="#1a1a1a"
    )
    self.welcome_title.pack(pady=(60, 25))

    self.welcome_text = ctk.CTkLabel(
      self.welcome_frame,
      text="Your intelligent assistant for diagram analysis.\nUpload your Visio files and let us help you understand them better.",
      font=("Segoe UI", 15),
      text_color="#666666"
    )
    self.welcome_text.pack(pady=(0, 50))

    # Prominent upload button with enhanced styling
    self.upload_btn = ctk.CTkButton(
      self.welcome_frame,
      text="Upload Your File",
      font=("Segoe UI", 15, "bold"),
      command=self.upload_file,
      width=220,
      height=48,
      corner_radius=10,
      fg_color="#2d3436",
      hover_color="#1e2224",
      border_width=1,
      border_color="#1e2224"
    )
    self.upload_btn.pack()

    # Refined chat interface
    self.chat_frame = ctk.CTkFrame(
      self.main_frame,
      fg_color="#ffffff",
      corner_radius=12,
      border_width=1,
      border_color="#e8e8e8"
    )
    
    self.messages_frame = ctk.CTkScrollableFrame(
      self.chat_frame,
      fg_color="#ffffff",
      corner_radius=12,
      height=520,
      scrollbar_button_color="#2d3436",
      scrollbar_button_hover_color="#1e2224"
    )
    self.messages_frame.pack(fill="both", expand=True, padx=2, pady=2)

  def create_message_bubble(self, sender, message):
    msg_frame = ctk.CTkFrame(
      self.messages_frame,
      fg_color="transparent",
      corner_radius=0
    )
    msg_frame.pack(fill="x", pady=8, padx=15)

    if sender == "system":
      # Bot styling
      avatar_label = ctk.CTkLabel(
        msg_frame,
        text="🤖",
        font=("Segoe UI", 20),
        width=35
      )
      bubble_color = "#edf6ff"  # Light blue tint for bot messages
      border_color = "#d1e6ff"
      text_color = "#0a2540"
      align = "left"
    else:
      # User styling
      avatar_label = ctk.CTkLabel(
        msg_frame,
        text="👤",
        font=("Segoe UI", 20),
        width=35
      )
      bubble_color = "#f0f4f9"  # Light gray for user messages
      border_color = "#e2e8f0"
      text_color = "#2d3748"
      align = "right"
    
    message_bubble = ctk.CTkFrame(
      msg_frame,
      corner_radius=12,
      fg_color=bubble_color,
      border_width=1,
      border_color=border_color
    )
    
    message_text = ctk.CTkLabel(
      message_bubble,
      text=message,
      font=("Segoe UI", 13),
      text_color=text_color,
      wraplength=620,
      justify="left"
    )
    message_text.pack(padx=16, pady=12)

    if align == "left":
      avatar_label.pack(side="left", padx=(0, 8))
      message_bubble.pack(side="left", fill="x", expand=True, padx=(0, 80))
    else:
      avatar_label.pack(side="right", padx=(8, 0))
      message_bubble.pack(side="right", fill="x", expand=True, padx=(80, 0))

  def add_file_separator(self):
    separator = ctk.CTkFrame(
      self.messages_frame,
      height=1,
      fg_color="#e8e8e8"
    )
    separator.pack(fill="x", pady=15, padx=15)

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
        ("system", "I've completed my initial analysis. Let me break down what I found:"),
        ("system", "Key findings from the diagram:\n"
                  "• Structure: Network of interconnected elements and their relationships\n"
                  "• Components: Multiple shapes and connectors forming a workflow\n"
                  "• Relationships: Clear connections between components\n"
                  "• Properties: Additional metadata and document context\n\n"
                  "Would you like me to elaborate on any specific aspect?")
      ]

      for sender, message in messages:
        self.create_message_bubble(sender, message)
        self.update()
        time.sleep(0.8)
        self.messages_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
  app = VisioChatbotApp()
  app.mainloop()