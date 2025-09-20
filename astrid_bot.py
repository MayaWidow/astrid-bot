import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === ДАННЫЕ ТОВАРОВ ===
PRODUCTS = [
    {
        "name": "Твидовый жакет Chanel",
        "price": "800 000 ₽",
        "image_url": "https://i.ibb.co/cKB2D4jq/chanel.jpg",
        "gender": "Женская одежда",
        "type": "Платья",
        "brand": "Chanel"
    },
    {
        "name": "Рубашка поло Ralph Lauren",
        "price": "15 000 ₽",
        "image_url": "https://i.ibb.co/Dgf640zG/Polo-Ralph-Lauren.jpg",
        "gender": "Мужская одежда",
        "type": "Рубашки/Поло",
        "brand": "Polo Ralph Lauren"
    },
    {
        "name": "Туфли Jimmy Choo",
        "price": "130 000 ₽",
        "image_url": "https://i.ibb.co/WpF7M4Rk/Jimmy-Choo.jpg",
        "gender": "Женская одежда",
        "type": "Обувь",
        "brand": "Jimmy Choo"
    },
    {
        "name": "Платье Dolce & Gabbana",
        "price": "150 000 ₽",
        "image_url": "https://i.ibb.co/LzqkFMTq/dolce-gabbana.jpg",
        "gender": "Женская одежда",
        "type": "Платья",
        "brand": "Dolce & Gabbana"
    },
    {
        "name": "Лоферы Horsebit от Gucci",
        "price": "66 000 ₽",
        "image_url": "https://i.ibb.co/S4ntRfSc/GUCCI.jpg",
        "gender": "Мужская одежда",
        "type": "Обувь",
        "brand": "Gucci"
    },
    {
        "name": "Свитер Hermes",
        "price": "110 000 ₽",
        "image_url": "https://i.ibb.co/GQp60bxR/Hermes.jpg",
        "gender": "Мужская одежда",
        "type": "Толстовка/худи/свитер",
        "brand": "Hermes"
    },
    {
        "name": "Пуховик Prada re-nylon",
        "price": "110 000 ₽",
        "image_url": "https://i.ibb.co/1tSnsFSb/prada-re-nylon.jpg",
        "gender": "Женская одежда",
        "type": "Верхняя одежда",
        "brand": "Prada"
    },
    {
        "name": "Шарф Burberry",
        "price": "65 000 ₽",
        "image_url": "https://i.ibb.co/qFhR20Xd/Burberry.jpg",
        "gender": "Мужская одежда",
        "type": "Аксессуары",
        "brand": "Burberry"
    },
    {
        "name": "Куртка Fendi",
        "price": "200 000 ₽",
        "image_url": "https://i.ibb.co/Qv5SqzP9/Fendi.jpg",
        "gender": "Женская одежда",
        "type": "Верхняя одежда",
        "brand": "Fendi"
    },
    {
        "name": "Платье Givenchy",
        "price": "500 000 ₽",
        "image_url": "https://i.ibb.co/Q1WbzRR/Givenchy.jpg",
        "gender": "Женская одежда",
        "type": "Платья",
        "brand": "Givenchy"
    },
    {
        "name": "Туфли Versace",
        "price": "115 000 ₽",
        "image_url": "https://i.ibb.co/LDXjtw5q/Versace.jpg",
        "gender": "Женская одежда",
        "type": "Обувь",
        "brand": "Versace"
    },
    {
        "name": "Худи Balenciaga",
        "price": "150 000 ₽",
        "image_url": "https://i.ibb.co/KpNJfrgn/Balenciaga.jpg",
        "gender": "Мужская одежда",
        "type": "Толстовка/худи/свитер",
        "brand": "Balenciaga"
    },
    {
        "name": "Кожанка Yves Saint Laurent",
        "price": "780 000 ₽",
        "image_url": "https://i.ibb.co/SwXhscL4/Yves-Saint-Laurent.jpg",
        "gender": "Женская одежда",
        "type": "Верхняя одежда",
        "brand": "Yves Saint Laurent"
    },
    {
        "name": "Туфли Christian Louboutin",
        "price": "110 000 ₽",
        "image_url": "https://i.ibb.co/zTmQKt8M/Christian-Louboutin.jpg",
        "gender": "Женская одежда",
        "type": "Обувь",
        "brand": "Christian Louboutin"
    },
    {
        "name": "Кроссовки Christian Louboutin",
        "price": "100 000 ₽",
        "image_url": "https://i.ibb.co/HL2DY0Nt/Christian-Louboutin.jpg",
        "gender": "Мужская одежда",
        "type": "Обувь",
        "brand": "Christian Louboutin"
    },
    {
        "name": "Туфли Cesare Paciotti",
        "price": "150 000 ₽",
        "image_url": "https://i.ibb.co/PGCDC83Q/Cesare-Paciotti.jpg",
        "gender": "Женская одежда",
        "type": "Обувь",
        "brand": "Cesare Paciotti"
    },
    {
        "name": "Рубашка поло Lacoste",
        "price": "10 000 ₽",
        "image_url": "https://i.ibb.co/ccQQC7nt/Lacoste.jpg",
        "gender": "Мужская одежда",
        "type": "Рубашки/Поло",
        "brand": "Lacoste"
    },
    {
        "name": "Платье Valentino",
        "price": "300 000 ₽",
        "image_url": "https://i.ibb.co/whwWqx2Y/Valentino.jpg",
        "gender": "Женская одежда",
        "type": "Платья",
        "brand": "Valentino"
    },
    {
        "name": "Платье Nina Ricci",
        "price": "180 000 ₽",
        "image_url": "https://i.ibb.co/Hfq88qcQ/Nina-Ricci.jpg",
        "gender": "Женская одежда",
        "type": "Платья",
        "brand": "Nina Ricci"
    },
    {
        "name": "Туфли Mach & Mach",
        "price": "149 000 ₽",
        "image_url": "https://i.ibb.co/6cV61wmH/Mach-Mach.jpg",
        "gender": "Женская одежда",
        "type": "Обувь",
        "brand": "Mach & Mach"
    }
]

# === СТРУКТУРА КАТЕГОРИЙ ===
MEN_CATEGORIES = [
    "Футболки", "Майки", "Рубашки/Поло", "Джинсы", "Брюки",
    "Толстовка/худи/свитер", "Верхняя одежда", "Обувь", "Аксессуары"
]

WOMEN_CATEGORIES = [
    "Платья", "Блузки/Рубашки", "Кроп-топы/Майки", "Толстовки/Худи",
    "Лонгсливы", "Верхняя одежда", "Юбки", "Джинсы/Брюки", "Обувь"
]

BRANDS = sorted(set(p["brand"] for p in PRODUCTS))  # Уникальные бренды

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
async def send_product(update: Update, context: ContextTypes.DEFAULT_TYPE, product: dict):
    """Отправляет информацию о товаре."""
    caption = f"<b>{product['name']}</b>\n\n💰 Цена: {product['price']}\n🏷️ Бренд: {product['brand']}"
    keyboard = [[InlineKeyboardButton("⬅️ Назад к результатам", callback_data="back_to_results")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_photo(
            chat_id=update.callback_query.message.chat_id,
            photo=product["image_url"],
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке фото: {e}")
        await update.callback_query.message.reply_text(
            f"📷 Фото временно недоступно.\n\n{caption}",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

async def show_no_products_found(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сообщение, если товары не найдены."""
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        text="Товары не найдены 😕",
        reply_markup=reply_markup
    )

async def display_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE, products: list):
    """Отображает список товаров в виде кнопок."""
    keyboard = [
        [InlineKeyboardButton(p["name"], callback_data=f"product_{i}")]
        for i, p in enumerate(products)
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        text=f"📦 Найдено товаров: {len(products)}\nВыберите товар для просмотра:",
        reply_markup=reply_markup
    )

async def display_search_results_as_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE, products: list):
    """Отображает список товаров в виде кнопок в НОВОМ сообщении."""
    keyboard = [
        [InlineKeyboardButton(p["name"], callback_data=f"product_{i}")]
        for i, p in enumerate(products)
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(
        text=f"📦 Найдено товаров: {len(products)}\nВыберите товар для просмотра:",
        reply_markup=reply_markup
    )

# === ОСНОВНОЕ МЕНЮ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🟢 Получена команда /start от пользователя:", update.message.from_user.id)
    keyboard = [
        [InlineKeyboardButton("👕 Мужская одежда", callback_data="men")],
        [InlineKeyboardButton("👗 Женская одежда", callback_data="women")],
        [InlineKeyboardButton("🏷️ Бренды", callback_data="brands")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌟 Добро пожаловать в <b>Astrid</b>!\nВыберите категорию:", reply_markup=reply_markup, parse_mode="HTML")

# === ОБРАБОТЧИК КНОПОК ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "men":
        keyboard = [[InlineKeyboardButton(cat, callback_data=f"men_{cat}")] for cat in MEN_CATEGORIES]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="👔 Выберите тип мужской одежды:", reply_markup=reply_markup)

    elif data == "women":
        keyboard = [[InlineKeyboardButton(cat, callback_data=f"women_{cat}")] for cat in WOMEN_CATEGORIES]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="👗 Выберите тип женской одежды:", reply_markup=reply_markup)

    elif data == "brands":
        keyboard = [[InlineKeyboardButton(brand, callback_data=f"brand_{brand}")] for brand in BRANDS]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="🏷️ Выберите бренд:", reply_markup=reply_markup)

    elif data == "main":
        keyboard = [
            [InlineKeyboardButton("👕 Мужская одежда", callback_data="men")],
            [InlineKeyboardButton("👗 Женская одежда", callback_data="women")],
            [InlineKeyboardButton("🏷️ Бренды", callback_data="brands")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="🌟 Добро пожаловать в <b>Astrid</b>!\nВыберите категорию:", reply_markup=reply_markup, parse_mode="HTML")

    elif data.startswith("men_"):
        category = data[4:]  # "men_Футболки" → "Футболки"
        await show_products(update, context, "Мужская одежда", category=category)

    elif data.startswith("women_"):
        category = data[6:]  # "women_Платья" → "Платья"
        await show_products(update, context, "Женская одежда", category=category)

    elif data.startswith("brand_"):
        brand = data[6:]  # "brand_Chanel" → "Chanel"
        await show_products(update, context, brand=brand)

    elif data.startswith("product_"):
        index = int(data.split("_")[1])
        products = context.user_data.get('last_search_results', [])
        if 0 <= index < len(products):
            product = products[index]
            await send_product(update, context, product)
        else:
            await query.answer("Товар не найден.", show_alert=True)

    elif data == "back_to_results":
        products = context.user_data.get('last_search_results', [])
        if products:
            await display_search_results_as_new_message(update, context, products)
        else:
            await query.answer("Нет предыдущих результатов.", show_alert=True)
            await query.message.reply_text(
                text="🌟 Добро пожаловать в <b>Astrid</b>!\nВыберите категорию:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👕 Мужская одежда", callback_data="men")],
                    [InlineKeyboardButton("👗 Женская одежда", callback_data="women")],
                    [InlineKeyboardButton("🏷️ Бренды", callback_data="brands")]
                ]),
                parse_mode="HTML"
            )

# === ПОКАЗАТЬ ТОВАРЫ ===
async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE, gender: str = None, category: str = None, brand: str = None):
    """Показывает товары по фильтрам."""
    products = PRODUCTS

    if gender:
        products = [p for p in products if p["gender"] == gender]
    if category:
        products = [p for p in products if p["type"] == category]
    if brand:
        products = [p for p in products if p["brand"] == brand]

    if not products:
        await show_no_products_found(update, context)
        return

    # Сохраняем результаты для кнопки "Назад к результатам"
    context.user_data['last_search_results'] = products

    await display_search_results(update, context, products)

# === ЗАПУСК БОТА ===
def main():
    print("🔧 Запуск бота...")
    TOKEN = "8294975968:AAEn2if-Cast6nrEhzYildWwWqB6H2BQ1HA"

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    logger.info("🚀 Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
