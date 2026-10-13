import os
from dotenv import load_dotenv

load_dotenv()

# ===================== ОСНОВНЫЕ НАСТРОЙКИ =====================
# Токен вашего бота из @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# Ваш числовой Telegram ID для уведомлений (узнать в @userinfobot)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Ваш личный никнейм в Telegram для связи (без @)
LAWYER_USERNAME = os.getenv("LAWYER_USERNAME", "travel_advokat")

# Ссылки на канал и сайт компании
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/travel_advokat")
REVIEWS_URL = os.getenv("REVIEWS_URL", "https://t.me/travel_advokat")
COMPANY_SITE_URL = os.getenv("COMPANY_SITE_URL", "https://zakon.ru/olesya64")  # Ссылка на сайт агентства [RE]Акция

# ===================== ССЫЛКИ НА БЕСПЛАТНЫЕ МАТЕРИАЛЫ =====================
# Ссылки на закрепленные посты в Telegram-канале @travel_advokat
FREE_MATERIALS_LINKS = {
    "avia_collapse": os.getenv("LINK_AVIA_COLLAPSE", "https://t.me/travel_advokat"),
    "passengers_memo": os.getenv("LINK_PASSENGERS_MEMO", "https://t.me/travel_advokat"),
    "passport_encyclopedia": os.getenv("LINK_PASSPORT", "https://t.me/travel_advokat"),
    "customs_encyclopedia": os.getenv("LINK_CUSTOMS", "https://t.me/travel_advokat"),
    "thai_encyclopedia": os.getenv("LINK_THAI_ENCYCLOPEDIA", "https://t.me/travel_advokat"),
    "claim_damages": os.getenv("LINK_CLAIM_DAMAGES", "https://t.me/travel_advokat"),
    "tour_cancellation": os.getenv("LINK_TOUR_CANCEL", "https://t.me/travel_advokat"),
    "emergency_situations": os.getenv("LINK_EMERGENCY", "https://t.me/travel_advokat"),
}

# ===================== ССЫЛКИ НА ПОЛЕЗНЫЕ ГАЙДЫ =====================
# Заглушки на оплату в Tribute и страницы подробного описания на сайте [RE]Акция
GUIDES_DATA = {
    "flight_delay_kover": {
        "title": "✈️ Задержка рейса из-за плана «Ковёр»",
        "description": (
            "<b>✈️ Гайд: Задержка рейса из-за плана «Ковёр» и БПЛА</b>\n\n"
            "Авиакомпании списывают всё на форс-мажор, но закон обязывает их возмещать убытки! "
            "Разбираем, как получить положенное прямо в аэропорту и взыскать расходы.\n\n"
            "<b>Что внутри:</b>\n"
            "• Пошаговый алгоритм: что требовать через 2, 4 и 8 часов ожидания;\n"
            "• Инструкция по фиксации доказательств на табло аэропорта;\n"
            "• Список убытков к возмещению (отели, такси, питание);\n"
            "• Готовый шаблон досудебной претензии к авиакомпании."
        ),
        "buy_url": os.getenv("BUY_URL_FLIGHT_DELAY", "https://tribute.tg/"),
        "info_url": os.getenv("INFO_URL_FLIGHT_DELAY", "https://zakon.ru/olesya64"),
    },
    "flight_cancel_kover": {
        "title": "🚫 Отмена рейса из-за плана «Ковёр»",
        "description": (
            "<b>🚫 Гайд: Отмена рейса из-за закрытия неба и плана «Ковёр»</b>\n\n"
            "Если рейс отменили полностью, вы имеете право на 100% возврат стоимости даже «невозвратных» "
            "билетов, а также компенсацию сопутствующих потерь.\n\n"
            "<b>Что внутри:</b>\n"
            "• Как оформить вынужденный возврат без штрафов и комиссий;\n"
            "• Прецедент взыскания 868 000 ₽ при удержании 279 000 ₽;\n"
            "• Что делать со стыковочными рейсами разных авиакомпаний;\n"
            "• Шаблон заявления на полный возврат и досудебной претензии."
        ),
        "buy_url": os.getenv("BUY_URL_FLIGHT_CANCEL", "https://tribute.tg/"),
        "info_url": os.getenv("INFO_URL_FLIGHT_CANCEL", "https://zakon.ru/olesya64"),
    },
    "tour_cancel_kover": {
        "title": "🏝 Отмена тура из-за плана «Ковёр»",
        "description": (
            "<b>🏝 Гайд: Отмена тура из-за форс-мажора и плана «Ковёр»</b>\n\n"
            "Туроператор заявляет о фактически понесенных расходах (ФПР) и удерживает 80–100% стоимости тура? "
            "Это незаконно, если расходы документально не подтверждены!\n\n"
            "<b>Что внутри:</b>\n"
            "• Как оспорить удержания и «фактические расходы» туроператора;\n"
            "• Разделение ответственности турагента и туроператора;\n"
            "• Алгоритм возврата денег в досудебном порядке;\n"
            "• Шаблон претензии к туроператору с правовым обоснованием."
        ),
        "buy_url": os.getenv("BUY_URL_TOUR_CANCEL", "https://tribute.tg/"),
        "info_url": os.getenv("INFO_URL_TOUR_CANCEL", "https://zakon.ru/olesya64"),
    },
    "tour_delay_kover": {
        "title": "⏳ Задержка тура из-за плана «Ковёр»",
        "description": (
            "<b>⏳ Гайд: Задержка начала тура и потеря дней отдыха</b>\n\n"
            "Если из-за задержки вылета вы потеряли 1–2 дня оплаченного отеля и экскурсий, "
            "вы вправе требовать соразмерного уменьшения цены тура.\n\n"
            "<b>Что внутри:</b>\n"
            "• Расчет стоимости потерянных суток проживания и питания;\n"
            "• Как зафиксировать время заселения в отель;\n"
            "• Взыскание неустойки по Закону о защите прав потребителей;\n"
            "• Образец претензии туроператору за сокращение срока отдыха."
        ),
        "buy_url": os.getenv("BUY_URL_TOUR_DELAY", "https://tribute.tg/"),
        "info_url": os.getenv("INFO_URL_TOUR_DELAY", "https://zakon.ru/olesya64"),
    },
    "thailand_guide": {
        "title": "🇹🇭 Гайд по Таиланду (Правила и безопасность)",
        "description": (
            "<b>🇹🇭 Практический юридический гайд по Таиланду</b>\n\n"
            "Всё, что нужно знать туристу и зимовщику, чтобы избежать депортации, "
            "штрафов и проблем с тайской полицией и миграционной службой.\n\n"
            "<b>Что внутри:</b>\n"
            "• Сроки безвиза, бордер-раны, продления виз и оверстей;\n"
            "• Аренда байков и авто: права, страховки, частые схемы развода;\n"
            "• Ввоз лекарств, вейпов, дронов и таможенные ограничения;\n"
            "• Действия при ДТП и контакты проверенных русскоязычных юристов."
        ),
        "buy_url": os.getenv("BUY_URL_THAILAND", "https://tribute.tg/"),
        "info_url": os.getenv("INFO_URL_THAILAND", "https://zakon.ru/olesya64"),
    },
    "locations_guide": {
        "title": "📍 Авторский гайд по топовым локациям",
        "description": (
            "<b>📍 Секретные и проверенные локации от путешественника</b>\n\n"
            "Лучшие пляжи, видовые рестораны, чилл-зоны и фотогеничные места без толп туристов, "
            "с проверенными маршрутами и точными координатами.\n\n"
            "<b>Что внутри:</b>\n"
            "• Метки на Google Maps с подробными комментариями;\n"
            "• Лайфхаки по депозитам в beach club и времени посещения;\n"
            "• Советы, как сэкономить на трансфере и билетах."
        ),
        "buy_url": os.getenv("BUY_URL_LOCATIONS", "https://tribute.tg/"),
        "info_url": os.getenv("INFO_URL_LOCATIONS", "https://zakon.ru/olesya64"),
    },
}
