'''функции которые спользуются в боте'''

import json


# функция которая отрывает json файлы и возвращает их в виде словаря
def open_file_json(name_file:str):
    with open(name_file, 'r', encoding='utf-8') as f:
        load_file = json.load(f)
        return load_file

if __name__=="__main__":
    file = open_file_json("database/services.json")
    print(file)