import flet as ft

def create_header(page):
    """Create the green header with navigation"""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SHOPPING_CART_OUTLINED, color="white", size=32),
                        ft.Text("GrowBak", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[
                        ft.TextButton("Home", style=ft.ButtonStyle(color="white")),
                        ft.TextButton("Order", style=ft.ButtonStyle(color="white")),
                        ft.TextButton("Point Mart", style=ft.ButtonStyle(color="white")),
                    ],
                    spacing=40,
                ),
                ft.Row(
                    controls=[
                        ft.Text("999 Points", color="white", size=14),
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.PERSON, color="white", size=20),
                            bgcolor="#4a7c59",
                            border_radius=20,
                            padding=8,
                        ),
                        ft.Text("User", color="white", size=14),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#2e7d32",
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
    )

def create_sidebar(page, current_step, order_state=None):
    steps = [
        {"number": 1, "label": "General Details", "route": "/order/general-details"},
        {"number": 2, "label": "Address", "route": "/order/address"},
        {"number": 3, "label": "Date and Time", "route": "/order/date-and-time"},
        {"number": 4, "label": "Navigation", "route": "/order/navigation"},
    ]
    
    def navigate_to_step(route):
        if current_step == 4:
            return
        
        step_key = route.split("/")[-1]
        if step_key == steps[current_step-1]["route"].split("/")[-1] or (order_state and step_key in order_state.completed_steps):
            page.go(route)
    
    sidebar_items = []
    for step in steps:
        is_current = step["number"] == current_step
        is_completed = order_state and step["route"].split("/")[-1] in order_state.completed_steps
        
        clickable = (current_step != 4) and (is_current or is_completed)
        
        item = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(str(step["number"]), color="white" if is_current else "#2e7d32"),
                        width=40,
                        height=40,
                        bgcolor="#2e7d32" if is_current else ("#e8f5e9" if is_completed else "#e0e0e0"),
                        border_radius=20,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(step["label"], color="#2e7d32" if (is_current or is_completed) else "#757575"),
                ],
                spacing=15,
            ),
            padding=15,
            on_click=lambda e, r=step["route"]: navigate_to_step(r) if clickable else None,
            opacity=1.0 if clickable else 0.5,  # grey
        )
        sidebar_items.append(item)
    
    return ft.Container(
        content=ft.Column(
            controls=sidebar_items,
            spacing=10,
        ),
        width=200,
        padding=20,
        bgcolor="white",
    )