import flet as ft

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
        padding=ft.padding.only(left=20, top=28, right=28, bottom=36),
        margin=ft.margin.only(right=40),
        bgcolor="white",
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.08, "#000000"),
        ),
    )