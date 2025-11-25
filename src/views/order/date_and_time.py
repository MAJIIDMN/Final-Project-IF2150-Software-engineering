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
    
    # Stop point cards (timeline-style)
    def create_stop_card(stop_id, location, time, status_color=None, status_text=None, subdistrict=None, time2=None, location2=None, on_click=None):
        # Badge color indicates subdistrict (fallback to neutral green)
        subdistrict_colors = {
            "Fast": "#2e7d32",
            "Moderate": "#ff9800",
            "Slow": "#ff5722",
        }
        badge_text = subdistrict if subdistrict else (status_text if status_text else None)
        badge_color = subdistrict_colors.get(badge_text, "#2e7d32") if badge_text else None

        status_badge = None
        if badge_text:
            status_badge = ft.Container(
                content=ft.Text(badge_text, size=12, color="white", weight=ft.FontWeight.BOLD),
                bgcolor=badge_color,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
            )

        # layout timeline and two road labels as separate rows so dots and texts align
        dot_size = 10
        connector_height = 28
        timeline_col_width = 40

        # row 1: time label placed in the timeline column
        time_row = ft.Row(
            controls=[
                ft.Container(content=ft.Text(time, size=12, color="#757575"), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(),
            ],
        )

        # row 2: top dot aligned with top location
        top_row = ft.Row(
            controls=[
                ft.Container(content=ft.Container(width=dot_size, height=dot_size, bgcolor="#212121", border_radius=dot_size), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(content=ft.Text(location, size=15, color="#212121"), alignment=ft.alignment.center_left),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # row 3: connector line
        connector_row = ft.Row(
            controls=[
                ft.Container(content=ft.Container(width=2, height=connector_height, bgcolor="#e0e0e0"), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(),
            ],
        )

        # row 4: bottom dot aligned with bottom location (may differ via `location2`)
        bottom_loc_text = location2 if location2 is not None else location
        bottom_row = ft.Row(
            controls=[
                ft.Container(content=ft.Container(width=dot_size, height=dot_size, bgcolor="#212121", border_radius=dot_size), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(content=ft.Text(bottom_loc_text, size=15, color="#212121"), alignment=ft.alignment.center_left),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # optional bottom time label (under the bottom dot). if time2 not provided, reuse `time`.
        bottom_time_value = time2 if time2 is not None else time
        bottom_time_row = ft.Row(
            controls=[
                ft.Container(content=ft.Text(bottom_time_value, size=12, color="#757575"), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(),
            ],
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(stop_id, size=16, weight=ft.FontWeight.BOLD, color="#212121"),
                            status_badge if status_badge else ft.Container(),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=14),
                    time_row,
                    top_row,
                    connector_row,
                    bottom_row,
                    bottom_time_row,
                ],
                spacing=6,
            ),
            bgcolor="white",
            border=ft.border.all(1, "#f0f0f0"),
            border_radius=24,
            padding=24,
            width=500,
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=12, color=ft.Colors.with_opacity(0.06, "#000000")),
            on_click=on_click,
        )
    
    # Build collector card dynamically from `order_state.selected_collector_data`
    def build_collector_card():
        data = getattr(order_state, 'selected_collector_data', None)
        visible = getattr(order_state, 'show_collector', False)
        if not visible or not data:
            return ft.Container()

        name = data.get('name', 'Unknown')
        role = data.get('role', 'Waste Collector')
        experience = data.get('experience', '')
        id_number = data.get('id_number', '')
        vehicle = data.get('vehicle', '')
        license_plate = data.get('license_plate', '')

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Waste Collector Information", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
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
                                    ft.Text(name, size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Text(role, size=12, color="#757575"),
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
                                    ft.Text(experience, size=13, weight=ft.FontWeight.BOLD, color="#555555"),
                                ],
                                spacing=2,
                            ),
                            ft.Container(width=30),
                            ft.Column(
                                controls=[
                                    ft.Text("ID-Number", size=11, color="#757575"),
                                    ft.Text(id_number, size=13, weight=ft.FontWeight.BOLD, color="#555555"),
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
                                    ft.Text(vehicle, size=13, weight=ft.FontWeight.BOLD, color="#555555"),
                                ],
                                spacing=2,
                            ),
                            ft.Container(width=30),
                            ft.Column(
                                controls=[
                                    ft.Text("License Plate", size=11, color="#757575"),
                                    ft.Text(license_plate, size=13, weight=ft.FontWeight.BOLD, color="#555555"),
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

    # prepare dynamic stops data (use order_state.stops if provided)
    stops = getattr(order_state, 'stops', None)
    if not stops:
        stops = [
            {
                'id': 'ID 1111-2222',
                'location1': 'Jl. Siliwangi Dalam IV No.28, RT.06/RW.01',
                'location2': 'Jl. Siliwangi Dalam IV No.28, RT.06/RW.01',
                'time1': '02:30',
                'time2': '02:30',
                'status_text': 'Accepted',
            },
            {
                'id': 'ID 1111-2222',
                'location1': 'Jl. Tamansari No.43a/56',
                'location2': 'Jl. Tamansari No.43a/56',
                'time1': '02:40',
                'time2': '02:40',
            },
            {
                'id': 'ID 1111-2222',
                'location1': 'Jl. Raya Cirebon - Bandung, Sayang',
                'location2': 'Jl. Raya Cirebon - Bandung, Sayang',
                'time1': '03:30',
                'time2': '03:30',
                'status_text': 'Wait Pickup',
            },
            {
                'id': 'ID 1111-2222',
                'location1': 'Jl. Padasuka Atas Kampung Caringin 3 No.41',
                'location2': 'Jl. Padasuka Atas Kampung Caringin 3 No.41',
                'time1': '03:34',
                'time2': '03:34',
            },
        ]

    stop_controls = []
    # ensure flags exist
    if not hasattr(order_state, 'show_collector'):
        order_state.show_collector = False
    if not hasattr(order_state, 'selected_collector_data'):
        order_state.selected_collector_data = None

    def make_on_click(s):
        def _on_click(e):
            # set selected collector data from the stop's collector field (fallback sample)
            collector = s.get('collector', {
                'name': 'Vincent R',
                'role': 'Waste Collector',
                'experience': '12 years',
                'id_number': '1234-5678',
                'vehicle': 'Motorcycle',
                'license_plate': 'D 9999 FF',
            })
            order_state.selected_collector_data = collector
            order_state.show_collector = True
            page.update()
        return _on_click

    for s in stops:
        stop_controls.append(
            create_stop_card(
                s.get('id', 'ID'),
                s.get('location1', ''),
                s.get('time1', ''),
                status_text=s.get('status_text'),
                subdistrict=(order_state.district if getattr(order_state, 'district', None) else "Fast"),
                time2=s.get('time2'),
                location2=s.get('location2'),
                on_click=make_on_click(s),
            )
        )
        stop_controls.append(ft.Container(height=15))

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
                *stop_controls,
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
                content=build_collector_card(),
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