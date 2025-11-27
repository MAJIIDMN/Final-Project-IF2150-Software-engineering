import flet as ft
import re
from views.components.navbar import create_navbar
from models.waste_info import wasteController

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    waste = wasteController()
    page.title = "GrowBak - Informasi Sampah"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    page.bgcolor = "#ffffff"
    
    page.fonts = fonts
    page.theme = ft.Theme(font_family="Poppins")
    page.update()

    page.scroll = True


    # ini declare navbar
    top_nav = create_navbar(page, "info")

    
    def make_waste_section(data):

        section = ft.Container(
            width=float("inf"),
            content=ft.Column(
                [
                    # title
                    ft.Container(
                        width=float("inf"),
                        content=ft.Column(
                            [
                                ft.Text(
                                    data.title,
                                    size=50,
                                    weight="bold",
                                    color="#145C39"
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=0, vertical=20),
                        bgcolor="#EBF8A9",
                    ),

                    # image
                    ft.Image(
                        src=data.image_path,
                        fit=ft.ImageFit.COVER,
                        width=float("inf")
                    ),

                    # deskripsi
                    ft.Container(
                        width=float("inf"),
                        content=ft.Column(
                            [
                                ft.Text(
                                    data.text_part,
                                    size=20,
                                    color="black",
                                    text_align=ft.TextAlign.JUSTIFY,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=100, vertical=20),
                        bgcolor="#FFFFFF",
                    ),
                ],
                spacing=0,
            ),
        )

        return section
    
    waste_list = waste.load_waste_info()

    main_container = ft.Column(
        [
            top_nav,
            ft.Container(
                width=float("inf"),
                padding=ft.padding.symmetric(horizontal=100, vertical=20),
                content=ft.Column(
                    [
                        make_waste_section(data)
                        for data in waste_list
                    ],
                    spacing=30,
                ),
            ),
        ],
        expand=True,
        spacing=0,
    )

    page.add(main_container)