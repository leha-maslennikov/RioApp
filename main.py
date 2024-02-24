import flet as ft
import pages

def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed='blue', font_family='Verdana')
    #page.window_center()
    #page.window_full_screen = True

    def f(route: ft.RouteChangeEvent):
        tr = ft.TemplateRoute(route.route)
        if tr.match(f'/{pages.MAIN}/:offset'):
            page.views.clear()
            route.page.views.append(pages.main(page, int(tr.offset)))
        elif tr.match(f'/{pages.KEY_TOP}/:offset'):
            page.views.clear()
            route.page.views.append(pages.key_top(page, int(tr.offset)))
        elif tr.match(f'/{pages.CHARACTER_PAGE}/:guid'):
            route.page.views.append(pages.character_page(page, int(tr.guid)))

    def p(view: ft.ViewPopEvent):
        page = view.page
        page.views.pop()
        if len(page.views) != 0:
            page.clean()
            page.go(page.views[-1].route)

    def u(e: ft.ControlEvent):
        e.page.clean()
        e.page.go(e.page.route)

    page.on_route_change = f
    page.on_resize = u
    page.on_view_pop = p
    page.go(f'/{pages.KEY_TOP}/0')


    


ft.app(target=main)