import flet as ft
from views.components.navbar import create_navbar
from views.components.point_mart_control import create_point_mart_control
from views.components.waste_info_control import create_waste_info_control
from models.PointMart import PointMart

point_mart = PointMart()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    page.title = "GrowBak - Control Menu"
    page.window_width = 1440
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")
    
    # Create Point Mart Control component

    products = point_mart.load_hadiah()
    page_active = create_point_mart_control(page)
    page_active_container = ft.Ref[ft.Container]()
    
    # Fungsi untuk mengubah warna button filter
    def update_button_colors(active_idx):
        for idx, btn in enumerate(sort_buttons):
            if idx == active_idx:
                btn.bgcolor = "#1e8c45"
                btn.color = "white"
            else:
                btn.bgcolor = "#cccccc"
                btn.color = "#666666"
        page.update()

    def point_mart_control(e):
        nonlocal page_active
        page_active = create_point_mart_control(page)
        page_active_container.current.content = page_active
        update_button_colors(0)
        page.update()

    def informasi_sampah_control(e):
        nonlocal page_active
        page_active = create_waste_info_control(page)
        page_active_container.current.content = page_active
        update_button_colors(1)
        page.update()

    # Top navigation bar
    top_nav = create_navbar(page, "Control Menu")

    # Product grid - dinamis berdasarkan window width
    grid_runs_count = max(3, (page.window_width - 300) // 240)  # Minimal 3 kolom
    
    products_grid = ft.GridView(
        runs_count=grid_runs_count,
        spacing=15,
        run_spacing=30,
        child_aspect_ratio=1,
        auto_scroll=False,
    )

    martControl = ft.ElevatedButton(
        "Point Mart",
        width=float("inf"),
        on_click=lambda e: point_mart_control(0),
        height=40,
        bgcolor="#1e8c45",
        color="white",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    orderControl = ft.ElevatedButton(
        "Informasi Sampah",
        width=float("inf"),
        on_click=informasi_sampah_control,
        height=40,
        bgcolor="#cccccc",
        color="#666666",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    userControl = ft.ElevatedButton(
        "User",
        width=float("inf"),
        on_click=lambda e: update_button_colors(2),
        height=40,
        bgcolor="#cccccc",
        color="#666666",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    wasteCollectorControl = ft.ElevatedButton(
        "Waste Collector",
        width=float("inf"),
        on_click=lambda e: update_button_colors(3),
        height=40,
        bgcolor="#cccccc",
        color="#666666",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    sort_buttons = [martControl, orderControl, userControl, wasteCollectorControl]
    
    filters_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Control Menu", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Divider(height=15, color="transparent"),
                martControl,
                ft.Container(height=6),
                orderControl,
                ft.Container(height=6),
                userControl,
                ft.Container(height=6),
                wasteCollectorControl,
                
                ft.Divider(height=20, color="#e0e0e0"),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        border_radius=ft.border_radius.all(8),
        border=ft.border.all(1, "#e0e0e0"),
        expand=True,
    )

    # Main content
    content_area = ft.Column(
        [
            ft.Text("Point Mart", size=36, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Container(height=20),
            
            ft.Container(height=20),
            products_grid,
        ],
        spacing=10,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # Main layout dengan filters dan content
    main_content = ft.Row(
        [
            ft.Container(
                content=filters_panel,
                width=200,
            ),
            ft.Container(width=20),
            ft.Container(
                ref=page_active_container,
                content=page_active,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # Main container
    main_container = ft.Column(
        [
            top_nav,
            ft.Container(
                content=main_content,
                padding=ft.padding.symmetric(horizontal=40, vertical=30),
                expand=True,
            ),
        ],
        expand=True,
    )

    page.add(main_container)
