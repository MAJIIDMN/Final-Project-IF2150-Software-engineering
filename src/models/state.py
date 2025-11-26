import json

class AppState:
    is_logged_in = False
    save_login = False
    username = None
    role = None

    @classmethod
    def load_state(cls):
        try:
            with open("src/state.json", "r") as f:
                data = json.load(f)
                cls.is_logged_in = data.get("is_logged_in", False)
                cls.save_login = data.get("save_login", False)
                cls.username = data.get("username", None)
                cls.role = data.get("role", None)
        except FileNotFoundError:
            cls.is_logged_in = False
            cls.save_login = False
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
            "save_login": cls.save_login,
            "username": cls.username,
            "role": cls.role
        }
        with open("src/state.json", "w") as f:
            json.dump(data, f)

    @classmethod
    def clear_state(cls):
        cls.is_logged_in = False
        cls.save_login = False
        cls.username = None
        cls.role = None
        cls.save_state()

    @classmethod
    def change_state(cls, is_logged_in: bool, save_login: bool, username: str, role: str):
        cls.is_logged_in = is_logged_in
        cls.save_login = save_login
        cls.username = username
        cls.role = role

