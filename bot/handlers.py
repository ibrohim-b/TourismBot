from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy import select

from db.session import AsyncSessionLocal
from db.models import City, Excursion, Point
from bot.states import TripState
from bot.keyboards import simple_kb, start_excursion_kb, im_here_kb, next_kb, home_kb
from utils.logger import setup_logger

logger = setup_logger('bot_handlers')
router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    logger.info(f"User {msg.from_user.id} started bot")
    await msg.answer(
        "👋 Привет! Это телеграм бот: <b>ГИД В КАРМАНЕ</b>\n\n"
        "🎧 Аудиогид по локациям\n"
        "🗺 Маршрут на карте\n\n"
        "Меню → /instruction\n"
        "Выбрать экскурсию → /get_trips",
        parse_mode=ParseMode.HTML,
    )

@router.callback_query(F.data == "home")
async def go_home(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()
    await call.message.answer(
        "👋 Привет! Это телеграм бот: <b>ГИД В КАРМАНЕ</b>\n\n"
        "🎧 Аудиогид по локациям\n"
        "🗺 Маршрут на карте\n\n"
        "Меню → /instruction\n"
        "Выбрать экскурсию → /get_trips",
        parse_mode=ParseMode.HTML,
    )

@router.message(Command("instruction"))
async def instruction(msg: Message):
    await msg.answer(
        "📖 Вы выбираете экскурсию → следуете маршруту → слушаете аудиогид."
    )


@router.message(Command("get_trips"))
async def get_trips(msg: Message, state: FSMContext):
    try:
        logger.info(f"User {msg.from_user.id} requested trips")
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(City).where(City.excursions.any()))
            cities = result.scalars().all()
        
        logger.info(f"Found {len(cities)} cities")
        
        if not cities:
            await msg.answer("❌ Нет доступных городов. Добавьте города через админ панель.")
            return
        
        kb = simple_kb(
            [[InlineKeyboardButton(text=c.name, callback_data=f"city:{c.id}")] for c in cities]
            
        )
        await msg.answer("🌍 Выберите город:", reply_markup=kb)
        await state.set_state(TripState.city)
    except Exception as e:
        logger.error(f"Error in get_trips: {str(e)}")
        await msg.answer(f"Ошибка: {str(e)}")
        # raise e


@router.callback_query(F.data.startswith("city:"))
async def choose_city(call: CallbackQuery, state: FSMContext):
    city_id = int(call.data.split(":")[1])
    logger.info(f"User {call.from_user.id} selected city {city_id}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(city_id=city_id)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Excursion).where(Excursion.city_id == city_id).where(Excursion.points.any()))
        excursions = result.scalars().all()
        city = await session.execute(select(City).where(City.id == city_id))
        city = city.scalars().first()
        if city.image:
            await call.message.answer_photo(FSInputFile(city.image))
    
    await call.message.answer(f"✅ Выбрано: *{city.name}*", parse_mode="Markdown")

    kb = simple_kb(
        [[InlineKeyboardButton(text=e.title, callback_data=f"exc:{e.id}")]for e in excursions]
    )
    await call.message.answer("🎒 Выберите экскурсию:", reply_markup=kb)


@router.callback_query(F.data.startswith("exc:"))
async def excursion_info(call: CallbackQuery, state: FSMContext):
    exc_id = int(call.data.split(":")[1])
    logger.info(f"User {call.from_user.id} selected excursion {exc_id}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(excursion_id=exc_id, point_index=0)

    async with AsyncSessionLocal() as session:
        exc = await session.get(Excursion, exc_id)
        result = await session.execute(select(Point).where(Point.excursion_id == exc_id))
        points = result.scalars().all()
        
    await call.message.answer(f"✅ Выбрано: *{exc.title}*", parse_mode="Markdown")

    await call.message.answer(
        f"*{exc.title}*\n\n{exc.description}\n\n📍 Точек: {len(points)}",
        reply_markup=start_excursion_kb(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "start_trip")
async def start_trip(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.info(f"User {call.from_user.id} started excursion {data['excursion_id']}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await send_point(call, data["excursion_id"], 0)


async def send_point(call, exc_id, index):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Point)
            .where(Point.excursion_id == exc_id)
            .order_by(Point.order)
        )
        points = result.scalars().all()
        point = points[index]

    await call.message.answer_location(point.lat, point.lng)
    await call.message.answer(
        f"📍 *{point.title}*\n\nНажмите кнопку, когда будете на месте.",
        reply_markup=im_here_kb(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "im_here")
async def at_place(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idx = data["point_index"]
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Point)
            .where(Point.excursion_id == data["excursion_id"])
            .order_by(Point.order)
        )
        points = result.scalars().all()

    point = points[idx]

    if point.image:
        await call.message.answer_photo(FSInputFile(point.image))
    if point.audio:
        await call.message.answer_audio(FSInputFile(point.audio))

    await call.message.answer(point.text, reply_markup=next_kb())


@router.callback_query(F.data == "next")
async def next_point(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idx = data["point_index"] + 1
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)


    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Point).where(Point.excursion_id == data["excursion_id"])
        )
        points = result.scalars().all()

    if idx >= len(points):
        await call.message.answer("🎉 Экскурсия завершена!", reply_markup=home_kb())
        await state.clear()
        return

    await state.update_data(point_index=idx)
    await send_point(call, data["excursion_id"], idx)
