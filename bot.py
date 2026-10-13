import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота с поддержкой aiogram 3.7+
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

BASE_DIR = Path(__file__).parent


# ===================== КЛАВИАТУРЫ =====================

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню бота (6 кнопок)"""
    keyboard = [
        [InlineKeyboardButton(text="🗓 Запись на консультацию", callback_data="menu_consultation")],
        [InlineKeyboardButton(text="🎁 Бесплатные материалы", callback_data="menu_free_materials")],
        [InlineKeyboardButton(text="📖 Полезные гайды", callback_data="menu_guides")],
        [
            InlineKeyboardButton(text="⭐ Отзывы", url=config.REVIEWS_URL),
            InlineKeyboardButton(text="👩‍💼 Обо мне", callback_data="menu_about"),
        ],
        [InlineKeyboardButton(text="🏛 О юридической компании", url=config.COMPANY_SITE_URL)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_consultation_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура экрана консультаций с фильтром"""
    keyboard = [
        [InlineKeyboardButton(text="💬 Написать юристу (перейти в диалог)", url=f"https://t.me/{config.LAWYER_USERNAME}")],
        [InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_free_materials_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура бесплатных материалов из канала"""
    links = config.FREE_MATERIALS_LINKS
    keyboard = [
        [InlineKeyboardButton(text="📋 Памятка «Авиаколлапс»", url=links["avia_collapse"])],
        [InlineKeyboardButton(text="✈️ Памятка пассажирам при задержке", url=links["passengers_memo"])],
        [InlineKeyboardButton(text="📕 Паспортная энциклопедия", url=links["passport_encyclopedia"])],
        [InlineKeyboardButton(text="🛃 Таможенная энциклопедия", url=links["customs_encyclopedia"])],
        [InlineKeyboardButton(text="🇹🇭 Тайская энциклопедия", url=links["thai_encyclopedia"])],
        [InlineKeyboardButton(text="⚖️ Взыскание убытков с АК и ТО", url=links["claim_damages"])],
        [InlineKeyboardButton(text="🏝 Что делать при отмене тура", url=links["tour_cancellation"])],
        [InlineKeyboardButton(text="🚨 Действия туристов при ЧС в мире", url=links["emergency_situations"])],
        [InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_guides_catalog_keyboard() -> InlineKeyboardMarkup:
    """Каталог полезных гайдов (6 подразделов)"""
    keyboard = [
        [InlineKeyboardButton(text="✈️ Задержка рейса (план «Ковёр»)", callback_data="guide_flight_delay_kover")],
        [InlineKeyboardButton(text="🚫 Отмена рейса (план «Ковёр»)", callback_data="guide_flight_cancel_kover")],
        [InlineKeyboardButton(text="🏝 Отмена тура (план «Ковёр»)", callback_data="guide_tour_cancel_kover")],
        [InlineKeyboardButton(text="⏳ Задержка тура (план «Ковёр»)", callback_data="guide_tour_delay_kover")],
        [InlineKeyboardButton(text="🇹🇭 Гайд по Таиланду", callback_data="guide_thailand_guide")],
        [InlineKeyboardButton(text="📍 Гайд по локациям", callback_data="guide_locations_guide")],
        [InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_single_guide_keyboard(guide_key: str) -> InlineKeyboardMarkup:
    """Две кнопки для конкретного гайда: Купить и Подробная информация"""
    guide = config.GUIDES_DATA[guide_key]
    keyboard = [
        [InlineKeyboardButton(text="💳 Купить гайд", url=guide["buy_url"])],
        [InlineKeyboardButton(text="ℹ️ Подробная информация о гайде", url=guide["info_url"])],
        [InlineKeyboardButton(text="⬅️ Назад к гайдам", callback_data="menu_guides")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_about_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для раздела Обо мне"""
    keyboard = [
        [InlineKeyboardButton(text="📢 Канал «Адвокат туриста»", url=config.CHANNEL_URL)],
        [InlineKeyboardButton(text="🏛 Сайт Правового агентства [RE]Акция", url=config.COMPANY_SITE_URL)],
        [InlineKeyboardButton(text="⬅️ Главное меню", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ===================== ТЕКСТЫ И ОБРАБОТЧИКИ =====================

WELCOME_TEXT = (
    "<b>Здравствуйте! Рада приветствовать вас!</b> 💼\n\n"
    "Я — <b>Олеся Аблёзгова</b>, кандидат юридических наук, соучредитель Правового агентства <b>«[RE]Акция»</b> "
    "и автор экспертного канала <b>«Адвокат туриста»</b>.\n\n"
    "Этот бот — ваш надежный юридический помощник в путешествиях:\n"
    "• <b>Запись на индивидуальную консультацию</b> с разбором документов;\n"
    "• <b>Полезные гайды и инструкции</b> по возврату денег и убытков;\n"
    "• <b>Бесплатные материалы и энциклопедии</b> на случай форс-мажоров в дороге.\n\n"
    "Выберите нужный раздел в меню ниже 👇"
)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Стартовое сообщение бота (с фото при наличии welcome.jpg)"""
    photo_path = BASE_DIR / "welcome.jpg"

    if photo_path.exists():
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo,
            caption=WELCOME_TEXT,
            reply_markup=get_main_menu_keyboard(),
        )
    else:
        await message.answer(
            text=WELCOME_TEXT,
            reply_markup=get_main_menu_keyboard(),
        )


@dp.callback_query(F.data == "back_to_main")
async def callback_back_to_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    try:
        await callback.message.edit_text(
            text=WELCOME_TEXT,
            reply_markup=get_main_menu_keyboard(),
        )
    except Exception:
        await callback.message.answer(
            text=WELCOME_TEXT,
            reply_markup=get_main_menu_keyboard(),
        )
    await callback.answer()


# ===================== РАЗДЕЛ: ЗАПИСЬ НА КОНСУЛЬТАЦИЮ =====================

@dp.callback_query(F.data == "menu_consultation")
async def show_consultation(callback: CallbackQuery):
    text = (
        "<b>⚖️ Юридическая консультация Олеси Аблёзговой</b>\n\n"
        "Консультации проводит кандидат юридических наук, специалист по туристскому праву "
        "и спорам с авиаперевозчиками.\n\n"
        "<b>Форматы работы и стоимость:</b>\n\n"
        "1️⃣ <b>Письменный экспресс-разбор ситуации</b>\n"
        "• Анализ ваших авиабилетов, договоров с туроператором и переписки;\n"
        "• Правовой вывод: положена ли компенсация, каковы шансы в суде и сколько можно взыскать;\n"
        "• <i>Стоимость: от 3 000 ₽</i>\n\n"
        "2️⃣ <b>Индивидуальная онлайн-консультация (45–60 мин)</b>\n"
        "• Видео- или аудиосозвон с детальным аудитом всех документов;\n"
        "• Пошаговая персональная стратегия переговоров с компанией или обращения в суд;\n"
        "• Ответы на все сопутствующие вопросы;\n"
        "• <i>Стоимость: от 7 000 ₽</i>\n\n"
        "3️⃣ <b>Сопровождение «под ключ» / Досудебная претензия и иск</b>\n"
        "• Подготовка юридически безупречной претензии, жалоб в Роспотребнадзор и Росавиацию;\n"
        "• Судебное взыскание стоимости билетов, неустоек, штрафов и морального вреда;\n"
        "• <i>Стоимость: рассчитывается индивидуально</i>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ <b>ПРАВИЛА ОБРАЩЕНИЯ:</b>\n"
        "<i>Я ценю профессиональное время, поэтому индивидуальные разборы в личных сообщениях "
        "проводятся только на платной основе (все базовые памятки и статьи доступны бесплатно "
        "в канале @travel_advokat).</i>\n\n"
        "<b>Если указанная стоимость и формат вас устраивают:</b>\n"
        "Нажмите кнопку ниже и отправьте мне сообщение с краткой информацией:\n"
        "1. Что произошло (даты, авиакомпания или туроператор, суть проблемы);\n"
        "2. Какие документы уже есть на руках (билеты, отказ в возврате, чеки расходов).\n\n"
        "Жду ваше сообщение! 👇"
    )
    await callback.message.edit_text(text=text, reply_markup=get_consultation_keyboard())
    await callback.answer()


# ===================== РАЗДЕЛ: БЕСПЛАТНЫЕ МАТЕРИАЛЫ =====================

@dp.callback_query(F.data == "menu_free_materials")
async def show_free_materials(callback: CallbackQuery):
    text = (
        "<b>🎁 База знаний и бесплатные материалы</b>\n\n"
        "Здесь собраны ключевые памятки, чек-листы и энциклопедии из закрепленных "
        "сообщений канала <b>«Адвокат туриста»</b> (@travel_advokat).\n\n"
        "Нажмите на интересующую тему, чтобы открыть подробную статью:"
    )
    await callback.message.edit_text(text=text, reply_markup=get_free_materials_keyboard())
    await callback.answer()


# ===================== РАЗДЕЛ: ПОЛЕЗНЫЕ ГАЙДЫ =====================

@dp.callback_query(F.data == "menu_guides")
async def show_guides_catalog(callback: CallbackQuery):
    text = (
        "<b>📖 Каталог практических гайдов и инструкций</b>\n\n"
        "Каждый гайд — это выверенное юридическое руководство с готовыми образцами "
        "претензий, разбором судебных прецедентов и алгоритмами действий при форс-мажорах.\n\n"
        "Выберите интересующий гайд, чтобы прочитать краткое описание 👇"
    )
    await callback.message.edit_text(text=text, reply_markup=get_guides_catalog_keyboard())
    await callback.answer()


@dp.callback_query(F.data.startswith("guide_"))
async def show_single_guide(callback: CallbackQuery):
    guide_key = callback.data.replace("guide_", "")
    guide = config.GUIDES_DATA.get(guide_key)

    if not guide:
        await callback.answer("Гайд не найден", show_alert=True)
        return

    await callback.message.edit_text(
        text=guide["description"],
        reply_markup=get_single_guide_keyboard(guide_key),
    )
    await callback.answer()


# ===================== РАЗДЕЛ: ОБО МНЕ =====================

@dp.callback_query(F.data == "menu_about")
async def show_about(callback: CallbackQuery):
    text = (
        "<b>👩‍💼 Об авторе: Олеся Аблёзгова</b>\n\n"
        "• <b>Кандидат юридических наук</b>, соучредитель Правового агентства <b>«[RE]Акция»</b>;\n"
        "• Автор экспертного телеграм-канала <b>«Адвокат туриста»</b> (@travel_advokat);\n"
        "• Более 10 лет успешной практики в защите прав потребителей, туристов и авиапассажиров;\n"
        "• Регулярный спикер правовых СМИ и эксперт по спорам с авиакомпаниями и туроператорами;\n"
        "• Реальные судебные победы: взыскание сотен тысяч рублей компенсаций при отказах перевозчиков.\n\n"
        "Подписывайтесь на канал и изучайте судебную практику в закреплённых сообщениях!"
    )
    await callback.message.edit_text(text=text, reply_markup=get_about_keyboard())
    await callback.answer()


# ===================== ЗАПУСК БОТА =====================

async def main():
    logger.info("Запуск бота «Помощник Адвоката туриста»...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
