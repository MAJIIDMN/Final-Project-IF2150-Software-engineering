import flet as ft
from components.shared import create_sidebar

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
                            hint_text="",
                            border_color="#e0e0e0",
                            on_change=address_changed,
                            color="#000000",
                        ),
                    ],
                    spacing=5,
                ),
                ft.Container(height=20),
                ft.Container(height=30),
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=order_state.notify_on_arrival,
                            fill_color="white",
                            check_color="#2e7d32",
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
                width=page.window_width - sidebar_ctrl.width if page.window_width else 940,
                height=page.window_height - 140 if page.window_height else 1024,
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