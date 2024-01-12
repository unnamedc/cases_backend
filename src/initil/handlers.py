from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
from aiogram import F, Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
import time
from postsql import examination, new_user, paiding, inventory_case, id_to_name, id_to_price, new_skin
from random_skin import random_skin_one

from aiocryptopay import AioCryptoPay, Networks
crypto = AioCryptoPay(token='121732:AAAVWKHbeZT0XhxuVyJxLV3mx1wPEV9MAwU', network=Networks.MAIN_NET)

expires_in = 600 #срок действия чека в секундах

photo = "https://vkplay.ru/hotbox/content_files/article/2021/06/15/d503b7f588d6468b82b7abe2e16dc2b0.jpg"
photo2 = "https://s32677.pcdn.co/wp-content/uploads/2023/09/best-crypto-telegram-group-cover-850x478-1.jpg.optimal.jpg.optimal.jpg"
router = Router()

exit_money = InlineKeyboardBuilder()
exit_money.add(types.InlineKeyboardButton(text="отменить", callback_data="replenishment"))

class Gen(StatesGroup):
    popolnenie = State()

@router.callback_query(F.data == "start")
@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    if examination(msg.from_user.id) == None:
        new_user(msg.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Кейсы", web_app=WebAppInfo(url='https://743d-178-214-248-19.ngrok-free.app')))
    builder.row(types.InlineKeyboardButton(text="💳 Пополнить", callback_data="replenishment"))
    builder.row(types.InlineKeyboardButton(text="Открыть кейс!", callback_data="open"))
    builder.row(types.InlineKeyboardButton(text="Инвентарь", callback_data="inventory"))
    await msg.answer_photo(photo, caption=f"Привет! Твой ID: `{msg.from_user.id}`, Баланс: `{examination(msg.from_user.id)}`. Открывай кейсы и получай самое лучшее", reply_markup=builder.as_markup(), parse_mode="MARKDOWN")

@router.callback_query(F.data == "replenishment")
async def popolnenie(clbck: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="TONCOIN", callback_data="TON"))
    builder.row(
        InlineKeyboardButton(text="ETHEREUM", callback_data="ETH"))
    builder.row(
        InlineKeyboardButton(text="LITECOIN", callback_data="LTC"))
    await clbck.message.answer_photo(photo2, 'Пополнение через криптовалюту, актуальный курс для пополнения.\n\n1000 GEMS = ' + str(round(float(await crypto.get_amount_by_fiat(summ=1000, asset='TON', target='RUB')), 5)) + 'TON' +
                               '\n1000 GEMS = ' + str(round(float(await crypto.get_amount_by_fiat(summ=1000, asset='ETH', target='RUB')), 5)) + 'ETH' +
                               '\n1000 GEMS = ' + str(round(float(await crypto.get_amount_by_fiat(summ=1000, asset='LTC', target='RUB')), 5)) + 'LTC', reply_markup=builder.as_markup())
    await clbck.message.delete()

@router.callback_query(F.data == "TON")
@router.callback_query(F.data == "ETH")
@router.callback_query(F.data == "LTC")
async def kolichestvo(clbck: types.CallbackQuery, state: FSMContext):
    await state.update_data(valuta_monet = clbck.data)
    await clbck.message.answer("Введите количество пополняемой GEMS, в целых числах.")
    await clbck.message.delete()
    await state.set_state(Gen.popolnenie)


@router.message(Gen.popolnenie)
async def obmen_valut(msg: types.Message, state: FSMContext):
    if 0 < int(msg.text) < 10000:
        user_data = await state.get_data()
        amount = await crypto.get_amount_by_fiat(summ=float(msg.text), asset=user_data['valuta_monet'], target='RUB') #перевод в рубли
        invoice = await crypto.create_invoice(asset=user_data['valuta_monet'], amount=amount, expires_in=expires_in)
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Пополнить", url=invoice.pay_url))
        builder.row(InlineKeyboardButton(text="Проверить оплату", callback_data="status"))
        await state.update_data(pay = invoice, time_1 = int(time.time()), gems = int(msg.text))
        await msg.answer(text='Чек на сумму пополнения на ' + str(msg.text) + f' GEMS. `Срок действия чека 10 минут:`\n', reply_markup=builder.as_markup(), parse_mode="MARKDOWN")
    else:
        await msg.answer('Ошибка. Нужно ввести количество. Максимальная сумма для пополения 9999 GEMS', reply_markup=exit_money.as_markup())


@router.callback_query(F.data == "status")
async def curs(clbck: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if int(time.time()) - user_data['time_1'] < expires_in:
        invoices = await crypto.get_invoices(invoice_ids=user_data['pay'].invoice_id)
        if invoices.status == 'paid':
            await clbck.message.answer('Ваш баланс успешно пополнен /start')
            paiding(user_data['gems'] + examination(str(clbck.message.chat.id)), clbck.message.chat.id)
            await state.clear()
        else:
            await clbck.message.answer('Пополнения не было /start')
    else:
        await clbck.message.answer('Срок действия чека истек /start')
        await state.clear()

@router.callback_query(F.data == "open")
async def open_case(clbck: types.CallbackQuery):
    chat_id = clbck.message.chat.id
    open_balance = examination(chat_id) - 10
    if open_balance >= 0:
        paiding(open_balance, chat_id)
        number_skin = random_skin_one()
        await clbck.message.answer('Вы выиграли ' + str(id_to_name(number_skin)) + ' ' + str(id_to_price(number_skin)))
        new_skin(chat_id, number_skin)
    else:
        await clbck.message.answer('У вас недостатоно баланса')

@router.callback_query(F.data == "inventory")
async def inventory(clbck: types.CallbackQuery):
    invet_message = ''
    invent = inventory_case(clbck.message.chat.id)
    print(invent)
    for i in range(len(invent)):
        invet_message += str(id_to_name(invent[i])) + '\n'
    await clbck.message.answer('Ваш инвентарь: \n' + invet_message)
