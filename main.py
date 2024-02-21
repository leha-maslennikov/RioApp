import flet as ft
from db import dung, get_keys

def user_page(page: ft.Page):
    panel = []
    for a, b in dung.items():
        panel.append(
            ft.ExpansionPanel(
                header=ft.Row([ft.Text(b, color=ft.colors.ON_SECONDARY)]),
                expanded=False,
                bgcolor=ft.colors.SECONDARY
            )
        )

    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.WHITE,
        expanded_header_padding=10,
        divider_color=ft.colors.WHITE,
        controls=panel
    )
    page.add(panel)


def keys_table(offset = 0):
    table = []
    for key in get_keys(offset):
        


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed='blue')
    page.bgcolor = ft.colors.PRIMARY

    


ft.app(target=main)