"""
Notes Panel - Persistent note-taking functionality
"""
import customtkinter as ctk
from tkinter import filedialog
import json
import os
from pathlib import Path


class NotesPanel:
    """Manages the notes panel UI and persistence"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.notes_file = self._get_notes_file_path()
        
        # Create panel frame
        self.frame = ctk.CTkFrame(parent)
        
        # Build UI
        self._build_ui()
        
        # Load saved notes
        self._load_notes()
    
    def _get_notes_file_path(self):
        """Get the path to the notes file"""
        app_data_dir = Path.home() / ".pixelperfect"
        app_data_dir.mkdir(exist_ok=True)
        return app_data_dir / "notes.json"
    
    def _build_ui(self):
        """Build the notes panel UI"""
        # Header with title and buttons
        header_frame = ctk.CTkFrame(self.frame)
        header_frame.pack(fill="x", padx=5, pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Notes",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(side="left", padx=5)
        
        # Export button
        export_btn = ctk.CTkButton(
            header_frame,
            text="Export to TXT",
            width=100,
            height=24,
            command=self._export_to_txt
        )
        export_btn.pack(side="right", padx=5)
        
        # Clear button
        clear_btn = ctk.CTkButton(
            header_frame,
            text="Clear",
            width=60,
            height=24,
            command=self._clear_notes
        )
        clear_btn.pack(side="right", padx=5)
        
        # Text area
        self.text_area = ctk.CTkTextbox(
            self.frame,
            wrap="word",
            font=ctk.CTkFont(size=12)
        )
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Auto-save on text change
        self.text_area.bind("<<Modified>>", self._on_text_modified)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.frame,
            text="Auto-saved",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.status_label.pack(side="bottom", padx=5, pady=2)
    
    def _on_text_modified(self, event=None):
        """Handle text modification - auto-save"""
        if self.text_area.edit_modified():
            self._save_notes()
            self.text_area.edit_modified(False)
            self._update_status("Auto-saved")
    
    def _save_notes(self):
        """Save notes to file"""
        try:
            content = self.text_area.get("1.0", "end-1c")
            data = {
                "content": content,
                "version": "1.0"
            }
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[NOTES] Error saving notes: {e}")
    
    def _load_notes(self):
        """Load notes from file"""
        try:
            if self.notes_file.exists():
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content = data.get("content", "")
                    self.text_area.delete("1.0", "end")
                    self.text_area.insert("1.0", content)
                    print(f"[NOTES] Loaded from: {self.notes_file}")
            else:
                # Set default welcome message
                welcome_text = "# Notes\n\nType your notes here. They will auto-save.\n\n"
                self.text_area.insert("1.0", welcome_text)
        except Exception as e:
            print(f"[NOTES] Error loading notes: {e}")
    
    def _export_to_txt(self):
        """Export notes to a text file"""
        try:
            content = self.text_area.get("1.0", "end-1c")
            
            if not content.strip():
                self._update_status("Nothing to export", error=True)
                return
            
            # Ask user where to save
            file_path = filedialog.asksaveasfilename(
                title="Export Notes",
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                initialfile="pixel_perfect_notes.txt"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self._update_status(f"Exported to {os.path.basename(file_path)}")
                print(f"[NOTES] Exported to: {file_path}")
        except Exception as e:
            print(f"[NOTES] Error exporting notes: {e}")
            self._update_status("Export failed", error=True)
    
    def _clear_notes(self):
        """Clear all notes"""
        self.text_area.delete("1.0", "end")
        self._save_notes()
        self._update_status("Notes cleared")
    
    def _update_status(self, message, error=False):
        """Update status label"""
        color = "red" if error else "gray"
        self.status_label.configure(text=message, text_color=color)
        
        # Reset to "Auto-saved" after 3 seconds
        if not error:
            self.frame.after(3000, lambda: self.status_label.configure(text="Auto-saved", text_color="gray"))
    
    def show(self):
        """Show the notes panel"""
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        """Hide the notes panel"""
        self.frame.pack_forget()
    
    def update_theme(self, theme):
        """Update panel colors based on theme"""
        # Theme will be applied automatically by customtkinter
        pass

