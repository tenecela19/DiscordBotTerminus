import json
import os

class AdminBypassManager:
    def __init__(self, filepath="admin_bypass.json"):
        self.filepath = filepath
        self.admins = set()
        self.load()

    def load(self):
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r') as f:
                    self.admins = set(json.load(f))
            else:
                self.admins = set()
        except (json.JSONDecodeError, IOError):
            self.admins = set()

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(list(self.admins), f, indent=2)

    def add(self, name):
        name = name.strip()
        if name not in self.admins:
            self.admins.add(name)
            self.save()
            return True
        return False

    def remove(self, name):
        if name in self.admins:
            self.admins.remove(name)
            self.save()
            return True
        return False

    def is_bypassed(self, name):
        return name in self.admins

    def list(self):
        return sorted(self.admins)

    def __contains__(self, name):
        return name in self.admins

