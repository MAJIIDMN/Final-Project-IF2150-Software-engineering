import flet as ft
from views.navbar import create_navbar
from models.PointMart import PointMart

point_mart = PointMart()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    page.title = "GrowBak - Point Mart"
    page.window_width = 1440
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")

    # Variabel untuk menyimpan masukan pengguna
    search_input = ft.Ref[ft.TextField]()
    sort_filter = ft.Ref[ft.Dropdown]()
    availability_filter = ft.Ref[ft.Column]()
    
    checkbox_availability = ft.Ref[ft.Checkbox]()
    checkbox_out_of_stock = ft.Ref[ft.Checkbox]()

    # Fungsi untuk mengubah warna kotak centang
    def on_checkbox_change(e, checkbox_ref):
        if checkbox_ref.current.value:
            checkbox_ref.current.fill_color = "#1e8c45"
            checkbox_ref.current.check_color = "#FFFFFF"
        else:
            checkbox_ref.current.fill_color = "#FFFFFF"
        page.update()

    # Fungsi untuk mengubah warna field
    def on_focus(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#000000")
        page.update()
    def on_blur_label(e, field_ref):
        field_ref.current.label_style = ft.TextStyle(color="#c2c2c2")
        page.update()


    # Dummy data
    products = point_mart.load_hadiah()

    def sort_by_point(e, reverse: bool, hadiah: list):
        products_grid.controls.clear()
        if reverse == True:
            sorted_products = point_mart.sort_by_points_down(hadiah)
        else:
            sorted_products = point_mart.sort_by_points_up(hadiah)
        
        for product in sorted_products:
            products_grid.controls.append(product_card(product))
        page.update()

    def sort_by_stock(e, reverse: bool, hadiah: list):
        products_grid.controls.clear()
        if reverse == True:
            sorted_products = point_mart.sort_by_stock_down(hadiah)
        else:
            sorted_products = point_mart.sort_by_stock_up(hadiah)
        
        for product in sorted_products:
            products_grid.controls.append(product_card(product))
        page.update()

    def search(e, keyword: str):
        products_grid.controls.clear()
        searched_products = point_mart.search_hadiah(keyword)
        for product in searched_products:
            products_grid.controls.append(product_card(product))
        page.update()
    
    def on_search_change(e):
        search(e, search_input.current.value)

    # Top navigation bar
    top_nav = create_navbar(page)

    # List reward yang dapat ditukar pengguna
    def product_card(product):
        def on_product_click(e):
            page.clean()
            page.product_detail_main(page, product)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Image(
                            src=product["image"],
                            fit=ft.ImageFit.COVER,
                        ),
                        width=180,
                        height=200,
                        border_radius=ft.border_radius.all(8),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),
                    ft.Text(
                        product["category"],
                        size=11,
                        color="#999999",
                    ),
                    ft.Text(
                        product["name"],
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color="#000000",
                        max_lines=2,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"{product['points']} points",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color="#1e8c45",
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=8,
            ),
            width=180,
            on_click=on_product_click,
        )

    # Product grid
    products_grid = ft.GridView(
        runs_count=4,
        spacing=20,
        run_spacing=20,
        child_aspect_ratio=1,
        auto_scroll=False,
    )

    for product in products:
        products_grid.controls.append(product_card(product))

    # Panel untuk mengurutkan produk berdasarkan kriteria tertentu
    filters_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Filters", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Container(height=10),
                
                ft.ElevatedButton(
                    "Low to High Price",
                    width=float("inf"),
                    on_click=lambda e: sort_by_point(e, False, products),
                    height=40,
                    bgcolor="#1e8c45",
                    color="white",
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.ElevatedButton(
                    "High to Low Price",
                    width=float("inf"),
                    on_click=lambda e: sort_by_point(e, True, products),
                    height=40,
                    bgcolor="#1e8c45",
                    color="white",
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.ElevatedButton(
                    "Most to Least Stock",
                    width=float("inf"),
                    on_click=lambda e: sort_by_stock(e, True, products),
                    height=40,
                    bgcolor="#1e8c45",
                    color="white",
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.ElevatedButton(
                    "Least to Most Stock",
                    width=float("inf"),
                    on_click=lambda e: sort_by_stock(e, False, products),
                    height=40,
                    bgcolor="#1e8c45",
                    color="white",
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                
                ft.Container(height=20),
                
                # Availability filter
                ft.Text("Availability", size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Container(height=10),
                ft.Checkbox(
                    ref=checkbox_availability,
                    label="Availability (450)",
                    value=True,
                    fill_color="#1e8c45",
                    check_color="#FFFFFF",
                    on_change=lambda e: on_checkbox_change(e, checkbox_availability),
                ),
                ft.Checkbox(
                    ref=checkbox_out_of_stock,
                    label="Out Of Stock (18)",
                    value=False,
                    fill_color="#9e9e9e",
                    on_change=lambda e: on_checkbox_change(e, checkbox_out_of_stock),
                ),
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=200,
        padding=20,
        border_radius=ft.border_radius.all(8),
        border=ft.border.all(1, "#e0e0e0"),
    )

    # Main content
    content_area = ft.Column(
        [
            ft.Text("Point Mart", size=36, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Container(height=20),
            
            # Search bar
            ft.TextField(
                ref=search_input,
                label="Search",
                border_color="#e0e0e0",
                focused_border_color="#1e8c45",
                height=50,
                prefix_icon=ft.Icons.SEARCH,
                text_style=ft.TextStyle(color="#000000"),
                cursor_color="#000000",
                label_style=ft.TextStyle(color="#c2c2c2"),
                on_focus=lambda e: on_focus(e, search_input),
                on_blur=lambda e: on_blur_label(e, search_input),\
                on_change=on_search_change,
            ),
            
            ft.Container(height=20),
            
            # Products grid
            products_grid,
        ],
        spacing=10,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # Main layout dengan filters dan content
    main_content = ft.Row(
        [
            filters_panel,
            ft.Container(width=20),
            content_area,
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
