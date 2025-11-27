import flet as ft
from views.components.navbar import create_navbar
from models.PointMart import PointMart
from models.state import AppState
from views.components.Alert import create_alert_dialog as Alert

point_mart = PointMart()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page, product_data=None):
    page.title = "GrowBak - Product Detail"
    page.window_width = 1440
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")

    # Default data produk
    if product_data is None:
        product_data = {
            "id": "sample",
            "name": "ABSTRACT PRINT SHIRT",
            "image": "img/product1.png",
            "points": 199,
            "stock": 10,
            "description": "Relaxed fit shirt. Camp collar and short sleeves. Button-up front.",
            "colors": ["#e0e0e0", "#888888", "#000000", "#7dd3c0", "#c5b3e6"],
            "sizes": ["XS", "S", "M", "L", "XL", "2XL"],
        }

    selected_color = ft.Ref[str]()
    selected_size = ft.Ref[str]()
    selected_color.current = product_data["colors"][0]
    selected_size.current = None

    # Back button
    def go_back(e):
        page.clean()
        page.point_mart_main(page)

    # Pemilihan warna
    def on_color_click(color):
        def handler(e):
            selected_color.current = color
            update_color_buttons()
        return handler

    # Pemilihan size
    def on_size_click(size):
        def handler(e):
            selected_size.current = size
            update_size_buttons()
        return handler

    # Fungsi untuk mengubah model button
    def update_color_buttons():
        for i, btn in enumerate(color_buttons):
            if i < len(product_data["colors"]):
                if product_data["colors"][i] == selected_color.current:
                    btn.border = ft.border.all(3, "#1e8c45")
                else:
                    btn.border = ft.border.all(1, "#e0e0e0")
        page.update()
    def update_size_buttons():
        for i, btn in enumerate(size_buttons):
            if i < len(product_data["sizes"]):
                if product_data["sizes"][i] == selected_size.current:
                    btn.bgcolor = "#1e8c45"
                    btn.color = "white"
                else:
                    btn.bgcolor = "white"
                    btn.color = "#000000"
        page.update()

    # Redeem button

    def on_redeem(e):
        if product_data.get("stock", 0) <= 0:
            dialog = Alert("Gagal", "Stok produk habis")
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return
        if not selected_size.current:
            # Show error dialog
            dialog = Alert("Perhatian", "Silakan pilih ukuran produk terlebih dahulu.")
            page.dialog = dialog
            dialog.open = True
            page.update()
        else:
            valid = point_mart.redeem_hadiah(AppState.username, product_data["id"], point_mart.load_hadiah())
            if valid:
                dialog = Alert("Berhasil!", "Produk berhasil ditukarkan!")
            else:
                dialog = Alert("Gagal", "Poin tidak cukup untuk menukarkan produk ini.")
            page.dialog = dialog
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            page.clear()
            page.product_detail_main(page, product_data)

    # Top navigation bar
    top_nav = create_navbar(page, "point_mart")

    # Left side - Product image
    left_side = ft.Container(
        content=ft.Column(
            [
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color="#000000",
                    icon_size=24,
                    on_click=go_back,
                ),
                ft.Container(
                    content=ft.Image(
                        src=product_data["image"],
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    width=750,
                    height=550,
                    alignment=ft.alignment.center,
                   padding=ft.padding.only(left=100),
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
        expand=True,
    )

    # Color selection buttons
    color_buttons = []
    color_row_content = [ft.Text("Color", size=12, weight=ft.FontWeight.BOLD, color="#000000")]
    color_button_row = ft.Row(spacing=10)
    
    for color in product_data["colors"]:
        btn = ft.Container(
            width=40,
            height=40,
            bgcolor=color,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(3, "#1e8c45" if color == selected_color.current else "#e0e0e0"),
            ink=True,
            on_click=on_color_click(color),
        )
        color_buttons.append(btn)
        color_button_row.controls.append(btn)

    # Size selection buttons
    size_buttons = []
    size_row_content = [ft.Text("Size", size=12, weight=ft.FontWeight.BOLD, color="#000000")]
    size_button_row = ft.Row(spacing=10)
    
    for size in product_data["sizes"]:
        btn = ft.ElevatedButton(
            text=size,
            width=50,
            height=45,
            bgcolor="white",
            color="#000000",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=4),
                text_style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD),
                side=ft.BorderSide(1, "#e0e0e0"),
            ),
            on_click=on_size_click(size),
        )
        size_buttons.append(btn)
        size_button_row.controls.append(btn)

    # Right side - Product details
    right_side = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=10),
                ft.IconButton(
                    ft.Icons.FAVORITE_BORDER,
                    icon_color="#ccc",
                    icon_size=24,
                ),
                ft.Container(height=10),
                ft.Text(
                    product_data["name"],
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                ft.Container(height=10),
                ft.Text(
                    f"{product_data['points']} points",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#1e8c45",
                ),
                ft.Container(height=5),
                ft.Text(
                    f"Stock: {product_data.get('stock', 0)}",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                ft.Container(height=5),
                ft.Text(
                    "MRP Incl. of all taxes",
                    size=11,
                    color="#999999",
                ),
                ft.Container(height=15),
                ft.Text(
                    product_data["description"],
                    size=13,
                    color="#666666",
                ),
                ft.Container(height=20),
                ft.Column(
                    [
                        ft.Text("Color", size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                        color_button_row,
                    ],
                    spacing=10,
                ),
                ft.Container(height=15),
                ft.Column(
                    [
                        ft.Text("Size", size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                        size_button_row,
                    ],
                    spacing=10,
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "REDEEM",
                    on_click=on_redeem,
                    bgcolor="#1e8c45",
                    color="white",
                    width=float("inf"),
                    height=55,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        text_style=ft.TextStyle(font_family="PoppinsBold", size=16),
                    ),
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
        expand=True,
        width=500,
    )

    # Main layout
    main_content = ft.Row(
        [
            left_side,
            right_side,
        ],
        spacing=0,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # Main container
    main_container = ft.Column(
        [
            top_nav,
            main_content,
        ],
        expand=True,
    )

    page.add(main_container)
