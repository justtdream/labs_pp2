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

# Создание SQL-функции для поиска по шаблону
def create_search_function():
    cur.execute("""
        CREATE OR REPLACE FUNCTION search_phonebook(pattern VARCHAR)
        RETURNS TABLE(id INTEGER, name VARCHAR, telephone VARCHAR) AS $$
        BEGIN
            RETURN QUERY
            SELECT p.id, p.name, p.telephone
            FROM phonebook p
            WHERE p.name ILIKE '%' || pattern || '%'
               OR p.telephone ILIKE '%' || pattern || '%';
        END;
        $$ LANGUAGE plpgsql;
    """)
    conn.commit()

# Python-функция для вызова SQL-функции поиска
def search_by_pattern(pattern):
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cur.fetchall()
    return rows

# Функция для вывода таблицы (для демонстрации результатов)
def print_phonebook_table(rows):
    headers = ["ID", "Name", "Telephone"]
    col_widths = [len(header) for header in headers]
    
    # Определяем максимальную ширину столбцов
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
def main():
    try:
        # Создаем SQL-функцию
        create_search_function()
        
        # Пример поиска
        pattern = input("Enter search information (part of name or phone): ")
        results = search_by_pattern(pattern)
        
        if results:
            print(f"\n Result: '{pattern}':")
            print_phonebook_table(results)
        else:
            print(f"\n By '{pattern}' nothing found :( ")
            
    except psycopg2.Error as e:
        print(f" Error of db {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()