import flet as ft

from views.components.navbar import create_navbar
from views.order.general_details import GeneralDetailsView
from views.order.address import AddressView
from views.order.navigation import NavigationView
from views.order.date_and_time import DateAndTimeView

class OrderState:
    def __init__(self):
        self.waste_types = []
        self.weight = ""
        self.weight_1 = ""
        self.weight_2 = ""
        self.weight_3 = ""
        self.condition = "Good"
        self.attachment = None
        self.district = ""
        self.address = ""
        self.notify_on_arrival = False
        self.selected_date = None
        self.selected_time = None
        self.selected_collector = None
        self.completed_steps = set()
        self.point_gained = 0


def main(page: ft.Page):
    page.title = "GrowBak - Order"
    page.window_width = 1440
    page.window_height = 1024
    page.padding = 0
    
    order_state = OrderState()
    content_area = ft.Container(expand=True)
    
    def navigate_to(route):
        content_area.content = None
        
        if route == "/order/general-details":
            content_area.content = GeneralDetailsView(page, order_state)
        elif route == "/order/address":
            content_area.content = AddressView(page, order_state)
        elif route == "/order/date-and-time":
            content_area.content = DateAndTimeView(page, order_state)
        elif route == "/order/navigation":
            content_area.content = NavigationView(page, order_state)
        
        page.update()

    def route_change(route):
        navigate_to(page.route)
    
    page.on_route_change = route_change
    top_nav = create_navbar(page, "order")
    navigate_to("/order/general-details")

    main_container = ft.Column(
        controls = [
            top_nav,
            content_area,
        ],
        expand=True,
    )

    page.add(main_container)