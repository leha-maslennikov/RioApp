import flet as ft
from Text import *
from Controls import *


def main(page: ft.Page) -> ft.View:
   return ft.View(
      route = f'/{MAIN}',
      appbar = get_menu_bar(page),
      controls = get_keys_table(0, [Key.DATE], [True]),
      bgcolor = ft.colors.PRIMARY
   )


def key_top(page: ft.Page) -> ft.View:
   return ft.View(
      route = f'/{KEY_TOP}',
      appbar = get_menu_bar(page),
      controls = get_keys_table(0, [Key.ID], [False]),
      bgcolor = ft.colors.PRIMARY
   )

def character_page(page: ft.Page, guid: int):
   return ft.View(
      route = f'/{CHARACTER_PAGE}/{guid}',
      appbar=get_menu_bar(page),
      controls = [],
      bgcolor = ft.colors.PRIMARY
   )

alert = ft.AlertDialog(open=True, title=ft.Row([ft.Text(PROGRES_RING, color=ft.colors.ON_TERTIARY_CONTAINER, size=16)], alignment=ft.MainAxisAlignment.CENTER), content = ft.Row([ft.ProgressRing(color=ft.colors.ON_TERTIARY_CONTAINER)], alignment=ft.MainAxisAlignment.CENTER), bgcolor=ft.colors.TERTIARY_CONTAINER)
def progress(page: ft.Page):
   alert.open = True
   page.views[-1].controls.append(alert)


if __name__ == '__main__':
   #print('\n'.join(map(str, MDB.get_keys(10, limit=10).get())))
   pass