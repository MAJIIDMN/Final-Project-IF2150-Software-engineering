import flet as ft
from models.state import AppState
from controllers.account_controller import AccountController

app_state = AppState()
acc_controller = AccountController()

def create_navbar(page):
    point = acc_controller.get_point(app_state.username)
    def go_to_point_mart(e):
        page.clean()
        page.point_mart_main(page)
    def go_to_home(e):
        page.clean()
        page.login_main(page)
    def go_to_order(e):
        print("Go to Order - Not Implemented Yet")
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
                            style=ft.ButtonStyle(color="white"),
                            on_click=go_to_home,
                            ),
                        ft.TextButton(
                            "Order", 
                            style=ft.ButtonStyle(color="white"),
                            on_click=go_to_order,
                            ),
                        ft.TextButton(
                            "Point Mart",
                            style=ft.ButtonStyle(color="white"), 
                            on_click=go_to_point_mart,
                            )
                            
                    ],
                    spacing=20,
                ),
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.STAR, color="white", size=20),
                                ft.Text(str(point), color="white", size=14),
                            ],
                            spacing=5,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.IconButton(
                            ft.Icons.PERSON,
                            icon_color="white",
                            on_click=lambda e: print("User clicked"),
                        ),
                    ],
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
        bgcolor="#145c39",
    )
    return navbar
