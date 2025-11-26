import flet as ft
import re
from views.navbar import create_navbar

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
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

    plastic_title = ft.Container(
        width=float("inf"),
        content=ft.Column(
            [
                ft.Text("Plastic Bottles", size=50, weight="bold", color="#145C39"),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=0, vertical=20),
        bgcolor="#EBF8A9",  
    )

    plastic_text = ft.Container(
        width=float("inf"),
        content=ft.Column([
            ft.Text("               Every minute, about one million plastic bottles are purchased worldwide, contributing to more than 480 billion bottles sold each year, most of which are designed for single use. Unfortunately, only about 9% of all plastic waste is recycled, while the rest ends up in landfills, incinerated, or polluting natural environments such as rivers and oceans. These bottles, mostly made of PET plastic, can take up to 450 years to decompose, causing long-term environmental damage and contributing to microplastic pollution. Their production also consumes large amounts of fossil fuels and releases significant greenhouse gas emissions, linking plastic waste directly to climate change. Without improved recycling systems, stronger waste management infrastructure, and reduced single-use consumption, plastic bottle waste will continue to grow, harming ecosystems, wildlife, and human health on a global scale.", 
                size=20, color="black",text_align=ft.TextAlign.JUSTIFY,),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=100, vertical=20),
        bgcolor = "#FFFFFF"
    )


    metal_title = ft.Container(
        width=float("inf"),
        content=ft.Column(
            [
                ft.Text("Metal Cans", size=50, weight="bold", color="#145C39"),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=0, vertical=20),
        bgcolor="#EBF8A9",  
    )

    metal_text = ft.Container(
        width=float("inf"),
        content=ft.Column([
            ft.Text("          Every year, billions of metal cans—mostly made from aluminum and steel—are produced and used for beverages and food packaging worldwide. While aluminum cans are highly recyclable, with around 70–75% of all aluminum ever produced still in use today, millions of cans are still discarded improperly each day, wasting valuable materials and energy. Producing new aluminum from raw bauxite ore requires up to 95% more energy than recycling existing metal, and it emits large amounts of carbon dioxide, contributing to climate change. When not recycled, metal cans can take 50 to 200 years to fully decompose in landfills, potentially releasing harmful substances into soil and water. Increasing recycling rates, improving waste collection systems, and reducing single-use packaging are crucial steps to minimize the environmental impact of metal can waste and promote a more sustainable circular economy.", 
                size=20, color="black",text_align=ft.TextAlign.JUSTIFY,),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=100, vertical=20),
        bgcolor = "#FFFFFF"
    )

    clothes_title = ft.Container(
        width=float("inf"),
        content=ft.Column(
            [
                ft.Text("Textile Waste", size=50, weight="bold", color="#145C39"),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=0, vertical=20),
        bgcolor="#EBF8A9",  
    )

    clothes_text = ft.Container(
        width=float("inf"),
        content=ft.Column([
            ft.Text("Every year, millions of tons of used clothing are discarded worldwide as fast-fashion trends accelerate consumption and shorten the lifespan of garments. Although many textiles could be reused or recycled, only a small fraction—roughly 12%—is actually recovered, while the majority is dumped in landfills or incinerated, releasing harmful chemicals and microfibers into the environment. Most modern clothing contains synthetic fibers like polyester, which can take 20 to 200 years or more to decompose, while other synthetics such as nylon may take 30 to 40 years, and more elastic fibers like spandex can persist even longer. Natural fibers decompose much faster: for example, cotton can break down in as little as a few months (1 – 5 months), wool takes about 1–5 years, and linen can decompose in just a few weeks to months.", 
                size=20, color="black",text_align=ft.TextAlign.JUSTIFY,),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=100, vertical=20),
        bgcolor = "#FFFFFF"
    )

    main_container = ft.Column(
        [
            top_nav,
            ft.Container(
                content=ft.Column(
                    [
                        plastic_title,
                        ft.Image(
                            src="src/database/image/waste_information/plastic.png",
                            fit=ft.ImageFit.COVER,
                        ),
                        plastic_text,
                        metal_title,
                        ft.Image(
                            src="src/database/image/waste_information/metal.png",
                            fit=ft.ImageFit.COVER,
                        ),
                        metal_text,
                        clothes_title,
                        ft.Image(
                            src="src/database/image/waste_information/clothes.jpg",
                            fit=ft.ImageFit.COVER,
                            width="inf",
                        ),
                        clothes_text,
                    ],
                    expand=True,
                    spacing=0,
                ),
                padding=ft.padding.symmetric(horizontal=0, vertical=0),
                expand=True,
            ),
        ],
        expand=True,
        spacing=0,
    )

    page.add(main_container)