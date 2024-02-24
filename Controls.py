import flet as ft
from Text import *
from mythicdatabase import Key, MDB


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
                data=KEY_TOP,
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

def get_keys_table(page: ft.Page, offset: int, column: list[str], reverse: list[bool]):
    def click(e: ft.ControlEvent):
        e.page.views[-1].controls = get_keys_table(e.page, e.control.data, column=column, reverse=reverse)
        e.page.update()

    size = MDB.size()
    btns = [
        (ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT, True if offset == 0 else False, 0),
        (ft.icons.CHEVRON_LEFT, True if offset == 0 else False, max(0, offset - 10)),
        (ft.icons.CHEVRON_RIGHT, False if size.get() - offset - 10 > 0 else True, offset+10),
        (ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT, False if size.get() - offset - 10 > 0 else True, size.get()-10)
    ]
    btns = [ft.IconButton(icon = icon, bgcolor=ft.colors.PRIMARY_CONTAINER, icon_color=ft.colors.ON_PRIMARY_CONTAINER, disabled=dis, data=offset, on_click=click) for icon, dis, offset in btns]
    keys = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.ON_SECONDARY_CONTAINER,
        divider_color=ft.colors.SECONDARY,
        controls=[]
    )
    for i in MDB.get_keys(offset=offset, limit=10, column=column, reverse=reverse).get():
        keys.controls.append(get_key_row(page, i))
    controls = [
        ft.Row(btns),
        ft.Container(
            ft.Column(
                [
                    ft.Row([get_key_block(ft.Text(i, color=ft.colors.ON_SECONDARY, size=16)) for i in 'Rank	Dungeon	Level	Time	Affixes	Tank	Healer	DPS	Score'.split()]),
                    ft.Column([keys], height=page.height-200,scroll=ft.ScrollMode.ADAPTIVE)
                ]
            ),
            bgcolor=ft.colors.SECONDARY,
            border_radius=10
        )
    ]

    return controls