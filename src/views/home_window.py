import flet as ft
import re
from views.navbar import create_navbar

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    page.title = "GrowBak - Home"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")
    page.update()

    page.scroll = True

    

    # variabel untuk simpan data (harusnya gada)


    # ini declare navbar
    top_nav = create_navbar(page)

    def show_message(e):
        print("Button diclick!")
        page.update()

    about_us_text = ft.Container(
        content=ft.Row(
            [
                ft.Text("Welcome to GrowBak!", size=32, weight="bold", color="white"),
                ft.Divider(height=30, color="transparent"),
                ft.Text("Growbak is a smart waste management platform that", size=20, weight="bold", color="white"),
            ],
            expand=True,
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=180),
        bgcolor="#1e8c45",        # warna hijau
    )


    # ini nanti dimasukin ke page.add
    # ini adalah bagian dari maincontainer
    about_us = ft.Container(
        content=ft.Row(
            [
                ft.Text("Ini about us (nanti diisi)", size=32, weight="bold", color="white"),
                # ft.Divider(width=100, color="transparent"),
                about_us_text
            ],
            expand=True,
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=180),
        bgcolor="#1e8c45",        # warna hijau
    )

    content_us =  ft.Container(
        content=ft.Row(
            [
                ft.Text("Ini content us", size=32, weight="bold", color="white")
            ],
            expand=True,
            spacing=50,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
        bgcolor="#121413",        # warna hijau
    )

    services = ft.Container(
        content=ft.Row(
            [
                ft.Text("Ini services", size=32, weight="bold", color="white")
            ],
            expand=True,
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
        bgcolor="#1e8c45",        # warna hijau
    )


    main_container = ft.Column(
        [
            top_nav,
            ft.Container(
                content=ft.Column(
                    [
                        about_us,
                        ft.Divider(height=60, color="transparent"),
                        content_us,
                        ft.Divider(height=100, color="transparent"),
                        services
                    ],
                    expand=True,
                ),
                padding=ft.padding.symmetric(horizontal=0, vertical=30),
                expand=True,
            ),
        ],
        expand=True,
    )

    page.add(main_container)