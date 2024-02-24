import flet as ft
from Text import *
from mythicdatabase import Key, MDB, Character
from threading import Thread, Lock

lock = Lock()

def go_char_page(e: ft.ControlEvent):
    e.page.go(f'/{CHARACTER_PAGE}/{e.control.data}')
    

def get_search_bar(page: ft.Page):
    def listen(page: ft.Page, e: ft.SearchBar):
        v = page.views[-1]
        name = e.value
        while (len(page.views) != 0) and (v == page.views[-1]):
            if name != e.value:
                name = e.value
                chars = []
                if len(name) != 0:
                    chars = MDB.get_character_by_name(name[0]).get()
                e.controls[0].controls = [ft.ListTile(title=ft.Text(i.name), data = i.guid, on_click = go_char_page) for i in chars]
                e.controls[0].update()
            else:
                from time import sleep
                sleep(0.1)
        lock.release()

    def start_listen(e: ft.ControlEvent):
        if not lock.locked():
            lock.acquire()
            Thread(target=listen, args=(e.page, e.control), daemon=True).start()
    
    return ft.Container(
        ft.SearchBar(
            view_leading = ft.Icon(ft.icons.SEARCH),
            bar_leading = ft.Icon(ft.icons.SEARCH),
            divider_color=ft.colors.ON_PRIMARY_CONTAINER,
            bar_hint_text=FIND,
            view_hint_text=FIND,
            width=page.width*0.25,
            height=page.width*0.03,
            on_change=lambda e: e.control.open_view(),
            on_tap=start_listen,
            controls=[ft.Column()]
        ),
        expand=True,
        padding=5,
        alignment=ft.alignment.center_right
    )

def get_menu_bar(page: ft.Page):
    def go_to_page(e: ft.ControlEvent):
        e.page.go(f'/{e.control.data}')
    bar = ft.Row(
        [
            ft.MenuItemButton(
                content = ft.Text(MAIN, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                data=f'{MAIN}/0',
                on_click=go_to_page
            ),
            ft.MenuItemButton(
                content = ft.Text(KEY_TOP, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                data=f'{KEY_TOP}/0',
                on_click=go_to_page
            ),
            ft.SubmenuButton(
                content = ft.Text(CHARACTER_TOP, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                controls = [
                    ft.MenuItemButton(
                        leading=ft.Image(src='/img/all.png', width=25),
                        content = ft.Text(ALL, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=ALL,
                        on_click=go_to_page,
                        expand=True,
                    ),
                    ft.MenuItemButton(
                        leading = ft.Image(src='/img/tank.png', width=25),
                        content = ft.Text(TANK, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=TANK,
                        on_click=go_to_page
                    ),
                    ft.MenuItemButton(
                        leading=ft.Image(src='/img/healer.png', width=25),
                        content = ft.Text(HEAL, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=HEAL,
                        on_click=go_to_page
                    ),
                    ft.MenuItemButton(
                        leading=ft.Image(src='/img/dps.png', width=25),
                        content = ft.Text(DD, color=ft.colors.ON_PRIMARY_CONTAINER),
                        data=DD,
                        on_click=go_to_page
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
                        on_click=go_to_page,
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
        page.go(f"/{''.join(e.page.views[-1].route.split('/')[:-1])}/{e.control.data}")

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