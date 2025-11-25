import flet as ft
# from views.order.general_details import GeneralDetailsView
# from views.order.address import AddressView
# from views.order.navigation import NavigationView
# from views.order.date_and_time import DateAndTimeView

import sys
from views.signup_window import main as signup_main
from views.login_window import main as login_main
from services.database import DatabaseService
from views.forget_password_window import main as forget_password_main
from views.forget_password_verify_window import main as forget_password_verify_main
from views.reset_password_window import main as reset_password_main
from views.point_mart_window import main as point_mart_main
from views.product_detail_window import main as product_detail_main
from views.order_window import main as order_main
from views.home_window import main as home_main
from models.state import AppState

# # Initialize OrderState
# class OrderState:
#     def __init__(self):
#         self.waste_types = []
#         self.weight = ""
#         self.condition = "Good"
#         self.attachment = None
#         self.district = ""
#         self.address = ""
#         self.notify_on_arrival = False
#         self.selected_date = None
#         self.selected_time = None
#         self.selected_collector = None
#         self.completed_steps = set()

# def main_order(page: ft.Page):
#     page.title = "GrowBak"
#     page.window_width = 1440
#     page.window_height = 1024
#     page.padding = 0
    
#     order_state = OrderState()
#     content_area = ft.Container(expand=True)
    
#     def navigate_to(route):
#         content_area.content = None
        
#         if route == "/order/general-details":
#             content_area.content = GeneralDetailsView(page, order_state)
#         elif route == "/order/address":
#             content_area.content = AddressView(page, order_state)
#         elif route == "/order/date-and-time":
#             content_area.content = DateAndTimeView(page, order_state)
#         elif route == "/order/navigation":
#             content_area.content = NavigationView(page, order_state)
        
#         page.update()
    
#     def route_change(route):
#         navigate_to(page.route)
    
#     page.on_route_change = route_change
#     page.add(content_area)
#     page.go("/order/general-details")


def app_main(page: ft.Page):
    try:
        db = DatabaseService()
        db.create_tables()
        page.signup_main = signup_main
        page.login_main = login_main
        page.forget_password_main = forget_password_main
        page.forget_password_verify_main = forget_password_verify_main
        page.reset_password_main = reset_password_main
        page.point_mart_main = point_mart_main
        page.product_detail_main = product_detail_main
        page.order_main = order_main
        page.home_main = home_main
        if AppState.is_logged_in == True:
            home_main(page)
        else:
            login_main(page)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ft.app(target=app_main)
