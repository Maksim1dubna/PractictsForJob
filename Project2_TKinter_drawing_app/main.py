import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        '''Для задания 2 запоминть последний цвет'''
        self.l_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        # self.brush_size_scale.pack(side=tk.LEFT)
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

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.l_color = self.pen_color
        self.eraser_button.configure(foreground='black')

    def save_image(self):
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
        else:
            self.pen_color = "white"
            self.eraser_button.configure(foreground='red')

    '''Задача №3. Реализовать функционал: Пипетка для выбора цвета с холста'''
    def pick_color(self, event):
        '''Перевод RGB в hex'''
        self.pen_color = '#%02x%02x%02x' % self.image.getpixel([event.x, event.y])
        self.eraser_button.configure(foreground='black')


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
