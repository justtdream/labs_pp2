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

# Создание таблицы
cur.execute('''
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telephone VARCHAR(40) NOT NULL)
''')
conn.commit()
'''
CREATE TABLE — команда, которая создаёт новую таблицу в базе данных (в данном случае phonebook).
IF NOT EXISTS — это условие, которое говорит PostgreSQL: "Создай таблицу только если она ещё не существует в базе данных
'''

# Синхронизация последовательности
cur.execute('''
    SELECT setval(pg_get_serial_sequence('phonebook', 'id'), 
                  COALESCE((SELECT MAX(id) FROM phonebook), 1));
''')
conn.commit()
'''
Это функция, которая находит имя последовательности, связанной со столбцом id в таблице phonebook.
'''

# Создание хранимой процедуры
cur.execute('''
    CREATE OR REPLACE PROCEDURE insert_or_update_user(
        p_name VARCHAR,
        p_telephone VARCHAR
    )
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
            UPDATE phonebook
            SET telephone = p_telephone
            WHERE name = p_name;
        ELSE
            INSERT INTO phonebook (name, telephone)
            VALUES (p_name, p_telephone);
        END IF;
    END;
    $$;
''')
conn.commit()

# Вызов процедуры
name = input("Enter name: ")
telephone = input("Enter telephone: ")
try:
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, telephone))
    conn.commit()
    cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    result = cur.fetchone()
    if result:
        print(f"Result: ID={result[0]}, Name={result[1]}, Telephone={result[2]}")
    else:
        print("No record found")
except psycopg2.Error as e:
    print(f"Error: {e}")
    conn.rollback()

# Закрытие соединения
cur.close()
conn.close()