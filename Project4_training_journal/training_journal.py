import csv
import json
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from datetime import datetime
import pandas as pd

# Файл для сохранения данных
data_file = 'training_log.json'

def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self):
        # Виджеты для ввода данных
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

    def add_entry(self):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self):
        data = load_data()
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")
        records_window.minsize(800, 200)

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")
        def update_records():
            for row in tree.get_children():
                tree.delete(row)
            data = load_data()
            for entry in data:
                tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
            tree.pack(expand=True, fill=tk.BOTH)
            records_window.update()
        update_records()

        def btnExportCSV():
            '''3. Экспорт данных в CSV - функция для экспорта всех записей в CSV файл.'''
            with open('training_log.json', encoding='utf-8') as inputfile:
                df = pd.read_json(inputfile)
            df.to_csv('training_log.csv', encoding='utf-8', index=False)
        def btnImportCSV():
            '''4. Импорт данных из CSV - функция для импорта записей из CSV файла.'''
            filepath = "training_log.csv"
            output_path = "training_log.json"

            df = pd.read_csv(filepath)

            # Create a multiline json
            record_dict = json.loads(df.to_json(orient="records"))
            record_json = json.dumps(record_dict, indent=2)

            with open(output_path, 'w') as f:
                f.write(record_json)
            update_records()


        btnExportCSV = ttk.Button(tree, text="Экспортировать в CSV", command = btnExportCSV)
        btnImportCSV = ttk.Button(tree, text="Импортировать из CSV", command = btnImportCSV)
        btnExportCSV.pack(anchor = "w", side = "bottom")
        btnImportCSV.pack(anchor = "w", side = "bottom")


def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()