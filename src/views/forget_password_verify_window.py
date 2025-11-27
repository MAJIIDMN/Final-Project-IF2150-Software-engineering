import flet as ft
import re
from controllers.account_controller import AccountController
ac = AccountController()


fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    page.title = "GrowBak - Verify Code"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    page.bgcolor = "#ffffff"

    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")

    verify_code = ft.Ref[ft.TextField]()

    def on_focus(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#000000")
        page.update()

    def on_blur_label(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#c2c2c2")
        page.update()

    # Fungsi untuk memvalidasi kode. Jangan lupa tambahkan kode OTP yang seharusnya di sini
    def validate_code(e):
        if not verify_code.current:
            return False
        
        code = verify_code.current.value

        if code and len(code) < 6:
            verify_code.current.error_text = "Kode harus minimal 6 karakter"
            on_blur_label(e, verify_code)
            return False
        
        if ac.correct_vcode(code):
            verify_code.current.error_text = None
            on_blur_label(e, verify_code)
            return True
        else:
            verify_code.current.error_text = "Kode Anda salah!"
            on_blur_label(e, verify_code)
            return False

    # Back to login
    def go_to_login(e):
        page.clean()
        page.login_main(page)

    # Submit verification
    def submit_verification(e):
        verify_code.current.error_text = None
        is_valid = True

        if not verify_code.current.value:
            verify_code.current.error_text = "Kode verifikasi harus diisi"
            is_valid = False
        elif len(verify_code.current.value) < 6:
            verify_code.current.error_text = "Kode verifikasi tidak valid"
            is_valid = False

        if is_valid:
            if validate_code(e):
                page.update()
                page.clean()
                page.reset_password_main(page)

    # Right side - Image
    right_side = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=100),
                ft.Image(
                    src="img/forget_password_verify_image.jpg",
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
                "Verify code",
                size=36,
                weight=ft.FontWeight.BOLD,
                font_family="PoppinsSBold",
                color="#000000",
            ),
            ft.Text(
                "An authentication code has been sent to your email.",
                size=13,
                color="#313131",
                opacity=0.75,
            ),
            ft.Container(height=30),
            ft.TextField(
                ref=verify_code,
                label="Enter Code",
                border_color="#e0e0e0",
                focused_border_color="#1e8c45",
                height=65,
                text_style=ft.TextStyle(color="#000000"),
                cursor_color="#000000",
                label_style=ft.TextStyle(color="#c2c2c2"),
                on_focus=lambda e: on_focus(e, verify_code),
                on_blur=lambda e: validate_code(e),
            ),
            ft.Container(height=5),
            ft.ElevatedButton(
                "Verify",
                on_click=submit_verification,
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
