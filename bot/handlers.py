import base64
import traceback
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy import select

from db.session import AsyncSessionLocal
from db.models import City, Excursion, Point
from bot.states import TripState
from bot.keyboards import simple_kb, start_excursion_kb, im_here_kb, next_kb, home_kb
from utils.logger import setup_logger

logger = setup_logger('bot_handlers')
router = Router()


def fmt_error(e: Exception) -> str:
    trace = traceback.format_exc()
    encoded = base64.b64encode(trace.encode()).decode()
    return f"An error occurred. Forward this message to the bot owner (contact info in description):\n<code>{encoded}</code>"

BASE_DIR = Path(__file__).resolve().parent.parent


PHOTO_SIZE_LIMIT = 10 * 1024 * 1024  # 10MB


def media_file(path: str):
    full = BASE_DIR / path
    if full.exists():
        return FSInputFile(full)
    logger.warning(f"Media file not found: {full}")
    return None


def is_large(path: str) -> bool:
    return (BASE_DIR / path).stat().st_size > PHOTO_SIZE_LIMIT


@router.message(Command("start"))
async def start(msg: Message):
    logger.info(f"User {msg.from_user.id} started bot")
    await msg.answer(
        "👋 Hello! This is a Telegram bot: <b>GUIDE IN YOUR POCKET</b>\n\n"
        "🎧 Audio guide for locations\n"
        "🗺 Route on the map\n\n"
        "Menu → /instruction\n"
        "Choose a tour → /get_trips",
        parse_mode=ParseMode.HTML,
    )

@router.callback_query(F.data == "home")
async def go_home(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()
    await call.message.answer(
        "👋 Hello! This is a Telegram bot: <b>GUIDE IN YOUR POCKET</b>\n\n"
        "🎧 Audio guide for locations\n"
        "🗺 Route on the map\n\n"
        "Menu → /instruction\n"
        "Choose a tour → /get_trips",
        parse_mode=ParseMode.HTML,
    )

@router.message(Command("instruction"))
async def instruction(msg: Message):
    await msg.answer(
        "📖 You choose a tour → follow the route → listen to the audio guide."
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
            await msg.answer("❌ No cities available. Add cities via the admin panel.")
            return
        
        kb = simple_kb(
            [[InlineKeyboardButton(text=c.name, callback_data=f"city:{c.id}")] for c in cities]
            
        )
        await msg.answer("🌍 Select a city:", reply_markup=kb)
        await state.set_state(TripState.city)
    except Exception as e:
        logger.error("Error in get_trips", exc_info=True)
        await msg.answer(fmt_error(e), parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("city:"))
async def choose_city(call: CallbackQuery, state: FSMContext):
    city_id = int(call.data.split(":")[1])
    logger.info(f"User {call.from_user.id} selected city {city_id}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(city_id=city_id)
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Excursion).where(Excursion.city_id == city_id).where(Excursion.points.any()))
            excursions = result.scalars().all()
            city = await session.execute(select(City).where(City.id == city_id))
            city = city.scalars().first()
            if city.image:
                f = media_file(city.image)
                if f:
                    if is_large(city.image):
                        await call.message.answer_document(f)
                    else:
                        await call.message.answer_photo(f)

        await call.message.answer(f"✅ Selected: *{city.name}*", parse_mode="Markdown")

        kb = simple_kb(
            [[InlineKeyboardButton(text=e.title, callback_data=f"exc:{e.id}")] for e in excursions]
        )
        await call.message.answer("🎒 Choose a tour:", reply_markup=kb)
    except Exception as e:
        logger.error(f"Error in choose_city for city_id={city_id}", exc_info=True)
        await call.message.answer(fmt_error(e), parse_mode=ParseMode.HTML)


@router.callback_query(F.data.startswith("exc:"))
async def excursion_info(call: CallbackQuery, state: FSMContext):
    exc_id = int(call.data.split(":")[1])
    logger.info(f"User {call.from_user.id} selected excursion {exc_id}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(excursion_id=exc_id, point_index=0)
    try:
        async with AsyncSessionLocal() as session:
            exc = await session.get(Excursion, exc_id)
            result = await session.execute(select(Point).where(Point.excursion_id == exc_id))
            points = result.scalars().all()

        await call.message.answer(f"✅ Selected: *{exc.title}*", parse_mode="Markdown")

        for img_path in [exc.image] if exc.image else []:
            f = media_file(img_path)
            if f:
                if is_large(img_path):
                    await call.message.answer_document(f)
                else:
                    await call.message.answer_photo(f)
        if exc.video and (f := media_file(exc.video)):
            await call.message.answer_video(f)

        await call.message.answer(
            f"*{exc.title}*\n\n{exc.description}\n\n📍 Points: {len(points)}",
            reply_markup=start_excursion_kb(),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Error in excursion_info for exc_id={exc_id}", exc_info=True)
        await call.message.answer(fmt_error(e), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "start_trip")
async def start_trip(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.info(f"User {call.from_user.id} started excursion {data['excursion_id']}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    try:
        await send_point(call, data["excursion_id"], 0)
    except Exception as e:
        logger.error(f"Error in start_trip for excursion_id={data['excursion_id']}", exc_info=True)
        await call.message.answer(fmt_error(e), parse_mode=ParseMode.HTML)


async def send_point(call, exc_id, index):
    logger.debug(f"send_point exc_id={exc_id} index={index}")
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Point)
            .where(Point.excursion_id == exc_id)
            .order_by(Point.order)
        )
        points = result.scalars().all()

    if index >= len(points):
        logger.warning(f"send_point: index {index} out of range (total={len(points)}) for exc_id={exc_id}")
        raise IndexError(f"Point index {index} out of range")

    point = points[index]
    logger.debug(f"Sending point '{point.title}' (id={point.id})")

    if point.lat and point.lng:
        await call.message.answer_location(point.lat, point.lng)
    await call.message.answer(
        f"📍 *{point.title}*\n\nPress the button when you arrive at the location.",
        reply_markup=im_here_kb(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "im_here")
async def at_place(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idx = data["point_index"]
    logger.info(f"User {call.from_user.id} arrived at point index={idx} excursion={data['excursion_id']}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Point)
                .where(Point.excursion_id == data["excursion_id"])
                .order_by(Point.order)
            )
            points = result.scalars().all()

        point = points[idx]
        logger.debug(f"Delivering content for point '{point.title}' (id={point.id})")

        if point.image and (f := media_file(point.image)):
            if is_large(point.image):
                await call.message.answer_document(f)
            else:
                await call.message.answer_photo(f)
        if point.video and (f := media_file(point.video)):
            await call.message.answer_video(f)
        if point.audio and (f := media_file(point.audio)):
            await call.message.answer_audio(f)

        await call.message.answer(point.text, reply_markup=next_kb())
    except Exception as e:
        logger.error(f"Error in at_place idx={idx}", exc_info=True)
        await call.message.answer(fmt_error(e), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "next")
async def next_point(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idx = data["point_index"] + 1
    logger.info(f"User {call.from_user.id} advancing to point index={idx} excursion={data['excursion_id']}")
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Point).where(Point.excursion_id == data["excursion_id"])
            )
            points = result.scalars().all()

        if idx >= len(points):
            logger.info(f"Excursion {data['excursion_id']} completed by user {call.from_user.id}")
            await call.message.answer("🎉 Tour completed!", reply_markup=home_kb())
            await state.clear()
            return

        await state.update_data(point_index=idx)
        await send_point(call, data["excursion_id"], idx)
    except Exception as e:
        logger.error(f"Error in next_point idx={idx}", exc_info=True)
        await call.message.answer(fmt_error(e), parse_mode=ParseMode.HTML)
