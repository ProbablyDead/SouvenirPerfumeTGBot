from aiogram import F, types
from aiogram.filters import Command

from poll import router, start_test, reply_keyboard, database

from payment import Payment

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Приветствуем тебя в нашем замечательном боте!", reply_markup=reply_keyboard())


@router.message(F.text.lower() == "пройти тест")
async def start_poll(message: types.Message):
    await start_test(message)


@router.message(F.text.lower() == "заказать аромат") 
async def get_contacts(message: types.Message):
    if not database.get_db_pass_count(message.from_user.id):
        await message.answer("Для начала нужно пройти тест!", reply_markup=reply_keyboard())
        return

    payment = Payment()

    async def callback(succeed: bool):
        if succeed:
            database.add_db_payment(message.from_user.id)
            await message.answer("Спасибо за покупку!\nДля согласования доставки свяжись, пожалуйста, с ответственным за заказы: @souvenir_perfume_order")
        else:
            await message.answer("*К сожалению оплата не прошла.*\n\nЕсли возникла ошибка, напиши, пожалуйста, нашему техническому специалисту: @wrkngYkz", parse_mode="Markdown")

    await message.answer(f"Конечно! Вот ссылка для оплаты:\n\n{payment.create_payment(callback, message.from_user.username)},\n\nПосле оплаты ты можешь связаться с ответственным за заказы: @souvenir_perfume_order и договориться о способе получения _(самовывоз метро Таганская, Москва и доставка по России)_, а так же обговорить интересующие тебя вопросы и пожелания касательно аромата\n\n_Срок изготовления 2-5 дней_",
                        reply_markup=reply_keyboard(), parse_mode="Markdown")

