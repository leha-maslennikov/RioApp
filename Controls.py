import flet as ft
from Text import *
from mythicdatabase import Key


def get_search_bar(page: ft.Page):
    return ft.Container(
        content = ft.SearchBar(
            view_leading=ft.Icon(ft.icons.SEARCH),
            bar_leading= ft.Icon(ft.icons.SEARCH),
            divider_color=ft.colors.AMBER,
            bar_hint_text=FIND,
            view_hint_text=FIND,
            width=page.width*0.25,
            height=page.width*0.03,
            scale=0.9
        ),
        alignment=ft.alignment.center_right,
        expand=True,
        padding=5,
    )

def get_menu_bar(page: ft.Page):
    def main(e: ft.ControlEvent):
        e.page.go(f'/{e.control.data}')

    return ft.Container(
        content = ft.Row(
            controls = [
                ft.MenuItemButton(
                    content = ft.Text(MAIN, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                    data=MAIN,
                    on_click=main
                ),
                ft.MenuItemButton(
                    content = ft.Text(KEY_TOP, color=ft.colors.ON_PRIMARY_CONTAINER),
                    data=KEY_TOP,
                    on_click=main
                ),
                ft.SubmenuButton(
                    content = ft.Text(CHARACTER_TOP, color=ft.colors.ON_PRIMARY_CONTAINER),
                    controls = [
                        ft.MenuItemButton(
                            leading=ft.Icon(ft.icons.CIRCLE_SHARP),
                            content = ft.Text(TANK, color=ft.colors.ON_PRIMARY_CONTAINER),
                            data=TANK,
                            on_click=main
                        ),
                        ft.MenuItemButton(
                            leading=ft.Icon(ft.icons.CIRCLE_SHARP),
                            content = ft.Text(HEAL, color=ft.colors.ON_PRIMARY_CONTAINER),
                            data=HEAL,
                            on_click=main
                        ),
                        ft.MenuItemButton(
                            leading=ft.Icon(ft.icons.CIRCLE_SHARP),
                            content = ft.Text(DD, color=ft.colors.ON_PRIMARY_CONTAINER),
                            data=DD,
                            on_click=main
                        )
                    ]
                ),
                get_search_bar(page)
            ],
            expand = True
        ),
        bgcolor = ft.colors.PRIMARY_CONTAINER,
        border_radius = 10
    )

def get_key_row(page: ft.Page, key: Key):
    return ft.Container(
        ft.Text(f"{'+'*key.timer_level}{key.challenge_level} {key.inst} {key.record_time}", color=ft.colors.ON_SECONDARY, size=16),
        bgcolor = ft.colors.SECONDARY,
        border_radius=1,
        width = page.width*0.5,
        padding=5
    )