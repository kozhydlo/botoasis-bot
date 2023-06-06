from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Створюємо клас зі станами для збереження даних
class OrderForm(StatesGroup):
    name = State()
    phone = State()
    requirements = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Про розробників"))
    keyboard.add(types.KeyboardButton("Замовити"))
    keyboard.add(types.KeyboardButton("Контакти"))
    keyboard.add(types.KeyboardButton("Наші проекти"))

    await message.reply("Виберіть опцію:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Про розробників')
async def developers_info(message: types.Message):
    text = "<b>Кожидло Марк</b> та <b>Мрочка Святослав</b> - це два талановиті та пристрасні програмісти, які мають різні ролі у цьому проекті.\n\n" \
           "<b>Марк</b> - досвідчений full stack програміст та Python Telegram bot розробник з п'ятирічним досвідом. Він має глибокі знання та навички в розробці програмного забезпечення. Його досвід у створенні веб-додатків та Telegram ботів дозволяє йому ефективно вирішувати завдання та пропонувати якісні рішення для клієнтів. Він постійно вдосконалює свої навички та слідкує за новими технологіями.\n\n" \
           "<b>Святослав</b> - це початковий Python програміст з великим ентузіазмом та бажанням розвиватися у цій галузі. Він має сильні основи в Python та старанно працює над покращенням своїх навичок. Святослав завжди відкритий для нових викликів та готовий навчатися від більш досвідчених колег.\n\n" \
           "Обидва розробники працюють разом, діляться знаннями та досвідом, щоб забезпечити високу якість програмного забезпечення. Вони мають спільну мету - створювати ефективні та інноваційні рішення для клієнтів. Їхнє співпраця сприяє розвитку проекту та досягненню високих результатів у галузі програмування."

    await bot.send_message(message.chat.id, text, parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: message.text == 'Контакти')
async def contact_info(message: types.Message):
    await bot.send_message(message.chat.id, "Наші контактні дані:\nEmail: botoasis2023@gmail.com\nТелефон: +380 50 958 60 69")


@dp.message_handler(lambda message: message.text == 'Замовити')
async def order_info(message: types.Message):
    await bot.send_message(message.chat.id, "Будь ласка, введіть своє ім'я:")
    await OrderForm.name.set()


@dp.message_handler(state=OrderForm.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await bot.send_message(message.chat.id, "Будь ласка, введіть свій номер телефону:")
    await OrderForm.next()


@dp.message_handler(state=OrderForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await bot.send_message(message.chat.id, "Будь ласка, введіть вимоги до замовлення:")
    await OrderForm.next()


@dp.message_handler(state=OrderForm.requirements)
async def process_requirements(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['requirements'] = message.text

    # Отримання даних зі стану
    name = data['name']
    phone = data['phone']
    requirements = data['requirements']

    # Відправка повідомлення менеджеру
    manager_message = f"Нове замовлення!\nІм'я: {name}\nНомер телефону: {phone}\nВимоги до замовлення: {requirements}"

    await bot.send_message(config.MANAGER_CHAT_ID, manager_message)

    # Відправка підтвердження користувачу
    await bot.send_message(message.chat.id, "Дякуємо за ваше замовлення! Наш менеджер скоро з вами зв'яжеться.")

    # Скидання стану
    await state.finish()


@dp.message_handler(lambda message: message.text == 'Наші проекти')
async def projects_info(message: types.Message):
    text = "Наші проекти доступні на нашому сайті. Клікніть на кнопку нижче, щоб перейти до сайту."

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Перейти до сайту", url="https://647f7c3373577359fbe2f818--joyful-parfait-0df51c.netlify.app/"))

    await bot.send_message(message.chat.id, text, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
