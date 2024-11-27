import json
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from tkcalendar import *
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

'''Файл для сохранения данных'''
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
        records_window.minsize(800, 300)

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        def update_records_from_json(text='', fromDt='', toDt=''):
            for row in tree.get_children():
                tree.delete(row)
            data = load_data()
            #(entry['date'] >= fromDt and entry['date'] <= toDt)
            for entry in data:
                if text == '' and (fromDt == '' or toDt == ''):
                    tree.insert('', tk.END,
                                values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
                elif entry['exercise'] == text and (entry['date'] >= fromDt and entry['date'] <= toDt):
                    tree.insert('', tk.END,
                                values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
            tree.pack(expand=True, fill=tk.BOTH)
            records_window.update()

        def update_records_to_json():
            data = []
            keys = ["date", "exercise", "weight", "repetitions"]
            for i in tree.get_children():
                row = tree.item(i)["values"]
                row = dict(zip(keys, row))
                data.append(row)
            with open(data_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)

        update_records_from_json()

        def btnExportCSV():
            '''3. Экспорт данных в CSV - функция для экспорта всех записей в CSV файл.'''
            with open(data_file, encoding='utf-8') as inputfile:
                df = pd.read_json(inputfile)
            df.to_csv(data_file, encoding='utf-8', index=False)

        def btnImportCSV():
            '''4. Импорт данных из CSV - функция для импорта записей из CSV файла.'''
            filepath = "training_log.csv"

            df = pd.read_csv(filepath)

            # Create a multiline json
            record_dict = json.loads(df.to_json(orient="records"))
            record_json = json.dumps(record_dict, indent=4)

            with open(data_file, 'w') as f:
                f.write(record_json)
            update_records_from_json()

        tree.bind("<Double-1>", lambda event: EditOne(event))

        def EditOne(event):
            '''5. Редактирование записи - возможность редактировать выбранную запись.'''
            region_clicked = tree.identify_region(event.x, event.y)
            if region_clicked not in "cell":
                return
            column = tree.identify_column(event.x)
            column_index = int(column[1:]) - 1
            selected_iid = tree.focus()
            selected_values = tree.item(selected_iid)
            selected_text = selected_values.get("values")[column_index]
            column_box = tree.bbox(selected_iid, column)
            entry_edit = ttk.Entry(tree, width=column_box[2])
            entry_edit.editing_column_index = column_index
            entry_edit.editing_item_iid = selected_iid
            entry_edit.insert(0, selected_text)
            entry_edit.select_range(0, tk.END)
            entry_edit.focus()
            entry_edit.bind("<Return>", lambda event: EnterPressed(event))
            entry_edit.bind("<FocusOut>", lambda event: FocusOut(event))
            entry_edit.place(x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3])

            def EnterPressed(event):
                '''Завершение редактирования'''
                new_text = event.widget.get()
                selected_iid = event.widget.editing_item_iid
                column_index = event.widget.editing_column_index
                selected_values = tree.item(selected_iid).get("values")
                selected_values[column_index] = new_text
                tree.item(selected_iid, values=selected_values)
                update_records_to_json()
                event.widget.destroy()

            def FocusOut(event):
                '''Выход из фокуса'''
                EnterPressed(event)

        def btnRemoveOne():
            '''6. Удаление записи - возможность удалить выбранную запись.'''
            i = tree.selection()[0]
            tree.delete(i)
            update_records_to_json()

        def getAvgWeight():
            '''7. Статистика по упражнениям - отображение статистики по выполненным упражнениям (Средний вес).'''
            total = 0
            count = 0
            for i in tree.get_children():
                row = tree.item(i)["values"]
                total += row[2]
                count += 1
            total = total / count
            return int(total)

        btnExportCSV = ttk.Button(records_window, text="Экспортировать в CSV", command=btnExportCSV)
        btnImportCSV = ttk.Button(records_window, text="Импортировать из CSV", command=btnImportCSV)
        btnRemoveOne = ttk.Button(records_window, text="Удалить элемент", command=btnRemoveOne)
        statisticText = ttk.Label(records_window, text=f"Средний вес:{getAvgWeight()}")

        fromLabel = ttk.Label(records_window, text="От")
        toLabel = ttk.Label(records_window, text="До")
        fromEntry = ttk.Entry(records_window, cursor="hand1")
        toEntry = ttk.Entry(records_window, cursor="hand1")

        def btnGetPlot():
            '''8. Визуализация прогресса - графики изменения веса и повторений по упражнениям за определенный период.'''
            fromDt = fromEntry.get()
            toDt = toEntry.get()
            data = []
            keys = ["date", "exercise", "weight", "repetitions"]
            for i in tree.get_children():
                row = tree.item(i)["values"]
                row = dict(zip(keys, row))
                data.append(row)
            df = pd.DataFrame(data, columns=["date", "exercise", "weight", "repetitions"])
            newdf = (df['date'] >= fromDt) & (df['date'] <= toDt)
            df = df.loc[newdf]
            df.plot(x="exercise", y=["weight", "repetitions"],
                    kind="bar", figsize=(10, 10))
            plt.title(f'Period: {fromDt} / {toDt}')
            plt.show()

        btnGetPlot = ttk.Button(records_window, text="График", command=btnGetPlot)
        btnExportCSV.pack(anchor='nw', side='left')
        btnImportCSV.pack(anchor='nw', side='left')
        btnRemoveOne.pack(anchor='nw', side='left')
        statisticText.pack(anchor='ne', side='right')
        btnGetPlot.pack(anchor='nw', side='left')
        fromLabel.pack(anchor='nw', side='left')
        fromEntry.pack(anchor='nw', side='left')
        toLabel.pack(anchor='nw', side='left')
        toEntry.pack(anchor='nw')

        fromEntry.bind("<1>", lambda event: PickDate(event, pick="from"))
        toEntry.bind("<1>", lambda event: PickDate(event, pick="to"))

        def PickDate(event, pick):
            '''8. Визуализация прогресса - графики изменения веса и повторений по упражнениям за определенный период.'''
            global cal, date_window
            date_window = Toplevel()
            if pick == "from":
                date_window.title("Дата От")
            elif pick == "to":
                date_window.title("Дата До")
            cal = Calendar(date_window, selectmode="day", date_pattern="yyyy-mm-dd")
            cal.pack(anchor='center')
            date_window.bind("<Double-1>", lambda event: GrabDate(event, pick))

        def GrabDate(event, pick):
            '''8. Визуализация прогресса - графики изменения веса и повторений по упражнениям за определенный период.'''
            if pick == "from":
                fromEntry.delete(0, 'end')
                fromEntry.insert(0, cal.get_date())
            elif pick == "to":
                toEntry.delete(0, 'end')
                toEntry.insert(0, cal.get_date())
            date_window.destroy()

        searchExerciseLabel = ttk.Label(records_window, text="Поиск упражнения")
        searchExerciseEntry = ttk.Entry(records_window)
        searchExerciseEntry.pack(anchor='sw', side='right')
        searchExerciseLabel.pack(anchor='sw', side='right')
        searchExerciseEntry.bind("<Return>", lambda event: searchExercise(event))

        def searchExercise(event):
            '''1. Фильтрация записей по дате - возможность просматривать записи за определенный период.'''
            '''2. Фильтрация записей по упражнению - возможность просматривать записи по конкретному упражнению.'''
            lookup_record = searchExerciseEntry.get()
            for row in tree.get_children():
                tree.delete(row)
            update_records_from_json(text=lookup_record, fromDt=fromEntry.get(), toDt=toEntry.get())


def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
