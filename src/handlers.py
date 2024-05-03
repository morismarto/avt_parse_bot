from concurrent.futures import ThreadPoolExecutor
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from src.scraper import Parser
import src.keyboards as kb
from aiogram import Router, F
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.city_list import cities
from functools import partial

router = Router()


class Choise(StatesGroup):
    find_proc = State()
    choise_city = State()


def format_response(arg) -> str:
    response: list[str] = Parser(query=arg).parse() 
    return ''.join(response)


cmd_start_text = 'Привет, я бот для парсинга цен на процессоры с Авито'
    
@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.delete()
    await message.answer(text=cmd_start_text, reply_markup=kb.start_kb)


@router.message(F.text == 'Найти процессоры')
async def find_processors(message: Message, state: FSMContext) -> None:
    await state.set_state(Choise.find_proc)
    await message.delete()
    await message.answer(text='Введите название процессора:')


@router.message(F.text == 'Выбрать город')
async def select_city(message: Message, state: FSMContext) -> None:
    await state.set_state(Choise.choise_city)
    await message.delete()
    await message.answer('Список доступных городов:', reply_markup=kb.cities_kb)


@router.message(Choise.find_proc)
async def get_prices(message: Message, state: FSMContext) -> None:
    await message.answer('Ищем процессоры по вашему запросу...')
    await state.update_data(proc=message.text)
    data = await state.get_data()
    
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        future: asyncio.Future[str] = loop.run_in_executor(pool, partial(format_response, data['proc']))
        await future
        await message.answer(future.result())

    await state.clear()


@router.callback_query(F.data)
async def select_city_handler(callback: CallbackQuery) -> None:
    await callback.answer(f'Вы выбрали {callback.data}', show_alert=True)
    inv_d = {value: key for key, value in cities.items()}
    selected_city = inv_d.get(callback.data)
    Parser.city = selected_city
    await callback.message.delete_reply_markup()


