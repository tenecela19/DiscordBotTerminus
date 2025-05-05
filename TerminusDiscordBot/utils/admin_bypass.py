import json
import os
import time

class AdminBypassManager:
    def __init__(self, filepath="admin_bypass.json"):
        self.filepath = filepath
        self.admins = set()
        self.last_mtime = os.path.getmtime(filepath) if os.path.exists(filepath) else 0
        self.load()

    def load(self):
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r') as f:
                    self.admins = set(json.load(f))
                self.last_mtime = os.path.getmtime(self.filepath)  # Update after successful load
            else:
                self.admins = set()
        except (json.JSONDecodeError, IOError):
            self.admins = set()

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(list(self.admins), f, indent=2)
        self.last_mtime = os.path.getmtime(self.filepath)  # Update after saving

    def add(self, name):
        name = name.strip()
        if name not in self.admins:
            self.admins.add(name)
            self.save()
            return True
        return False

    def remove(self, name):
        name = name.strip()
        if name in self.admins:
            self.admins.remove(name)
            self.save()
            return True
        return False

    def is_bypassed(self, name):
        return name.strip() in self.admins

    def list(self):
        return sorted(self.admins)

    def __contains__(self, name):
        return name.strip() in self.admins

    def reload_if_needed(self):
        """Check if file modified and reload if necessary."""
        try:
            if os.path.exists(self.filepath):
                current_mtime = os.path.getmtime(self.filepath)
                if current_mtime != self.last_mtime:
                    self.load()
                    print(f"[AdminBypassManager] Reloaded from {self.filepath}")
        except Exception as e:
            print(f"[AdminBypassManager] Error checking file: {e}")
