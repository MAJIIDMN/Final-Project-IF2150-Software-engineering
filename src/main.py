import flet as ft
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.signup_window import main as signup_main
from views.login_window import main as login_main
from controllers.account_controller import AccountController
from services.database import DatabaseService

def run_cli():
    print("Running in CLI mode...")
    app = AccountController()
    running = True

    while running:
        print("\n================ GROWBAK ================")
        
        if not app.is_logged_in:
            print("1. Login\n2. Register\n3. Quit")
            choice = input("Pilih: ")

            if choice == '1': app.login()
            elif choice == '2': app.register()
            elif choice == '3': 
                running = False
                app.db.close() # Tutup koneksi DB
                print("Aplikasi ditutup.")
            else: print("Input salah.")
        
        else:
            role = app.current_user.role
            print(f"Menu User: {role.upper()}")
            
            if role == 'client':
                print("1. Pesan Layanan\n2. Logout")
                if input("Pilih: ") == '1':
                    app.create_order()
                else:
                    app.logout()
            
            elif role == 'wc':
                print("1. Cek Pesanan Masuk\n2. Logout")
                if input("Pilih: ") == '1':
                    app.get_pending_orders()
                else:
                    app.logout()
            else:
                app.logout()



def app_main(page: ft.Page):
    try:
        db = DatabaseService()
        db.create_tables()
        page.signup_main = signup_main
        page.login_main = login_main
        signup_main(page)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        ft.app(target=app_main)
