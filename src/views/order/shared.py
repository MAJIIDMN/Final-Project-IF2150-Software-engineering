import flet as ft

def create_sidebar(page, current_step, order_state=None):
    steps = [
        {"number": 1, "label": "General Details", "route": "/order/general-details"},
        {"number": 2, "label": "Address", "route": "/order/address"},
        {"number": 3, "label": "Date and Time", "route": "/order/date-and-time"},
        {"number": 4, "label": "Navigation", "route": "/order/navigation"},
    ]
    
    def navigate_to_step(route):
        # allow navigation to the current step, any previous step, or any step marked completed
        step_key = route.split("/")[-1]
        # find the step number for this route
        step_index = next((s["number"] for s in steps if s["route"].split("/")[-1] == step_key), None)
        if step_index is None:
            return
        # allow if it's the current step, a previous step, or explicitly completed
        if step_index <= current_step or (order_state and step_key in order_state.completed_steps):
            page.go(route)
    
    sidebar_items = []
    # map each step number to a fixed icon (these will not change to indicate completion)
    icon_map = {
        1: ft.Icons.VISIBILITY,   
        2: ft.Icons.PLACE,        
        3: ft.Icons.ACCESS_TIME,  
        4: ft.Icons.ROUTE,        
    }
    for step in steps:
        is_less_than = step["number"] < current_step
        is_completed = order_state and step["route"].split("/")[-1] in order_state.completed_steps
        
        clickable = (is_less_than or is_completed)
        
        item = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            icon_map.get(step["number"], ft.Icons.LABEL),
                            color=("#155F39" if (is_less_than or is_completed) else "#757575"),
                        ),
                        width=40,
                        height=40,
                        bgcolor="#e0e0e0",
                        border_radius=20,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(step["label"], color="#2e7d32" if (is_less_than or is_completed) else "#757575"),
                ],
                spacing=15,
            ),
            padding=15,
            on_click=lambda e, r=step["route"]: navigate_to_step(r) if clickable else None,
            opacity=1.0 if clickable else 0.5,  
        )
        sidebar_items.append(item)
    
    return ft.Container(
        content=ft.Column(
            controls=sidebar_items,
            spacing=10,
        ),
        width=260,
        padding=ft.padding.only(left=20, top=28, right=48, bottom=36),
        margin=ft.margin.only(right=64),
        bgcolor="white",
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.08, "#000000"),
        ),
    )