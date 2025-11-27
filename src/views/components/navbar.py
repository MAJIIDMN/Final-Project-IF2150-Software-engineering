import flet as ft
from models.state import AppState
from controllers.account_controller import AccountController

app_state = AppState()
acc_controller = AccountController()

def create_navbar(page, active_page="home"):
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
        page.home_main(page)
    
    def go_to_order(e):
        page.clean()
        if AppState.is_logged_in:
            page.order_main(page)
        else:
            page.login_main(page)
    def go_to_control(e):
        page.clean()
        page.admin_control_main(page)

    def go_to_info(e):
        page.clean()
        page.info_main(page)
    
    def go_to_profile(e):
        page.clean()
        page.profil_main(page)
    
    # Fungsi untuk membuat style text sesuai active page
    def get_nav_text_style(page_name):
        if page_name == active_page:
            return ft.TextStyle(size=20, weight=ft.FontWeight.BOLD, font_family="PoppinsBold")
        else:
            return ft.TextStyle(size=20, font_family="Poppins")
        
    profil = ft.PopupMenuButton(
                        icon=ft.Icons.PERSON,
                        icon_color="white",
                        bgcolor="#ffffff",
                        items=[
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.PERSON, color="#145c39", size=30),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    "Guest",
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="#000000"
                                                ),
                                                ft.Text(
                                                    "Guest",
                                                    size=11,
                                                    color="#000000"
                                                ),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.LOGIN, color="#145c39", size=20),
                                        ft.Text("Login", size=13, color="#000000"),
                                    ],
                                    spacing=5,
                                ),
                                on_click=logout,
                            ),
                        ],
                    )
    profil_popup = ft.PopupMenuButton(
                        icon=ft.Icons.PERSON,
                        icon_color="white",
                        bgcolor="#ffffff",
                        items=[
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.PERSON, color="#145c39", size=30),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    app_state.username if app_state.username else "Guest",
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="#000000"
                                                ),
                                                ft.Text(
                                                    app_state.role if app_state.role else "Guest",
                                                    size=11,
                                                    color="#000000"
                                                ),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                on_click=go_to_profile,
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.STAR, color="#145c39", size=20),
                                        ft.Text(f"{point} Points", size=13, color="#000000"),
                                    ],
                                    spacing=5,
                                ),
                                on_click=go_to_point_mart,
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.LOGOUT, color="#145c39", size=20),
                                        ft.Text("Logout", size=13, color="#000000"),
                                    ],
                                    spacing=5,
                                ),
                                on_click=logout,
                            ),
                        ],
                    )
    profil_admin = ft.PopupMenuButton(
                        icon=ft.Icons.PERSON,
                        icon_color="white",
                        bgcolor="#ffffff",
                        items=[
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.PERSON, color="#145c39", size=30),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    app_state.username if app_state.username else "Guest",
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="#000000"
                                                ),
                                                ft.Text(
                                                    app_state.role if app_state.role else "Guest",
                                                    size=11,
                                                    color="#000000"
                                                ),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                on_click=go_to_profile,
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.STAR, color="#145c39", size=20),
                                        ft.Text(f"{point} Points", size=13, color="#000000"),
                                    ],
                                    spacing=5,
                                ),
                                on_click=go_to_point_mart,
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.CONTROL_POINT, color="#145c39", size=20),
                                        ft.Text(f"Control", size=13, color="#000000"),
                                    ],
                                    spacing=5,
                                ),
                                on_click=go_to_control,
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.LOGOUT, color="#145c39", size=20),
                                        ft.Text("Logout", size=13, color="#000000"),
                                    ],
                                    spacing=5,
                                ),
                                on_click=logout,
                            ),
                        ],
                    )
    if AppState.is_logged_in:
        if app_state.role == "admin":
            profil = profil_admin
        else:
            profil = profil_popup
    
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
                            style=ft.ButtonStyle(color="white", text_style=get_nav_text_style("home")),
                            on_click=go_to_home,
                            ),
                        ft.TextButton(
                            "Info Sampah", 
                            style=ft.ButtonStyle(color="white", text_style=get_nav_text_style("info")),
                            on_click=go_to_info,
                            ),
                        ft.TextButton(
                            "Order", 
                            style=ft.ButtonStyle(color="white", text_style=get_nav_text_style("order")),
                            on_click=go_to_order,
                            ),
                        ft.TextButton(
                            "Point Mart",
                            style=ft.ButtonStyle(color="white", text_style=get_nav_text_style("point_mart")), 
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
                        profil,
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
