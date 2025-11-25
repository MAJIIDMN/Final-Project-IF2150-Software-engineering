import flet as ft
from views.navbar import create_navbar
from components.shared import create_sidebar

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def GeneralDetailsView(page, order_state):
    selected_types = order_state.waste_types if order_state.waste_types else []
    card_height = page.window_height - 140 if page.window_height else 680
    
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
    
    def dropdown_change(e):
        dd = [first_dropdown, second_dropdown, third_dropdown]

        for other in dd:
            if other is e.control:
                continue
            if e.control.value != "- None -" and e.control.value == other.value:
                # revert the one the user just changed
                e.control.value = "- None -"
                e.control.update()
                e.page.update()
                show_alert(e.page, "That item is already selected!")
                return
        update_points()

    def update_points():
        try:
            weight = float(weight_input.value) if weight_input.value else 0
            # points = int(weight * len(selected_types) * 2)

            val = [first_dropdown.value, second_dropdown.value, third_dropdown.value]
            # choose = [i for i in val if v and v!="- None -"]

            points = 0
            for i in val:
                if (i == "Plastic"):
                    points += 1
                elif (i == "Clothes"):
                    points += 2
                elif (i == "Metal"):
                    points += 3
            
            points *= weight
            points_text.value = f"+ {points} points"
            order_state.point_gained = points
        except:
            points_text.value = "+ 0 points"
        points_text.update()
    
    def weight_changed(e):
        order_state.weight = e.control.value
        update_points()
    
    def condition_changed(e):
        order_state.condition = e.control.value
    
    def next_step(e):
        # validate required fields before proceeding
        # waste types
        if len(selected_types) == 0:
            page.snack_bar = ft.SnackBar(ft.Text("Please select at least one waste type."))
            page.snack_bar.open = True
            page.update()
            return
        # weight
        w = weight_input.value.strip() if weight_input.value else ""
        try:
            wv = float(w)
        except:
            wv = 0
        if not w or wv < 3:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid weight (min. 3 kg)."))
            page.snack_bar.open = True
            page.update()
            return
        # condition
        if condition_dropdown.value in (None, "", "- None -"):
            page.snack_bar = ft.SnackBar(ft.Text("Please select the waste condition."))
            page.snack_bar.open = True
            page.update()
            return

        order_state.waste_types = selected_types.copy()
        order_state.weight = w
        order_state.condition = condition_dropdown.value
        page.go("/order/address")
    
    # Waste type images
    plastic_img = ft.Container(
        # content=ft.Icon(name=ft.Icons.RECYCLING_OUTLINED, size=60, color="white"),
        content=ft.Image(src="https://recykal.com/wp-content/uploads/2021/11/12c26-017154e4-47d7-45af-95ab-ad3b8e4ff3f9-1.jpg", width=120,height=80,fit=ft.ImageFit.COVER),
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
        value=order_state.weight if order_state.weight else "",
        hint_text="5",
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
    
    first_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("- None -"),
            ft.dropdown.Option("Plastic"),
            ft.dropdown.Option("Metal"),
            ft.dropdown.Option("Clothes"),
        ],
        value=selected_types[0] if selected_types else "- None -",
        border_color="#e0e0e0",
        color="#000000",
        on_change=dropdown_change,
    )

    second_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("- None -"),
            ft.dropdown.Option("Plastic"),
            ft.dropdown.Option("Metal"),
            ft.dropdown.Option("Clothes"),
        ],
        value="- None -",
        border_color="#e0e0e0",
        color="#000000",
        on_change=dropdown_change,
    )

    third_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("- None -"),
            ft.dropdown.Option("Plastic"),
            ft.dropdown.Option("Metal"),
            ft.dropdown.Option("Clothes"),
        ],
        value="- None -",
        border_color="#e0e0e0",
        color="#000000",
        on_change=dropdown_change,
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
                                first_dropdown,
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("", size=12, color="#757575"),
                                second_dropdown,
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("", size=12, color="#757575"),
                                third_dropdown,
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
                            controls = [
                                ft.Text("Weight (kg) (min. 3 kg)", size=12, color="#000000"),
                                weight_input,
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Condition", size=12, color="#000000"),
                                # condition dropdown
                                condition_dropdown := ft.Dropdown(
                                    width=200,
                                    options=[
                                        ft.dropdown.Option("- None -"),
                                        ft.dropdown.Option("Good"),
                                        ft.dropdown.Option("Fair"),
                                        ft.dropdown.Option("Poor"),
                                    ],
                                    value=order_state.condition if order_state.condition else "- None -",
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
        height=card_height,
        expand = True,
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
                content,
            ],
            spacing=0,
            expand=True,
        ),
        padding=0,
        expand=True,
    )