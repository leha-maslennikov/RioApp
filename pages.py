import flet as ft
from Text import *
from Controls import *
from mythicdatabase import MDB

def key_top(page: ft.Page, offset: int) -> ft.View:
   return ft.View(
      route = f'/{KEY_TOP}',
      appbar=get_menu_bar(page),
      controls = get_keys_table(page, offset, [Key.ID], [False]),
      bgcolor = ft.colors.PRIMARY
   )


def main(page: ft.Page, offset: int) -> ft.View:
   return ft.View(
      route = f'/{MAIN}',
      appbar=get_menu_bar(page),
      controls = get_keys_table(page, offset, [Key.DATE], [True]),
      bgcolor = ft.colors.PRIMARY
   )

if __name__ == '__main__':
   #print('\n'.join(map(str, MDB.get_keys(10, limit=10).get())))
   pass