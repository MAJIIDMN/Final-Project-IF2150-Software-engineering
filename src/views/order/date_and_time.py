import flet as ft
import random
from views.order.shared import create_sidebar

from services.database import DatabaseService
db = DatabaseService()

def DateAndTimeView(page, order_state):
    
    dur = 0

    # map district names to letter codes
    def district_to_code(name: str) -> str:
        if not name:
            return 'x'
        m = {
            'coblong': 'a',
            'sukajadi': 'b',
            'cidadap': 'c',
            'cicendo': 'd',
            'lengkong': 'e',
        }
        return m.get(str(name).strip().lower(), 'x')

    def get_map_path(map_districts: str) -> str:
        # returns the expected map image path for a map_districts key
        # Normalize pair ordering alphabetically so e.g. 'c_a' -> 'a_c'
        try:
            if not map_districts:
                return "img/order-bg-image.avif"
            parts = str(map_districts).strip().lower().split("_")
            # if we have at least two parts, sort the first two and join
            if len(parts) >= 2:
                a = parts[0].strip()
                b = parts[1].strip()
                pair = "_".join(sorted([a, b]))
                return f"src/services/{pair}.jpg"
            # fallback: single part
            part = parts[0].strip()
            return f"src/services/{part}.jpg"
        except Exception:
            # on any error, fallback to the default local image
            return "img/order-bg-image.avif"

    def back_step(e):
        page.go("/order/address")
    
    def select_collector(e):
        # show confirmation dialog because order cannot be cancelled
        row = getattr(order_state, 'selected_collector_data', None)
        if row is None:
            page.snack_bar = ft.SnackBar(ft.Text("No collector selected."))
            page.snack_bar.open = True
            page.update()
            return

        def _confirm_order(e_confirm):
            # apply selection to state
            order_state.selected_collector = row[1]
            order_state.selected_collector_id = row[0]
            order_state.selected_collector_experience = row[2]
            order_state.selected_collector_vehicle = row[3]
            order_state.selected_collector_plate = row[4]

            if not getattr(order_state, 'duration', None):
                order_state.duration = "14:18"

            # close dialog and navigate
            try:
                dialog.open = False
            except Exception:
                pass
            page.update()
            page.go("/order/navigation")

        def _cancel(e_cancel):
            try:
                dialog.open = False
            except Exception:
                pass
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirm Order"),
            content=ft.Text("This order cannot be cancelled after being placed. Do you want to proceed?"),
            actions=[
                ft.TextButton("Cancel", on_click=_cancel),
                ft.ElevatedButton("Confirm", on_click=_confirm_order, bgcolor="#2e7d32", color="white"),
            ],
        )
        page.dialog = dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    # Stop point cards (timeline-style)
    def create_stop_card(stop_id, loc1, loc2, time1, time2, wait_time, wc_id, on_click=None):
        wait_colors = {
            "Fast": "#2e7d32",
            "Moderate": "#ff9800",
            "Slow": "#ff5722",
        }
        badge_text = wait_time
        badge_color = wait_colors.get(badge_text, "#2e7d32") if badge_text else None

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
                ft.Container(content=ft.Text(time1, size=12, color="#757575"), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(),
            ],
        )

        # row 2: top dot aligned with top loc1
        top_row = ft.Row(
            controls=[
                ft.Container(content=ft.Container(width=dot_size, height=dot_size, bgcolor="#212121", border_radius=dot_size), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(content=ft.Text(loc1, size=15, color="#212121"), alignment=ft.alignment.center_left),
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

        # row 4: bottom dot aligned with bottom location (may differ via `loc2`)
        bottom_row = ft.Row(
            controls=[
                ft.Container(content=ft.Container(width=dot_size, height=dot_size, bgcolor="#212121", border_radius=dot_size), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(content=ft.Text(loc2, size=15, color="#212121"), alignment=ft.alignment.center_left),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        bottom_time_row = ft.Row(
            controls=[
                ft.Container(content=ft.Text(time2, size=12, color="#757575"), width=timeline_col_width, alignment=ft.alignment.center),
                ft.Container(width=12),
                ft.Container(),
            ],
        )

        return ft.Container(
            # key=ret_id,
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
    
    # Build collector card berdasarkan satu row collector dari tabel `wc`
    def build_collector_card(row):
        visible = getattr(order_state, 'show_collector', False)
        if not visible or row is None:
            return ft.Container()

        # row format: (id, name, experience, vehicle, platenumber)
        id_number = row[0]
        name = row[1]
        experience = row[2]
        vehicle = row[3]
        license_plate = row[4]
        role = "Waste Collector"

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
    
    # ================================================ #
    card_height = page.window_height - 140 if page.window_height else 680

    # helper: generate levels distribution
    def _generate_levels(n):
        if random.random() < 0.12:
            chosen_level = random.choice(["Fast", "Moderate", "Slow"])
            return [chosen_level] * n
        if n == 1:
            return [random.choice(["Fast", "Moderate", "Slow"])]
        if n == 2:
            pair_options = [["Fast", "Moderate"], ["Moderate", "Slow"], ["Fast", "Slow"]]
            chosen_pair = random.choices(pair_options, weights=[0.6,0.2,0.2], k=1)[0]
            return [chosen_pair[0], chosen_pair[1]]
        # n >= 3
        base = ["Fast", "Moderate", "Slow"]
        levels = base.copy()
        extra = n - 3
        for _ in range(extra):
            levels.append(random.choices(["Fast","Moderate","Slow"], weights=[0.5,0.3,0.2], k=1)[0])
        # group levels to keep ordering Fast -> Moderate -> Slow
        return [l for l in levels if l == "Fast"] + [l for l in levels if l == "Moderate"] + [l for l in levels if l == "Slow"]

    # helper: pick another district (not the user's)
    def _pick_other_district(user_district, district_roads):
        available = [d for d in district_roads.keys() if d != user_district]
        return random.choice(available) if available else None

    # helper: generate stops and return (stops_list, chosen_district)
    def _generate_stops(user_district, user_address):
        sample_locations = [
            'Jl. Musik VII No.23b',
            'Jl. Taman Suri I 001/004 No.12',
            'Jl. Raya Cirebon, Sayang, No.52b',
            'Jl. Joji Singa XVI No.5/7a',
        ]
        district_roads = {
            'Coblong': [
                'Jl. Tamansari No.43a/56',
                'Jl. Padasuka Caringin 3 No.41',
                'Jl. Ciliwung Kecil No.12',
            ],
            'Sukajadi': [
                'Jl. Sukajadi IV No.7',
                'Jl. Sukajadi Raya No.21',
                'Jl. Rancabadak No.3',
            ],
            'Cidadap': [
                'Jl. Cidadap III No.1',
                'Jl. Cidadap Raya No.10',
                'Jl. Siliwangi Dalam IV No.28',
            ],
            'Cicendo': [
                'Jl. Cicendo Raya No.5',
                'Jl. Cibadak No.8',
                'Jl. Aceh No.22',
            ],
            'Lengkong': [
                'Jl. Lengkong Kecil No.2',
                'Jl. Pasteur No.99',
                'Jl. Soekarno Hatta No.150',
            ],
        }

        # Mapping fixed ID waste collector (WC00001 - WC00020) per kecamatan pengguna
        district_collectors = {
            'Coblong': [
                'WC00001', 'WC00002', 'WC00003', 'WC00004',
            ],
            'Sukajadi': [
                'WC00005', 'WC00006', 'WC00007', 'WC00008',
            ],
            'Cidadap': [
                'WC00009', 'WC00010', 'WC00011', 'WC00012',
            ],
            'Cicendo': [
                'WC00013', 'WC00014', 'WC00015', 'WC00016',
            ],
            'Lengkong': [
                'WC00017', 'WC00018', 'WC00019', 'WC00020',
            ],
        }

        n = random.randint(1, 4)
        levels = _generate_levels(n)

        start_hour = random.randint(8, 15)
        start_min = random.choice([0, 15, 30, 45])
        current_minutes = start_hour * 60 + start_min
        speed_offset_ranges = {"Fast": (8, 12), "Moderate": (18, 35), "Slow": (45, 90)}

        stops_local = []
        chosen_district_local = None

        # Ambil semua collector dari DB lalu bangun pool per kecamatan
        all_collectors = db.load_all("wc")
        collectors_by_id = {row[0]: row for row in all_collectors}

        # Pool collector per district berdasarkan mapping ID di atas
        district_pools = {}
        for d, ids in district_collectors.items():
            rows = [collectors_by_id[cid] for cid in ids if cid in collectors_by_id]
            # fallback jika ID di mapping tidak ada di DB
            if not rows:
                rows = all_collectors.copy()
            district_pools[d] = rows

        global_pool = all_collectors.copy()

        for i in range(n):
            level = levels[i] if i < len(levels) else levels[-1]
            offset = random.randint(*speed_offset_ranges[level])
            current_minutes += offset
            time1 = f"{(current_minutes // 60) % 24:02d}:{current_minutes % 60:02d}"
            later = random.randint(5, 30)
            time2_minutes = current_minutes + later
            time2 = f"{(time2_minutes // 60) % 24:02d}:{time2_minutes % 60:02d}"

            # pick a different district than the user's and select a road from it
            other = _pick_other_district(user_district, district_roads)
            if other:
                chosen_district_local = other if chosen_district_local is None else chosen_district_local
                loc1 = random.choice(district_roads[other])
            else:
                loc1 = random.choice(sample_locations)

            loc2 = user_address if user_address and user_address.strip() else random.choice(sample_locations)

            # pilih collector berdasarkan origin district `other` dengan ID fix per district,
            # dan hindari duplikasi ID di satu list stops
            pool = None
            if other and other in district_pools and district_pools[other]:
                pool = district_pools[other]
            elif global_pool:
                pool = global_pool

            collector = None
            if pool:
                collector = random.choice(pool)
                pool.remove(collector)

            dur = time2_minutes - current_minutes
            # compute map district code pair based on user's district and collector origin
            user_code = district_to_code(user_district)
            other_code = district_to_code(other)
            map_districts = f"{user_code}_{other_code}"
            map_path = get_map_path(map_districts)

            stops_local.append({
                'id': collector[0] if collector else f'ID {random.randint(1000,9999)}-{random.randint(1000,9999)}',
                'location1': loc1,
                'location2': loc2,
                'time1': time1,
                'time2': time2,
                'wait_time': level,
                'origin_district': other,
                'collector_row': collector,
                'duration': dur,
                'map_districts': map_districts,
                'map_path': map_path,
            })

        def _time_to_minutes(t):
            h, m = t.split(':')
            return int(h) * 60 + int(m)

        stops_local.sort(key=lambda s: _time_to_minutes(s['time1']))
        return stops_local, chosen_district_local

    chosen_district = ""
    user_district = getattr(order_state, 'district', None)
    user_address = getattr(order_state, 'address', None)
    prev_district = getattr(order_state, 'stops_district', None)
    stops = getattr(order_state, 'stops', None)

    # regenerate stops kalau belum ada ATAU kecamatan user berubah
    if (not stops) or (prev_district != user_district):
        stops, chosen_district = _generate_stops(user_district, user_address)
        # simpan ke state agar konsisten saat user bolak-balik halaman,
        # tapi tetap per-kecamatan
        order_state.stops = stops
        order_state.stops_district = user_district

    stop_controls = []
    if not hasattr(order_state, 'show_collector'):
        order_state.show_collector = False
    if not hasattr(order_state, 'selected_collector_data'):
        order_state.selected_collector_data = None
    order_state.show_collector = True

    # ================================================ #
    def update_collector_data(row):
        # row adalah satu baris collector dari tabel wc
        order_state.selected_collector_data = row
        order_state.show_collector = True
        show_collector_card(row)
        page.update()

    def show_collector_card(data):
        collector_card.content = build_collector_card(data)
        collector_card.visible = True
        collector_card.update()

    def hide_collector_card():
        collector_card.visible = False
        collector_card.update()

    # --- Route box helpers (mirror collector_card mechanism) ---
    def show_route_box(path: str):
        # set the image source for the route box and make it visible
        try:
            # replace inner image content with new image path
            route_image_inner.content = ft.Image(src=path, fit=ft.ImageFit.COVER, expand=True)
        except Exception:
            # fallback: use default image if replacement fails
            route_image_inner.content = ft.Image(src="img/order-bg-image.avif", fit=ft.ImageFit.COVER, expand=True)
        # ensure the map card is visible and updated
        map_image_box.visible = True
        route_image_inner.update()
        map_image_box.update()

    def update_cards(collector_row, origin_district, duration, map_districts, map_path):
        nonlocal dur
        # show collector card (existing behavior)
        update_collector_data(collector_row)

        # set the outer dur variable and save to order_state
        dur = duration
        order_state.duration = duration

        # store map pair and path on order_state
        order_state.map_districts = map_districts
        order_state.map_path = map_path

        # show route box with provided map path (show_route_box will handle fallback)
        show_route_box(map_path)

    for s in stops:
        collector_row = s.get('collector_row')
        stop_id = s.get('id', '')
        origin = s.get('origin_district', None)
        duration = s.get('duration', 0)
        map_districts = s.get('map_districts', '')
        map_path = s.get('map_path', '')
        stop_controls.append(
            create_stop_card(
                stop_id,
                s.get('location1', ''),
                s.get('location2', ''),
                s.get('time1', ''),
                s.get('time2', ''),
                s.get('wait_time', ''),
                origin,
                on_click=lambda e, row=collector_row, origin=origin, duration=duration, md=map_districts, mp=map_path: update_cards(row, origin, duration, md, mp),
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
                ft.Container(height=20),
                *stop_controls,
                ft.Container(height=20),
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
    
    # constants for map box and spacing
    _map_top = 40
    _map_inner_w = 520
    _map_inner_h = 420
    _map_outer_pad = 12
    _map_outer_w = _map_inner_w + (_map_outer_pad * 2)
    _map_outer_h = _map_inner_h + (_map_outer_pad * 2) + 32  # extra space for title and spacing
    _map_gap = 40  # desired gap between map box and collector card (same as top padding)

    # inner container for the route image so we can swap its content dynamically
    route_image_inner = ft.Container(
        content=ft.Image(src="img/order-bg-image.avif", fit=ft.ImageFit.COVER, expand=True),
        border_radius=12,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        width=_map_inner_w,
        height=_map_inner_h,
    )

    # Image box in the upper-right, styled similar to the collector card
    map_image_box = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Chosen Route", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                route_image_inner,
            ],
            spacing=10,
        ),
        bgcolor="white",
        border=ft.border.all(1, "#f0f0f0"),
        border_radius=12,
        padding=_map_outer_pad,
        width=_map_outer_w,
        height=_map_outer_h,
        right=40,
        top=_map_top,
        visible=False,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=12, color=ft.Colors.with_opacity(0.06, "#000000")),
    )

    # collector card placed below the map box with the same gap as map top padding
    collector_card_top = _map_top + _map_outer_h + _map_gap
    collector_card = ft.Container(visible=False, right=40, top=collector_card_top)
    collector_card.content = build_collector_card(getattr(order_state, 'selected_collector_data', None))

    # Layout with map background
    content = ft.Stack(
        controls=[
            # Map background placeholder
                    # background placeholder removed so the global bg_container can show
                    ft.Container(expand=True),
                    
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
            # floating map image (upper-right) and collector card (bottom-right)
            map_image_box,
            collector_card,
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