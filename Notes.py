import csv
import datetime
from os.path import exists

file_name = "notes.csv"

class Note:
    def __init__(self, id, title, body, created_at):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = created_at

def create_file(file_name):
    try:
        if not exists(file_name):
            with open(file_name, "w", newline='', encoding="utf-8") as data:
                f_writer = csv.DictWriter(data, fieldnames=["id", "title", "body", "created_at"], delimiter=';')
                f_writer.writeheader()
                print(f"Создан файл {file_name}")
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")

def load_notes():
    notes = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                note_date = datetime.datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S")
                notes.append(Note(int(row["id"]), row["title"], row["body"], row["created_at"]))
    except FileNotFoundError:
        create_file(file_name)
    except Exception as e:
        print(f"Ошибка при загрузке заметок: {e}")
    return notes
def save_notes(notes):
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "title", "body", "created_at"], delimiter=';')
            writer.writeheader()
            for note in notes:
                writer.writerow({"id": note.id, "title": note.title, "body": note.body, "created_at": note.created_at})
    except Exception as e:
        print(f"Ошибка при сохранении заметок: {e}")

def add_note(title, body):
    try:
        notes = load_notes()
        new_id = 1 if not notes else max(note.id for note in notes) + 1
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notes.append(Note(new_id, title, body, created_at))
        save_notes(notes)
        print("Заметка успешно добавлена.")
    except Exception as e:
        print(f"Ошибка при добавлении заметки: {e}")

def find_note_by_id(id):
    try:
        notes = load_notes()
        for note in notes:
            if note.id == id:
                return note
        return None
    except ValueError:
        print("Некорректный ввод ID. Пожалуйста, введите целое число.")

def edit_note(id):
    notes = load_notes()
    id = int(id)
    try:
        for index, note in enumerate(notes):
            if note.id == id:
                notes[index].title = input("Введите новый заголовок заметки: ")
                notes[index].body = input("Введите новое содержание заметки: ")
                save_notes(notes)
                print("Заметка успешно отредактирована.")
                return
    except Exception as e:
        print(f"Ошибка при редактировании заметки: {e}")


def delete_note(id):
    try:
        id = int(id)
        notes = load_notes()
        notes = [note for note in notes if note.id != id]
        save_notes(notes)
        print("Заметка успешно удалена.")
    except Exception as e:
        print(f"Ошибка при удалении заметки: {e}")

def list_notes(date_filter=None):
    try:
        notes = load_notes()
        if len(notes) == 0:
            print("Список заметок пуст")
        else:
            if date_filter is None or date_filter == '':
                for note in notes:
                    print(f"ID: {note.id}; Дата: {note.created_at};\n Заголовок: {note.title};\n Содержание: {note.body}\n")
            else:
                date_filter = date_filter[:10]
                for note in notes:
                    note_date = datetime.datetime.strptime(note.created_at, "%Y-%m-%d %H:%M:%S")
                    if note_date.date() == datetime.datetime.strptime(date_filter, "%Y-%m-%d").date():
                        print(f"ID: {note.id}; Дата: {note.created_at};\n Заголовок: {note.title};\n Содержание: {note.body}\n")
    except Exception as e:
        print(f"Ошибка при выводе заметок: {e}")

def main():
    create_file(file_name)
    while True:
        print("Список команд:\n"
              "'add' - добавить заметку\n"
              "'edit' - отредактировать заметку\n"
              "'delete' - удалить заметку\n"
              "'list' - вывести список заметок\n"
              "'quit' - выйти из приложения")
        command = input("Введите команду: ")
        if command == "add":
            title = input("Введите заголовок заметки: ")
            body = input("Введите содержание заметки: ")
            add_note(title, body)
        elif command == "edit":
            id = int(input("Введите ID заметки для редактирования: "))
            if find_note_by_id(id) == None:
                print("Заметка с указанным ID не найдена.")
                continue
            edit_note(id)
        elif command == "delete":
            id = input("Введите ID заметки для удаления: ")
            if find_note_by_id(id) == None:
                print("Заметка с указанным ID не найдена.")
                continue
            delete_note(id)
        elif command == "list":
            date_filter = input("Введите дату для фильтрации (YYYY-MM-DD) или оставьте пустым: ")
            list_notes(date_filter)
        elif command == "quit":
            break
        else:
            print("Некорректная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()