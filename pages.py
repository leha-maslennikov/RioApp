import flet as ft
from Text import *
from Controls import *
from mythicdatabase import MDB


def main(page: ft.Page, offset: int) -> ft.View:
   return ft.View(
      route = f'/{MAIN}/{offset}',
      appbar=get_menu_bar(page),
      controls = get_keys_table(page, offset, [Key.DATE], [True]),
      bgcolor = ft.colors.PRIMARY
   )


def key_top(page: ft.Page, offset: int) -> ft.View:
   return ft.View(
      route = f'/{KEY_TOP}/{offset}',
      appbar=get_menu_bar(page),
      controls = get_keys_table(page, offset, [Key.ID], [False]),
      bgcolor = ft.colors.PRIMARY
   )

def character_page(page: ft.Page, guid: int):
   return ft.View(
      route = f'/{CHARACTER_PAGE}/{guid}',
      appbar=get_menu_bar(page),
      controls = [],
      bgcolor = ft.colors.PRIMARY
   )


if __name__ == '__main__':
   #print('\n'.join(map(str, MDB.get_keys(10, limit=10).get())))
   pass