import sqlite3


class SQLiteDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """Устанавливает соединение с базой данных."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.cursor = None
            self.connection.close()

    def create_table(self, table_name, columns):
        """
        Создает таблицу в базе данных.

        :param table_name: Имя таблицы.
        :param columns: Строка с определением колонок (например, "id INTEGER PRIMARY KEY, name TEXT").
        """
        self.connect()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.connection.commit()
        self.close()

    def insert_record(self, table_name, data):
        """
        Добавляет запись в таблицу.

        :param table_name: Имя таблицы.
        :param data: Словарь с данными для вставки (ключи - имена колонок, значения - данные).
        """
        self.connect()
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()
        self.close()

    def sort_select(self, table_name):
        """
        Используя select_records, выдает отсортированный список кортежей
        
        :param table_name: Имя таблицы
        """
        select_no_sort = self.select_records(table_name)
        select_sort = sorted(select_no_sort, key=lambda x: x[2])
        for i in range(len(select_sort)):
            id, name, result = select_sort[i]
            select_sort[i] = [name, str(result)]
        select_sort = list(map(lambda x: " ".join(x), select_sort))
        if len(select_sort) >= 5:
            select_sort = select_sort[:5]
        return select_sort

    def select_records(self, table_name, conditions=None):
        """
        Выбирает записи из таблицы по условиям.

        :param table_name: Имя таблицы.
        :param conditions: Словарь с условиями (ключи - имена колонок, значения - данные).
        :return: Список записей, удовлетворяющих условиям.
        """
        self.connect()
        if conditions:
            where_clause = ' AND '.join([f"{key} = ?" for key in conditions.keys()])
            query = f"SELECT * FROM {table_name} WHERE {where_clause}"
            self.cursor.execute(query, tuple(conditions.values()))
        else:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.close()
        return records

    def update_record(self, table_name, record_id, new_data):
        """
        Обновляет запись в таблице.

        :param table_name: Имя таблицы.
        :param record_id: ID записи, которую нужно обновить.
        :param new_data: Словарь с новыми данными (ключи - имена колонок, значения - данные).
        """
        self.connect()
        set_clause = ', '.join([f"{key} = ?" for key in new_data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        self.cursor.execute(query, tuple(new_data.values()) + (record_id,))
        self.connection.commit()
        self.close()

    def delete_record(self, table_name, record_id):
        """
        Удаляет запись из таблицы.

        :param table_name: Имя таблицы.
        :param record_id: ID записи, которую нужно удалить.
        """
        self.connect()
        query = f"DELETE FROM {table_name} WHERE id = ?"
        self.cursor.execute(query, (record_id,))
        self.connection.commit()
        self.close()

    def change_table(self, table_name, data):
        name = data["user_name"]
        select0 = self.select_records(table_name, {"user_name": name})
        print(select0)
        if select0:
            id, user_name, time = select0[0]
            if int(time) > data["result"]:
                self.update_record(table_name, id, {"result": data["result"]})
        else:
            self.insert_record(table_name, data)


# Пример использования:
if __name__ == "__main__":
    db = SQLiteDatabase("labyrinth_right.sqlite")

    # Создание таблицы
    # db.create_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")

    # Добавление записи
    # db.insert_record("users", {"name": "Alice", "age": 25})
    # db.insert_record("users", {"name": "Bob", "age": 30})

    # Выбор записей
    # records = db.select_records("users", {"name": "Alice"})
    # print(records)  # Вывод: [(1, 'Alice', 25)]

    # Обновление записи
    # db.update_record("users", 1, {"age": 26})

    # Удаление записи
    # db.delete_record("users", 2)

    # Проверка результатов
    # records = db.select_records("users")
    records = db.select_records("Level_1", {"user_name": "NoName", "result": 15})
    print(records)  # Вывод: [(1, 'Alice', 26)]