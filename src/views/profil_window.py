import flet as ft
from views.components.navbar import create_navbar
from models.state import AppState

app_state = AppState()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    page.title = "GrowBak - My Profile"
    page.window_width = 1440
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")

    # Refs untuk form inputs
    username_input = ft.Ref[ft.TextField]()
    email_input = ft.Ref[ft.TextField]()
    phone_input = ft.Ref[ft.TextField]()
    kecamatan_input = ft.Ref[ft.TextField]()
    current_password = ft.Ref[ft.TextField]()
    new_password = ft.Ref[ft.TextField]()
    confirm_password = ft.Ref[ft.TextField]()
    profile_image = ft.Ref[ft.Image]()

    # TODO: Load user data from database
    user_data = {
        "id": app_state.user_id if hasattr(app_state, 'user_id') else "U001",
        "username": app_state.username if app_state.username else "johndoe",
        "email": "johndoe@example.com",
        "phonenumber": "08123456789",
        "role": app_state.role if app_state.role else "User",
        "point": 0,
        "kecamatan": "Bandung Wetan",
        "profile_image": "img/default_profile.png"
    }

    # File picker untuk upload profile image
    def on_profile_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            # TODO: Save image to database
            profile_image.current.src = file.path
            page.update()
    
    file_picker = ft.FilePicker(on_result=on_profile_picked)
    page.overlay.append(file_picker)
    
    def on_upload_profile(e):
        file_picker.pick_files(
            allowed_extensions=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
            allow_multiple=False,
        )

    # Save profile handler
    def on_save_profile(e):
        # TODO: Implement save logic here
        print(f"Saving profile:")
        print(f"Username: {username_input.current.value}")
        print(f"Email: {email_input.current.value}")
        print(f"Phone: {phone_input.current.value}")
        print(f"Kecamatan: {kecamatan_input.current.value}")
        
        # Show success dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Success", color="#000000"),
            content=ft.Text("Profile updated successfully!", color="#000000"),
            actions=[
                ft.TextButton("OK", on_click=lambda x: (setattr(dialog, 'open', False), page.update()))
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # Change password handler
    def on_change_password(e):
        # TODO: Implement password change logic
        if new_password.current.value != confirm_password.current.value:
            error_dialog = ft.AlertDialog(
                title=ft.Text("Error", color="#d32f2f"),
                content=ft.Text("New password and confirmation don't match!", color="#000000"),
                actions=[
                    ft.TextButton("OK", on_click=lambda x: (setattr(error_dialog, 'open', False), page.update()))
                ],
            )
            page.overlay.append(error_dialog)
            error_dialog.open = True
            page.update()
            return
        
        print(f"Changing password:")
        print(f"Current: {current_password.current.value}")
        print(f"New: {new_password.current.value}")
        
        # Clear password fields
        current_password.current.value = ""
        new_password.current.value = ""
        confirm_password.current.value = ""
        
        # Show success dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Success", color="#000000"),
            content=ft.Text("Password changed successfully!", color="#000000"),
            actions=[
                ft.TextButton("OK", on_click=lambda x: (setattr(dialog, 'open', False), page.update()))
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # Top navigation bar
    top_nav = create_navbar(page, "profile")

    # Profile page content
    profile_content = ft.Container(
        content=ft.Column(
            [
                # Page Header
                ft.Text("My Profile", size=32, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Container(height=20),
                
                # Main content in two columns
                ft.Row(
                    [
                        # Left column - Profile image and info
                        ft.Container(
                            content=ft.Column(
                                [
                                    # Profile Image
                                    ft.Container(
                                        content=ft.Image(
                                            ref=profile_image,
                                            src=user_data.get("profile_image", "img/default_profile.png"),
                                            fit=ft.ImageFit.COVER,
                                        ),
                                        width=250,
                                        height=250,
                                        border_radius=125,
                                        border=ft.border.all(4, "#1e8c45"),
                                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                    ),
                                    ft.Container(height=20),
                                    
                                    # Upload button
                                    ft.ElevatedButton(
                                        "Change Profile Picture",
                                        icon=ft.Icons.CAMERA_ALT,
                                        width=250,
                                        bgcolor="#1e8c45",
                                        color="white",
                                        on_click=on_upload_profile,
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=13, font_family="PoppinsSBold"),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                    ft.Container(height=20),
                                    
                                    # User info card
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Account Information", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                            ft.Divider(height=15, color="#e0e0e0"),
                                            ft.Row([
                                                ft.Icon(ft.Icons.BADGE, color="#1e8c45", size=20),
                                                ft.Column([
                                                    ft.Text("User ID", size=11, color="#666666"),
                                                    ft.Text(user_data["id"], size=13, weight=ft.FontWeight.BOLD, color="#000000"),
                                                ], spacing=2),
                                            ], spacing=10),
                                            ft.Container(height=10),
                                            ft.Row([
                                                ft.Icon(ft.Icons.PERSON, color="#1e8c45", size=20),
                                                ft.Column([
                                                    ft.Text("Role", size=11, color="#666666"),
                                                    ft.Text(user_data["role"], size=13, weight=ft.FontWeight.BOLD, color="#000000"),
                                                ], spacing=2),
                                            ], spacing=10),
                                            ft.Container(height=10),
                                            ft.Row([
                                                ft.Icon(ft.Icons.STAR, color="#1e8c45", size=20),
                                                ft.Column([
                                                    ft.Text("Total Points", size=11, color="#666666"),
                                                    ft.Text(str(user_data["point"]), size=13, weight=ft.FontWeight.BOLD, color="#000000"),
                                                ], spacing=2),
                                            ], spacing=10),
                                        ], spacing=5),
                                        width=250,
                                        padding=20,
                                        border=ft.border.all(1, "#e0e0e0"),
                                        border_radius=12,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                            ),
                            width=300,
                        ),
                        
                        ft.Container(width=40),
                        
                        # Right column - Edit form
                        ft.Container(
                            content=ft.Column(
                                [
                                    # Personal Information Section
                                    ft.Text("Personal Information", size=20, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Container(height=15),
                                    
                                    # Username
                                    ft.TextField(
                                        ref=username_input,
                                        label="Username *",
                                        value=user_data["username"],
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                        prefix_icon=ft.Icons.PERSON_OUTLINE,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Email
                                    ft.TextField(
                                        ref=email_input,
                                        label="Email *",
                                        value=user_data["email"],
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                        prefix_icon=ft.Icons.EMAIL_OUTLINED,
                                        keyboard_type=ft.KeyboardType.EMAIL,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Phone Number
                                    ft.TextField(
                                        ref=phone_input,
                                        label="Phone Number *",
                                        value=user_data["phonenumber"],
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                        prefix_icon=ft.Icons.PHONE_OUTLINED,
                                        keyboard_type=ft.KeyboardType.PHONE,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Kecamatan
                                    ft.TextField(
                                        ref=kecamatan_input,
                                        label="Kecamatan *",
                                        value=user_data["kecamatan"],
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                        prefix_icon=ft.Icons.LOCATION_ON_OUTLINED,
                                    ),
                                    ft.Container(height=25),
                                    
                                    # Save button
                                    ft.ElevatedButton(
                                        "Save Changes",
                                        icon=ft.Icons.SAVE,
                                        on_click=on_save_profile,
                                        bgcolor="#1e8c45",
                                        color="white",
                                        height=45,
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=14, font_family="PoppinsSBold"),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                    
                                    ft.Divider(height=40, color="#e0e0e0"),
                                    
                                    # Change Password Section
                                    ft.Text("Change Password", size=20, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Container(height=15),
                                    
                                    # Current Password
                                    ft.TextField(
                                        ref=current_password,
                                        label="Current Password",
                                        password=True,
                                        can_reveal_password=True,
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                        prefix_icon=ft.Icons.LOCK_OUTLINE,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # New Password
                                    ft.TextField(
                                        ref=new_password,
                                        label="New Password",
                                        password=True,
                                        can_reveal_password=True,
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                        prefix_icon=ft.Icons.LOCK_OUTLINE,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Confirm Password
                                    ft.TextField(
                                        ref=confirm_password,
                                        label="Confirm New Password",
                                        password=True,
                                        can_reveal_password=True,
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                        prefix_icon=ft.Icons.LOCK_OUTLINE,
                                    ),
                                    ft.Container(height=25),
                                    
                                    # Change Password button
                                    ft.ElevatedButton(
                                        "Change Password",
                                        icon=ft.Icons.KEY,
                                        on_click=on_change_password,
                                        bgcolor="#d32f2f",
                                        color="white",
                                        height=45,
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=14, font_family="PoppinsSBold"),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                                spacing=0,
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
        expand=True,
    )

    # Main container
    main_container = ft.Column(
        [
            top_nav,
            profile_content,
        ],
        expand=True,
    )

    page.add(main_container)
