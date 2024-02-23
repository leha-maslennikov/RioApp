import flet as ft
from Text import *
from Controls import *
from mythicdatabase import MDB

def main(page: ft.Page) -> ft.View:
   return ft.View(
      route = f'/{MAIN}',
      controls = [
        get_menu_bar(page)
      ],
      bgcolor = ft.colors.PRIMARY
   ) 

def key_top(page: ft.Page) -> ft.View:
   keys = []
   for i in MDB.get_keys(limit=10).get():
      keys.append(get_key_row(page, i))
   return ft.View(
      route = f'/{KEY_TOP}',
      controls = [
         get_menu_bar(page), 
         ft.Container(
            content=ft.Row([ft.Column(keys, width=page.width)]),
            bgcolor=ft.colors.SECONDARY,
            expand=True
            )
      ],
      bgcolor = ft.colors.PRIMARY
   )

if __name__ == '__main__':
   #print('\n'.join(map(str, MDB.get_keys(10, limit=10).get())))
   pass