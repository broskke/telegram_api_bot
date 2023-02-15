import requests
import json


HOST = 'http://3.67.196.232/'

class GetAllMixin:
    def get_all_todos(self,url):
        response = requests.get(url + 'todo/all')
        if response.status_code == 200:
            return json.loads(response.text)
        raise Exception('Сервер упал')

# get = GetAllMixin()
# print(get.get_all_todos(HOST))

class CreateMixin:
    def creat_todo(self,url, data: dict):
        response = requests.post(url + 'todo/create',data=json.dumps(data))
        if response.status_code == 200:
            return 1 
        return 0

todo = {
    'title':'Эмир',
    'is_done': False
}
# print(creat_todo(HOST, todo))
# print(get_all_todos(HOST))

class RetrieveMixin:
    def retrieve_todo(self,url, id_: int):
        response = requests.get(url + f'todo/{id_}')
        if response.status_code == 200:
            return json.loads(response.text)
        elif response.status_code == 404:
            return 'Нет такой зaписи'
        
# print(retrieve_todo(HOST,112))

class UpdateMixin:
    def update_todo(self,url,id_:int,data:dict):
        response = requests.put(url + f'todo/{id_}/update',data=json.dumps(data))
        if response.status_code == 200:
            return 1
        return 0

data = {
    'title':'Emir',
    'is_done': False
}
# print(update_todo(HOST,30,data))
# print(get_all_todos(HOST))

class DeleteMixin:
    def delete_todo(self,url,id_:int):
        response = requests.delete(url + f'todo/{id_}/delete')
        if response.status_code == 200:
            return 1
        return 0

#TODO переписать в классы через миксины

