import flet as ft
from views.components.navbar import create_navbar
from views.components import Alert
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
    
    # Refs untuk buttons
    save_email_btn = ft.Ref[ft.ElevatedButton]()
    save_changes_btn = ft.Ref[ft.ElevatedButton]()
    change_password_btn = ft.Ref[ft.ElevatedButton]()

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
    
    # Track original data for validation
    original_email = user_data.get("email", "")
    original_phone = user_data.get("phonenumber", "")
    original_kecamatan = user_data.get("kecamatan", "")
    email_verified = False

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
    
    # Validation functions for buttons
    def check_email_changed(e):
        """Check if email changed and enable/disable save email button"""
        if email_input.current and save_email_btn.current:
            email_changed = email_input.current.value.strip() != original_email
            save_email_btn.current.disabled = not email_changed
            page.update()
    
    def check_profile_changed(e):
        """Check if phone/kecamatan changed and enable/disable save changes button"""
        if phone_input.current and kecamatan_input.current and save_changes_btn.current:
            phone_changed = phone_input.current.value.strip() != original_phone
            kecamatan_changed = kecamatan_input.current.value.strip() != original_kecamatan
            save_changes_btn.current.disabled = not (phone_changed or kecamatan_changed)
            page.update()
    
    def check_password_fields(e):
        """Check password fields and enable/disable change password button"""
        if current_password.current and new_password.current and confirm_password.current and change_password_btn.current:
            # Check if all fields filled
            all_filled = (
                current_password.current.value and 
                new_password.current.value and 
                confirm_password.current.value
            )
            # Check if new password matches confirm
            passwords_match = new_password.current.value == confirm_password.current.value
            
            # Show error if passwords don't match
            if confirm_password.current.value and not passwords_match:
                confirm_password.current.error_text = "Password confirmation does not match"
            else:
                confirm_password.current.error_text = None
            
            change_password_btn.current.disabled = not (all_filled and passwords_match)
            page.update()
    
    # Email change handler
    def on_save_email(e):
        nonlocal email_verified, original_email
        new_email = email_input.current.value.strip()
        
        # If email hasn't changed, just show info
        if new_email == original_email:
            info_dialog = ft.AlertDialog(
                title=ft.Text("Info", color="#000000"),
                content=ft.Text("Email has not been changed.", color="#000000"),
                actions=[
                    ft.TextButton("OK", on_click=lambda x: (setattr(info_dialog, 'open', False), page.update()))
                ],
            )
            page.overlay.append(info_dialog)
            info_dialog.open = True
            page.update()
            return
        
        # If email changed, require verification
        email_verified = False
        
        def on_verification_success():
            nonlocal email_verified, original_email
            email_verified = True
            original_email = new_email
            # TODO: Save email to database here
            # Disable save email button after successful save
            if save_email_btn.current:
                save_email_btn.current.disabled = True
            success_dialog = ft.AlertDialog(
                title=ft.Text("Success", color="#000000"),
                content=ft.Text("Email verified and updated successfully!", color="#000000"),
                actions=[
                    ft.TextButton("OK", on_click=lambda x: (setattr(success_dialog, 'open', False), page.update()))
                ],
            )
            page.overlay.append(success_dialog)
            success_dialog.open = True
            page.update()
        
        # Show verification dialog
        verify_dialog = Alert.email_verification_dialog(page, new_email, on_verification_success)
        page.overlay.append(verify_dialog)
        verify_dialog.open = True
        page.update()

    # Save profile handler
    def on_save_profile(e):
        # Check if email changed but not saved
        current_email = email_input.current.value.strip()
        if current_email != original_email:
            error_dialog = ft.AlertDialog(
                title=ft.Text("Email Not Saved", color="#d32f2f"),
                content=ft.Text("Please save your email changes first before saving other profile changes.", color="#000000"),
                actions=[
                    ft.TextButton("OK", on_click=lambda x: (setattr(error_dialog, 'open', False), page.update()))
                ],
            )
            page.overlay.append(error_dialog)
            error_dialog.open = True
            page.update()
            return
        
        def confirm_save(e):
            nonlocal original_phone, original_kecamatan
            # TODO: Implement save logic here
            print(f"Saving profile:")
            print(f"Email: {email_input.current.value}")
            print(f"Phone: {phone_input.current.value}")
            print(f"Kecamatan: {kecamatan_input.current.value}")
            
            # Update original values after save
            original_phone = phone_input.current.value.strip()
            original_kecamatan = kecamatan_input.current.value.strip()
            
            # Disable save changes button after successful save
            if save_changes_btn.current:
                save_changes_btn.current.disabled = True
            
            # Show success dialog
            success_dialog = ft.AlertDialog(
                title=ft.Text("Success", color="#000000"),
                content=ft.Text("Profile updated successfully!", color="#000000"),
                actions=[
                    ft.TextButton("OK", on_click=lambda x: (setattr(success_dialog, 'open', False), page.update()))
                ],
            )
            page.overlay.append(success_dialog)
            success_dialog.open = True
            page.update()
        
        # Show confirmation dialog
        dialog = Alert.confirm_alert_dialog(
            "Confirm Save",
            "Are you sure you want to save these changes?",
            confirm_save
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
        
        def confirm_change(e):
            print(f"Changing password:")
            print(f"Current: {current_password.current.value}")
            print(f"New: {new_password.current.value}")
            
            # Clear password fields
            current_password.current.value = ""
            new_password.current.value = ""
            confirm_password.current.value = ""
            
            # Disable button after clearing fields
            if change_password_btn.current:
                change_password_btn.current.disabled = True
            
            # Show success dialog
            success_dialog = ft.AlertDialog(
                title=ft.Text("Success", color="#000000"),
                content=ft.Text("Password changed successfully!", color="#000000"),
                actions=[
                    ft.TextButton("OK", on_click=lambda x: (setattr(success_dialog, 'open', False), page.update()))
                ],
            )
            page.overlay.append(success_dialog)
            success_dialog.open = True
            page.update()
        
        # Show confirmation dialog
        dialog = Alert.confirm_alert_dialog(
            "Confirm Password Change",
            "Are you sure you want to change your password?",
            confirm_change
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
                                                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color="#1e8c45", size=20),
                                                ft.Column([
                                                    ft.Text("Username", size=11, color="#666666"),
                                                    ft.Text(user_data["username"], size=13, weight=ft.FontWeight.BOLD, color="#000000"),
                                                ], spacing=2),
                                            ], spacing=10),
                                            ft.Container(height=10),
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
                                    
                                    # Email with Save button
                                    ft.Row([
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
                                            expand=True,
                                            on_change=check_email_changed,
                                        ),
                                        ft.Container(width=10),
                                        ft.ElevatedButton(
                                            "Save Email",
                                            ref=save_email_btn,
                                            icon=ft.Icons.SAVE,
                                            on_click=on_save_email,
                                            bgcolor="#1e8c45",
                                            color="white",
                                            height=55,
                                            disabled=True,
                                            style=ft.ButtonStyle(
                                                text_style=ft.TextStyle(size=13, font_family="PoppinsSBold"),
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                            ),
                                        ),
                                    ], spacing=0),
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
                                        on_change=check_profile_changed,
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
                                        on_change=check_profile_changed,
                                    ),
                                    ft.Container(height=25),
                                    
                                    # Save button
                                    ft.ElevatedButton(
                                        "Save Changes",
                                        ref=save_changes_btn,
                                        icon=ft.Icons.SAVE,
                                        on_click=on_save_profile,
                                        bgcolor="#1e8c45",
                                        color="white",
                                        height=45,
                                        disabled=True,
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
                                        on_change=check_password_fields,
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
                                        on_change=check_password_fields,
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
                                        on_change=check_password_fields,
                                    ),
                                    ft.Container(height=25),
                                    
                                    # Change Password button
                                    ft.ElevatedButton(
                                        "Change Password",
                                        ref=change_password_btn,
                                        icon=ft.Icons.KEY,
                                        on_click=on_change_password,
                                        bgcolor="#d32f2f",
                                        color="white",
                                        height=45,
                                        disabled=True,
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
