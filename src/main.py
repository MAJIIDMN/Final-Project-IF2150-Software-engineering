import flet as ft
import sys
from views.signup_window import main as signup_main
from views.login_window import main as login_main
from services.database import DatabaseService
from views.forget_password_window import main as forget_password_main
from views.forget_password_verify_window import main as forget_password_verify_main
from views.reset_password_window import main as reset_password_main
from views.point_mart_window import main as point_mart_main
from views.product_detail_window import main as product_detail_main
from views.order_window import main as order_main
from views.home_window import main as home_main
from views.informasi_sampah_window import main as info_main

def app_main(page: ft.Page):
    try:
        db = DatabaseService()
        db.create_tables()
        page.signup_main = signup_main
        page.login_main = login_main
        page.forget_password_main = forget_password_main
        page.forget_password_verify_main = forget_password_verify_main
        page.reset_password_main = reset_password_main
        page.point_mart_main = point_mart_main
        page.product_detail_main = product_detail_main
        page.order_main = order_main
        page.home_main = home_main
        page.info_main = info_main
        info_main(page)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ft.app(target=app_main)
