import sqlite3

MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5

#вывод на экран главного меню
def display_menu():
    print('/n-----Меню введения учёта инструментов-----')
    print('1. Создать новую позицию')
    print('2. Прочитать позицию')
    print('3. Обновить позицию')
    print('4. Удалить позицию')
    print('5. Выйти из программы')

#получаем от пользователя пункт меню
def get_menu_choice():
    choice = int(input('Введите ваш вариант: '))
    while choice < MIN_CHOICE or choice > MAX_CHOICE:
        print(f'Допустимые варианты таковы:{MIN_CHOICE} - {MAX_CHOICE}')
        choice = int(input('Введите ваш вариант:'))
    return choice

#создание новой позиции
def create():
    print('Создать новую позицию')
    name = input('Название позиции:')
    price = int(input('Цена:'))
    insert_row(name, price)

#чтение существующей позиции
def read():
    name = input('Введите название искомой позиции: ')
    num_found = display_item(name)
    print(f'{num_found} строк(а) найдено ')

#обновление существующей позиции
def update():
    read()
    selected_id = int(input('Выберите ID обновляемой позиции:'))
    name = input('Ведите новое название таблицы: ')
    price = input('Введите новую цену: ')
    num_updated = update_row(selected_id, name, price)
    print(f'{num_updated} строк(а) обновлено')

#удаление позиции
def delete():
    read()
    selected_id = int(input('Введите ID обновляемой позиции: '))
    sure = input('Вы уверены, что хотите удалить эту позицию? (да/нет')
    if sure.lower() == 'да':
        num_deleted = delete(selected_id)
        print(f'{num_deleted} строк(а) удалено')

#
def insert_row(name, price):
    conn = None
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO Inventory (ItemName, Price) VALUES (?, ?)''', (name, price))
        conn.commit()
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()

#выводит на экран все позиции с совпадающими названиями позиций
def display_item(name):
    conn = None
    results = []
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Inventory WHERE ItemName == ?''', (name,))
        results = cur.fetchall()

        for row in results:
            print(f'ID: {row[0]:<3}\nНазвание: {row[1]:<15}\nЦена: {row[2]:<6}')
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()
            return len(results)

#обновляем существующее значение новым названием и ценой. Возвращаем обновлённе число строк
def update_row(id, name, price):
    conn = None
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''UPDATE Inventory SET ItemName = ?, Price = ? WHERE ID == ?''', (name, price, id))
        conn.commit()
        num_updated = cur.rowcount
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()
            return num_updated

#Удаляет существующую позицию. Возвращает число удалённых строк
def delete_row(id):
    conn = None
    try:
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM Inventory WHERE ID == ? ''', (id))
        num_deleted2 = cur.rowcount
    except sqlite3.Error as err:
        print('Ошибка базы данных', err)
    finally:
        if conn != None:
            conn.close()
            return num_deleted2

#лавная функция программы
def main():
    choice = 0
    while choice != EXIT:
        display_menu()
        choice = get_menu_choice()
        if choice == CREATE:
            create()
        if choice == READ:
            read()
        if choice == UPDATE:
            update()
        if choice == DELETE:
            delete()

if __name__ == '__main__':
    main()


