import flet as ft
import re
from views.components.navbar import create_navbar
from models.state import AppState

fonts = {
    "Poppins": "fonts/poppins/Poppins-Regular.ttf",
    "PoppinsBold": "fonts/poppins/Poppins-Bold.ttf",
    "PoppinsSBold": "fonts/poppins/Poppins-SemiBold.ttf",
}

def main(page: ft.Page):
    AppState.load_state()
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
    top_nav = create_navbar(page, "home")

    about_us_text = ft.Container(
        width = 600,
        content=ft.Column(
            [
                ft.Text("Welcome to GrowBak!", size=70, weight="bold", color="white"),
                ft.Divider(height=30, color="transparent"),
                ft.Text("Growbak is a smart waste management platform that connects users, waste collectors, and recycling centers through one integrated system.\nYou can sort your recyclable waste, schedule pickup appointments, and earn reward points for every successful collection.", 
                        text_align=ft.TextAlign.JUSTIFY, size=20, color="white", width=800,),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=60, vertical=50),
        bgcolor="#145C39",        
    )


    # ini nanti dimasukin ke page.add
    # ini adalah bagian dari maincontainer
    about_us = ft.Container(
        height=580,
        content=ft.Stack(
            [
                # Background image
                ft.Image(
                    src="src/database/image/home/waste.jpeg",
                    opacity=0.3,        # semi-transparent
                    # width=None,
                    # height=400,
                    fit=ft.ImageFit.COVER,
                    expand=True,
                ),
                ft.Container(
                    height=580, 
                    content=ft.Row(
                        [
                            ft.VerticalDivider(width=650, color="transparent"),
                            about_us_text
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            ],
        ),
        padding=ft.padding.symmetric(horizontal=0, vertical=0),
        bgcolor="#1e8c45",        # warna hijau
    )

    content_us_left = ft.Container(
        width=640,
        content=ft.Column(
            [
                ft.Text("Why Should We Recycle Waste?", size=35, weight="bold", color="black"),
                ft.Divider(height=30, color="transparent"),
                ft.Container(
                    content=ft.Column([
                        ft.Text("♻️ 1. Protecting the Environment", 
                            size=20, font_family="PoppinsSBold", color="black", width=800,),
                        ft.Row([
                            ft.VerticalDivider(width=30, color="transparent"),
                            ft.Text("Recycling helps reduce pollution caused by waste. When we recycle materials like plastic, paper, and metal, we lessen the need for new raw materials — meaning fewer trees cut down, less mining, and lower carbon emissions. This keeps our air, water, and soil cleaner and healthier.", 
                                text_align=ft.TextAlign.JUSTIFY,size=15, color="black", width=600,),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Text("🌍 2. Saving Natural Resources and Energy", 
                            size=20, font_family="PoppinsSBold", color="black", width=800,),
                        ft.Row([
                            ft.VerticalDivider(width=30, color="transparent"),
                            ft.Text("Producing new materials from scratch consumes a lot of natural resources and energy. Recycling allows us to reuse existing materials, significantly cutting down energy use and preserving limited resources such as oil, minerals, and forests for future generations.", 
                                text_align=ft.TextAlign.JUSTIFY, size=15, color="black", width=600,),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Text("💚 3. Building a Sustainable Economy", 
                            size=20, font_family="PoppinsSBold", color="black", width=800,),
                        ft.Row([
                            ft.VerticalDivider(width=30, color="transparent"),
                            ft.Text("Recycling supports the growth of a circular economy, where waste becomes a valuable resource instead of a burden. It creates jobs in collection, sorting, and processing industries — and through platforms like Growbak, it turns responsible behavior into real rewards for everyone involved.", 
                                text_align=ft.TextAlign.JUSTIFY, size=15, color="black", width=600,),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        )
                        ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    )
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=20),
        bgcolor="#ffffff",        
    )

    content_us =  ft.Container(
        width=1360,
        content=ft.Row(
            [
                ft.VerticalDivider(width=100, color="transparent"),
                content_us_left,
                ft.VerticalDivider(width=40, color="transparent"),
                ft.Image(
                    src="src/database/image/home/wc.jpeg",
                    width=500,
                    height=350,
                    fit=ft.ImageFit.COVER,
                ),
            ],
            expand=True,
            spacing=50,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
        bgcolor="#FFFFFF",       
    )

    def go_to_order(e):
        page.clean()
        if AppState.is_logged_in:
            page.order_main(page)
        else:
            page.login_main(page)

    def go_to_point_mart(e):
        page.clean()
        if AppState.is_logged_in:
            page.point_mart_main(page)
        else:
            page.login_main(page)

    # Buat canvas untuk gradient
    gradient_canvas = ft.Image(
        src="src/database/image/home/background_service.png",
        fit=ft.ImageFit.COVER,
        expand=True
    )


    left_services = ft.Container(
        content=ft.Column(
            [
                ft.IconButton(
                    on_click=lambda e: go_to_order(page),
                    content=ft.Stack(
                        [
                            # BACKGROUND CIRCLE
                            ft.Container(
                                width=200,
                                height=200,
                                border_radius=9999,
                                bgcolor="#78d23d",     # warna lingkaran
                                alignment=ft.alignment.center,
                            ),

                            # IMAGE ICON (tidak terpotong)
                            ft.Image(
                                src="src/database/image/home/order.png",
                                width=140,       # ukuran bebas
                                height=140,
                                fit=ft.ImageFit.CONTAIN,  # tidak pernah terpotong
                            ),
                        ],
                        width=200,
                        height=200,
                        alignment=ft.alignment.center,
                    ),
                ),
                ft.Text("Waste Pickup", 
                    size=20, font_family="PoppinsSBold", color="black", width=250, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    # ft.VerticalDivider(width=30, color="transparent"),
                    ft.Text("Users can schedule waste collection appointments directly through the app, connecting with nearby waste collectors.", 
                        size=15, color="black", width=300, text_align=ft.TextAlign.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )

            ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    right_services = ft.Container(
        content=ft.Column(
            [
                ft.IconButton(
                    on_click=lambda e: go_to_point_mart(page),
                    content=ft.Stack(
                        [
                            # BACKGROUND CIRCLE
                            ft.Container(
                                width=200,
                                height=200,
                                border_radius=9999,
                                bgcolor="#78d23d",     # warna lingkaran
                                alignment=ft.alignment.center,
                            ),

                            # IMAGE ICON (tidak terpotong)
                            ft.Image(
                                src="src/database/image/home/mart.png",
                                width=140,       # ukuran bebas
                                height=140,
                                fit=ft.ImageFit.CONTAIN,  # tidak pernah terpotong
                            ),
                        ],
                        width=200,
                        height=200,
                        alignment=ft.alignment.center,
                    ),
                ),
                ft.Text("Point Mart", 
                    size=20, font_family="PoppinsSBold", color="black", width=250, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    # ft.VerticalDivider(width=30, color="transparent"),
                    ft.Text("We really appreciate users. Every successful recycling activity earns users points, which can be exchanged for rewards or gifts.", 
                        size=15, color="black", width=300, text_align=ft.TextAlign.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )

            ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    services_cont = ft.Container(
        content=ft.Column(
            [
                ft.Divider(height=70, color="transparent"),
                ft.Text("Our Services", size=70, weight="bold", color="black"),
                ft.Divider(height=80, color="transparent"),
                ft.Row([
                    left_services,
                    ft.VerticalDivider(width=300, color="transparent"),
                    right_services
                    ],        
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(height=80, color="transparent"),
                ft.Text("“If you truly love nature, you will find beauty everywhere.”", size=30, color="black"),
            ],
            expand=True,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
        bgcolor="transparent"
    )


    # Stack untuk menumpuk gradient canvas dan content container
    services = ft.Stack(
        [
            gradient_canvas,   
            services_cont      
        ]
    )


    main_container = ft.Column(
        [
            top_nav,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Divider(height=30, color="transparent"),
                        about_us,
                        ft.Divider(height=60, color="transparent"),
                        content_us,
                        ft.Divider(height=100, color="transparent"),
                        services
                    ],
                    expand=True,
                ),
                padding=ft.padding.symmetric(horizontal=0, vertical=0),
                expand=True,
            ),
        ],
        expand=True,
    )

    page.add(main_container)