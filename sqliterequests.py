from typing import Type

class Table:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

class Request:
    def get(self) -> str:
        pass

class Insert(Request):
    cmd: str

    def __init__(self, table: Type[Table], args: list[str], values: list) -> None:
        args = ', '.join(args)
        values = ', '.join([f"'{i}'" if type(i) == str else str(i) for i in values])
        self.cmd = f'''INSERT INTO {table.name} ({args}) VALUES ({values})'''

    def get(self) -> str:
        return self.cmd

class Select(Request):
    args: str

    def __init__(self, table: Type[Table], args: list[str], all = False) -> None:
        if all:
            args = '*'
        else:
            args = ', '.join(args)
        self.cmd = f'''SELECT {args} FROM {table.name}'''
    
    def get(self) -> str:
        return self.cmd
    

class Where(Request):

    def __init__(self, request: Request, args: list[str], values: list) -> None:
        args = ', '.join([f"{args[i]} = '{values[i]}'" if type(values[i]) == str else f"{args[i]} = {values[i]}" for i in range(len(args))])
        self.cmd = f'''{request.get()} WHERE {args}'''

    def get(self) -> str:
        return self.cmd
    
class Order(Request):
    
    def __init__(self, request: Request, column: list[str], reverse: list[bool]) -> None:
        args = ', '.join([f"{column[i]} {'DESC' if reverse[i] else 'ASC'}" for i in range(len(column))])
        self.cmd = f'{request.get()} ORDER BY {args}'

    def get(self) -> str:
        return self.cmd