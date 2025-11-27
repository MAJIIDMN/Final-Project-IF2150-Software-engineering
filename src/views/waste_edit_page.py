import flet as ft
from models.waste_info import wasteController
from views.components.navbar import create_navbar
from views.components import Alert
import os

waste_info_model = wasteController()

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page, waste_data=None):
    """
    Waste info edit page
    waste_data: dict with keys: id, jenis, title, description, image (for edit mode)
    If waste_data is None, it's in add mode
    """
    page.title = "GrowBak - Edit Waste Info" if waste_data else "GrowBak - Add Waste Info"
    page.window_width = 1440
    page.window_height = 900
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")
    
    # Edit mode or add mode
    is_edit_mode = waste_data is not None
    
    # Form state
    original_jenis = waste_data.jenis if is_edit_mode else ""
    original_title = waste_data.title if is_edit_mode else ""
    original_description = waste_data.text_part if is_edit_mode else ""
    original_image = waste_data.image_path if is_edit_mode else ""
    
    # Image picker
    selected_image_path = original_image
    
    def pick_image(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"],
        )
    
    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal selected_image_path
        if e.files:
            selected_image_path = e.files[0].path
            image_preview.current.src = selected_image_path
            image_preview.current.update()
    
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    
    # Form fields
    jenis_field = ft.Ref[ft.TextField]()
    title_field = ft.Ref[ft.TextField]()
    description_field = ft.Ref[ft.TextField]()
    image_preview = ft.Ref[ft.Image]()
    save_btn = ft.Ref[ft.ElevatedButton]()
    
    # Check if form has changes
    def check_changes():
        if not is_edit_mode:
            # Add mode: enable if all fields filled
            has_data = (
                jenis_field.current.value and
                title_field.current.value and
                description_field.current.value and
                selected_image_path
            )
            save_btn.current.disabled = not has_data
        else:
            # Edit mode: enable if something changed
            has_changes = (
                jenis_field.current.value != original_jenis or
                title_field.current.value != original_title or
                description_field.current.value != original_description or
                selected_image_path != original_image
            )
            save_btn.current.disabled = not has_changes
        
        save_btn.current.bgcolor = "#1e8c45" if not save_btn.current.disabled else "#cccccc"
        save_btn.current.update()
    
    def on_field_change(e):
        check_changes()
    
    # Save function
    def on_save(e):
        def confirm_save(e):
            jenis = jenis_field.current.value.strip()
            title = title_field.current.value.strip()
            description = description_field.current.value.strip()
            
            if not jenis or not title or not description or not selected_image_path:
                error_dialog = Alert.create_alert_dialog(
                    "Error",
                    "All fields must be filled!",
                    lambda e: None
                )
                page.dialog = error_dialog
                page.overlay.append(error_dialog)
                error_dialog.open = True
                page.update()
                return
            
            try:
                if is_edit_mode:
                    waste_info_model.update_waste_info(original_jenis, title, description, selected_image_path)
                    success_msg = "Waste information updated successfully!"
                else:
                    waste_info_model.add_waste_info(jenis, title, description, selected_image_path)
                    success_msg = "Waste information added successfully!"
                
                success_dialog = Alert.create_alert_dialog(
                    "Success",
                    success_msg,
                    lambda e: go_back(e)
                )
                page.dialog = success_dialog
                page.overlay.append(success_dialog)
                success_dialog.open = True
                page.update()
            except Exception as ex:
                error_dialog = Alert.create_alert_dialog(
                    "Error",
                    f"Failed to save: {str(ex)}",
                    lambda e: None
                )
                page.dialog = error_dialog
                page.overlay.append(error_dialog)
                error_dialog.open = True
                page.update()
        
        confirm_dialog = Alert.confirm_alert_dialog(
            "Confirm Save",
            f"Are you sure you want to {'update' if is_edit_mode else 'add'} this waste information?",
            confirm_save
        )
        page.dialog = confirm_dialog
        page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        page.update()
    
    def go_back(e):
        page.clean()
        page.admin_control_main(page)
    
    # Top navigation bar
    top_nav = create_navbar(page, "Control Menu")
    
    # Form content
    form_content = ft.Container(
        content=ft.Column(
            [
                # Header
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="#1e8c45",
                            on_click=go_back,
                            tooltip="Back to Control Menu",
                        ),
                        ft.Text(
                            f"{'Edit' if is_edit_mode else 'Add'} Waste Information",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#000000",
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=20),
                
                # Form fields
                ft.Container(
                    content=ft.Column(
                        [
                            # Image preview
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Image", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Container(height=5),
                                        ft.Image(
                                            ref=image_preview,
                                            src=original_image if original_image else "src/database/image/default_waste.png",
                                            width=300,
                                            height=200,
                                            fit=ft.ImageFit.COVER,
                                            border_radius=8,
                                        ),
                                        ft.Container(height=10),
                                        ft.ElevatedButton(
                                            "Choose Image",
                                            icon=ft.Icons.IMAGE,
                                            on_click=pick_image,
                                            bgcolor="#1e8c45",
                                            color="white",
                                            style=ft.ButtonStyle(
                                                text_style=ft.TextStyle(size=14, font_family="Poppins"),
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                            ),
                                        ),
                                    ],
                                ),
                                padding=20,
                            ),
                            
                            # Jenis
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Type (Jenis)", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Container(height=5),
                                        ft.TextField(
                                            ref=jenis_field,
                                            value=original_jenis,
                                            hint_text="e.g., plastic, metal, clothes",
                                            border_color="#e0e0e0",
                                            focused_border_color="#1e8c45",
                                            text_style=ft.TextStyle(size=14, color="#000000"),
                                            on_change=on_field_change,
                                            disabled=is_edit_mode,
                                        ),
                                    ],
                                ),
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                            ),
                            
                            # Title
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Title", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Container(height=5),
                                        ft.TextField(
                                            ref=title_field,
                                            value=original_title,
                                            hint_text="e.g., Plastic Bottles",
                                            border_color="#e0e0e0",
                                            focused_border_color="#1e8c45",
                                            text_style=ft.TextStyle(size=14, color="#000000"),
                                            on_change=on_field_change,
                                        ),
                                    ],
                                ),
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                            ),
                            
                            # Description
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Description", size=14, weight=ft.FontWeight.BOLD, color="#000000"),
                                        ft.Container(height=5),
                                        ft.TextField(
                                            ref=description_field,
                                            value=original_description,
                                            hint_text="Detailed description about this waste type...",
                                            multiline=True,
                                            min_lines=5,
                                            max_lines=10,
                                            border_color="#e0e0e0",
                                            focused_border_color="#1e8c45",
                                            text_style=ft.TextStyle(size=14, color="#000000"),
                                            on_change=on_field_change,
                                        ),
                                    ],
                                ),
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                            ),
                            
                            # Save button
                            ft.Container(
                                content=ft.ElevatedButton(
                                    ref=save_btn,
                                    text=f"{'Update' if is_edit_mode else 'Add'} Waste Information",
                                    icon=ft.Icons.SAVE,
                                    bgcolor="#cccccc" if is_edit_mode else "#cccccc",
                                    color="white",
                                    disabled=True if is_edit_mode else True,
                                    on_click=on_save,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size=16, font_family="PoppinsSBold"),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    height=50,
                                ),
                                padding=20,
                                alignment=ft.alignment.center,
                            ),
                        ],
                        spacing=0,
                    ),
                    border=ft.border.all(1, "#e0e0e0"),
                    border_radius=8,
                    bgcolor="#ffffff",
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.padding.symmetric(horizontal=100, vertical=30),
        expand=True,
    )
    
    # Main container
    main_container = ft.Column(
        [
            top_nav,
            form_content,
        ],
        expand=True,
    )
    
    page.add(main_container)
    
    # Initial check
    check_changes()
