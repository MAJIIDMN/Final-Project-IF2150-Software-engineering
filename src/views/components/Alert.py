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