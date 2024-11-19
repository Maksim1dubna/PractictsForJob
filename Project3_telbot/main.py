import telebot
from PIL import Image, ImageOps
import io
from telebot import types
import time

TOKEN = '0000'
bot = telebot.TeleBot(TOKEN)

user_states = {}  # тут будем хранить информацию о действиях пользователя

# набор символов из которых составляем изображение
'''Задача №1. Изменение набора символов для ASCII арта из изображений (Переделка пременной в global)'''
global ASCII_CHARS
ASCII_CHARS = ''


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def grayify(image):
    return image.convert("L")


def image_to_ascii(image_stream, new_width=40):
    # Переводим в оттенки серого
    image = Image.open(image_stream).convert('L')

    # меняем размер сохраняя отношение сторон
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55)  # 0,55 так как буквы выше чем шире
    img_resized = image.resize((new_width, new_height))

    img_str = pixels_to_ascii(img_resized)
    img_width = img_resized.width

    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)

    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art


def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return characters


# Огрубляем изображение
def pixelate_image(image, pixel_size, flip=False, heatmap=False, resize=False):
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    '''Задача №2. Инверсия цветов изображения'''
    image = ImageOps.invert(image)
    '''Задача №3. Отражение изображения'''
    if flip == True:
        image = mirror_image(image, flip_site='t_b')
    if heatmap == True:
        image = convert_to_heatmap(image)
    if resize == True:
        image = resize_for_sticker(image)
    return image


def mirror_image(image, flip_site='l_r'):
    '''Задача №3. Отражение изображения'''
    if flip_site == 'l_r':
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_site == 't_b':
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return image


def convert_to_heatmap(image):
    '''Задача №4. Преобразование изображения в тепловую карту'''
    image = image.convert("L")
    image = ImageOps.colorize(image, black='red', white='blue')
    return image


def resize_for_sticker(image):
    '''Задача №5. Изменение размера изображения для стикера'''
    mywidth = 128

    wpercent = (mywidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((mywidth, hsize), Image.Resampling.LANCZOS) # LANCZOS Для лучшего качества при изменении размера
    return image


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me an image, and I'll provide options for you!")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "I got your photo! Please choose what you'd like to do with it.",
                 reply_markup=get_options_keyboard())
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id}


def get_options_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    keyboard.add(pixelate_btn, ascii_btn)
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global ASCII_CHARS
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Pixelating your image...")
        '''Задача №3. Отражение изображения + без отражения'''
        pixelate_and_send(call.message, resize=True)
        pixelate_and_send(call.message, flip=True)
        '''Задача №4. Преобразование изображения в тепловую карту'''
        pixelate_and_send(call.message, heatmap=True)
    elif call.data == "ascii":
        sent = bot.send_message(call.message.chat.id, "Print your ASCII :")
        bot.register_next_step_handler(sent, ascii_set)
        while ASCII_CHARS == '':
            time.sleep(0.1)
        bot.answer_callback_query(call.id, "Converting your image to ASCII art...")
        ascii_and_send(call.message)
        ASCII_CHARS = ''


'''Задача №1. Изменение набора символов для ASCII арта из изображений'''


def ascii_set(message):
    global ASCII_CHARS
    ASCII_CHARS = message.text


def pixelate_and_send(message, flip=False, heatmap=False, resize=False):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    pixelated = pixelate_image(image, 20, flip, heatmap, resize)

    output_stream = io.BytesIO()
    pixelated.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)


def ascii_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    ascii_art = image_to_ascii(image_stream)
    bot.send_message(message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")


bot.polling(none_stop=True)
