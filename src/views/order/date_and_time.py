import flet as ft
from components.shared import create_sidebar

def DateAndTimeView(page, order_state):
    
    def back_step(e):
        page.go("/order/address")
    
    def select_collector(e):
        order_state.selected_collector = "Vincent R"
        order_state.selected_date = "03/12/24"
        order_state.selected_time = "14:18"
        page.go("/order/navigation")
    
    # Stop point cards
    def create_stop_card(stop_id, location, time, status_color=None, status_text=None):
        status_badge = None
        if status_text:
            badge_colors = {
                "Accepted": "#4caf50",
                "Wait Pickup": "#ff9800",
                "On the go": "#2196f3",
            }
            status_badge = ft.Container(
                content=ft.Text(status_text, size=11, color="white", weight=ft.FontWeight.BOLD),
                bgcolor=badge_colors.get(status_text, "#757575"),
                padding=ft.padding.symmetric(horizontal=12, vertical=4),
                border_radius=12,
            )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(stop_id, size=16, weight=ft.FontWeight.BOLD),
                            status_badge if status_badge else ft.Container(),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, size=8, color="#757575"),
                            ft.Text(time, size=12, color="#757575"),
                        ],
                        spacing=5,
                    ),
                    ft.Text(location, size=13, color="#424242"),
                ],
                spacing=8,
            ),
            bgcolor="white",
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=12,
            padding=20,
            width=380,
        )
    
    # Waste collector card
    collector_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Waste Collector Information", size=14, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color="#e0e0e0"),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.PERSON, size=30, color="white"),
                            width=60,
                            height=60,
                            bgcolor="#4a90e2",
                            border_radius=30,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Vincent R", size=14, weight=ft.FontWeight.BOLD),
                                ft.Text("Waste Collector", size=12, color="#757575"),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    "Call",
                                    style=ft.ButtonStyle(
                                        bgcolor="white",
                                        color="#2e7d32",
                                    ),
                                    height=35,
                                ),
                                ft.ElevatedButton(
                                    "Chat",
                                    style=ft.ButtonStyle(
                                        bgcolor="white",
                                        color="#2e7d32",
                                    ),
                                    height=35,
                                ),
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=1, color="#e0e0e0"),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Experience", size=11, color="#757575"),
                                ft.Text("12 years", size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                        ft.Container(width=30),
                        ft.Column(
                            controls=[
                                ft.Text("ID-Number", size=11, color="#757575"),
                                ft.Text("1234-5678", size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Vehicle", size=11, color="#757575"),
                                ft.Text("Motorcycle", size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                        ft.Container(width=30),
                        ft.Column(
                            controls=[
                                ft.Text("License Plate", size=11, color="#757575"),
                                ft.Text("D 9999 FF", size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                    ],
                ),
                ft.ElevatedButton(
                    "Order",
                    width=300,
                    height=45,
                    style=ft.ButtonStyle(
                        bgcolor="#2e7d32",
                        color="white",
                    ),
                    on_click=select_collector,
                ),
            ],
            spacing=15,
        ),
        bgcolor="white",
        border=ft.border.all(1, "#e0e0e0"),
        border_radius=12,
        padding=20,
        width=380,
    )
    
    card_height = page.window_height - 140 if page.window_height else 680

    # Main content
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Text(
                    "Date and Time",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#212121",
                ),
                ft.Text(
                    "Confirm when your waste will be picked up",
                    size=14,
                    color="#757575",
                ),
                ft.Container(height=20),
                ft.TextField(
                    prefix_icon=ft.Icons.SEARCH,
                    hint_text="Search",
                    width=380,
                    border_color="#e0e0e0",
                ),
                ft.Container(height=20),
                create_stop_card(
                    "ID 1111-2222",
                    "Jl. Siliwangi Dalam IV No.28, RT.06/RW.01",
                    "02:30",
                    status_text="Accepted"
                ),
                ft.Container(height=15),
                create_stop_card(
                    "ID 1111-2222",
                    "Jl. Tamansari No.43a/56",
                    "02:40"
                ),
                ft.Container(height=15),
                create_stop_card(
                    "ID 1111-2222",
                    "Jl. Raya Cirebon - Bandung, Sayang",
                    "03:30",
                    status_text="Wait Pickup"
                ),
                ft.Container(height=15),
                create_stop_card(
                    "ID 1111-2222",
                    "Jl. Padasuka Atas Kampung Caringin 3 No.41",
                    "03:34"
                ),
                ft.Container(height=20),
                # collector_card moved to a floating panel (bottom-right)
                ft.Container(height=20),
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor="white",
        expand=False,
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
                    create_sidebar(page, 3, order_state),
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
                        height=card_height,
                    ),
                ],
                spacing=0,
            ),
            # floating collector card at bottom-right
            ft.Container(
                content=collector_card,
                right=40,
                bottom=40,
            ),
        ],
        expand=True,
    )
    
    return ft.Container(
        content=ft.Column(
            controls=[
                content,
            ],
            spacing=0,
            expand=True,
        ),
        padding=0,
        expand=True,
    )