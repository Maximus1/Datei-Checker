import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import asyncio
import os
import threading
from core.processor import process_directory

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Datei Checker - File Signature & Recovery")
        self.geometry("800x600")

        # UI Styles
        self.style = ttk.Style(self)
        self.style.configure("TButton", padding=6)
        self.style.configure("TLabel", padding=4)

        # State
        self.directory = tk.StringVar(value=os.getcwd())
        self.dry_run = tk.BooleanVar(value=False)
        self.is_running = False
        self.stop_event = threading.Event()

        self.setup_ui()

    def setup_ui(self):
        # Header / Title
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(header_frame, text="Datei Checker - Filetype Detector", font=("Helvetica", 18, "bold")).pack(side="left")

        # Configuration Frame
        config_frame = ttk.LabelFrame(self, text="Konfiguration", padding=10)
        config_frame.pack(fill="x", padx=10, pady=5)

        # Folder Picker
        path_frame = ttk.Frame(config_frame)
        path_frame.pack(fill="x", pady=5)
        ttk.Label(path_frame, text="Ordner:").pack(side="left")
        ttk.Entry(path_frame, textvariable=self.directory).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(path_frame, text="Durchsuchen...", command=self.browse_folder).pack(side="left")

        # Checkbox & Start Button
        action_frame = ttk.Frame(config_frame)
        action_frame.pack(fill="x", pady=5)
        ttk.Checkbutton(action_frame, text="Vorschau-Modus (keine Änderungen)", variable=self.dry_run).pack(side="left")

        self.stop_btn = ttk.Button(action_frame, text="Abbrechen", command=self.stop_processing, state="disabled")
        self.stop_btn.pack(side="right", padx=5)
        self.start_btn = ttk.Button(action_frame, text="Starten", command=self.start_processing)
        self.start_btn.pack(side="right")

        # Progress Frame
        progress_frame = ttk.Frame(self, padding=10)
        progress_frame.pack(fill="x")
        self.progress_bar = ttk.Progressbar(progress_frame, mode="determinate", orient="horizontal")
        self.progress_bar.pack(fill="x", pady=5)
        self.status_label = ttk.Label(progress_frame, text="Bereit.")
        self.status_label.pack(side="left")

        # Results Table
        table_frame = ttk.Frame(self, padding=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("path", "type", "result", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("path", text="Datei")
        self.tree.heading("type", text="Typ")
        self.tree.heading("result", text="Neuer Name / Fehler")
        self.tree.heading("status", text="Status")

        self.tree.column("path", width=250)
        self.tree.column("type", width=100)
        self.tree.column("result", width=250)
        self.tree.column("status", width=80)

        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.directory.set(folder)

    def start_processing(self):
        if self.is_running:
            return

        folder = self.directory.get()
        if not os.path.isdir(folder):
            messagebox.showerror("Fehler", "Ungültiges Verzeichnis!")
            return

        self.is_running = True
        self.stop_event.clear()
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.tree.delete(*self.tree.get_children())
        self.progress_bar["value"] = 0

        # Start async task in background thread
        threading.Thread(target=self.run_async_task, args=(folder, self.dry_run.get()), daemon=True).start()

    def stop_processing(self):
        if self.is_running:
            self.stop_event.set()
            self.status_label.config(text="Breche ab...")
            self.stop_btn.config(state="disabled")

    def run_async_task(self, folder, dry_run):
        asyncio.run(self.process(folder, dry_run))

    async def process(self, folder, dry_run):
        def ui_callback(current, total, result):
            # Safe call back to main thread
            self.after(0, self.update_ui, current, total, result)

        await process_directory(folder, dry_run, ui_callback, self.stop_event)
        self.after(0, self.finish_processing)

    def update_ui(self, current, total, result):
        self.progress_bar["maximum"] = total
        self.progress_bar["value"] = current
        self.status_label.config(text=f"Verarbeite... {current}/{total}")

        status_icon = "✅" if result["status"] == "Success" else "❌"
        self.tree.insert("", "end", values=(
            os.path.basename(result["path"]),
            result.get("type", "Unbekannt"),
            result["msg"],
            status_icon
        ))
        self.tree.see(self.tree.get_children()[-1]) # Auto-scroll
        self.update_idletasks() # Ensure UI updates immediately

    def finish_processing(self):
        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        if self.stop_event.is_set():
            self.status_label.config(text="Abgebrochen.")
            messagebox.showwarning("Abbruch", "Verarbeitung wurde abgebrochen.")
        else:
            self.status_label.config(text="Fertig.")
            messagebox.showinfo("Abschluss", "Verarbeitung abgeschlossen.")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
