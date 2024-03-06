import flet as ft
import pages
import Controls


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed='blue', font_family='Verdana')
    #page.window_center()
    #page.window_full_screen = True

    def f(route: ft.RouteChangeEvent):
        tr = ft.TemplateRoute(route.route)
        page.clean()
        if tr.match(f'/{pages.MAIN}'):
            pages.progress(page)
            page.update()
            Controls.keys_cahce.clear()
            tmp = pages.main(page)
            pages.alert.open = False
            page.update()
            page.views.clear()
            route.page.views.append(tmp)
        elif tr.match(f'/{pages.KEY_TOP}'):
            pages.progress(page)
            page.update()
            Controls.keys_cahce.clear()
            tmp = pages.key_top(page)
            pages.alert.open = False
            page.update()
            page.views.clear()
            route.page.views.append(tmp)
        elif tr.match(f'/{pages.CHARACTER_PAGE}/:guid'):
            route.page.views.append(pages.character_page(page, int(tr.guid)))


    def p(view: ft.ViewPopEvent):
        page = view.page
        page.views.pop()
        if len(page.views) != 0:
            page.clean()
            page.update()

    def u(e: ft.ControlEvent):
        page.clean()
        e.route = page.route
        f(e)
        page.update()


    page.on_route_change = f
    #page.on_resize = u
    page.on_view_pop = p
    page.go(f'/{pages.KEY_TOP}')


    


ft.app(target=main)