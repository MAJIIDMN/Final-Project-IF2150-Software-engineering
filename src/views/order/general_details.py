import flet as ft
from views.navbar import create_navbar
from components.shared import create_sidebar

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def show_alert(page, message):
    page.snack_bar = ft.SnackBar(ft.Text(message))
    page.snack_bar.open = True
    page.update()

def GeneralDetailsView(page, order_state):
    selected_types = order_state.waste_types if order_state.waste_types else []
    # pastikan tidak ada duplikat dan maksimal 3 item
    seen = set()
    deduped = []
    for t in selected_types:
        if t in seen:
            continue
        if t in (None, "", "- None -"):
            continue
        seen.add(t)
        deduped.append(t)
        if len(deduped) == 3:
            break
    selected_types = deduped
    order_state.waste_types = deduped
    card_height = page.window_height - 140 if page.window_height else 680
    
    def file_picker_result(e):
        if e.files and len(e.files) > 0:
            f = e.files[0]
            order_state.attachment = f.name
            try:
                attachment_label.value = f.name
                attachment_label.color = "#000000"
                attachment_label.update()
            except NameError:
                # attachment_label belum dibuat (awal render), abaikan
                pass
            try:
                # simple preview untuk file gambar
                if getattr(f, "path", None) and f.name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                    attachment_preview.content = ft.Image(src=f.path, width=80, height=80, fit=ft.ImageFit.COVER)
                else:
                    attachment_preview.content = None
                attachment_preview.update()
            except NameError:
                # attachment_preview belum dibuat, abaikan
                pass

    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    def toggle_type(e, waste_type):
        if waste_type in selected_types:
            selected_types.remove(waste_type)
            e.control.border = ft.border.all(2, "#e0e0e0")
        else:
            if len(selected_types) < 3:
                selected_types.append(waste_type)
                e.control.border = ft.border.all(2, "#2e7d32")

        # sinkronkan dropdown berdasarkan selected_types (maks 3)
        dropdowns = [first_dropdown, second_dropdown, third_dropdown]
        for idx, t in enumerate(selected_types):
            dropdowns[idx].value = t
        for idx in range(len(selected_types), 3):
            dropdowns[idx].value = "- None -"
        for d in dropdowns:
            d.update()

        e.control.update()
        update_points()
    
    def dropdown_change(e):
        dd = [first_dropdown, second_dropdown, third_dropdown]

        # sync selected_types dari dropdown
        selected_types.clear()
        for d in dd:
            if d.value and d.value != "- None -":
                selected_types.append(d.value)

        # jika dropdown di-set ke None, kosongkan dan kunci weight terkait
        pairs_dd_weight = [
            (first_dropdown, weight_input),
            (second_dropdown, weight_input_2),
            (third_dropdown, weight_input_3),
        ]
        for d, field in pairs_dd_weight:
            is_none = d.value in (None, "", "- None -")
            if is_none:
                field.value = ""
            field.read_only = is_none
            field.bgcolor = "#f5f5f5" if is_none else "white"
            field.hint_text = "-" if is_none else "0"
            field.update()

        # perbarui opsi dropdown secara dinamis agar tipe yang sudah dipilih
        # tidak muncul lagi di dropdown lain
        all_types = ["Plastic", "Metal", "Clothes"]
        current_vals = [d.value for d in dd]
        for i, d in enumerate(dd):
            used_by_others = {
                v
                for j, v in enumerate(current_vals)
                if j != i and v not in (None, "", "- None -")
            }
            allowed = [t for t in all_types if t not in used_by_others]
            new_options = [ft.dropdown.Option("- None -")] + [
                ft.dropdown.Option(t) for t in allowed
            ]
            d.options = new_options
            valid_values = ["- None -"] + allowed
            if d.value not in valid_values:
                d.value = "- None -"
            d.update()

        # rebuild selected_types setelah kemungkinan reset value
        selected_types.clear()
        for d in dd:
            if d.value and d.value != "- None -":
                selected_types.append(d.value)

        update_points()

    def update_points():
        try:
            # ambil pasangan (tipe, berat) dari ketiga input
            val = [first_dropdown.value, second_dropdown.value, third_dropdown.value]
            raw_weights = [
                weight_input.value.strip() if weight_input.value else "",
                weight_input_2.value.strip() if weight_input_2.value else "",
                weight_input_3.value.strip() if weight_input_3.value else "",
            ]

            total_weight = 0.0
            points = 0.0

            for t, w_str in zip(val, raw_weights):
                if not w_str:
                    continue
                if t in (None, "", "- None -"):
                    # berat tanpa tipe diabaikan di sini; akan divalidasi di next_step
                    continue
                w = float(w_str)
                if w < 0:
                    # abaikan nilai negatif di perhitungan poin
                    continue
                base = 0
                if t == "Plastic":
                    base = 1
                elif t == "Clothes":
                    base = 2
                elif t == "Metal":
                    base = 3
                total_weight += w
                points += base * w

            order_state.weight = total_weight
            
            # faktor berdasarkan kondisi sampah
            condition_value = None
            try:
                condition_value = condition_dropdown.value
            except NameError:
                condition_value = getattr(order_state, "condition", None)

            factor = 1.0
            if condition_value == "Good":
                factor = 1.0
            elif condition_value == "Fair":
                factor = 0.8
            elif condition_value == "Poor":
                factor = 0.5

            points *= factor
            # tampilkan hanya 2 angka di belakang koma
            points_rounded = round(points, 2)
            points_text.value = f"+ {points_rounded:.2f} points"
            order_state.point_gained = points_rounded

        except:
            points_text.value = "+ 0 points"
        points_text.update()
    
    def weight_changed(e):
        pairs = [
            (first_dropdown.value, weight_input),
            (second_dropdown.value, weight_input_2),
            (third_dropdown.value, weight_input_3),
        ]

        total_weight = 0.0
        for t, field in pairs:
            v = field.value.strip() if field.value else ""
            if not v:
                continue
            if t in (None, "", "- None -"):
                # tidak boleh ada berat untuk tipe yang None
                field.value = ""
                field.update()
                show_alert(e.page, "Please select a type before entering weight.")
                continue
            try:
                w = float(v)
                if w < 0:
                    field.value = ""
                    field.update()
                    show_alert(e.page, "Weight cannot be negative.")
                    continue
                total_weight += w
            except:
                # biarkan validasi angka ditangani di next_step
                pass

        order_state.weight = total_weight
        # simpan masing-masing weight ke state agar bisa dipulihkan saat kembali dari halaman lain
        order_state.weight_1 = weight_input.value.strip() if weight_input.value else ""
        order_state.weight_2 = weight_input_2.value.strip() if weight_input_2.value else ""
        order_state.weight_3 = weight_input_3.value.strip() if weight_input_3.value else ""
        update_points()
    
    def condition_changed(e):
        order_state.condition = e.control.value
        update_points()
    
    def clean_checkbox_changed(e):
        order_state.confirm_clean = e.control.value

    def recyclable_checkbox_changed(e):
        order_state.confirm_recyclable = e.control.value

    def read_checkbox_changed(e):
        order_state.confirm_read = e.control.value

    def clear_attachment(e):
        order_state.attachment = None
        try:
            attachment_label.value = "No file selected"
            attachment_label.color = "#757575"
            attachment_label.update()
        except NameError:
            pass
        try:
            attachment_preview.content = None
            attachment_preview.update()
        except NameError:
            pass
    
    def next_step(e):
        # validate required fields before proceeding 
        # waste types
        if len(selected_types) == 0:
            page.snack_bar = ft.SnackBar(ft.Text("Please select at least one waste type."))
            page.snack_bar.open = True
            page.update()
            return
        # tidak boleh ada tipe yang duplikat
        type_values = [first_dropdown.value, second_dropdown.value, third_dropdown.value]
        types_no_none = [t for t in type_values if t not in (None, "", "- None -")]
        if len(types_no_none) != len(set(types_no_none)):
            page.snack_bar = ft.SnackBar(ft.Text("Each waste type must be unique."))
            page.snack_bar.open = True
            page.update()
            return
        # weight – hanya hitung berat dengan tipe valid, dan blok jika ada berat tanpa tipe
        pairs = [
            (first_dropdown.value, weight_input.value.strip() if weight_input.value else ""),
            (second_dropdown.value, weight_input_2.value.strip() if weight_input_2.value else ""),
            (third_dropdown.value, weight_input_3.value.strip() if weight_input_3.value else ""),
        ]
        total_weight = 0.0
        has_invalid = False
        has_orphan = False
        for t, w in pairs:
            if not w:
                continue
            if t in (None, "", "- None -"):
                has_orphan = True
                break
            try:
                val = float(w)
            except:
                has_invalid = True
                break
            if val < 0:
                has_invalid = True
                break
            total_weight += val
        if has_orphan:
            page.snack_bar = ft.SnackBar(ft.Text("Please select a type for each weight."))
            page.snack_bar.open = True
            page.update()
            return
        if has_invalid or total_weight < 3 or total_weight > 20:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter valid weights (total 3-20 kg)."))
            page.snack_bar.open = True
            page.update()
            return
        # condition
        if condition_dropdown.value in (None, "", "- None -"):
            page.snack_bar = ft.SnackBar(ft.Text("Please select the waste condition."))
            page.snack_bar.open = True
            page.update()
            return

        if not getattr(order_state, "attachment", None):
            page.snack_bar = ft.SnackBar(ft.Text("Please add an attachment before continuing."))
            page.snack_bar.open = True
            page.update()
            return

        if not (
            getattr(order_state, "confirm_clean", False)
            and getattr(order_state, "confirm_recyclable", False)
            and getattr(order_state, "confirm_read", False)
        ):
            page.snack_bar = ft.SnackBar(ft.Text("Please confirm all checkboxes before continuing."))
            page.snack_bar.open = True
            page.update()
            return

        order_state.waste_types = selected_types.copy()
        order_state.weight = total_weight
        order_state.condition = condition_dropdown.value
        page.go("/order/address")
    
    # Waste type images
    plastic_img = ft.Container(
        content=ft.Image(src="https://recykal.com/wp-content/uploads/2021/11/12c26-017154e4-47d7-45af-95ab-ad3b8e4ff3f9-1.jpg", width=120,height=80,fit=ft.ImageFit.COVER),
        width=120,
        height=80,
        bgcolor="#4a90e2",
        border_radius=10,
        alignment=ft.alignment.center,
        border=ft.border.all(2, "#2e7d32" if "Plastic" in selected_types else "#e0e0e0"),
        # on_click=lambda e: toggle_type(e, "Plastic"),
    )
    
    metal_img = ft.Container(
        content=ft.Image(src="https://media.generalkinematics.com/wp-content/uploads/2023/04/iStock-491962627.jpg", width=120,height=80,fit=ft.ImageFit.COVER),
        width=120,
        height=80,
        bgcolor="#5dade2",
        border_radius=10,
        alignment=ft.alignment.center,
        border=ft.border.all(2, "#2e7d32" if "Metal" in selected_types else "#e0e0e0"),
        # on_click=lambda e: toggle_type(e, "Metal"),
    )
    
    clothes_img = ft.Container(
        content=ft.Image(src="https://www.coventry.ac.uk/contentassets/e0764d99a985459fab1c995b519ed545/image4jo5.png", width=120,height=80,fit=ft.ImageFit.COVER),
        width=120,
        height=80,
        bgcolor="#85929e",
        border_radius=10,
        alignment=ft.alignment.center,
        border=ft.border.all(2, "#2e7d32" if "Clothes" in selected_types else "#e0e0e0"),
        # on_click=lambda e: toggle_type(e, "Clothes"),
    )
    
    # initial enabled/disabled state untuk field weight berdasarkan selected_types
    has_first_type = len(selected_types) > 0
    has_second_type = len(selected_types) > 1
    has_third_type = len(selected_types) > 2

    weight_input = ft.TextField(
        label="",
        value=order_state.weight_1 if getattr(order_state, "weight_1", "") else "",
        hint_text="-",
        width=200,
        on_change=weight_changed,
        border_color="#e0e0e0",
        text_style=ft.TextStyle(color="#000000"),
        cursor_color="#000000",
        read_only=not has_first_type,
        bgcolor="#f5f5f5" if not has_first_type else "white",
        
    )
    
    weight_input_2 = ft.TextField(
        label="",
        value=order_state.weight_2 if getattr(order_state, "weight_2", "") else "",
        hint_text="-",
        width=200,
        on_change=weight_changed,
        border_color="#e0e0e0",
        text_style=ft.TextStyle(color="#000000"),
        cursor_color="#000000",
        read_only=not has_second_type,
        bgcolor="#f5f5f5" if not has_second_type else "white",
    )

    weight_input_3 = ft.TextField(
        label="",
        value=order_state.weight_3 if getattr(order_state, "weight_3", "") else "",
        hint_text="-",
        width=200,
        on_change=weight_changed,
        border_color="#e0e0e0",
        text_style=ft.TextStyle(color="#000000"),
        cursor_color="#000000",
        read_only=not has_third_type,
        bgcolor="#f5f5f5" if not has_third_type else "white",
    )
    
    points_text = ft.Text(
        f"+ {order_state.point_gained:.2f} points" if getattr(order_state, "point_gained", 0) else "+ 0 points",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="#2e7d32",
    )

    # nilai awal dropdown berdasarkan selected_types (maks 3)
    first_value = selected_types[0] if len(selected_types) > 0 else "- None -"
    second_value = selected_types[1] if len(selected_types) > 1 else "- None -"
    third_value = selected_types[2] if len(selected_types) > 2 else "- None -"

    first_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("- None -"),
            ft.dropdown.Option("Plastic"),
            ft.dropdown.Option("Metal"),
            ft.dropdown.Option("Clothes"),
        ],
        value=first_value,
        border_color="#e0e0e0",
        color="#000000",
        on_change=dropdown_change,
    )

    second_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("- None -"),
            ft.dropdown.Option("Plastic"),
            ft.dropdown.Option("Metal"),
            ft.dropdown.Option("Clothes"),
        ],
        value=second_value,
        border_color="#e0e0e0",
        color="#000000",
        on_change=dropdown_change,
    )

    third_dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("- None -"),
            ft.dropdown.Option("Plastic"),
            ft.dropdown.Option("Metal"),
            ft.dropdown.Option("Clothes"),
        ],
        value=third_value,
        border_color="#e0e0e0",
        color="#000000",
        on_change=dropdown_change,
    )

    # Main content
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Text(
                    "General Details",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#212121",
                ),
                ft.Text(
                    "Add the details of your waste",
                    size=14,
                    color="#000000",
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[plastic_img, metal_img, clothes_img],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Type (max. 3)", size=12, color="#000000"),
                                first_dropdown,
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("", size=12, color="#757575"),
                                second_dropdown,
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("", size=12, color="#757575"),
                                third_dropdown,
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                # Row pertama: Weight (3 field sejajar)
                ft.Row(
                    controls=[
                        ft.Column(
                            controls = [
                                ft.Text("Weight (kg) (min. 3 kg, max. 20 kg)", size=12, color="#000000"),
                                ft.Row(
                                    controls=[
                                        weight_input,
                                        weight_input_2,
                                        weight_input_3,
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                # Row kedua: Condition dan Points di bawah weight
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Condition", size=12, color="#000000"),
                                # condition dropdown
                                condition_dropdown := ft.Dropdown(
                                    width=200,
                                    options=[
                                        ft.dropdown.Option("- None -"),
                                        ft.dropdown.Option("Good"),
                                        ft.dropdown.Option("Fair"),
                                        ft.dropdown.Option("Poor"),
                                    ],
                                    value=order_state.condition if order_state.condition else "- None -",
                                    border_color="#e0e0e0",
                                    on_change=condition_changed,
                                    color="#000000",
                                ),
                            ],
                            spacing=5,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Points Gained", size=12, color="#000000"),
                                points_text,
                            ],
                            spacing=5,
                        ),
                    ],
                    spacing=40,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Add an attachment", size=14, color="#000000"),
                                attachment_label := ft.Text(
                                    order_state.attachment if getattr(order_state, "attachment", None) else "No file selected",
                                    size=12,
                                    color="#757575",
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(name=ft.Icons.ADD, color="#2e7d32"),
                                            width=60,
                                            height=60,
                                            border=ft.border.all(2, "#e0e0e0"),
                                            border_radius=8,
                                            alignment=ft.alignment.center,
                                            on_click=lambda e: file_picker.pick_files(allow_multiple=False),
                                        ),
                                        ft.Container(
                                            content=ft.Icon(name=ft.Icons.DELETE_OUTLINE, size=30, color="white"),
                                            width=60,
                                            height=60,
                                            bgcolor="#4a90e2",
                                            border_radius=8,
                                            alignment=ft.alignment.center,
                                            on_click=clear_attachment,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                attachment_preview := ft.Container(),
                            ],
                            spacing=10,
                        ),
                        ft.Container(width=100),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Checkbox(
                                            value=getattr(order_state, "confirm_clean", False),
                                            fill_color="white",
                                            check_color="#2e7d32",
                                            on_change=clean_checkbox_changed,
                                        ),
                                        ft.Text("You have sort and clean your anorganic waste", size=13, color="#000000"),
                                    ],
                                    spacing=10,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Checkbox(
                                            value=getattr(order_state, "confirm_recyclable", False),
                                            fill_color="white",
                                            check_color="#2e7d32",
                                            on_change=recyclable_checkbox_changed,
                                        ),
                                        ft.Text("You agree that this waste is recyclable", size=13, color="#000000"),
                                    ],
                                    spacing=10,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Checkbox(
                                            value=getattr(order_state, "confirm_read", False),
                                            fill_color="white",
                                            check_color="#2e7d32",
                                            on_change=read_checkbox_changed,
                                        ),
                                        ft.Text("You have read the waste information", size=13, color="#000000"),
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=15,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=30),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Back",
                            width=120,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor="white",
                                color="#2e7d32",
                            ),
                        ),
                        ft.ElevatedButton(
                            "Next Step",
                            width=120,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor="#2e7d32",
                                color="white",
                            ),
                            on_click=next_step,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor="white",
        height=card_height,
        expand = True,
        padding=40,
    )
    
    # Layout
    content = ft.Row(
        controls=[
            create_sidebar(page, 1, order_state),
            main_content,
        ],
        spacing=0,
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