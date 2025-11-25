import flet as ft
from models.state import AppState
from controllers.account_controller import AccountController

app_state = AppState()
acc_controller = AccountController()

def create_navbar(page):
    point = acc_controller.get_point(app_state.username)
    def logout(e):
        app_state.clear_state()
        page.clean()
        page.login_main(page)
    def go_to_point_mart(e):
        page.clean()
        if AppState.is_logged_in:
            page.point_mart_main(page)
        else:
            page.login_main(page)
    def go_to_home(e):
        page.clean()
        page.home_main(page) # Nanti diubah ke home
    def go_to_order(e):
        page.clean()
        if AppState.is_logged_in:
            page.order_main(page)
        else:
            page.login_main(page)
    navbar = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Image(src="img/logo_only.png", width=40),
                        ft.Text("GrowBak", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.TextButton(
                            "Home", 
                            style=ft.ButtonStyle(color="white", text_style=ft.TextStyle(size=20)),
                            on_click=go_to_home,
                            ),
                        ft.TextButton(
                            "Order", 
                            style=ft.ButtonStyle(color="white", text_style=ft.TextStyle(size=20)),
                            on_click=go_to_order,
                            ),
                        ft.TextButton(
                            "Point Mart",
                            style=ft.ButtonStyle(color="white", text_style=ft.TextStyle(size=20)), 
                            on_click=go_to_point_mart,
                            )
                            
                    ],
                    spacing=20,
                ),
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.STAR, color="white", size=25),
                                ft.Text(str(point), color="white", size=20),
                            ],
                            spacing=5,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.IconButton(
                            ft.Icons.PERSON,
                            icon_color="white",
                            on_click=logout,
                        ),
                    ],
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
        bgcolor="#145c39",
    )
    return navbar
