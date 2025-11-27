import flet as ft

def create_alert_dialog(title, content, on_ok=None):
    dialog = ft.AlertDialog(
        title=ft.Text(title, weight=ft.FontWeight.BOLD, color="#1e8c45"),
        content=ft.Text(content, color="#000000"),
        actions=[
            ft.TextButton(
                "OK",
                style=ft.ButtonStyle(color="#000000"),
                on_click=lambda e: (
                    setattr(dialog, 'open', False),
                    on_ok(e) if on_ok else None,
                    e.page.update()
                )
            )
        ],
        bgcolor="#ffffff"
    )
    return dialog

def confirm_alert_dialog(title, content, on_confirm):
    dialog = ft.AlertDialog(
        title=ft.Text(title, weight=ft.FontWeight.BOLD, color="#1e8c45"),
        content=ft.Text(content, color="#1e8c45"),
        actions=[
            ft.TextButton(
                "Cancel",
                style=ft.ButtonStyle(color="#999999"),
                on_click=lambda e: (
                    setattr(dialog, 'open', False),
                    e.page.update()
                )
            ),
            ft.TextButton(
                "Confirm",
                style=ft.ButtonStyle(color="#1e8c45"),
                on_click=lambda e: (
                    setattr(dialog, 'open', False),
                    on_confirm(e),
                    e.page.update()
                )
            )
        ],
        bgcolor="#ffffff"
    )
    return dialog

def delete_confirm_dialog(title, item_name, on_delete):
    dialog = ft.AlertDialog(
        title=ft.Text(title, weight=ft.FontWeight.BOLD, color="#1e8c45"),
        content=ft.Text(f"Are you sure you want to delete '{item_name}'?", color="#1e8c45"),
        actions=[
            ft.TextButton(
                "Cancel",
                style=ft.ButtonStyle(color="#999999"),
                on_click=lambda e: (
                    setattr(dialog, 'open', False),
                    e.page.update()
                )
            ),
            ft.TextButton(
                "Delete",
                style=ft.ButtonStyle(color="#e53935"),
                on_click=lambda e: (
                    setattr(dialog, 'open', False),
                    on_delete(e),
                    e.page.update()
                )
            )
        ],
        bgcolor="#ffffff"
    )
    return dialog

def email_verification_dialog(page, new_email, on_verify_success):
    code_input = ft.Ref[ft.TextField]()
    error_text = ft.Ref[ft.Text]()
    
    def send_verification_code(e):
        # TODO: Implement send email verification code logic
        # Show success message
        error_text.current.value = "Verification code sent to your email!"
        error_text.current.color = "#1e8c45"
        page.update()
    
    def verify_code(e):
        # TODO: Implement code verification logic
        entered_code = code_input.current.value.strip()
        
        if not entered_code:
            error_text.current.value = "Please enter the verification code"
            error_text.current.color = "#e53935"
            page.update()
            return
        
        # Mock verification - replace with actual verification
        correct_code = "123456"  # TODO: Get this from backend
        
        if entered_code == correct_code:
            dialog.open = False
            page.update()
            if on_verify_success:
                on_verify_success()
        else:
            error_text.current.value = "Invalid verification code. Please try again."
            error_text.current.color = "#e53935"
            code_input.current.value = ""
            page.update()
    
    dialog = ft.AlertDialog(
        title=ft.Text("Verify Email Change", weight=ft.FontWeight.BOLD, color="#1e8c45"),
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    f"A verification code will be sent to:",
                    size=13,
                    color="#666666"
                ),
                ft.Text(
                    new_email,
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),
                ft.Container(height=10),
                ft.TextField(
                    ref=code_input,
                    label="Verification Code",
                    hint_text="Enter 6-digit code",
                    border_color="#e0e0e0",
                    focused_border_color="#1e8c45",
                    text_style=ft.TextStyle(size=14, color="#000000"),
                    max_length=6,
                    keyboard_type=ft.KeyboardType.NUMBER,
                ),
                ft.Container(height=5),
                ft.Text(
                    ref=error_text,
                    value="",
                    size=12,
                    color="#e53935"
                ),
            ], tight=True),
            width=350,
        ),
        actions=[
            ft.TextButton(
                "Send Code",
                style=ft.ButtonStyle(color="#1e8c45"),
                on_click=send_verification_code
            ),
            ft.TextButton(
                "Cancel",
                style=ft.ButtonStyle(color="#999999"),
                on_click=lambda e: (
                    setattr(dialog, 'open', False),
                    page.update()
                )
            ),
            ft.TextButton(
                "Verify",
                style=ft.ButtonStyle(color="#1e8c45"),
                on_click=verify_code
            ),
        ],
        bgcolor="#ffffff"
    )
    return dialog