import flet as ft

def create_alert_dialog(title, content, on_ok=None):
    dialog = ft.AlertDialog(
        title=ft.Text(title, weight=ft.FontWeight.BOLD, color="#1e8c45"),
        content=ft.Text(content, color="#1e8c45"),
        actions=[
            ft.TextButton(
                "OK",
                style=ft.ButtonStyle(color="#1e8c45"),
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