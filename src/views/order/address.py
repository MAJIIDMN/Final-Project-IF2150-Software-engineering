import flet as ft
from components.shared import create_sidebar

def AddressView(page, order_state):
    def file_picker_result(e):
        if e.files and len(e.files) > 0:
            f = e.files[0]
            order_state.attachment = f.name
            try:
                attachment_label.value = f.name
                attachment_label.color = "#000000"
                attachment_label.update()
            except NameError:
                pass
    def clear_attachment(e):
        order_state.attachment = None
        try:
            attachment_label.value = "No file selected"
            attachment_label.color = "#757575"
            attachment_label.update()
        except NameError:
            pass
    
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)
    
    def district_changed(e):
        order_state.district = e.control.value
    
    def address_changed(e):
        order_state.address = e.control.value
    
    def notify_changed(e):
        order_state.notify_on_arrival = e.control.value
    
    def back_step(e):
        page.go("/order/general-details")
    
    def next_step(e):
        # validation: district and address required
        sel_district = district_dropdown.value if 'district_dropdown' in locals() else (order_state.district if order_state.district else None)
        addr = address_field.value.strip() if 'address_field' in locals() and address_field.value else (order_state.address if order_state.address else "")
        if not sel_district or sel_district in ("- None -", ""):
            page.snack_bar = ft.SnackBar(ft.Text("Please select a city/district."))
            page.snack_bar.open = True
            page.update()
            return
        if not addr:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter the address."))
            page.snack_bar.open = True
            page.update()
            return
        if not getattr(order_state, "attachment", None):
            page.snack_bar = ft.SnackBar(ft.Text("Please add an attachment before continuing."))
            page.snack_bar.open = True
            page.update()
            return

        order_state.district = sel_district
        order_state.address = addr
        page.go("/order/date-and-time")
    
    card_height = page.window_height - 140 if page.window_height else 680

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
                        ft.Text("Subdistrict", size=12, color="#757575"),
                                district_dropdown := ft.Dropdown(
                                    width=400,
                                    options=[
                                        ft.dropdown.Option("- None -"),
                                        ft.dropdown.Option("Coblong"),
                                        ft.dropdown.Option("Sukajadi"),
                                        ft.dropdown.Option("Cidadap"),
                                        ft.dropdown.Option("Cicendo"),
                                        ft.dropdown.Option("Lengkong"),
                                    ],
                                    value=order_state.district if order_state.district else "- None -",
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
                        address_field := ft.TextField(
                            width=400,
                            value=order_state.address if order_state.address else "",
                            hint_text="Jl. Ganesha No. 10, Lb. Siliwangi",
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
                        attachment_label := ft.Text(
                                order_state.attachment if getattr(order_state, "attachment", None) else "No file selected",
                                size=12,
                                color="#757575",
                            ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(name=ft.Icons.ADD, color="#2e7d32"),
                                    width=60,
                                    height=60,
                                    border=ft.border.all(2, "#e0e0e0"),
                                    border_radius=8,
                                    alignment=ft.alignment.center,
                                    on_click=lambda e: file_picker.pick_files(allow_multiple=False),
                                ),
                                ft.Container(
                                    content=ft.Icon(name=ft.Icons.IMAGE_OUTLINED, size=30, color="white"),
                                    width=60,
                                    height=60,
                                    bgcolor="#4a90e2",
                                    border_radius=8,
                                    alignment=ft.alignment.center,
                                    on_click=clear_attachment,
                                ),
                            ],
                            spacing=10,
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
        expand=False,
        padding=40,
    )
    
    sidebar_ctrl = create_sidebar(page, 2, order_state)

    right_stack = ft.Stack(
        controls=[
            ft.Image(
                src="https://img.freepik.com/premium-vector/abstract-flat-map-city-plan-town-detailed-city-map_257312-609.jpg",
                fit=ft.ImageFit.COVER,
            ),
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
        expand=True,
    )

    # Layout with map background
    content = ft.Row(
        controls=[
            sidebar_ctrl,
            ft.Container(   # right panel, takes remaining width
                content=right_stack,
                expand=True,
            ),
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