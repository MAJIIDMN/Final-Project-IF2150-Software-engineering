import flet as ft
import re

from controllers.account_controller import AccountController
ac = AccountController()


from models.state import AppState
state = AppState()
state.load_state()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    page.title = "GrowBak - Forgot Password"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    page.bgcolor = "#ffffff"

    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")

    email = ft.Ref[ft.TextField]()

    def on_focus(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#000000")
        page.update()

    def on_blur_label(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#c2c2c2")
        page.update()

    # Fungsi untuk memvalidasi email
    def validate_email(e):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if email.current.value and not re.match(pattern, email.current.value):
            email.current.error_text = "Format email tidak valid"
        else:
            email.current.error_text = None
        user = ac.find_user_with_email(email.current.value)
        if user is None:
            message = "email ini tidak terdaftar!"
        else:
            message = None
        email.current.error_text = message    
        on_blur_label(e, email)
        page.update()
        if (message is None):
            return True
        else:
            return False
        

    # Back to login
    def go_to_login(e):
        page.clean()
        page.login_main(page)

    # Submit
    def submit_email(e):
        email.current.error_text = None
        is_valid = True

        if not email.current.value:
            email.current.error_text = "Email harus diisi"
            is_valid = False
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.current.value):
            email.current.error_text = "Format email tidak valid"
            is_valid = False

        page.update()
        if validate_email(e) is True:
            if is_valid:
                user = ac.find_user_with_email(email.current.value)
                state.change_state(True, user.username, user.role)
                page.clean()
                page.forget_password_verify_main(page)

    # Right side - Image
    right_side = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=100),
                ft.Image(
                    src="img/forget_password_image.jpg",
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(15),
                ),
            ]
        ),
        width=500,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Header row
    header_row = ft.Container(
    content=ft.Row(
        controls=[
                ft.TextButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ARROW_BACK, color="#000000"),
                            ft.Text("Back to login", color="#000000"),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    on_click=go_to_login,
                ),
                ft.Row(
                    [
                        ft.Image(src="img/logo.png", width=200),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(bottom=20),
    )

    # Form column
    form_column = ft.Column(
        [   
            ft.Container(height=150),
            header_row,
            ft.Text(
                "Forgot your password?",
                size=36,
                weight=ft.FontWeight.BOLD,
                font_family="PoppinsSBold",
                color="#000000",
            ),
            ft.Text(
                "Don't worry, happens to all of us. Enter your email below to recover your password",
                size=13,
                color="#313131",
                opacity=0.75,
            ),
            ft.Container(height=30),
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
                on_blur=lambda e: validate_email(e),
            ),
            ft.Container(height=20),
            ft.ElevatedButton(
                "Submit",
                on_click=submit_email,
                bgcolor="#1e8c45",
                color="white",
                width=float("inf"),
                height=55,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(font_family="PoppinsBold", size=16),
                ),
            ),
        ],
        spacing=12,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Left side - Form
    left_side = ft.Container(
        content=ft.Container(
            content=form_column,
            padding=ft.padding.only(left=60, right=60, top=20, bottom=40),
            alignment=ft.alignment.center,
        ),
        expand=1,
    )


    # Main Container
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
