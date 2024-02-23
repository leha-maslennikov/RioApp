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
   panel = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.ON_SECONDARY_CONTAINER,
        divider_color=ft.colors.SECONDARY,
        controls=[]
   )
   for i in MDB.get_keys(limit=10).get():
      panel.controls.append(get_key_row(page, i))
   controls = [
      get_menu_bar(page),
      ft.Container(
         ft.Column(
            [
               ft.Row(
                  [get_key_block(ft.Text(i, color=ft.colors.ON_SECONDARY_CONTAINER, size=16)) for i in 'Rank	Dungeon	Level	Time	Affixes	Tank	Healer	DPS	Score'.split()]
               ),
               panel
            ]
         ),
         bgcolor=ft.colors.SECONDARY
      )
   ]
   return ft.View(
      route = f'/{KEY_TOP}',
      controls = controls,
      bgcolor = ft.colors.PRIMARY
   )

if __name__ == '__main__':
   #print('\n'.join(map(str, MDB.get_keys(10, limit=10).get())))
   pass