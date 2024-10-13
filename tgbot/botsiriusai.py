import telebot
import aiohttp
import asyncio
from telebot import types
import time
# Ваш Telegram Bot API ключ
API_TOKEN = '7731308012:AAFEq5-45wKYDjSc5rpogVSsR5tkfpMjob0'

# Настройки для API Gemini
my_api = ['AIzaSyArqiOJ_Sa6ufkJDavMKS6Wyz1W_SeAd64']  # Замените на ваш API ключ

# Инициализация бота
bot = telebot.TeleBot(API_TOKEN)


# Асинхронный запрос к модели Gemini
async def request_to_model(prompt, api_id=0, model=0):
    models = ['gemini-1.5-flash-latest', 'gemini-1.5-pro-latest']
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{models[model]}:generateContent'
    params = {'key': my_api[api_id]}
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'temperature': 0.5},
        'safetySettings': [{'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE', }, ],
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, params=params, headers=headers, json=json_data) as response:
                if response.status != 200:
                    return {'error': f'Ошибка {response.status}: {await response.text()}'}
                return await response.json()
    except Exception as e:
        return {'error': str(e)}

# Стартовая команда бота
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.InlineKeyboardMarkup()
    summarize_btn = types.InlineKeyboardButton("Суммировать текст", callback_data="summarize")
    questions_btn = types.InlineKeyboardButton("Сгенерировать вопросы", callback_data="questions")
    markup.add(summarize_btn, questions_btn)
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие или отправьте .txt файл:", reply_markup=markup)

# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'summarize':
        bot.send_message(call.message.chat.id, "Пожалуйста, введите текст или отправьте файл для суммирования.")
        bot.register_next_step_handler(call.message, handle_text_or_file, process_summarize_step)
    elif call.data == 'questions':
        bot.send_message(call.message.chat.id, "Пожалуйста, введите текст или отправьте файл для генерации вопросов.")
        bot.register_next_step_handler(call.message, handle_text_or_file, process_questions_step)

# Универсальная функция для обработки текста или файла
def handle_text_or_file(message, next_step_function):
    if message.content_type == 'text':
        text = message.text.strip()
        if not text:
            bot.send_message(message.chat.id, "Текст пустой. Пожалуйста, введите текст или загрузите файл.")
            return
        next_step_function(message, text)
    elif message.content_type == 'document' and message.document.mime_type == 'text/plain':
        bot.send_message(message.chat.id, "Файл получен. Обрабатываю...")
        handle_txt_file(message, next_step_function)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите текст или загрузите файл в формате .txt.")

# Функция для обработки текстового файла
def handle_txt_file(message, next_step_function):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Попытка прочитать файл в различных кодировках
    text = None
    try:
        text = downloaded_file.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = downloaded_file.decode('windows-1251')  # Пробуем windows-1251
        except UnicodeDecodeError:
            bot.send_message(message.chat.id, "Ошибка чтения файла: неподдерживаемая кодировка.")
            return
    
    # Проверка содержимого файла
    text = text.strip()
    if not text:
        bot.send_message(message.chat.id, "Файл пустой или содержит только пробелы.")
        return
    
    # Передача текста для дальнейшей обработки
    next_step_function(message, text)

# Функция для суммирования текста
def process_summarize_step(message, text=None):
    if text is None:
        text = message.text.strip()
    if not text:
        bot.send_message(message.chat.id, "Текст пустой. Пожалуйста, введите текст или загрузите файл.")
        return
    asyncio.run(handle_summarize_request(message, text))

# Асинхронная функция для обработки суммирования текста
async def handle_summarize_request(message, user_text):
    prompt = f"ты обязан сделать и вывести конспект для упрощенного понимания данного текста(как будто его написал учитель литературы), если что ты точно можешь сделать, вот сам текст:\n\n{user_text}"
    result = await request_to_model(prompt)

    if 'error' in result:
        bot.send_message(message.chat.id, f"Ошибка: {result['error']}")
    elif 'candidates' in result and 'content' in result['candidates'][0]:  # Проверка на наличие 'content'
        summary = result['candidates'][0]['content']['parts'][0]['text']
        bot.send_message(message.chat.id, f"Краткое содержание: {summary}")
    else:
        bot.send_message(message.chat.id, "Не удалось получить краткое содержание. Попробуйте снова.")

# Функция для генерации вопросов
def process_questions_step(message, text=None):
    if text is None:
        text = message.text.strip()
    if not text:
        bot.send_message(message.chat.id, "Текст пустой. Пожалуйста, введите текст или загрузите файл.")
        return
    asyncio.run(handle_questions_request(message, text))

# Асинхронная функция для обработки генерации вопросов
async def handle_questions_request(message, user_text):
    prompt = f"твоя задача написать 5 вопросов и ответом к ним по данному тексту,все должно быть на русском.Cам текст:\n\n{user_text}"
    result = await request_to_model(prompt)

    if 'error' in result:
        bot.send_message(message.chat.id, f"Ошибка: {result['error']}")
    elif 'candidates' in result and 'content' in result['candidates'][0]:  # Проверка на наличие 'content'
        questions = result['candidates'][0]['content']['parts'][0]['text']
        bot.send_message(message.chat.id, f"Сгенерированные вопросы: {questions}")
    else:
        bot.send_message(message.chat.id, "Не удалось сгенерировать вопросы. Попробуйте снова.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

