import flet as ft
import re
from views.components.navbar import create_navbar
from services.database import DatabaseService


fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    db = DatabaseService()
    texts = db.load_waste_info("src/database/file/texts.csv")
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

    
    def make_waste_section(type: str):
        data = texts[type]  # dict: { title, desc, imgsource }

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
                                    data["title"],
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
                        src=data["imgsource"],
                        fit=ft.ImageFit.COVER,
                        width=float("inf")
                    ),

                    # deskripsi
                    ft.Container(
                        width=float("inf"),
                        content=ft.Column(
                            [
                                ft.Text(
                                    data["desc"],
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

    main_container = ft.Column(
        [
            top_nav,
            make_waste_section("plastic"),
            make_waste_section("metal"),
            make_waste_section("clothes"),

        ],
        expand=True,
        spacing=0,
    )

    page.add(main_container)