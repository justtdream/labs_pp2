import psycopg2
import csv
#присоединение к базе данных
conn = psycopg2.connect(database="phonebbok_db", 
                        user="postgres", 
                        host='localhost',
                        password="_Avndfgt!",
                        port=5432)
cur = conn.cursor()

# Создание таблицы
cur.execute('''
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telephone VARCHAR(40) NOT NULL)
''')
conn.commit()

# Функция для загрузки данных из CSV файла
def upload_csv(filename):
    command = """INSERT INTO phonebook(id, name, telephone) VALUES (%s, %s, %s)"""
    filename = "lab10/1task/phonebookk.csv"
    try:
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            next(csvreader)  # Пропускаем заголовок
            for row in csvreader:
                id, name, telephone = row
                cur.execute(command, (id, name, telephone))
                conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Функция для добавления контакта через консоль
def enter_yourself():
    id = int(input("New contact's ID: "))
    name = input("Enter contact's name: ")
    telephone = input("Enter contact's telephone number: ")
    cur.execute("INSERT INTO phonebook (id, name, telephone) VALUES (%s, %s, %s)", (id, name, telephone))
    conn.commit()

# Функция для обновления данных контакта
def update_table():
    id = int(input("Enter id of a contact you want to change: "))
    print("What do you want to change?")
    print("1. Contact's name")
    print("2. Contact's telephone number")
    choice = int(input("Your choice: "))

    if choice == 1:
        new_name = input("Write new name: ")
        cur.execute("""UPDATE phonebook
                        SET name = %s
                        WHERE id = %s""", (new_name, id))
        conn.commit()
    elif choice == 2:
        new_num = input("Write necessary phone number: ")
        cur.execute("""UPDATE phonebook
                        SET telephone = %s
                        WHERE id = %s""", (new_num, id))
        conn.commit()

# Функция для запроса данных по фильтру
def query_data():
    print("How do you want to filter your data?")
    print("1. By contact's name")
    print("2. By contact's phone number")
    choice = int(input("Your choice: "))

    if choice == 1:
        name = input("Enter needed name: ")
        cur.execute("""SELECT * FROM phonebook WHERE name = %s;""", (name,))
    elif choice == 2:
        num = input("Enter needed phone number: ")
        cur.execute("""SELECT * FROM phonebook WHERE telephone = %s;""", (num,))

    rows = cur.fetchall()
    for row in rows:
        print(row)

# Функция для удаления контакта
def delete_data():
    name = input("Enter name of a contact you want to delete: ")
    cur.execute("""DELETE FROM phonebook WHERE name = %s""", (name,))
    conn.commit()

# Функция для вывода всех данных
def print_phonebook_table():
    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    headers = ["ID", "Name", "Telephone"]
    
    col_widths = [len(header) for header in headers]
    for row in rows:
        col_widths[0] = max(col_widths[0], len(str(row[0])))
        col_widths[1] = max(col_widths[1], len(str(row[1])))
        col_widths[2] = max(col_widths[2], len(str(row[2])))

    divider = '+' + '+'.join(['-' * (w + 2) for w in col_widths]) + '+'
    header_row = '| ' + ' | '.join(f'{headers[i]:<{col_widths[i]}}' for i in range(len(headers))) + ' |'
    
    print(divider)
    print(header_row)
    print(divider)
    
    for row in rows:
        row_str = '| ' + ' | '.join(f'{str(row[i]):<{col_widths[i]}}' for i in range(len(row))) + ' |'
        print(row_str)
    print(divider)

# Основной код
print("Choose what you want to do with the table:")
print("1. Insert some data")
print("2. Change contact")
print("3. Filter data by name or phone number")
print("4. Delete contact")
command = int(input("Your choice: "))

if command == 1:
    print("Choose the method you want to insert data with:")
    print("1. By the CSV-file")
    print("2. By the console")
    choice = int(input("Your choice: "))

    if choice == 1:
        filename = input("Enter CSV-file name: ")
        upload_csv(filename)
    elif choice == 2:
        enter_yourself()

elif command == 2:
    update_table()
elif command == 3:
    query_data()
elif command == 4:
    delete_data()

print_phonebook_table()

# Закрытие соединения
conn.close()
