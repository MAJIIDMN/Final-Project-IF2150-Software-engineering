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
    AppState.load_state()
    username = AppState.username 

    page.title = "GrowBak - Reset Password"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    page.bgcolor = "#ffffff"
    page.scroll = None

    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")

    new_password = ft.Ref[ft.TextField]()
    confirm_password = ft.Ref[ft.TextField]()

    def on_focus(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#000000")
        page.update()

    def on_blur_label(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#c2c2c2")
        page.update()

    # Fungsi untuk melakukan validasi password
    def validate_password(e):
        if new_password.current.value and len(new_password.current.value) < 8:
            new_password.current.error_text = "Password minimal 8 karakter"
        else:
            new_password.current.error_text = None
        on_blur_label(e, new_password)

    def validate_confirm_password(e):
        if confirm_password.current.value and new_password.current.value:
            if confirm_password.current.value != new_password.current.value:
                confirm_password.current.error_text = "Password tidak cocok"
            else:
                confirm_password.current.error_text = None
        on_blur_label(e, confirm_password)

    # Back to login
    def go_to_login(e):
        page.clean()
        page.login_main(page)

    # Submit reset password
    def submit_reset_password(e):
        new_password.current.error_text = None
        confirm_password.current.error_text = None
        is_valid = True

        if not new_password.current.value:
            new_password.current.error_text = "Password harus diisi"
            is_valid = False
        elif len(new_password.current.value) < 8:
            new_password.current.error_text = "Password minimal 8 karakter"
            is_valid = False

        if not confirm_password.current.value:
            confirm_password.current.error_text = "Konfirmasi password harus diisi"
            is_valid = False
        elif new_password.current.value != confirm_password.current.value:
            confirm_password.current.error_text = "Password tidak cocok"
            is_valid = False

        page.update()

        if is_valid:
            email = ac.find_email_of_user(username)
            success, message = ac.change_password(new_password.current.value, email)

            def close_dialog(e):
                dialog.open = False
                page.update()
                page.clean()
                page.login_main(page)

            if success:
                dialog = ft.AlertDialog(
                    title=ft.Text("Berhasil!"),
                    content=ft.Text("Password Anda telah berhasil diubah. Silakan login dengan password baru Anda"),
                    actions=[ft.TextButton("OK", on_click=close_dialog)],
                )
            else:
                dialog = ft.AlertDialog(
                    title=ft.Text("Gagal!"),
                    content=ft.Text(message),
                    actions=[ft.TextButton("OK", on_click=close_dialog)],
                )

            page.dialog = dialog
            dialog.open = True
            page.update()

    # Right side - Image
    right_side = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=100),
                ft.Image(
                    src="img/reset_image.png",
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
                "Set a password",
                size=36,
                weight=ft.FontWeight.BOLD,
                font_family="PoppinsSBold",
                color="#000000",
            ),
            ft.Text(
                "Your previous password has been reset. Please set a new password for your account.",
                size=13,
                color="#313131",
                opacity=0.75,
            ),
            ft.Container(height=30),
            ft.TextField(
                ref=new_password,
                label="Create Password",
                border_color="#e0e0e0",
                focused_border_color="#1e8c45",
                height=65,
                password=True,
                can_reveal_password=True,
                text_style=ft.TextStyle(color="#000000"),
                cursor_color="#000000",
                label_style=ft.TextStyle(color="#c2c2c2"),
                on_focus=lambda e: on_focus(e, new_password),
                on_blur=lambda e: validate_password(e),
            ),
            ft.Container(height=15),
            ft.TextField(
                ref=confirm_password,
                label="Re-enter Password",
                border_color="#e0e0e0",
                focused_border_color="#1e8c45",
                height=65,
                password=True,
                can_reveal_password=True,
                text_style=ft.TextStyle(color="#000000"),
                cursor_color="#000000",
                label_style=ft.TextStyle(color="#c2c2c2"),
                on_focus=lambda e: on_focus(e, confirm_password),
                on_blur=lambda e: validate_confirm_password(e),
            ),
            ft.Container(height=20),
            ft.ElevatedButton(
                "Set password",
                on_click=submit_reset_password,
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
