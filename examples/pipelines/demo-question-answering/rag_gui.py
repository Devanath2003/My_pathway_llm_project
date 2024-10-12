import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import subprocess
import threading
import requests
import json
import time
import atexit
import signal
import os
import shutil

class RAGApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RAG Application")
        self.geometry("600x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        self.settings_frame = ctk.CTkFrame(self.main_frame)
        self.settings_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(self.settings_frame, text="Pathway Directory:")
        self.path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.path_entry = ctk.CTkEntry(self.settings_frame)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.path_entry.insert(0, "C:\\Users\\devan\\Desktop\\pathway")
        self.path_button = ctk.CTkButton(self.settings_frame, text="Browse", command=self.browse_path)
        self.path_button.grid(row=0, column=2, padx=5, pady=5)

        self.pdf_button = ctk.CTkButton(self.settings_frame, text="Upload PDF", command=self.upload_pdf)
        self.pdf_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.run_button = ctk.CTkButton(self.main_frame, text="Run Engine", command=self.start_engine, fg_color="green", hover_color="dark green")
        self.run_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.prompt_frame = ctk.CTkFrame(self.main_frame)
        self.prompt_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.prompt_frame.grid_columnconfigure(0, weight=1)

        self.prompt_entry = ctk.CTkEntry(self.prompt_frame, placeholder_text="Enter your prompt here")
        self.prompt_entry.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")

        self.execute_button = ctk.CTkButton(self.prompt_frame, text="Execute", command=self.execute_prompt, fg_color="orange", hover_color="dark orange")
        self.execute_button.grid(row=0, column=1, pady=5)

        self.output_text = ctk.CTkTextbox(self.main_frame, wrap="word")
        self.output_text.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.engine_process = None


        atexit.register(self.shutdown_engine)

        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            destination_path = os.path.join(self.path_entry.get(), "llm-app", "examples", "pipelines", "demo-question-answering", "data")
            os.makedirs(destination_path, exist_ok=True)
            shutil.copy(file_path, destination_path)
            self.output_text.insert("end", f"PDF uploaded: {os.path.basename(file_path)}\n\n")
            self.output_text.see("end")

    def start_engine(self):
        if self.engine_process is None or self.engine_process.poll() is not None:
            path = self.path_entry.get()
            command = f'docker run -v "{path}\\llm-app\\examples\\pipelines\\demo-question-answering:/app" -p 8080:8000 raggem'
            self.engine_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            threading.Thread(target=self.update_output, args=(self.engine_process.stdout,), daemon=True).start()
            threading.Thread(target=self.update_output, args=(self.engine_process.stderr,), daemon=True).start()
            self.output_text.insert("end", "Engine started. Please wait...\n\n")
            self.animate_loading(10)  
        else:
            self.output_text.insert("end", "Engine is already running.\n\n")

    def animate_loading(self, seconds):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for i in range(seconds * 2):  
            self.output_text.delete("end-2l", "end")
            self.output_text.insert("end", f"Loading {frames[i % len(frames)]}\n")
            self.output_text.see("end")
            self.update()
            time.sleep(0.5)
        self.output_text.delete("end-2l", "end")  
        self.output_text.insert("end", "You can now enter your prompt and click Execute.\n\n")

    def execute_prompt(self):
        prompt = self.prompt_entry.get()
        if not prompt:
            self.output_text.insert("end", "Please enter a prompt.\n\n")
            return

        try:
            url = "http://localhost:8080/v1/pw_ai_answer"
            headers = {
                "accept": "*/*",
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt
            }
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.output_text.insert("end", "Here is the answer for what you asked:\n\n")
                self.output_text.insert("end", result + "\n\n")  
            else:
                self.animate_error_message()
        except requests.RequestException as e:
            self.animate_error_message()
        
        self.output_text.see("end")

    def animate_error_message(self):
        message = "The engine may need more time to set up. Please try again in a few moments."
        for i in range(3):  
            self.output_text.insert("end", message + "   \n")
            self.output_text.see("end")
            self.update()
            time.sleep(0.5)
            self.output_text.delete("end-2l", "end")
            self.output_text.insert("end", message + "...   \n")
            self.output_text.see("end")
            self.update()
            time.sleep(0.5)
            self.output_text.delete("end-2l", "end")
        self.output_text.insert("end", message + "\n\n")

    def update_output(self, pipe):
        for line in iter(pipe.readline, b''):
            print(line.decode().strip())  

    def shutdown_engine(self):
        if self.engine_process:
            print("Shutting down the engine...")
            if os.name == 'nt':  
                self.engine_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:  # Unix/Linux
                self.engine_process.send_signal(signal.SIGINT)
            try:
                self.engine_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.engine_process.kill()
            print("Engine shut down.")

    def on_closing(self):
        self.shutdown_engine()
        self.quit()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set the theme to dark mode
    app = RAGApplication()
    app.mainloop()
