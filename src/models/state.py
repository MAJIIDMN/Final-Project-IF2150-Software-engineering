import json

class AppState:
    is_logged_in = False
    username = None
    role = None

    @classmethod
    def load_state(cls):
        try:
            with open("src/state.json", "r") as f:
                data = json.load(f)
                cls.is_logged_in = data.get("is_logged_in", False)
                cls.username = data.get("username", None)
                cls.role = data.get("role", None)
        except FileNotFoundError:
            cls.is_logged_in = False
            cls.username = None
            cls.role = None
    
    @classmethod
    def save_state(cls):
        if cls.username is None:
            cls.username = ""
        if cls.role is None:
            cls.role = ""
        data = {
            "is_logged_in": cls.is_logged_in,
            "username": cls.username,
            "role": cls.role
        }
        with open("src/state.json", "w") as f:
            json.dump(data, f)

    @classmethod
    def clear_state(cls):
        cls.is_logged_in = False
        cls.username = None
        cls.role = None
        cls.save_state()

    @classmethod
    def change_state(cls, is_logged_in: bool, username: str, role: str):
        cls.is_logged_in = is_logged_in
        cls.username = username
        cls.role = role
        cls.save_state()

