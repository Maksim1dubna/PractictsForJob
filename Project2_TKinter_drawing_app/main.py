import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.x = 600
        self.y = 400
        self.text = ''
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (self.x, self.y), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.pen_color = 'black'
        self.canvas = tk.Canvas(root, width=self.x, height=self.y, bg="white")
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        '''Для задания 2 запоминть последний цвет'''
        self.l_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind("<Button-1>", self.add_text)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        '''Задача №1. Реализовать функционал: Выбор размера кисти из списка'''
        self.sizes = [1, 2, 5, 10]
        '''Переменная, определенная с помощью IntVar() функции, содержит целочисленные данные, 
        где мы можем их можем установить, а также можем извлечь их с помощью методов getter и setter.'''
        self.variable = tk.IntVar()
        self.variable.set(1)
        self.brush_size_scale = tk.OptionMenu(control_frame, self.variable, *self.sizes)
        self.brush_size_scale.pack(side=tk.LEFT)

        '''Задача №2. Реализовать функционал: Инструмент "Ластик"'''
        self.eraser_button = tk.Button(control_frame, text="Ластик", command=self.eraser)
        self.eraser_button.pack(side=tk.LEFT)

        '''Задача №3. Реализовать функционал: Пипетка для выбора цвета с холста'''
        self.canvas.bind('<Button-3>', self.pick_color)

        '''Задача №4. Реализовать функционал: Горячие клавиши для быстрых действий'''
        self.root.bind('<s>', self.save_image)
        self.root.bind('<c>', self.choose_color)

        '''Задача №5. Реализовать функционал: Предварительный просмотр цвета кисти'''
        self.preview_color_label = tk.Label(self.root, bg=self.pen_color, width=3)
        self.preview_color_label.pack(side=tk.RIGHT)

        '''Задача №6. Реализовать функционал: Изменение размера холста'''
        self.size_canvas_button = tk.Button(control_frame, text="Размер холста", command=self.size_canvas)
        self.size_canvas_button.pack(side=tk.LEFT)

        '''Задача №7. Реализовать функционал: Инструмент "Текст" для добавления текста на изображение'''
        self.set_text_button = tk.Button(control_frame, text="Текст", command=self.set_text)
        self.set_text_button.pack(side=tk.LEFT)

        self.background_color_button = tk.Button(control_frame, text="Цвет фона", command=self.background_color)
        self.background_color_button.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x and self.last_y:
            '''Задание 1. width теперь принимает self.variable.get() из brush_size_scale'''
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.variable.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.variable.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    '''Задача №4. добавлена переменная event=0 (Для возможности запустить события)'''

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    '''Задача №4. добавлена переменная event=0 (Для возможности запустить события)'''

    def choose_color(self, event=0):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.l_color = self.pen_color
        self.eraser_button.configure(foreground='black')
        self.preview_color_label.configure(bg=self.pen_color)

    def save_image(self, event=0):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    '''Задача №2. Реализовать функционал: Инструмент "Ластик"'''

    def eraser(self):
        if self.pen_color == "white":
            self.pen_color = self.l_color
            self.eraser_button.configure(foreground='black')
            self.preview_color_label.configure(bg=self.l_color)
        else:
            self.pen_color = "white"
            self.eraser_button.configure(foreground='red')
            self.preview_color_label.configure(bg=self.pen_color)

    '''Задача №3. Реализовать функционал: Пипетка для выбора цвета с холста'''

    def pick_color(self, event):
        '''Перевод RGB в hex'''
        self.pen_color = '#%02x%02x%02x' % self.image.getpixel([event.x, event.y])
        self.eraser_button.configure(foreground='black')

    '''Задача №6. Реализовать функционал: Изменение размера холста'''

    def size_canvas(self):
        self.y = tk.simpledialog.askinteger("Размер холста", "Координата Y|", parent=self.root)
        self.x = tk.simpledialog.askinteger("Размер холста", "Координата X_", parent=self.root)
        self.root.mainloop()

    '''Задача №7. Реализовать функционал: Инструмент "Текст" для добавления текста на изображение'''

    def set_text(self):
        self.text = tk.simpledialog.askstring("Текст для вставки", "Текст", parent=self.root)
        self.set_text_button.configure(foreground='red')

    def add_text(self, event):
        self.draw.text((event.x, event.y), self.text, fill=self.pen_color)
        self.set_text_button.configure(foreground='black')
        ts = self.canvas.create_text([event.x, event.y], text=self.text, fill=self.pen_color)
        self.canvas.itemconfig(ts, text=self.text)
        self.text = ''

    def background_color(self):
        new_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.canvas.config(background=new_color)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
