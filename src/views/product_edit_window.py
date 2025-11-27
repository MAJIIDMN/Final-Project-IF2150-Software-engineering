import flet as ft
from views.components.navbar import create_navbar
import views.components.Alert as Alert
from models.PointMart import PointMart

point_mart = PointMart()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page, product_data=None):
    page.title = "GrowBak - Edit Product"
    page.window_width = 1440
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")
    new = False

    # Default product data untuk testing
    if product_data is None:
        new = True
        product_data = {
            "id": "",
            "name": "",
            "category": "",
            "points": 0,
            "stock": 0,
            "image": "",
            "description": "",
            "colors": [],
            "sizes": []
        }

    # Refs untuk form inputs
    product_name = ft.Ref[ft.TextField]()
    category = ft.Ref[ft.TextField]()
    points = ft.Ref[ft.TextField]()
    stock = ft.Ref[ft.TextField]()
    description = ft.Ref[ft.TextField]()
    image_path = ft.Ref[ft.TextField]()
    
    # State untuk colors dan sizes
    colors_list = list(product_data.get("colors", []))
    sizes_list = list(product_data.get("sizes", []))
    
    # Refs untuk list views
    colors_listview = ft.Ref[ft.Column]()
    sizes_listview = ft.Ref[ft.Column]()
    size_input = ft.Ref[ft.TextField]()
    product_image = ft.Ref[ft.Image]()

    # File picker untuk upload image
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            # Update image path
            image_path.current.value = file.path
            # Update image preview
            product_image.current.src = file.path
            page.update()
    
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    
    def on_upload_image(e):
        file_picker.pick_files(
            allowed_extensions=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
            allow_multiple=False,
        )

    # Back button
    def go_back(e):
        page.clean()
        page.admin_control_main(page)
    
    # Color picker handler
    def add_color(e):
        hex_input = ft.Ref[ft.TextField]()
        selected_color = ft.Ref[ft.Container]()
        
        def pick_hex_color(e):
            hex_value = hex_input.current.value.strip()
            if not hex_value.startswith('#'):
                hex_value = '#' + hex_value
            
            # Validate hex color
            if len(hex_value) in [4, 7, 9]:  # #RGB, #RRGGBB, or #RRGGBBAA
                if hex_value not in colors_list:
                    colors_list.append(hex_value)
                    update_colors_display()
                color_dialog.open = False
                page.update()
        
        def update_hex_preview(e):
            hex_value = hex_input.current.value.strip()
            if not hex_value.startswith('#'):
                hex_value = '#' + hex_value
            try:
                selected_color.current.bgcolor = hex_value
                page.update()
            except:
                pass
        
        quick_colors = [
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
            "#FFA500", "#800080", "#FFC0CB", "#000000", "#FFFFFF", "#808080",
        ]
        
        def select_quick_color(color):
            hex_input.current.value = color
            selected_color.current.bgcolor = color
            page.update()
        
        quick_color_buttons = []
        for color in quick_colors:
            quick_color_buttons.append(
                ft.Container(
                    bgcolor=color,
                    width=35,
                    height=35,
                    border_radius=6,
                    border=ft.border.all(2, "#e0e0e0"),
                    on_click=lambda e, c=color: select_quick_color(c),
                    ink=True,
                )
            )
        
        color_dialog = ft.AlertDialog(
            title=ft.Text("Pick a Color", color="#1e8c45", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    # Color preview
                    ft.Container(
                        content=ft.Container(
                            ref=selected_color,
                            bgcolor="#FFFFFF",
                            expand=True,
                            border_radius=8,
                        ),
                        width=350,
                        height=60,
                        border=ft.border.all(2, "#e0e0e0"),
                        border_radius=8,
                        padding=5,
                    ),
                    ft.Container(height=15),
                    
                    # Hex input
                    ft.TextField(
                        ref=hex_input,
                        label=ft.Text("Hex Color Code", size=12, color="#1e8c45"),
                        value="#FFFFFF",
                        prefix_text="",
                        on_change=update_hex_preview,
                        border_color="#e0e0e0",
                        focused_border_color="#1e8c45",
                        text_style=ft.TextStyle(size=14, color="#000000"),
                    ),
                    ft.Container(height=15),
                    
                    # Quick colors
                    ft.Text("Quick Colors:", size=12, weight=ft.FontWeight.BOLD, color="#1e8c45"),
                    ft.Container(height=8),
                    ft.Row(
                        quick_color_buttons,
                        wrap=True,
                        spacing=8,
                        run_spacing=8,
                    ),
                ], tight=True),
                width=400,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: (setattr(color_dialog, 'open', False), page.update()), style=ft.ButtonStyle(color="#1e8c45")),
                ft.TextButton("Add Color", on_click=pick_hex_color, style=ft.ButtonStyle(color="#1e8c45")),
            ],
            bgcolor="#ffffff"
        )
        page.overlay.append(color_dialog)
        color_dialog.open = True
        page.update()
    
    # Remove color handler
    def remove_color(color):
        colors_list.remove(color)
        update_colors_display()
    
    # Update colors display
    def update_colors_display():
        colors_listview.current.controls.clear()
        for color in colors_list:
            color_hex = color

            colors_listview.current.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            bgcolor=color_hex,
                            width=30,
                            height=30,
                            border_radius=6,
                            border=ft.border.all(1, "#e0e0e0"),
                        ),
                        ft.Text(color, size=13, expand=True, color="#000000"),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="#d32f2f",
                            icon_size=18,
                            on_click=lambda e, c=color: remove_color(c),
                        ),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=8,
                    border=ft.border.all(1, "#e0e0e0"),
                    border_radius=6,
                    margin=ft.margin.only(bottom=5),
                )
            )
        page.update()
    
    # Add size handler
    def add_size(e):
        size_value = size_input.current.value.strip()
        if size_value and size_value not in sizes_list:
            sizes_list.append(size_value)
            size_input.current.value = ""
            update_sizes_display()
    
    # Remove size handler
    def remove_size(size):
        sizes_list.remove(size)
        update_sizes_display()
    
    # Update sizes display
    def update_sizes_display():
        sizes_listview.current.controls.clear()
        for size in sizes_list:
            sizes_listview.current.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(size, size=13, expand=True, color="#000000"),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="#d32f2f",
                            icon_size=18,
                            on_click=lambda e, s=size: remove_size(s),
                        ),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=8,
                    border=ft.border.all(1, "#e0e0e0"),
                    border_radius=6,
                    margin=ft.margin.only(bottom=5),
                )
            )
        page.update()

    # Save button handler
    def on_save(e):
        dialog = Alert.confirm_alert_dialog("Konfirmasi", "Apakah Anda yakin ingin menyimpan perubahan pada produk ini?",lambda e: save(e, dialog))
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def save(e, dialog):
        dialog.open = False
        page.update()
        if new:
            point_mart.add_hadiah(
                name=product_name.current.value,
                points=int(points.current.value),
                stock=int(stock.current.value),
                image=image_path.current.value,
                description=description.current.value,
                category=category.current.value,
                colors=colors_list,
                sizes=sizes_list
            )
        else:
            point_mart.edit_hadiah(
                hadiah_id=product_data["id"],
                name=product_name.current.value,
                points=int(points.current.value),
                stock=int(stock.current.value),
                image=image_path.current.value,
                description=description.current.value,
                category=category.current.value,
                colors=colors_list,
                sizes=sizes_list
            )
        dialog = Alert.create_alert_dialog("Berhasil", "Perubahan pada produk telah disimpan.", lambda e: go_back(None))
        dialog.open = True
        page.overlay.append(dialog)
        page.update()

    # Top navigation bar
    top_nav = create_navbar(page, "Control Menu")

    # Edit Form
    edit_form = ft.Container(
        content=ft.Column(
            [
                # Header with back button
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="#000000",
                            icon_size=24,
                            on_click=go_back,
                        ),
                        ft.Text("Edit Product", size=28, weight=ft.FontWeight.BOLD, color="#000000"),
                    ],
                    spacing=10,
                ),
                ft.Container(height=20),
                
                # Form content in two columns
                ft.Row(
                    [
                        # Left column - Image preview and upload
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Product Image", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Container(height=10),
                                    ft.Container(
                                        content=ft.Image(
                                            ref=product_image,
                                            src=product_data["image"],
                                            fit=ft.ImageFit.COVER,
                                        ),
                                        width=300,
                                        height=300,
                                        border_radius=12,
                                        border=ft.border.all(2, "#e0e0e0"),
                                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                    ),
                                    ft.Container(height=15),
                                    ft.TextField(
                                        ref=image_path,
                                        label="Image Path",
                                        value=product_data["image"],
                                        width=300,
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=13, color="#000000"),
                                    ),
                                    ft.Container(height=10),
                                    ft.ElevatedButton(
                                        "Upload New Image",
                                        icon=ft.Icons.UPLOAD_FILE,
                                        width=300,
                                        bgcolor="#1e8c45",
                                        color="white",
                                        on_click=on_upload_image,
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=13, font_family="PoppinsSBold"),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                ],
                                spacing=0,
                            ),
                            width=350,
                        ),
                        
                        ft.Container(width=40),
                        
                        # Right column - Product details form
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Product Details", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Container(height=20),
                                    
                                    # Product Name
                                    ft.TextField(
                                        ref=product_name,
                                        label="Product Name *",
                                        value=product_data["name"],
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Category
                                    ft.TextField(
                                        ref=category,
                                        label="Category *",
                                        value=product_data["category"],
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        height=55,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Points and Stock in a row
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                ref=points,
                                                label="Points Cost *",
                                                value=str(product_data["points"]),
                                                border_color="#e0e0e0",
                                                focused_border_color="#1e8c45",
                                                text_style=ft.TextStyle(size=14, color="#000000"),
                                                height=55,
                                                keyboard_type=ft.KeyboardType.NUMBER,
                                                expand=True,
                                            ),
                                            ft.Container(width=15),
                                            ft.TextField(
                                                ref=stock,
                                                label="Stock *",
                                                value=str(product_data["stock"]),
                                                border_color="#e0e0e0",
                                                focused_border_color="#1e8c45",
                                                text_style=ft.TextStyle(size=14, color="#000000"),
                                                height=55,
                                                keyboard_type=ft.KeyboardType.NUMBER,
                                                expand=True,
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Description
                                    ft.TextField(
                                        ref=description,
                                        label="Description",
                                        value=product_data.get("description", ""),
                                        border_color="#e0e0e0",
                                        focused_border_color="#1e8c45",
                                        text_style=ft.TextStyle(size=14, color="#000000"),
                                        multiline=True,
                                        min_lines=3,
                                        max_lines=4,
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Colors Section
                                    ft.Text("Available Colors", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Container(height=8),
                                    ft.Container(
                                        content=ft.Column(
                                            ref=colors_listview,
                                            controls=[],
                                            spacing=0,
                                            scroll=ft.ScrollMode.AUTO,
                                        ),
                                        height=120,
                                        border=ft.border.all(1, "#e0e0e0"),
                                        border_radius=8,
                                        padding=8,
                                    ),
                                    ft.Container(height=8),
                                    ft.ElevatedButton(
                                        "Add Color",
                                        icon=ft.Icons.ADD,
                                        on_click=add_color,
                                        bgcolor="#1e8c45",
                                        color="white",
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=13, font_family="PoppinsSBold"),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                    ft.Container(height=15),
                                    
                                    # Sizes Section
                                    ft.Text("Available Sizes", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                                    ft.Container(height=8),
                                    ft.Container(
                                        content=ft.Column(
                                            ref=sizes_listview,
                                            controls=[],
                                            spacing=0,
                                            scroll=ft.ScrollMode.AUTO,
                                        ),
                                        height=120,
                                        border=ft.border.all(1, "#e0e0e0"),
                                        border_radius=8,
                                        padding=8,
                                    ),
                                    ft.Container(height=8),
                                    ft.Row([
                                        ft.TextField(
                                            ref=size_input,
                                            label="Size (e.g. S, M, L, XL)",
                                            border_color="#e0e0e0",
                                            focused_border_color="#1e8c45",
                                            text_style=ft.TextStyle(size=13, color="#000000"),
                                            height=45,
                                            expand=True,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.ADD,
                                            icon_color="white",
                                            bgcolor="#1e8c45",
                                            on_click=add_size,
                                            tooltip="Add Size",
                                        ),
                                    ], spacing=5),
                                    ft.Container(height=25),
                                    
                                    # Action buttons
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Cancel",
                                                on_click=go_back,
                                                bgcolor="#e0e0e0",
                                                color="#666666",
                                                expand=True,
                                                height=45,
                                                style=ft.ButtonStyle(
                                                    text_style=ft.TextStyle(size=14, font_family="PoppinsSBold"),
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                ),
                                            ),
                                            ft.Container(width=15),
                                            ft.ElevatedButton(
                                                "Save Changes",
                                                on_click=on_save,
                                                bgcolor="#1e8c45",
                                                color="white",
                                                expand=True,
                                                height=45,
                                                style=ft.ButtonStyle(
                                                    text_style=ft.TextStyle(size=14, font_family="PoppinsSBold"),
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                ),
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                ],
                                spacing=0,
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
        expand=True,
    )

    # Main container
    main_container = ft.Column(
        [
            top_nav,
            edit_form,
        ],
        expand=True,
    )

    page.add(main_container)
    
    # Initialize displays after page is added
    update_colors_display()
    update_sizes_display()
