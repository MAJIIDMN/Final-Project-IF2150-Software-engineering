import flet as ft
import random
import threading
import time
from views.order.shared import create_sidebar
from services.database import DatabaseService
from models.state import AppState

# DB service for updating points
db = DatabaseService()

def NavigationView(page, order_state):
    # If user is logged in and points from this order haven't been applied yet,
    # add them to the user's account and mark as applied so it runs once.
    try:
        AppState.load_state()
    except Exception:
        pass
    points_to_add = getattr(order_state, 'point_gained', 0)
    already_applied = getattr(order_state, 'point_gained_applied', False)
    if points_to_add and not already_applied and AppState.is_logged_in and AppState.username:
        try:
            # Ensure numeric
            pts = float(points_to_add)
        except Exception:
            pts = 0
        if pts > 0:
            update_q = "UPDATE users SET point = COALESCE(point,0) + ? WHERE username = ?"
            success, msg = db.execute_query(update_q, (pts, AppState.username))
            if success:
                # mark applied to avoid double-adding when navigating back and forth
                order_state.point_gained_applied = True
            else:
                # log or silently ignore - no snackbar here per request
                pass
    # ambil data collector yang sudah dipilih di halaman Date and Time
    row = getattr(order_state, "selected_collector_data", None)
    if row is not None:
        # row: (id, name, experience, vehicle, platenumber)
        collector_id = row[0]
        collector_name = row[1]
        collector_experience = row[2]
        collector_vehicle = row[3]
        collector_plate = row[4]
    else:
        # fallback kalau user masuk langsung tanpa pilih collector dulu
        collector_id = "1234-5678"
        collector_name = "Vincent R"
        collector_experience = "12 years"
        collector_vehicle = "Motorcycle"
        collector_plate = "D 9999 FF"

    def call_collector(e):
        phone = getattr(order_state, "collector_phone", None) or "6281234567890"
        page.launch_url(f"https://wa.me/{phone}")

    def chat_collector(e):
        phone = getattr(order_state, "collector_phone", None) or "6281234567890"
        text = "Hello, I would like to ask about my waste pickup order"
        import urllib.parse
        encoded = urllib.parse.quote(text)
        page.launch_url(f"https://wa.me/{phone}?text={encoded}")

    def cancel_order(e):
        # kembali ke step sebelumnya dalam alur order
        page.go("/order/date-and-time")

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
                                ft.Text(collector_name, size=14, weight=ft.FontWeight.BOLD, color="black"),
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
                                ft.Text(collector_experience, size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                        ft.Container(width=30),
                        ft.Column(
                            controls=[
                                ft.Text("ID-Number", size=11, color="#757575"),
                                ft.Text(collector_id, size=13, weight=ft.FontWeight.BOLD),
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
                                ft.Text(collector_vehicle, size=13, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                        ft.Container(width=30),
                        ft.Column(
                            controls=[
                                ft.Text("License Plate", size=11, color="#757575"),
                                ft.Text(collector_plate, size=13, weight=ft.FontWeight.BOLD),
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
    # Layout: sidebar + content, with a small minutes-left box and collector card overlay
    # Note: removed the gray map bar under the navbar per request.
    # compute a minutes-left integer (random if not provided) and persist it on order_state
    minutes = getattr(order_state, 'duration', None)
    if minutes is None:
        minutes = random.randint(0, 59)
        order_state.duration = minutes

    # determine status text and accent color
    try:
        m = int(minutes)
    except Exception:
        m = 58

    if m == 0:
        status_text = "The Driver has arrived"
        accent = "#2e7d32"
    elif 1 <= m <= 10:
        status_text = "The Driver is Close!"
        accent = "#1976d2"
    else:
        status_text = "The driver is on the way"
        accent = "#ff9800"

    def compute_status(mins):
        if mins == 0:
            return "The Driver has arrived", "#2e7d32"
        elif 1 <= mins <= 10:
            return "The Driver is Close!", "#ff9800"
        else:
            return "The driver is on the way", "#1976d2"

    status_text, accent = compute_status(m)

    # controls that will be updated by the countdown thread
    minutes_text = ft.Text(f"{m} min", size=22, weight=ft.FontWeight.BOLD, color="#212121")
    status_text_control = ft.Text(status_text, size=14, color=accent)
    icon_container = ft.Container(
        content=ft.Icon(ft.Icons.ACCESS_TIME, color="white", size=32),
        width=72,
        height=72,
        bgcolor=accent,
        border_radius=14,
        alignment=ft.alignment.center,
    )

    minutes_box = ft.Container(
        content=ft.Row(
            controls=[
                icon_container,
                ft.Container(width=16),
                ft.Column(
                    controls=[
                        ft.Text("Arrival Estimation", size=14, color="#757575"),
                        minutes_text,
                        status_text_control,
                    ],
                    spacing=6,
                    alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="white",
        border=ft.border.all(1, "#e0e0e0"),
        border_radius=16,
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        width=360,
        height=132,
        right=40,
        bottom=72,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.09, "#000000")),
    )

    # start a background thread that decrements minutes once per minute
    def start_minutes_countdown():
        if getattr(order_state, "_minutes_timer_started", False):
            return
        order_state._minutes_timer_started = True

        def worker():
            # run until minutes_left reaches 0
            while True:
                try:
                    cur = int(getattr(order_state, "duration", 0))
                except Exception:
                    cur = 0
                if cur <= 0:
                    # ensure UI reflects arrival
                    def arrive():
                        minutes_text.value = "0 min"
                        st, ac = compute_status(0)
                        status_text_control.value = st
                        status_text_control.color = ac
                        icon_container.bgcolor = ac
                        page.update()
                    try:
                        page.call_from_thread(arrive)
                    except Exception:
                        try:
                            # fallback: update on main thread
                            arrive()
                        except Exception:
                            pass
                        # show pickup confirmation dialog immediately (no timer) when arrived
                        if not getattr(order_state, "_arrival_dialog_scheduled", False):
                            order_state._arrival_dialog_scheduled = True

                            def show_pickup_dialog():
                                def _ok(e):
                                    # Close the dialog (safe on most Flet versions), then
                                    # remove the page.dialog reference and navigate home.
                                    try:
                                        dialog.open = False
                                        page.update()
                                    except Exception:
                                        pass

                                    try:
                                        page.dialog = None
                                    except Exception:
                                        pass

                                    try:
                                        page.update()
                                    except Exception:
                                        pass

                                    # Navigate back to home following the app pattern.
                                    try:
                                        page.clean()
                                    except Exception:
                                        pass
                                    try:
                                        page.home_main(page)
                                    except Exception:
                                        try:
                                            page.go("/")
                                        except Exception:
                                            pass

                                pts = getattr(order_state, 'point_gained', 0)
                                try:
                                    pts_txt = f"{float(pts):.2f}"
                                except Exception:
                                    pts_txt = str(pts)

                                dialog = ft.AlertDialog(
                                    title=ft.Text("Waste Picked Up"),
                                    content=ft.Text(f"Your waste has been picked up. You gained {pts_txt} points."),
                                    actions=[
                                        ft.ElevatedButton("OK", on_click=_ok, bgcolor="#2e7d32", color="white"),
                                    ],
                                )
                                # Use page.overlay.append so the dialog is shown reliably in this app.
                                try:
                                    page.overlay.append(dialog)
                                except Exception:
                                    # fallback: set page.dialog if overlay isn't available
                                    try:
                                        page.dialog = dialog
                                    except Exception:
                                        pass
                                dialog.open = True
                                page.update()

                            # try to show on main thread, otherwise call directly as fallback
                            try:
                                page.call_from_thread(show_pickup_dialog)
                            except Exception:
                                try:
                                    show_pickup_dialog()
                                except Exception:
                                    pass
                    break

                # sleep one minute
                time.sleep(60)

                # decrement
                try:
                    order_state.duration = max(0, int(order_state.duration) - 1)
                except Exception:
                    order_state.duration = 0

                # update UI controls on main thread
                def tick():
                    try:
                        cur2 = int(getattr(order_state, "duration", 0))
                    except Exception:
                        cur2 = 0
                    minutes_text.value = f"{cur2} min"
                    st2, ac2 = compute_status(cur2)
                    status_text_control.value = st2
                    status_text_control.color = ac2
                    icon_container.bgcolor = ac2
                    page.update()

                try:
                    page.call_from_thread(tick)
                except Exception:
                    try:
                        tick()
                    except Exception:
                        pass

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    # start the countdown if needed
    start_minutes_countdown()

    content = ft.Stack(
        controls=[
            # Sidebar and card content (centered)
            ft.Container(
                content=ft.Row(
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
                alignment=ft.alignment.center,
                expand=True,
            ),
            # minutes left box and floating collector card
            minutes_box,
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