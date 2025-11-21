import flet as ft
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.signup_window import main as signup_main

def app_main(page: ft.Page):
    try:
        page.signup_main = signup_main
        signup_main(page)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ft.app(target=app_main)
