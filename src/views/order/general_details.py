import flet as ft
from components.shared import create_header, create_sidebar

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def GeneralDetailsView(page, order_state):
    selected_types = order_state.waste_types if order_state.waste_types else []
    
    def toggle_type(e, waste_type):
        if waste_type in selected_types:
            selected_types.remove(waste_type)
            e.control.border = ft.border.all(2, "#e0e0e0")
        else:
            if len(selected_types) < 3:
                selected_types.append(waste_type)
                e.control.border = ft.border.all(2, "#2e7d32")
        e.control.update()
        update_points()
    
    def update_points():
        try:
            weight = float(weight_input.value) if weight_input.value else 0
            points = int(weight * len(selected_types) * 2)
            points_text.value = f"+ {points} points"
        except:
            points_text.value = "+ 0 points"
        points_text.update()
    
    def weight_changed(e):
        order_state.weight = e.control.value
        update_points()
    
    def condition_changed(e):
        order_state.condition = e.control.value
    
    def next_step(e):
        order_state.waste_types = selected_types.copy()
        page.go("/order/address")
    
    # Waste type images
    plastic_img = ft.Container(
        content=ft.Icon(name=ft.Icons.RECYCLING_OUTLINED, size=60, color="white"),
        width=120,
        height=80,
        bgcolor="#4a90e2",
        border_radius=10,
        alignment=ft.alignment.center,
        border=ft.border.all(2, "#2e7d32" if "Plastic Bottles" in selected_types else "#e0e0e0"),
        on_click=lambda e: toggle_type(e, "Plastic Bottles"),
    )
    
    metal_img = ft.Container(
        content=ft.Icon(name=ft.Icons.RECYCLING_OUTLINED, size=60, color="white"),
        width=120,
        height=80,
        bgcolor="#5dade2",
        border_radius=10,
        alignment=ft.alignment.center,
        border=ft.border.all(2, "#2e7d32" if "Metal" in selected_types else "#e0e0e0"),
        on_click=lambda e: toggle_type(e, "Metal"),
    )
    
    clothes_img = ft.Container(
        content=ft.Icon(name=ft.Icons.CHECKROOM_OUTLINED, size=60, color="white"),
        width=120,
        height=80,
        bgcolor="#85929e",
        border_radius=10,
        alignment=ft.alignment.center,
        border=ft.border.all(2, "#2e7d32" if "Clothes" in selected_types else "#e0e0e0"),
        on_click=lambda e: toggle_type(e, "Clothes"),
    )
    
    weight_input = ft.TextField(
        label="",
        value=order_state.weight if order_state.weight else "5",
        width=200,
        on_change=weight_changed,
        border_color="#e0e0e0",
        text_style=ft.TextStyle(color="#000000"),
        cursor_color="#000000",
    )
    
    points_text = ft.Text(
        "+ 0 points",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="#2e7d32",
    )
    
    # Main content
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Text(
                    "General Details",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#212121",
                ),
                ft.Text(
                    "Add the details of your waste",
                    size=14,
                    color="#000000",
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[plastic_img, metal_img, clothes_img],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Type (max. 3)", size=12, color="#000000"),
                                ft.Dropdown(
                                    width=200,
                                    options=[
                                        ft.dropdown.Option("Plastic Bottles"),
                                        ft.dropdown.Option("Metal"),
                                        ft.dropdown.Option("Clothes"),
                                    ],
                                    value="Plastic Bottles",
                                    border_color="#e0e0e0",
                                    color="#000000",
                                ),
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("", size=12, color="#757575"),
                                ft.Dropdown(
                                    width=200,
                                    options=[
                                        ft.dropdown.Option("Metal"),
                                        ft.dropdown.Option("Plastic"),
                                        ft.dropdown.Option("Clothes"),
                                    ],
                                    value="Metal",
                                    border_color="#e0e0e0",
                                    color="#000000",
                                ),
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("", size=12, color="#757575"),
                                ft.Dropdown(
                                    width=200,
                                    options=[
                                        ft.dropdown.Option("Clothes"),
                                        ft.dropdown.Option("Metal"),
                                        ft.dropdown.Option("Plastic"),
                                    ],
                                    value="Clothes",
                                    border_color="#e0e0e0",
                                    color="#000000",
                                ),
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Weight (kg) (min. 3 kg)", size=12, color="#000000"),
                                weight_input,
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Condition", size=12, color="#000000"),
                                ft.Dropdown(
                                    width=200,
                                    options=[
                                        ft.dropdown.Option("Good"),
                                        ft.dropdown.Option("Fair"),
                                        ft.dropdown.Option("Poor"),
                                    ],
                                    value=order_state.condition,
                                    border_color="#e0e0e0",
                                    on_change=condition_changed,
                                    color="#000000",
                                ),
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Points Gained", size=12, color="#000000"),
                                points_text,
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Add an attachment", size=14, color="#000000"),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(name=ft.Icons.ADD, color="#2e7d32"),
                                            width=60,
                                            height=60,
                                            border=ft.border.all(2, "#e0e0e0"),
                                            border_radius=8,
                                            alignment=ft.alignment.center,
                                        ),
                                        ft.Container(
                                            content=ft.Icon(name=ft.Icons.IMAGE_OUTLINED, size=30, color="white"),
                                            width=60,
                                            height=60,
                                            bgcolor="#4a90e2",
                                            border_radius=8,
                                            alignment=ft.alignment.center,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Container(width=100),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Checkbox(value=False, fill_color="#2e7d32", check_color="white"),
                                        ft.Text("You have sort and clean your anorganic waste", size=13, color="#000000"),
                                    ],
                                    spacing=10,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Checkbox(value=False, fill_color="#2e7d32", check_color="white"),
                                        ft.Text("You agree that this waste is recyclable", size=13, color="#000000"),
                                    ],
                                    spacing=10,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Checkbox(value=False, fill_color="#2e7d32", check_color="white"),
                                        ft.Text("You have read the waste information", size=13, color="#000000"),
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=15,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
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
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor="white",
        expand=True,
        padding=40,
    )
    
    # Layout
    content = ft.Row(
        controls=[
            create_sidebar(page, 1, order_state),
            main_content,
        ],
        spacing=0,
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