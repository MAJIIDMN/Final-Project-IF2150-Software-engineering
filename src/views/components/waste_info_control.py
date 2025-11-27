import flet as ft
from models.waste_info import wasteController
from views.components import Alert

waste_info = wasteController()

def create_waste_info_control(page: ft.Page):
    waste_list = waste_info.load_waste_info()
    """
    Creates the Waste Info Control panel component for admin page.
    Returns the complete UI container with table and waste info management.
    """
    
    # Search state
    search_query = ""
    
    # Function to navigate to edit page
    def go_to_edit(waste):
        page.clean()
        page.waste_edit_main(page, waste)
    
    # Function to handle delete
    def on_delete_waste(waste_title):
        def confirm_delete(e):
            waste_info.delete_waste_info(waste_title)
            dialog.open = False
            page.update()
            load_waste_info()
        
        dialog = Alert.delete_confirm_dialog("Hapus Informasi Sampah", waste_title, confirm_delete)
        page.dialog = dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    # Function to create waste row component
    def create_waste_row(waste):
        return ft.Container(
            content=ft.Row(
                [
                    # Image
                    ft.Container(
                        content=ft.Image(
                            src=waste.image_path,
                            fit=ft.ImageFit.COVER,
                        ),
                        width=60,
                        height=60,
                        border_radius=8,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),
                    # Jenis
                    ft.Container(
                        content=ft.Text(waste.jenis, size=13, weight=ft.FontWeight.BOLD, color="#1e8c45"),
                        width=150,
                    ),
                    # Title
                    ft.Container(
                        content=ft.Text(waste.title, size=13, color="#000000"),
                        expand=2,
                    ),
                    # Description (truncated)
                    ft.Container(
                        content=ft.Text(
                            waste.text_part[:100] + "..." if len(waste.text_part) > 100 else waste.text_part,
                            size=12,
                            color="#666666",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        expand=3,
                    ),
                    # Actions
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color="#1976d2",
                                    tooltip="Edit",
                                    on_click=lambda e, w=waste: go_to_edit(w),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="#d32f2f",
                                    tooltip="Delete",
                                    on_click=lambda e, wtitle=waste.jenis: on_delete_waste(wtitle),
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
    
    # Waste list view reference
    waste_list_view = ft.Ref[ft.ListView]()
    search_field = ft.Ref[ft.TextField]()
    
    # Function to handle search
    def on_search_change(e):
        nonlocal search_query, waste_list
        search_query = e.control.value
        waste_list = waste_info.search_waste_info(search_query)
        waste_list_view.current.controls.clear()
        for waste in waste_list:
            waste_list_view.current.controls.append(create_waste_row(waste))
        waste_control_container.update()
    
    # Function to load waste info from database
    def load_waste_info():
        nonlocal waste_list
        waste_list_view.current.controls.clear()
        for waste in waste_list:
            waste_list_view.current.controls.append(create_waste_row(waste))
    
    # Function to handle add new waste info
    def on_add_waste(e):
        page.clean()
        page.waste_edit_main(page, None)  # Pass None for new waste info

    # Main container
    waste_control_container = ft.Container(
        content=ft.Column(
            [
                # Header dengan tombol Add New Waste Info
                ft.Row(
                    [
                        ft.Text("Waste Information Management", size=24, weight=ft.FontWeight.BOLD, color="#000000"),
                        ft.ElevatedButton(
                            "Add New Waste Info",
                            icon=ft.Icons.ADD,
                            bgcolor="#1e8c45",
                            color="white",
                            on_click=on_add_waste,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=14, font_family="PoppinsSBold"),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=20),
                
                # Search Bar
                ft.Container(
                    content=ft.TextField(
                        ref=search_field,
                        hint_text="Search by ID, Type, or Title",
                        prefix_icon=ft.Icons.SEARCH,
                        border_color="#e0e0e0",
                        focused_border_color="#1e8c45",
                        on_change=on_search_change,
                        text_style=ft.TextStyle(size=14, color="#000000"),
                        height=50,
                    ),
                    margin=ft.margin.only(bottom=20),
                ),
                
                # Table Header
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Image", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                width=80,
                            ),
                            ft.Container(
                                content=ft.Text("Type", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                width=150,
                            ),
                            ft.Container(
                                content=ft.Text("Title", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                expand=2,
                            ),
                            ft.Container(
                                content=ft.Text("Description", size=12, weight=ft.FontWeight.BOLD, color="#666666"),
                                expand=3,
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
                
                # Waste List (Scrollable)
                ft.Container(
                    content=ft.ListView(
                        ref=waste_list_view,
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
    load_waste_info()
    
    return waste_control_container
