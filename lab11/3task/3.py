import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    database="phonebbok_db",
    user="postgres",
    host='localhost',
    password="_Avndfgt!",
    port=5432
)
cur = conn.cursor()

# Создание таблицы phonebook
cur.execute('''
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telephone VARCHAR(40) NOT NULL)
''')
conn.commit()

# Синхронизация последовательности id
cur.execute('''
    SELECT setval(pg_get_serial_sequence('phonebook', 'id'), 
                  COALESCE((SELECT MAX(id) FROM phonebook), 1));
''')
conn.commit()

# Создание хранимой процедуры
cur.execute('''
    CREATE OR REPLACE PROCEDURE insert_many_users(
        p_names VARCHAR[],
        p_phones VARCHAR[],
        INOUT incorrect_data VARCHAR[]
    )
    LANGUAGE plpgsql
    AS $$
    DECLARE
        i INTEGER;
        temp_incorrect VARCHAR[];
        phone_pattern VARCHAR := '^\+[0-9]{9,14}$'; -- Формат: + и 9-14 цифр
    BEGIN
        -- Инициализируем массив для некорректных данных
        temp_incorrect := '{}';

        -- Цикл по списку имён и телефонов
        FOR i IN 1..array_length(p_names, 1) LOOP
            -- Проверяем, соответствует ли телефон формату
            IF p_phones[i] ~ phone_pattern THEN
                -- Если телефон корректен, добавляем запись
                INSERT INTO phonebook (name, telephone)
                VALUES (p_names[i], p_phones[i]);
            ELSE
                -- Если телефон некорректен, добавляем имя и телефон в список
                temp_incorrect := temp_incorrect || ARRAY[p_names[i], p_phones[i]];
            END IF;
        END LOOP;

        -- Возвращаем список некорректных данных
        incorrect_data := temp_incorrect;
    END;
    $$;
''')
conn.commit()

# Функция для ввода данных и вызова процедуры
def insert_many_users():
    # Запрашиваем имена и телефоны (через запятую)
    names_input = input("Enter names (separated by commas): ")
    phones_input = input("Enter phone numbers (separated by commas, e.g., +77712345678): ")

    # Разделяем введённые строки на списки
    names = [name.strip() for name in names_input.split(',')]
    phones = [phone.strip() for phone in phones_input.split(',')]

    try:
        # Вызываем процедуру, передавая списки имён и телефонов
        cur.execute("CALL insert_many_users(%s, %s, %s)", (names, phones, []))
        # Получаем возвращённые некорректные данные
        incorrect_data = cur.fetchone()[0]
        conn.commit()

        # Выводим результат
        if incorrect_data:
            print("Incorrect data:")
            for i in range(0, len(incorrect_data), 2):
                print(f"Name: {incorrect_data[i]}, Phone: {incorrect_data[i+1]}")
        else:
            print("All data inserted successfully!")
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()

# Запускаем функцию
insert_many_users()

# Закрываем соединение
cur.close()
conn.close()