import flet as ft
import pages


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed='blue', font_family='Verdana')
    #page.window_center()
    #page.window_full_screen = True

    def f(route: ft.RouteChangeEvent):
        page.views.clear()
        tr = ft.TemplateRoute(route.route)
        if tr.match(f'/{pages.MAIN}'):
            route.page.views.append(pages.main(page, 0))
        elif tr.match(f'/{pages.KEY_TOP}'):
            route.page.views.append(pages.key_top(page, 0))
        route.page.update()

    def p(view: ft.View):
        page.views.pop()
        if len(page.view):
            top_view = page.views[-1]
            page.go(top_view.route)

    def u(e: ft.ControlEvent):
        e.route = e.page.route
        f(e)
    page.on_route_change = f
    page.on_view_pop = p
    page.on_resize = u
    page.go(f'/{pages.KEY_TOP}')

    


ft.app(target=main)