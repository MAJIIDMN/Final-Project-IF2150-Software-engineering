import flet as ft
from views.components.navbar import create_navbar
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
    
    # Variabel untuk button filter
    sort_buttons = []
    active_button = ft.Ref[int]()
    active_button.current = -1  # -1 berarti tidak ada button yang aktif

    avail_hadiah = point_mart.avail_hadiah_list()
    non_avail_hadiah = point_mart.non_avail_hadiah_list()

    # Fungsi untuk mengubah warna kotak centang
    def on_checkbox_change(e, checkbox_ref):
        if checkbox_ref.current.value:
            checkbox_ref.current.fill_color = "#1e8c45"
            checkbox_ref.current.check_color = "#FFFFFF"
            checkbox_ref.current.label_style = ft.TextStyle(color="#000000")
        else:
            checkbox_ref.current.fill_color = "#FFFFFF"
            checkbox_ref.current.label_style = ft.TextStyle(color="#999999")
        # if checkbox_ref == checkbox_availability and checkbox_ref.current.value:
        #     checkbox_out_of_stock.current.value = False
        #     checkbox_out_of_stock.current.fill_color = "#FFFFFF"
        # elif checkbox_ref == checkbox_out_of_stock and checkbox_ref.current.value:
        #     checkbox_availability.current.value = False
        #     checkbox_availability.current.fill_color = "#FFFFFF"
        products_grid.controls.clear()
        if checkbox_availability.current.value and not checkbox_out_of_stock.current.value:
            for product in avail_hadiah:
                products_grid.controls.append(product_card(product))
        elif not checkbox_availability.current.value and checkbox_out_of_stock.current.value:
            for product in non_avail_hadiah:
                products_grid.controls.append(product_card(product))
        elif checkbox_availability.current.value and checkbox_out_of_stock.current.value:
            for product in avail_hadiah + non_avail_hadiah:
                products_grid.controls.append(product_card(product))
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

    def sort_by_point(e, reverse: bool, hadiah: list, button_idx: int):
        active_button.current = button_idx
        update_button_colors(button_idx)
        if checkbox_availability.current.value and not checkbox_out_of_stock.current.value:
            hadiah = avail_hadiah
        elif not checkbox_availability.current.value and checkbox_out_of_stock.current.value:
            hadiah = non_avail_hadiah
        elif not checkbox_availability.current.value and not checkbox_out_of_stock.current.value:
            hadiah = []
        products_grid.controls.clear()
        if reverse == True:
            hadiah = point_mart.sort_by_points_down(hadiah)
        else:
            hadiah = point_mart.sort_by_points_up(hadiah)
        
        for product in hadiah:
            products_grid.controls.append(product_card(product))
        page.update()

    def sort_by_stock(e, reverse: bool, hadiah: list, button_idx: int):
        active_button.current = button_idx
        update_button_colors(button_idx)
        products_grid.controls.clear()
        if checkbox_availability.current.value and not checkbox_out_of_stock.current.value:
            hadiah = avail_hadiah
        elif not checkbox_availability.current.value and checkbox_out_of_stock.current.value:
            hadiah = non_avail_hadiah
        elif not checkbox_availability.current.value and not checkbox_out_of_stock.current.value:
            hadiah = []

        if reverse == True:
            hadiah = point_mart.sort_by_stock_down(hadiah)
        else:
            hadiah = point_mart.sort_by_stock_up(hadiah)
        
        for product in hadiah:
            products_grid.controls.append(product_card(product))
        page.update()

    def search(e, keyword: str, hadiah):
        products_grid.controls.clear()
        if checkbox_availability.current.value and not checkbox_out_of_stock.current.value:
            hadiah = avail_hadiah
        if not checkbox_availability.current.value and checkbox_out_of_stock.current.value:
            hadiah = non_avail_hadiah
        if not checkbox_availability.current.value and not checkbox_out_of_stock.current.value:
            hadiah = []
        searched_products = point_mart.search_hadiah(keyword)
        for product in searched_products:
            if product in hadiah:
                products_grid.controls.append(product_card(product))
        page.update()
    
    def on_search_change(e):
        search(e, search_input.current.value, products)

    # Top navigation bar
    top_nav = create_navbar(page, "point_mart")

    # List reward yang dapat ditukar pengguna
    def product_card(product):
        def on_product_click(e):
            page.clean()
            page.product_detail_main(page, product)
        
        # Dinamis ukuran card berdasarkan window width
        card_width = (page.window_width - 300) / 5  # Estimasi untuk 5 kolom
        card_img_height = card_width * 1.0 # Rasio tinggi gambar
        card_text_width = card_width - 10
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Image(
                            src=product["image"],
                            fit=ft.ImageFit.FILL,
                        ),
                        width=card_width,
                        height=card_img_height,
                        border_radius=ft.border_radius.all(8),
                        clip_behavior=ft.ClipBehavior.NONE,
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        product["category"],
                        size=10,
                        color="#999999",
                        width=card_text_width,
                        no_wrap=True,
                    ),
                    ft.Container(height=3),
                    ft.Text(
                        product["name"],
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color="#000000",
                        max_lines=2,
                        width=card_text_width,
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        f"{product['points']} points",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color="#1e8c45",
                    ),
                ],
                spacing=0,
                tight=True,
            ),
            width=card_width,
            padding=8,
            on_click=on_product_click,
        )

    # Product grid - dinamis berdasarkan window width
    grid_runs_count = max(3, (page.window_width - 300) // 240)  # Minimal 3 kolom
    
    products_grid = ft.GridView(
        runs_count=grid_runs_count,
        spacing=15,
        run_spacing=30,
        child_aspect_ratio=1,
        auto_scroll=False,
    )

    for product in products:
        products_grid.controls.append(product_card(product))

    # Panel untuk mengurutkan produk berdasarkan kriteria tertentu
    # Buat button dan simpan ke list
    btn_low_to_high = ft.ElevatedButton(
        "Low to High Price",
        width=float("inf"),
        on_click=lambda e: sort_by_point(e, False, products, 0),
        height=40,
        bgcolor="#cccccc",
        color="#666666",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    btn_high_to_low = ft.ElevatedButton(
        "High to Low Price",
        width=float("inf"),
        on_click=lambda e: sort_by_point(e, True, products, 1),
        height=40,
        bgcolor="#cccccc",
        color="#666666",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    btn_most_to_least = ft.ElevatedButton(
        "Most to Least Stock",
        width=float("inf"),
        on_click=lambda e: sort_by_stock(e, True, products, 2),
        height=40,
        bgcolor="#cccccc",
        color="#666666",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    btn_least_to_most = ft.ElevatedButton(
        "Least to Most Stock",
        width=float("inf"),
        on_click=lambda e: sort_by_stock(e, False, products, 3),
        height=40,
        bgcolor="#cccccc",
        color="#666666",
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=12, font_family="PoppinsSBold"),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    sort_buttons = [btn_low_to_high, btn_high_to_low, btn_most_to_least, btn_least_to_most]
    
    filters_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Filters", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Divider(height=15, color="transparent"),
                
                ft.Text("Sort", size=11, weight=ft.FontWeight.BOLD, color="#666666"),
                ft.Container(height=8),
                btn_low_to_high,
                ft.Container(height=6),
                btn_high_to_low,
                ft.Container(height=6),
                btn_most_to_least,
                ft.Container(height=6),
                btn_least_to_most,
                
                ft.Divider(height=20, color="#e0e0e0"),
                
                # Availability filter
                ft.Text("Availability", size=11, weight=ft.FontWeight.BOLD, color="#666666"),
                ft.Container(height=8),
                ft.Checkbox(
                    ref=checkbox_availability,
                    label=f"Availability ({len(avail_hadiah)})",
                    value=True,
                    fill_color="#1e8c45",
                    check_color="#FFFFFF",
                    label_style=ft.TextStyle(color="#000000"),
                    on_change=lambda e: on_checkbox_change(e, checkbox_availability),
                ),
                ft.Container(height=4),
                ft.Checkbox(
                    ref=checkbox_out_of_stock,
                    label=f"Out Of Stock ({len(non_avail_hadiah)})",
                    value=True,
                    fill_color="#1e8c45",
                    check_color="#FFFFFF",
                    label_style=ft.TextStyle(color="#000000"),
                    on_change=lambda e: on_checkbox_change(e, checkbox_out_of_stock),
                ),
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
                on_blur=lambda e: on_blur_label(e, search_input),
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
            ft.Container(
                content=filters_panel,
                width=200,
            ),
            ft.Container(width=20),
            ft.Container(
                content=content_area,
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
