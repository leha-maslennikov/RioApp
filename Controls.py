import flet as ft
from Text import *
from mythicdatabase import Key, MDB, Character, KeyCharacter, LastSeason
from threading import Thread, Lock
from wow import Specialization
from time import time, sleep

lock = Lock()

def go_char_page(e: ft.ControlEvent):
    e.page.go(f'/{CHARACTER_PAGE}/{e.control.data}')
    
def get_search_bar(page: ft.Page):
    def listen(page: ft.Page, e: ft.SearchBar):
        v = page.views[-1]
        name = e.value
        while (len(page.views) != 0) and (v == page.views[-1]):
            if name != e.value and len(e.value) >= 3:
                name = e.value
                chars = []
                if len(name) != 0:
                    chars = MDB.get_character_by_name(name).get()
                e.controls[0].controls = [ft.ListTile(title=ft.Text(i.name), data = i.guid, on_click = go_char_page) for i in chars]
                e.controls[0].update()
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
                data=MAIN,
                on_click=go_to_page
            ),
            ft.MenuItemButton(
                content = ft.Text(KEY_TOP, color=ft.colors.ON_PRIMARY_CONTAINER, weight=ft.FontWeight.BOLD),
                data=KEY_TOP,
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

def get_char_block(char: KeyCharacter):
    spec = Specialization(char.spec_id, char.name)
    return spec.get_text()

cahce = {}
def get_affix_img(src: str) -> ft.Image:
    if src in cahce:
        return cahce[src]
    cahce[src] = ft.Image(src=src, width=25)
    return cahce[src]

def get_key_row(key: Key):
    row = ft.Row()
    size = [65, 70, 140, 70, 90, 140]
    char = key.characters
    affixes = ft.Row(
        [get_affix_img(i) for i in key.affixes.split()],
        spacing=0
    )
    key = [key.id, key.score, key.inst, f'{key.challenge_level}{key.timer_level*"+"}', key.record_time]
    for i in range(len(key)):
        row.controls.append(
            ft.Container(
                content=ft.Text(key[i], color=ft.colors.ON_SECONDARY, size=16),
                width=size[i],
                alignment=ft.alignment.center_left,
                padding=10
            )
        )
    row.controls.append(
            ft.Container(
                content=affixes,
                width=size[4],
                alignment=ft.alignment.center_left,
                padding=0
            )
        )
    for i in char.get():
        row.controls.append(
            ft.Container(
                content=get_char_block(i),
                #alignment=ft.alignment.ce,
                padding=10
            )
        )
    return ft.ExpansionPanel(
                header=row,
                bgcolor=ft.colors.SECONDARY
            )

def get_table_headers():
    row = ft.Row()
    size = [65, 70, 140, 90, 70, 140]
    headers = 'Rank Score Dungeon	Level	Time	Affixes'.split()
    for i in range(len(headers)):
        row.controls.append(
            ft.Container(
                content=ft.Text(headers[i], color=ft.colors.ON_PRIMARY_CONTAINER, size=16),
                width=size[i],
                alignment=ft.alignment.center_left,
                padding=10
            )
        )

    return row

keys_cahce = {}
def get_keys_table(offset: int, column: list[str], reverse: list[bool]):
    def click(e: ft.ControlEvent):
        from pages import progress, alert
        progress(e.page)
        e.page.update()
        args = ([Key.DATE], [True]) if MAIN in e.page.route else ([Key.ID], [False])
        tmp = get_keys_table(e.control.data, *args)
        alert.open = False
        e.page.update()
        e.page.views[-1].controls = tmp
        sleep(0.1)
        e.page.views[-1].update()
    size = MDB.size()
    if offset in keys_cahce:
        g = keys_cahce[offset]
        if len(keys_cahce) > 30:
            keys_cahce.clear()
        if offset+10 not in keys_cahce:
            keys_cahce[offset+10] = MDB.get_keys(offset=offset+10, limit=10, column=column, reverse=reverse)
        if offset-10 not in keys_cahce:
            keys_cahce[offset-10] = MDB.get_keys(offset=offset-10, limit=10, column=column, reverse=reverse)
    else:
        g = MDB.get_keys(offset=offset, limit=10, column=column, reverse=reverse)
        keys_cahce[offset] = g
    headers = get_table_headers()
    exp1 = (offset == 0)
    exp2 = (size - offset - 10 <= 0)
    btns = (
        (ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT, exp1, 0),
        (ft.icons.CHEVRON_LEFT, exp1, offset - 10),
        (ft.icons.CHEVRON_RIGHT, exp2, offset + 10),
        (ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT, exp2, size-10)
    )
    btns = [ft.IconButton(icon = icon, bgcolor=ft.colors.PRIMARY_CONTAINER, icon_color=ft.colors.ON_PRIMARY_CONTAINER, disabled=dis, data=offset, on_click=click) for icon, dis, offset in btns]
    
    keys = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.ON_SECONDARY,
        divider_color=ft.colors.PRIMARY_CONTAINER,
        controls=[]
    )
    g = g.get()
    for i in g:
        keys.controls.append(get_key_row(key=i))
    if offset+10 not in keys_cahce:
        keys_cahce[offset+10] = MDB.get_keys(offset=offset+10, limit=10, column=column, reverse=reverse)
    if offset-10 not in keys_cahce:
        keys_cahce[offset-10] = MDB.get_keys(offset=offset-10, limit=10, column=column, reverse=reverse)

    controls = ft.Container(
        ft.Column(
            [
                headers,
                ft.Column(
                    [keys],
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
            ]
        ),
        expand=True
    )

    controls = [
        ft.Row(btns),
        ft.Container(
            controls,
            bgcolor=ft.colors.PRIMARY_CONTAINER,
            border_radius=10,
            expand=True
        )
    ]
    return controls

def get_char_score_row(char: Character) -> ft.Container:
    score_row = ft.Row(
        [],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )
    for score, name in [(char.score, BEST), (char.tank_score, TANK[:-1]), (char.heal_score, HEAL[:-1]), (char.dps_score, DD)]:
        if score > 0:
            score_row.controls.append(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(str(score), size = 17, 
                                    #color=ft.colors.ON_TERTIARY
                                    ),
                            ft.Text(name, size = 15, 
                                    #color=ft.colors.ON_TERTIARY
                                    )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    #bgcolor=ft.colors.TERTIARY,
                    border_radius=10,
                    padding=10
                )
            )
    return ft.Container(
        score_row,
        bgcolor=ft.colors.PRIMARY_CONTAINER,
        padding=10,
        border_radius=10
    )

def get_char_header(char: Character) -> ft.Container:
    title = ft.Row(
        [
            ft.Icon(ft.icons.ACCOUNT_CIRCLE, scale=4),
            ft.Column(
                [
                    ft.Text(char.name, size=17, color=ft.colors.ON_PRIMARY_CONTAINER),
                    ft.Text('Guild')
                ]
            )

        ]
    )

    tmp = get_char_score_row(char)
    tmp.content.controls = [title] + tmp.content.controls

    return tmp

def get_char_keys_table(c_keys: list[Key]):
    headers = get_table_headers()
    keys = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.ON_SECONDARY,
        divider_color=ft.colors.PRIMARY_CONTAINER,
        controls=[]
    )
    for i in c_keys:
        keys.controls.append(get_key_row(key=i.get()))

    controls = ft.Container(
        ft.Column(
            [
                headers,
                ft.Column(
                    [keys],
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS
                )
            ]
        ),
        expand=True
    )
    return ft.Container(
            controls,
            bgcolor=ft.colors.PRIMARY_CONTAINER,
            border_radius=10,
            expand=True
        )