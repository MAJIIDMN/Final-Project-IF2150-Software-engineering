import flet as ft
from components.shared import create_sidebar

def NavigationView(page, order_state):
    def call_collector(e):
        phone = getattr(order_state, "collector_phone", None) or "6281234567890"
        page.launch_url(f"https://wa.me/{phone}")

    def chat_collector(e):
        phone = getattr(order_state, "collector_phone", None) or "6281234567890"
        text = "Hello, I would like to ask about my waste pickup order"
        import urllib.parse
        encoded = urllib.parse.quote(text)
        page.launch_url(f"https://wa.me/{phone}?text={encoded}")

    # Waste collector information card
    collector_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Waste Collector Information", size=14, weight=ft.FontWeight.BOLD, color="black"),
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
                                ft.Text("Vincent R", size=14, weight=ft.FontWeight.BOLD, color="black"),
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
                                        bgcolor="#2e7d32",
                                        color="white",
                                    ),
                                    height=35,
                                    width=80,
                                    on_click=call_collector,
                                ),
                                ft.ElevatedButton(
                                    "Chat",
                                    style=ft.ButtonStyle(
                                        bgcolor="white",
                                        color="#2e7d32",
                                    ),
                                    height=35,
                                    width=80,
                                    on_click=chat_collector,
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
            ],
            spacing=15,
        ),
        bgcolor="white",
        border=ft.border.all(1, "#e0e0e0"),
        border_radius=12,
        padding=20,
        width=380,
    )
    
    # Order information card
    order_info_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Order Information", size=14, weight=ft.FontWeight.BOLD, color="black"),
                ft.Divider(height=1, color="#e0e0e0"),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Type", size=11, color="#757575"),
                                ft.Text(", ".join(order_state.waste_types) if order_state.waste_types else "Plastic Bottles", 
                                       size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                        ft.Container(width=30),
                        ft.Column(
                            controls=[
                                ft.Text("Weight (min. 3 kg)", size=11, color="#757575"),
                                ft.Text(f"{order_state.weight} kg" if order_state.weight else "5 kg", 
                                       size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Condition", size=11, color="#757575"),
                                ft.Text(order_state.condition, size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                    ],
                ),
                ft.Divider(height=1, color="#e0e0e0"),
                ft.Column(
                    controls=[
                        ft.Text("Points Gained", size=11, color="#757575"),
                        ft.Text(
                            f"+ {order_state.point_gained:.2f} points" if order_state.point_gained else "+ 0.00 points",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#2e7d32",
                        ),
                    ],
                    spacing=2,
                ),
                ft.ElevatedButton(
                    "Cancel",
                    width=320,
                    height=45,
                    style=ft.ButtonStyle(
                        bgcolor="#f44336",
                        color="white",
                    ),
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
                    "Navigation",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#212121",
                ),
                ft.Text(
                    "Find out where your waste collector is",
                    size=14,
                    color="#757575",
                ),
                ft.Container(height=20),
                collector_card,
                ft.Container(height=20),
                order_info_card,
                ft.Container(height=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor="white",
        expand=False,
        padding=40,
    )
    
    # Layout with map background showing route
    content = ft.Stack(
        controls=[
            # Map background with route (placeholder - would be actual map in production)
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "Map with Route\n58 min\nEvery 15 min: 1 hr 5 min",
                                text_align=ft.TextAlign.CENTER,
                                color="#757575",
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#e0e0e0",
                expand=True,
            ),
            # Sidebar and content
            ft.Row(
                controls=[
                    create_sidebar(page, 4, order_state),
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