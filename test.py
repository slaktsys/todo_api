import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1/todos"

def test_all_operations():
    print("Начинаем тестирование API...\n")
    
    print("1. 📝 Создаем новую задачу...")
    new_todo = {
        "title": "Какая то задача",
        "description": "Пройти тест задачи",
        "priority": "high"
    }
    
    response = requests.post(f"{BASE_URL}/", json=new_todo)
    print(f"   Статус: {response.status_code}")
    
    if response.status_code == 201:
        todo = response.json()
        todo_id = todo["id"]
        print(f"   ✅ Создана задача ID: {todo_id}")
        print(f"   Заголовок: {todo['title']}")
        print(f"   Приоритет: {todo['priority']}")
    else:
        print(f"   ❌ Ошибка: {response.text}")
        return
    
    print("\n" + "="*50 + "\n")
    
    print("2. 🔍 Получаем задачу по ID...")
    response = requests.get(f"{BASE_URL}/{todo_id}")
    
    if response.status_code == 200:
        todo = response.json()
        print(f"   ✅ Задача получена")
        print(f"   Заголовок: {todo['title']}")
        print(f"   Статус: {'Выполнена' if todo['completed'] else 'Не выполнена'}")
    else:
        print(f"   ❌ Ошибка: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    print("3. 📋 Получаем все задачи...")
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Всего задач: {data['total']}")
        print(f"   Страница: {data['page']} из {data['pages']}")
        
        for i, task in enumerate(data['items'], 1):
            print(f"   {i}. {task['title']} ({'✅' if task['completed'] else '❌'})")
    else:
        print(f"   ❌ Ошибка: {response.text}")
    
    print("\n" + "="*50 + "\n")

    print("4. ✏️ Обновляем задачу...")
    update_data = {
        "title": "Обновленная задача",
        "completed": True,
        "priority": "low"
    }
    
    response = requests.put(f"{BASE_URL}/{todo_id}", json=update_data)
    
    if response.status_code == 200:
        todo = response.json()
        print(f"   ✅ Задача обновлена")
        print(f"   Новый заголовок: {todo['title']}")
        print(f"   Новый статус: {'✅ Выполнена' if todo['completed'] else '⭕ Не выполнена'}")
    else:
        print(f"   ❌ Ошибка: {response.text}")
    
    print("\n" + "="*50 + "\n")

    print("5. 🗑️ Удаляем задачу...")
    response = requests.delete(f"{BASE_URL}/{todo_id}")
    
    if response.status_code == 204:
        print(f"   ✅ Задача ID:{todo_id} удалена")
    else:
        print(f"   ❌ Ошибка: {response.text}")
    
    print("\n" + "="*50)
    print("🎉 Тестирование завершено!")

if __name__ == "__main__":
    time.sleep(2)
    test_all_operations()