import flet as ft
import re
from controllers.account_controller import AccountController

acc = AccountController()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}


def main(page: ft.Page):
    page.title = "GrowBak - Login"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    page.bgcolor = "#ffffff"
    page.scroll = ft.ScrollMode.AUTO
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")
    page.update()

    # Variabel untuk menyimpan data
    email = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    checkbox = ft.Ref[ft.Checkbox]()
    
    # Fungsi untuk mengubah warna saat fokus
    def on_focus(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#000000")
        page.update()
    
    def on_blur_label(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#c2c2c2")
        page.update()
    
    # Fungsi validasi email
    def validate_email(e):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if email.current.value and not re.match(email_pattern, email.current.value):
            email.current.error_text = "Format email tidak valid"
        else:
            email.current.error_text = None
        on_blur_label(e, email)
    
    def on_checkbox_change(e):
        if checkbox.current.value:
            checkbox.current.fill_color = "#1e8c45"   # warna saat dicentang
            checkbox.current.check_color = "#FFFFFF"
        else:
            checkbox.current.fill_color = "#9e9e9e"   # warna saat tidak dicentang
        page.update()

    # Fungsi login
    def login(e):
        # Reset error messages
        email.current.error_text = None
        password.current.error_text = None

        # Validasi
        is_valid = True
        
        if not email.current.value:
            email.current.error_text = "Email harus diisi"
            is_valid = False
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.current.value):
            email.current.error_text = "Format email tidak valid"
            is_valid = False
            
        if not password.current.value:
            password.current.error_text = "Password harus diisi"
            is_valid = False

        page.update()

        # Tidak valid → stop
        if not is_valid:
            return
        
        def close_dialog(e):
            dialog.open = False
            page.update()

        user = acc.login(email.current.value, password.current.value)

        #jujur harusnya dah nyambung sama backend 
        #tapi gatau kenapa nih dialog gagal sama berhasilnya gamau keluar
        #tapi tadi aku debung emg bisa jalan dan bisa login. tolong atur lah ya Frontend wkwkwk

        if user is None:
            # Login gagal
            dialog = ft.AlertDialog(
                title=ft.Text("Gagal!"),
                content=ft.Text("Email atau password salah"),
                actions=[ft.TextButton("OK", on_click=close_dialog)],
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            return
        
        dialog = ft.AlertDialog(
            title=ft.Text("Berhasil!"),
            content=ft.Text(f"Selamat datang, {user.username}!"),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Fungsi navigasi ke Sign Up
    def go_to_signup(e):
        page.clean()
        page.signup_main(page)
    
    # Left side - Image
    right_side = ft.Container(
        content=ft.Image(
            src="img/login_image.png",
            fit=ft.ImageFit.COVER,
        ),
        width=500,
        border_radius=ft.border_radius.only(top_left=20, bottom_left=20, top_right=20, bottom_right=20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )
    
    # Right side - Form
    left_side = ft.Container(
        content=ft.Stack(
            [
                # Form content
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height = 20),
                            ft.Text("Login", size=36, weight=ft.FontWeight.BOLD, font_family="PoppinsSBold", color="#000000"),
                            ft.Text(
                                "Login to access your travelwise account",
                                size=13,
                                color="#313131",
                                opacity=0.75,
                            ),
                            ft.Container(height=30),
                            
                            # Email field
                            ft.TextField(
                                ref=email,
                                label="Email",
                                border_color="#e0e0e0",
                                focused_border_color="#1e8c45",
                                height=65,
                                text_style=ft.TextStyle(color="#000000"),
                                cursor_color="#000000",
                                label_style=ft.TextStyle(color="#c2c2c2"),
                                on_focus=lambda e: on_focus(e, email),
                                on_blur=lambda e: on_blur_label(e, email),
                            ),
                            
                            ft.Container(height=15),
                            
                            # Password field
                            ft.TextField(
                                ref=password,
                                label="Password",
                                password=True,
                                can_reveal_password=True,
                                border_color="#e0e0e0",
                                focused_border_color="#1e8c45",
                                height=65,
                                text_style=ft.TextStyle(color="#000000"),
                                cursor_color="#000000",
                                label_style=ft.TextStyle(color="#c2c2c2"),
                                on_focus=lambda e: on_focus(e, password),
                                on_blur=lambda e: on_blur_label(e, password),
                            ),
                            
                            ft.Container(height=10),
                            
                            # Remember me and Forgot password
                            ft.Row(
                                [
                                    ft.Checkbox(
                                        ref=checkbox,
                                        label="Remember me",
                                        on_change=on_checkbox_change,
                                    ),
                                    ft.TextButton(
                                        "Forgot Password",
                                        style=ft.ButtonStyle(
                                            color="#d32f2f",
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            
                            ft.Container(height=5),
                            
                            # Login button
                            ft.ElevatedButton(
                                "Login",
                                on_click=login,
                                bgcolor="#1e8c45",
                                color="white",
                                width=float('inf'),
                                height=55,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    text_style=ft.TextStyle(font_family="PoppinsBold", size=16),
                                ),
                            ),
                            
                            ft.Container(height=5),
                            
                            # Sign up link
                            ft.Row(
                                [
                                    ft.Text("Don't have an account?", size=13, color="#666666", font_family="Poppins"),
                                    ft.TextButton(
                                        "Sign up",
                                        on_click=go_to_signup,
                                        style=ft.ButtonStyle(
                                            color="#d32f2f",
                                            padding=0,
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5,
                            ),
                        ],
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    padding=ft.padding.only(left=60, right=60, top=60, bottom=40),
                ),
                
                # Logo on top right
                ft.Container(
                    content=ft.Image(
                        src="img/logo.png",
                        width=200,
                        height=200,
                    ),
                    right=670,
                    top=-70,
                ),
            ],
        ),
        expand=1,
    )
    
    # Main container
    main_container = ft.Container(
        content=ft.Row(
            [
                left_side,
                right_side,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=50,
        alignment=ft.alignment.center,
    )
    
    page.add(main_container)
