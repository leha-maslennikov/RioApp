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

def key_top(page: ft.Page, offset: int) -> ft.View:
   def click(e: ft.ControlEvent):
      e.page.go(f'/{KEY_TOP}/:{e.control.data}')

   size = MDB.size()
   btns = [
      (ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT, True if offset == 0 else False, 0),
      (ft.icons.CHEVRON_LEFT, True if offset == 0 else False, max(0, offset - 10)),
      (ft.icons.CHEVRON_RIGHT, False if size.get() - offset - 10 > 0 else True, offset+10),
      (ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT, False if size.get() - offset - 10 > 0 else True, size.get()-10)]
   btns = [ft.IconButton(icon = icon, bgcolor=ft.colors.PRIMARY_CONTAINER, icon_color=ft.colors.ON_PRIMARY_CONTAINER, disabled=dis, data=offset, on_click=click) for icon, dis, offset in btns]
   keys = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.ON_SECONDARY_CONTAINER,
        divider_color=ft.colors.SECONDARY,
        controls=[]
   )
   for i in MDB.get_keys(offset=offset, limit=10).get():
      keys.controls.append(get_key_row(page, i))
   controls = [
      get_menu_bar(page),
      ft.Row(btns),
      ft.Container(
         ft.Column([
               ft.Row([get_key_block(ft.Text(i, color=ft.colors.ON_SECONDARY, size=16)) for i in 'Rank	Dungeon	Level	Time	Affixes	Tank	Healer	DPS	Score'.split()]),
               ft.Column([keys], height=page.height-200,scroll=ft.ScrollMode.ADAPTIVE)
            ]
         ),
         bgcolor=ft.colors.SECONDARY,
         border_radius=10
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