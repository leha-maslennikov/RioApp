import flet as ft
import pages

def user_page(page: ft.Page):
    panel = []
    

    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.WHITE,
        expanded_header_padding=10,
        divider_color=ft.colors.WHITE,
        controls=panel
    )
    page.add(panel)
    page.theme_mode = ft.ThemeMode.LIGHT

    


def keys_table(offset = 0):
    table = []
        


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed='green')
    page.window_width = 1500
    page.window_height = 1000
    page.window_center()
    page.window_full_screen = True

    def f(route: ft.RouteChangeEvent):
        page.views.clear()
        if route.route == f'/{pages.MAIN}':
            route.page.views.append(pages.main(page))
        elif route.route == f'/{pages.KEY_TOP}':
            route.page.views.append(pages.key_top(page))
        route.page.update()

    def p(view: ft.View):
        page.views.pop()
        if len(page.view):
            top_view = page.views[-1]
            page.go(top_view.route)
    page.on_route_change = f
    page.on_view_pop = p
    page.go(f'/{pages.MAIN}')

    


ft.app(target=main)