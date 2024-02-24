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
    bar = ft.Row(
        [
            ft.MenuItemButton(
                content = ft.Text(MAIN, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                data=MAIN,
                on_click=main
            ),
            ft.MenuItemButton(
                content = ft.Text(KEY_TOP, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                data=f'{KEY_TOP}/:0',
                on_click=main
            ),
            ft.SubmenuButton(
                content = ft.Text(CHARACTER_TOP, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                controls = [
                    ft.MenuItemButton(
                        leading=ft.Image(src='/img/all.png', width=25),
                        content = ft.Text(ALL, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=ALL,
                        on_click=main,
                        expand=True,
                    ),
                    ft.MenuItemButton(
                        leading = ft.Image(src='/img/tank.png', width=25),
                        content = ft.Text(TANK, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=TANK,
                        on_click=main
                    ),
                    ft.MenuItemButton(
                        leading=ft.Image(src='/img/healer.png', width=25),
                        content = ft.Text(HEAL, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=HEAL,
                        on_click=main
                    ),
                    ft.MenuItemButton(
                        leading=ft.Image(src='/img/dps.png', width=25),
                        content = ft.Text(DD, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=DD,
                        on_click=main
                    )
                ]
            ),
            ft.SubmenuButton(
                content = ft.Text(CLASS_TOP, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                controls = [
                    ft.MenuItemButton(
                        leading=ft.Image(src='/img/all.png', width=25),
                        content = ft.Text(ALL, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=ALL,
                        on_click=main,
                        expand=True
                    )
                ]
            ),
            get_search_bar(page)
        ],
        expand = True
    )

    return ft.AppBar(title=bar, bgcolor=ft.colors.PRIMARY_CONTAINER)

def get_key_block(content: ft.Control):
    return ft.Container(
        content=content,
        width=150,
        alignment=ft.alignment.center_left,
        padding=10
    )

def get_key_row(page: ft.Page, key: Key):
    row = ft.Row()
    for i in key.id, key.inst, f'{key.challenge_level}{key.timer_level*"+"}', key.record_time, key.affixes:
        row.controls.append(
            get_key_block(
                ft.Text(
                    i, color=ft.colors.ON_SECONDARY_CONTAINER, size=16
                )
            )
        )
    return ft.ExpansionPanel(
                header=row,
                bgcolor=ft.colors.SECONDARY_CONTAINER
            )