from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from data.OT_messages import (
    HELP_MESSAGE, BEGIN_MESSAGE, LANGUAGE_MESSAGE,
    UNIVERSITY_MESSAGES, COURSES_MESSAGES, COURSES_MESSAGES_BEGIN,
    COURSES_MESSAGES_WHY, COURSES_CANCEL
    )
from data.OT_constants import (
    LANGUAGES_DICT, UNIVERSITIES_DICT, COURSES_FULL_DICT
    )
from data.OT_storage import SQLiteStorage
from keyboards import OT_builders, OT_inline, OT_reply
from callbacks.OT_procedures import *
from aiogram.fsm.context import FSMContext
from utils.states import Form

router = Router()

@router.message(F.text.lower().in_(["hi", "hello", "привет"]))
async def greetings(message: Message):
    await message.reply("Hello mate! (MENU->START OR type <</start>>)")

@router.message(Command(commands=["help"]))
async def help(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, HELP_MESSAGE[0])
        
# @router.message(CommandStart(), IsAdmin(1490170564))
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.BEGIN)
    await message.answer(BEGIN_MESSAGE.get("all"), 
                         reply_markup=OT_inline.begin_markup)
    
@router.callback_query(F.data == "begin", Form.BEGIN)
async def language_choise(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.LANGUAGE)
    await callback.message.answer(LANGUAGE_MESSAGE.get("all"), 
                                  reply_markup=OT_builders.language_reply(),
                                  disable_notification=True)  
    
@router.message(Form.LANGUAGE)
async def univerersity_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(LANGUAGE=get_dict_key_from_value(message.text, LANGUAGES_DICT))
    await state.set_state(Form.UNIVERSITY)
    data = await state.get_data()
    await message.answer(UNIVERSITY_MESSAGES.get(data["LANGUAGE"]), 
                         reply_markup=OT_builders.universities_reply(),
                         disable_notification=True)
    
@router.message(Form.UNIVERSITY)
async def course_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(UNIVERSITY=message.text)
    await state.set_state(Form.COURSE)
    data = await state.get_data()
    await message.answer(COURSES_MESSAGES.get(data["LANGUAGE"]), 
                         reply_markup=OT_builders.courses_reply(message.text),
                         disable_notification=True)
    
@router.message(Form.COURSE)
async def course_handler_begin(message: Message, state: FSMContext) -> None:
    await state.update_data(COURSE=message.text)
    data = await state.get_data()
    await message.answer(COURSES_MESSAGES_BEGIN.get(data["LANGUAGE"]), 
                         reply_markup=OT_inline.begin_course_markup)
    
@router.callback_query(F.data == "begin_course", Form.COURSE)
async def course_handler_begin_callback(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await callback.message.answer(COURSES_MESSAGES_WHY.get(data["LANGUAGE"]), reply_markup=ReplyKeyboardRemove())      
    
    full_university = UNIVERSITIES_DICT.get(data["UNIVERSITY"])
    full_course = COURSES_FULL_DICT.get(data["COURSE"])
    aprove_text = f"Ai aplicat la cursul <b><u>{full_course}</u></b>  universitatea <b><u>{full_university}</u></b> ?" 
    await callback.message.answer(aprove_text, reply_markup=OT_builders.bool_reply(data["LANGUAGE"]))      

    await state.set_state(Form.CHOICE)
    await state.update_data(CHOICE=callback.message.text)
    data = await state.get_data()
    
@router.message(Form.CHOICE)
async def course_handler_start(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if (message.text == "No/Nu") or (message.text == "No"):
        await message.answer("...", reply_markup=ReplyKeyboardRemove())      
        await message.answer(COURSES_CANCEL.get(data["LANGUAGE"]))
        await state.clear()
    else:
        conn = SQLiteStorage()._get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT mess_desc
                          FROM courses_mess c_mess
                          INNER JOIN courses ON courses.course_id = c_mess.course_id
                          WHERE courses.course_name = ?
                          AND c_mess.mess_lang = ?
                          AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 1))
        course_mess = cursor.fetchone()
        cursor.close()
        await message.answer(course_mess[0], reply_markup=OT_reply.ok_markup)
        await state.set_state(Form.CHOICE1)
        
@router.message(Form.CHOICE1)
async def course_handler_choice2(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 2))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)
    await state.set_state(Form.CHOICE2)

@router.message(Form.CHOICE2)
async def course_handler_choice3(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 3))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.show_markup)
    await state.set_state(Form.CHOICE3)
    
@router.message(Form.CHOICE3)
async def course_handler_choice4(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 4))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)
    await state.set_state(Form.CHOICE4)

@router.message(Form.CHOICE4)
async def course_handler_choice5(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 5))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE5)
    
@router.message(Form.CHOICE5)
async def course_handler_choice6(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 6))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE6)   
    
@router.message(Form.CHOICE6)
async def course_handler_choice7(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 7))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE7)  
    
@router.message(Form.CHOICE7)
async def course_handler_choice8(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 8))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE8)         
    
@router.message(Form.CHOICE8)
async def course_handler_choice9(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 9))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE9)    
    
@router.message(Form.CHOICE9)
async def course_handler_choice10(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 10))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE10)  
    
@router.message(Form.CHOICE10)
async def course_handler_choice11(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 11))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE11) 
    
@router.message(Form.CHOICE11)
async def course_handler_choice12(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 12))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE12)   
    
@router.message(Form.CHOICE12)
async def course_handler_choice13(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 13))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE13)  
    
@router.message(Form.CHOICE13)
async def course_handler_choice14(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 14))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE14) 
    
@router.message(Form.CHOICE14)
async def course_handler_choice15(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 15))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE15) 
    
@router.message(Form.CHOICE15)
async def course_handler_choice16(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 16))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE16)                      
    
@router.message(Form.CHOICE16)
async def course_handler_choice17(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 17))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE17)   
    
@router.message(Form.CHOICE17)
async def course_handler_choice18(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 18))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE18)              
    
@router.message(Form.CHOICE18)
async def course_handler_choice19(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 19))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE19)                  
    
@router.message(Form.CHOICE19)
async def course_handler_choice20(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 20))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE20)         
    
@router.message(Form.CHOICE20)
async def course_handler_choice21(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 21))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE21)      
    
@router.message(Form.CHOICE21)
async def course_handler_choice22(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 22))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE22)    
    
@router.message(Form.CHOICE22)
async def course_handler_choice23(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 23))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE23)
    
@router.message(Form.CHOICE23)
async def course_handler_choice24(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 24))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_builders.bool_reply(data["LANGUAGE"]))    
    await state.set_state(Form.CHOICE24)          
    
@router.message(Form.CHOICE24)
async def course_handler_choice25(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                        FROM courses_mess c_mess
                        INNER JOIN courses ON courses.course_id = c_mess.course_id
                        WHERE courses.course_name = ?
                        AND c_mess.mess_lang = ?
                        AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 25))
    course_mess = cursor.fetchall()
    cursor.close()
    
    if (message.text == "No/Nu") or (message.text == "No"):
        await message.answer(course_mess[1][0], reply_markup=OT_reply.next_markup)
    else:
        await message.answer(course_mess[0][0], reply_markup=OT_reply.next_markup)
        
    await state.set_state(Form.CHOICE25)
    
@router.message(Form.CHOICE25)
async def course_handler_choice26(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 26))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE26)   
    
@router.message(Form.CHOICE26)
async def course_handler_choice27(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 27))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE27)            

@router.message(Form.CHOICE27)
async def course_handler_choice28(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 28))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE28)       
    
@router.message(Form.CHOICE28)
async def course_handler_choice29(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 29))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE29) 
    
@router.message(Form.CHOICE29)
async def course_handler_choice30(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT mess_desc
                    FROM courses_mess c_mess
                    INNER JOIN courses ON courses.course_id = c_mess.course_id
                    WHERE courses.course_name = ?
                    AND c_mess.mess_lang = ?
                    AND c_mess.mess_step = ?""", (data["COURSE"], data["LANGUAGE"], 30))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(f"<b><u>{course_mess[0]}</u></b>", reply_markup=OT_reply.next_markup)    
    await state.set_state(Form.CHOICE30)                
    await state.clear()
    