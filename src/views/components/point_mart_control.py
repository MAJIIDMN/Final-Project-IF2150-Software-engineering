import flet as ft
from models.PointMart import PointMart
from views.components import Alert

point_mart = PointMart()

def create_point_mart_control(page: ft.Page):
    """
    Creates the Point Mart Control panel component for admin page.
    Returns the complete UI container with table and product management.
    """
    
    # Function to navigate to edit page
    def go_to_edit(product):
        page.clean()
        page.product_edit_main(page, product)
    
    # Function to handle delete
    def on_delete_product(product_id, product_name):
        def confirm_delete(e):
            point_mart.delete_hadiah(product_id)
            dialog.open = False
            page.update()
            load_products()
        
        dialog = Alert.delete_confirm_dialog("Hapus Produk", product_name, confirm_delete)
        page.dialog = dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    # Function to create product row component
    def create_product_row(product):
        return ft.Container(
            content=ft.Row(
                [
                    # Image
                    ft.Container(
                        content=ft.Image(
                            src=product.get("image", ""),
                            fit=ft.ImageFit.COVER,
                        ),
                        width=60,
                        height=60,
                        border_radius=8,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),
                    # Product Name
                    ft.Container(
                        content=ft.Text(product.get("name", ""), size=13, color="#000000"),
                        expand=2,
                    ),
                    # Category
                    ft.Container(
                        content=ft.Text(product.get("category", ""), size=13, color="#666666"),
                        width=120,
                    ),
                    # Points
                    ft.Container(
                        content=ft.Text(str(product.get("points", 0)), size=13, weight=ft.FontWeight.BOLD, color="#1e8c45"),
                        width=100,
                    ),
                    # Stock
                    ft.Container(
                        content=ft.Text(str(product.get("stock", 0)), size=13, color="#000000"),
                        width=80,
                    ),
                    # Actions
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color="#1976d2",
                                    tooltip="Edit",
                                    on_click=lambda e, p=product: go_to_edit(p),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="#d32f2f",
                                    tooltip="Delete",
                                    on_click=lambda e, pid=product.get("id", ""), pname=product.get("name", ""): on_delete_product(pid, pname),
                                ),
                            ],
                            spacing=5,
                        ),
                        width=150,
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            border=ft.border.only(bottom=ft.BorderSide(1, "#e0e0e0")),
        )
    
    # Product list view reference
    product_list_view = ft.Ref[ft.ListView]()
    
    # Function to load products from database
    def load_products():
        product_list = point_mart.load_hadiah()
        
        # Clear and populate list
        product_list_view.current.controls.clear()
        for product in product_list:
            product_list_view.current.controls.append(create_product_row(product))
        page.update()
    
    # Function to handle add new product
    def on_add_product(e):
        page.clean()
        page.product_edit_main(page, None)  # Pass None for new product

    # Main container
    mart_control_container = ft.Container(
        content=ft.Column(
            [
                # Header dengan tombol Add New Product
                ft.Row(
                    [
                        ft.Text("Point Mart Management", size=24, weight=ft.FontWeight.BOLD, color="#000000"),
                        ft.ElevatedButton(
                            "Add New Product",
                            icon=ft.Icons.ADD,
                            bgcolor="#1e8c45",
                            color="white",
                            on_click=on_add_product,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=14, font_family="PoppinsSBold"),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=20),
                
                # Table Header
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Image", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                width=80,
                            ),
                            ft.Container(
                                content=ft.Text("Product Name", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                expand=2,
                            ),
                            ft.Container(
                                content=ft.Text("Category", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                width=120,
                            ),
                            ft.Container(
                                content=ft.Text("Points", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                width=100,
                            ),
                            ft.Container(
                                content=ft.Text("Stock", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                width=80,
                            ),
                            ft.Container(
                                content=ft.Text("Actions", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                width=150,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    bgcolor="#f5f5f5",
                    border_radius=ft.border_radius.only(top_left=8, top_right=8),
                ),
                
                # Product List (Scrollable)
                ft.Container(
                    content=ft.ListView(
                        ref=product_list_view,
                        controls=[],
                        spacing=0,
                        expand=True,
                    ),
                    border=ft.border.all(1, "#e0e0e0"),
                    border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )
    
    # Load products when component is created
    load_products()
    
    return mart_control_container
