import flet as ft
import re

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}


def main(page: ft.Page):
    page.title = "GrowBak - Sign Up"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    page.bgcolor = "#ffffff"
    page.scroll = ft.ScrollMode.AUTO
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")
    page.update()

    # Variabel untuk menyimpan data
    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    email = ft.Ref[ft.TextField]()
    phone = ft.Ref[ft.TextField]()
    address = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    confirm_password = ft.Ref[ft.TextField]()
    
    # Fungsi untuk mengubah warna label saat fokus
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
    
    # Fungsi toggle password visibility
    def toggle_password_visibility(e, field):
        field.password = not field.password
        page.update()
    
    # Fungsi navigasi ke Login
    def go_to_login(e):
        page.clean()
        page.login_main(page)
    
    # Fungsi create account
    def create_account(e):
        # Reset error messages
        first_name.current.error_text = None
        last_name.current.error_text = None
        email.current.error_text = None
        phone.current.error_text = None
        address.current.error_text = None
        password.current.error_text = None
        confirm_password.current.error_text = None
        
        # Validasi
        is_valid = True
        
        if not first_name.current.value:
            first_name.current.error_text = "First name harus diisi"
            is_valid = False
            
        if not last_name.current.value:
            last_name.current.error_text = "Last name harus diisi"
            is_valid = False
            
        if not email.current.value:
            email.current.error_text = "Email harus diisi"
            is_valid = False
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.current.value):
            email.current.error_text = "Format email tidak valid"
            is_valid = False
            
        if not phone.current.value:
            phone.current.error_text = "Phone number harus diisi"
            is_valid = False
            
        if not address.current.value:
            address.current.error_text = "Address harus diisi"
            is_valid = False
            
        if not password.current.value:
            password.current.error_text = "Password harus diisi"
            is_valid = False
        elif len(password.current.value) < 6:
            password.current.error_text = "Password minimal 6 karakter"
            is_valid = False
            
        if not confirm_password.current.value:
            confirm_password.current.error_text = "Confirm password harus diisi"
            is_valid = False
        elif password.current.value != confirm_password.current.value:
            confirm_password.current.error_text = "Password tidak sama"
            is_valid = False
        
        page.update()
        
        if is_valid:
            # Tampilkan dialog sukses
            def close_dialog(e):
                dialog.open = False
                page.update()
                # Reset form
                first_name.current.value = ""
                last_name.current.value = ""
                email.current.value = ""
                phone.current.value = ""
                address.current.value = ""
                password.current.value = ""
                confirm_password.current.value = ""
                page.update()
            
            dialog = ft.AlertDialog(
                title=ft.Text("Berhasil!"),
                content=ft.Text("Account berhasil dibuat!"),
                actions=[
                    ft.TextButton("OK", on_click=close_dialog)
                ]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
    
    # Left side - Image
    left_side = ft.Container(
        content=ft.Image(
            src="img/signup_image.jpg",
            fit=ft.ImageFit.COVER,
        ),
        width=400,
        border_radius=ft.border_radius.only(top_left=20, bottom_left=20, top_right=20, bottom_right=20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )
    
    # Right side - Form
    right_side = ft.Container(
        content=ft.Stack(
            [
                # Form content
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Sign up", size=36, weight=ft.FontWeight.BOLD, font_family="PoppinsSBold", color="#000000"),
                            ft.Text(
                                "Let's get you all st up so you can access your personal account.",
                                size=13,
                                color="#313131",
                                opacity=0.75,
                            ),
                            ft.Container(height=10),
                
                # Form fields
                ft.Row(
                    [
                        ft.TextField(
                            ref=first_name,
                            label="First Name",
                            border_color="#e0e0e0",
                            focused_border_color="#1e8c45",
                            expand=True,
                            height=65,
                            text_style=ft.TextStyle(color="#000000"),
                            cursor_color="#000000",
                            label_style=ft.TextStyle(color="#c2c2c2"),
                            on_focus=lambda e: on_focus(e, first_name),
                            on_blur=lambda e: on_blur_label(e, first_name),
                        ),
                        ft.TextField(
                            ref=last_name,
                            label="Last Name",
                            border_color="#e0e0e0",
                            focused_border_color="#1e8c45",
                            expand=True,
                            height=65,
                            text_style=ft.TextStyle(color="#000000"),
                            cursor_color="#000000",
                            label_style=ft.TextStyle(color="#c2c2c2"),
                            on_focus=lambda e: on_focus(e, last_name),
                            on_blur=lambda e: on_blur_label(e, last_name),
                        ),
                    ],
                    spacing=15,
                ),
                
                ft.Row(
                    [
                        ft.TextField(
                            ref=email,
                            label="Email",
                            border_color="#e0e0e0",
                            focused_border_color="#1e8c45",
                            on_blur=validate_email,
                            on_focus=lambda e: on_focus(e, email),
                            expand=True,
                            height=65,
                            text_style=ft.TextStyle(color="#000000"),
                            cursor_color="#000000",
                            label_style=ft.TextStyle(color="#c2c2c2"),
                        ),
                        ft.TextField(
                            ref=phone,
                            label="Phone Number",
                            border_color="#e0e0e0",
                            focused_border_color="#1e8c45",
                            expand=True,
                            height=65,
                            text_style=ft.TextStyle(color="#000000"),
                            cursor_color="#000000",
                            label_style=ft.TextStyle(color="#c2c2c2"),
                            on_focus=lambda e: on_focus(e, phone),
                            on_blur=lambda e: on_blur_label(e, phone),
                        ),
                    ],
                    spacing=15,
                ),
                
                ft.TextField(
                    ref=address,
                    label="Address",
                    border_color="#e0e0e0",
                    focused_border_color="#1e8c45",
                    height=65,
                    text_style=ft.TextStyle(color="#000000"),
                    cursor_color="#000000",
                    label_style=ft.TextStyle(color="#c2c2c2"),
                    on_focus=lambda e: on_focus(e, address),
                    on_blur=lambda e: on_blur_label(e, address),
                ),
                
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
                
                ft.TextField(
                    ref=confirm_password,
                    label="Confirm Password",
                    password=True,
                    can_reveal_password=True,
                    border_color="#e0e0e0",
                    focused_border_color="#1e8c45",
                    height=65,
                    text_style=ft.TextStyle(color="#000000"),
                    cursor_color="#000000",
                    label_style=ft.TextStyle(color="#c2c2c2"),
                    on_focus=lambda e: on_focus(e, confirm_password),
                    on_blur=lambda e: on_blur_label(e, confirm_password),
                ),

                ft.Container(height=15),
                
                # Create account button
                ft.ElevatedButton(
                    "Create account",
                    on_click=create_account,
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
                                
                # Login link
                ft.Row(
                    [
                        ft.Text("Already have an account?", size=13, color="#666666", font_family="Poppins"),
                        ft.TextButton(
                            "Login",
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
                
                # Logo positioned absolutely in top right
                ft.Container(
                    content=ft.Image(
                        src="img/logo.png",
                        width=200,
                        height=200,
                    ),
                    right=50,
                    top=-40,
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