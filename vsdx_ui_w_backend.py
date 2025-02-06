import customtkinter as ctk
from tkinter import filedialog
import time
from test_ollama import prompt_ai_with_vsdx_data
import json
import threading

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class VisioChatbotApp(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.title("Visio Diagram AI")
    self.geometry("1000x700")
    self.configure(bg="#ffffff")

    self.header_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=80)
    self.header_frame.pack(fill="x", padx=20, pady=(20, 0))

    self.logo_label = ctk.CTkLabel(self.header_frame, text="📊", font=("Segoe UI", 24))
    self.logo_label.pack(side="left", padx=(20, 5))

    self.title_label = ctk.CTkLabel(
      self.header_frame, text="Visio Diagram AI", font=("Segoe UI", 24, "bold"), text_color="#1a1a1a"
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
      hover_color="#333333",
    )
    self.header_upload_btn.pack(side="right", padx=20)

    self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
    self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    self.chat_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")
    self.chat_frame.pack(fill="both", expand=True, padx=20, pady=20)

    self.messages_frame = ctk.CTkScrollableFrame(self.chat_frame, fg_color="#ffffff", corner_radius=0)
    self.messages_frame.pack(fill="both", expand=True, padx=20, pady=10)

  def create_message_bubble(self, sender, message):
    msg_frame = ctk.CTkFrame(self.messages_frame, fg_color="#ffffff", corner_radius=0)
    msg_frame.pack(fill="x", pady=8, padx=10, anchor="w" if sender == "system" else "e")

    if sender == "system":
      avatar_label = ctk.CTkLabel(msg_frame, text="🤖", font=("Segoe UI", 20), width=40)
      bubble_color = "#f0f4f9"
    else:
      avatar_label = ctk.CTkLabel(msg_frame, text="👤", font=("Segoe UI", 20), width=40)
      bubble_color = "#e9ecef"

    message_bubble = ctk.CTkFrame(msg_frame, corner_radius=15, fg_color=bubble_color, border_width=1, border_color="#e0e0e0")
    message_bubble.pack(fill="x", expand=True, padx=(0, 80) if sender == "system" else (80, 0), anchor="w")

    message_text = ctk.CTkTextbox(
      message_bubble,
      font=("Segoe UI", 13),
      text_color="#1a1a1a",
      wrap="none",
      width=600,
      corner_radius=10,
      fg_color=bubble_color,
      border_width=0
    )

    formatted_message = "\n".join(line.replace("    ", "\t") for line in message.split("\n"))

    message_text.insert("1.0", formatted_message)
    message_text.configure(state="disabled")
    message_text.pack(padx=15, pady=10, fill="both", expand=True)

    self.after(50, lambda: self.resize_textbox(message_text))

    return message_text

  def update_typing_message(self, msg_widget, new_text):
    formatted_text = "\n".join(line.replace("    ", "\t") for line in new_text.split("\n"))

    msg_widget.configure(state="normal")
    msg_widget.delete("1.0", "end")
    msg_widget.insert("1.0", formatted_text)
    msg_widget.configure(state="disabled")

    self.after(50, lambda: self.resize_textbox(msg_widget))

    self.messages_frame._parent_canvas.yview_moveto(1.0)

  def resize_textbox(self, msg_widget):
    num_lines = msg_widget.get("1.0", "end").count("\n") + 1
    msg_widget.configure(height=num_lines * 20)

  def finalize_typing_message(self, msg_widget):
    self.messages_frame._parent_canvas.yview_moveto(1.0)

  def upload_file(self):
    threading.Thread(target=self.process_upload, daemon=True).start()

  def process_upload(self):
    file_path = filedialog.askopenfilename(
      title="Select a Visio (.vsdx) File", filetypes=[("Visio Files", "*.vsdx")]
    )

    if not file_path:
      return

    self.after(0, self.smooth_transition)

    file_name = file_path.split("/")[-1]
    self.after(0, lambda: self.create_message_bubble("user", f"Uploaded: {file_name}"))

    response = prompt_ai_with_vsdx_data(file_path)

    ai_msg_widget = self.create_message_bubble("system", "...")

    full_response = ""

    for line in response:
      if line:
        line_data = line.decode("utf-8").strip()
        if line_data:
          try:
            json_line = json.loads(line_data)
            message = json_line.get("response", "")

            if message:
              full_response += message + ""
              print(message, end="", flush=True)

              formatted_response = "\n".join(line.rstrip() for line in full_response.split("\n"))
              self.after(0, lambda text=formatted_response: self.update_typing_message(ai_msg_widget, text))

          except json.JSONDecodeError:
            pass

    if full_response.strip():
      self.after(0, lambda: self.finalize_typing_message(ai_msg_widget))

  def smooth_transition(self):
    self.chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
    self.header_upload_btn.pack(side="right", padx=20)
    self.update()

if __name__ == "__main__":
  app = VisioChatbotApp()
  app.mainloop()
