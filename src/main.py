# from PyQt5.QtWidgets import QApplication
# import sys

# from views.example_view import ExampleWindow

# def main():
#     app = QApplication(sys.argv)
    
#     window = ExampleWindow()
#     window.show()
    
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

from controllers.account_controller import AccountController

def main():
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

if __name__ == "__main__":
    main()