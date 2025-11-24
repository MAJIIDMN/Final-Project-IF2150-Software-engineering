import flet as ft
from components.shared import create_header, create_sidebar

def AddressView(page, order_state):
    
    def district_changed(e):
        order_state.district = e.control.value
    
    def address_changed(e):
        order_state.address = e.control.value
    
    def notify_changed(e):
        order_state.notify_on_arrival = e.control.value
    
    def back_step(e):
        page.go("/order/general-details")
    
    def next_step(e):
        page.go("/order/date-and-time")
    
    # Main content
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Text(
                    "Address",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#212121",
                ),
                ft.Text(
                    "Add the address where a waste collector should arrive",
                    size=14,
                    color="#757575",
                ),
                ft.Container(height=30),
                ft.Column(
                    controls=[
                        ft.Text("City", size=12, color="#757575"),
                        ft.Dropdown(
                            width=400,
                            options=[
                                ft.dropdown.Option("Bandung"),
                                ft.dropdown.Option("Jakarta"),
                                ft.dropdown.Option("Surabaya"),
                            ],
                            value=order_state.district if order_state.district else "Bandung",
                            border_color="#e0e0e0",
                            on_change=district_changed,
                            color="#000000",
                        ),
                    ],
                    spacing=5,
                ),
                ft.Container(height=20),
                ft.Column(
                    controls=[
                        ft.Text("Address", size=12, color="#757575"),
                        ft.TextField(
                            width=400,
                            value=order_state.address if order_state.address else "Jl. Ganesha No. 10, Lb. Siliwangi",
                            border_color="#e0e0e0",
                            on_change=address_changed,
                            color="#000000",
                        ),
                    ],
                    spacing=5,
                ),
                ft.Container(height=20),
                # Address suggestion card
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(name=ft.Icons.MAP_OUTLINED, size=40, color="#2e7d32"),
                                width=80,
                                height=80,
                                bgcolor="#e8f5e9",
                                border_radius=8,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Bandung", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Text("Jl. Ganesha No. 10,\nLb. Siliwangi", size=13, color="#757575"),
                                ],
                                spacing=5,
                            ),
                        ],
                        spacing=15,
                    ),
                    bgcolor="white",
                    border=ft.border.all(1, "#e0e0e0"),
                    border_radius=12,
                    padding=20,
                    width=400,
                ),
                ft.Container(height=30),
                ft.Column(
                    controls=[
                        ft.Text("Add an attachment", size=14, color="#757575"),
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.ADD, color="#2e7d32"),
                            width=60,
                            height=60,
                            border=ft.border.all(2, "#e0e0e0"),
                            border_radius=8,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=order_state.notify_on_arrival,
                            fill_color="#2e7d32",
                            check_color="white"
                        ),
                        ft.Text("Notify me by phone when the waste collector arrives", size=13, color="#000000"),
                    ],
                    spacing=10,
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Back",
                            width=120,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor="white",
                                color="#2e7d32",
                            ),
                            on_click=back_step,
                        ),
                        ft.ElevatedButton(
                            "Next Step",
                            width=120,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor="#2e7d32",
                                color="white",
                            ),
                            on_click=next_step,
                        ),
                    ],
                    spacing=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor="white",
        expand=True,
        padding=40,
    )
    
    # Layout with map background
    content = ft.Stack(
        controls=[
            # Map background placeholder
            ft.Container(
                bgcolor="#e0e0e0",
                expand=True,
            ),
            # White card with form
            ft.Row(
                controls=[
                    create_sidebar(page, 2, order_state),
                    ft.Container(
                        content=main_content,
                        bgcolor="white",
                        border_radius=12,
                        margin=40,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.Colors.with_opacity(0.1, "#000000"),
                        ),
                        width=500,
                    ),
                ],
                spacing=0,
            ),
        ],
        expand=True,
    )
    
    return ft.Container(
        content=ft.Column(
            controls=[
                create_header(page),
                content,
            ],
            spacing=0,
            expand=True,
        ),
        padding=0,
        expand=True,
    )