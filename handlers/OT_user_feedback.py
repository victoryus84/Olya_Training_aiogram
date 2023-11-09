from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, user
from aiogram.filters import StateFilter
from data.OT_storage import SQLiteStorage
from keyboards import OT_builders, OT_inline, OT_reply
from callbacks.OT_procedures import *
from aiogram.fsm.context import FSMContext
from utils.states import Questions as Feedback
from data.OT_messages import FEEDBACK_COMMENT, FEEDBACK_WARNING 
from data.OT_constants import FEEDBACK_CHOISES_ARRAY

router = Router()

@router.message(Feedback.CHOICE30)
async def feedback_handler_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Feedback.CLARITY)
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT feed_desc
                          FROM feedback_mess f_mess
                          WHERE 
                          f_mess.feed_lang = ?
                          AND f_mess.feed_step = ?""", (data["LANGUAGE"], 1))
    feedback_mess = cursor.fetchone()
    cursor.close()
    await message.answer(feedback_mess[0], reply_markup=OT_reply.feed_markup)
    
@router.message(Feedback.CLARITY)
async def feedback_handler_clarity_feed(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if message.text in FEEDBACK_CHOISES_ARRAY:
        await state.update_data(CLARITY=message.text)
        await state.set_state(Feedback.CLARITY_FEED)
        await message.answer(FEEDBACK_COMMENT.get(data["LANGUAGE"]))
    else:
        await message.answer(FEEDBACK_WARNING.get(data["LANGUAGE"]))    
            
@router.message(Feedback.CLARITY_FEED)
async def feedback_handler_usefulness(message: Message, state: FSMContext) -> None:
    await state.update_data(CLARITY_FEED=message.text)
    await state.set_state(Feedback.USEFULNESS)
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT feed_desc
                          FROM feedback_mess f_mess
                          WHERE 
                          f_mess.feed_lang = ?
                          AND f_mess.feed_step = ?""", (data["LANGUAGE"], 2))
    feedback_mess = cursor.fetchone()
    cursor.close()
    await message.answer(feedback_mess[0], reply_markup=OT_reply.feed_markup)
    
@router.message(Feedback.USEFULNESS)
async def feedback_handler_usefulness_feed(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if message.text in FEEDBACK_CHOISES_ARRAY:
        await state.update_data(USEFULNESS=message.text)
        await state.set_state(Feedback.USEFULNESS_FEED)
        await message.answer(FEEDBACK_COMMENT.get(data["LANGUAGE"]))
    else:
        await message.answer(FEEDBACK_WARNING.get(data["LANGUAGE"]))    
    
@router.message(Feedback.USEFULNESS_FEED)
async def feedback_handler_support(message: Message, state: FSMContext) -> None:
    await state.update_data(USEFULNESS_FEED=message.text)
    await state.set_state(Feedback.SUPPORT)
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT feed_desc
                          FROM feedback_mess f_mess
                          WHERE 
                          f_mess.feed_lang = ?
                          AND f_mess.feed_step = ?""", (data["LANGUAGE"], 3))
    feedback_mess = cursor.fetchone()
    cursor.close()
    await message.answer(feedback_mess[0], reply_markup=OT_reply.feed_markup)
    
@router.message(Feedback.SUPPORT)
async def feedback_handler_support_feed(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if message.text in FEEDBACK_CHOISES_ARRAY:
        await state.update_data(SUPPORT=message.text)
        await state.set_state(Feedback.SUPPORT_FEED)
        await message.answer(FEEDBACK_COMMENT.get(data["LANGUAGE"]))    
    else:
        await message.answer(FEEDBACK_WARNING.get(data["LANGUAGE"]))    
        
@router.message(Feedback.SUPPORT_FEED)
async def feedback_handler_end(message: Message, state: FSMContext) -> None:
    await state.update_data(SUPPORT_FEED=message.text)
    await state.set_state(Feedback.END)
    data = await state.get_data()
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT feed_desc
                          FROM feedback_mess f_mess
                          WHERE 
                          f_mess.feed_lang = ?
                          AND f_mess.feed_step = ?""", (data["LANGUAGE"], 4))
    feedback_mess = cursor.fetchone()
    cursor.close()
    await message.answer(feedback_mess[0], reply_markup=ReplyKeyboardRemove())
    
    # insert data to DB
    conn = SQLiteStorage()._get_connection()
    cursor = conn.cursor()
    # Prepare the data as a list of tuples
    
    # Define the INSERT query
    insert_query = """INSERT INTO feedback_res (
                        feed_user_id,	        
                        feed_user_name,	        
                        feed_clarity,	        
                        feed_clarity_comment,	
                        feed_usefulness,	        
                        feed_usefulness_comment,	
                        feed_support,	        
                        feed_support_comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    # Use executemany to insert the data
    cursor.execute(insert_query, (message.from_user.url, message.from_user.full_name,
                                data["CLARITY"], data["CLARITY_FEED"],  
                                data["USEFULNESS"], data["USEFULNESS_FEED"],
                                data["SUPPORT"], data["SUPPORT_FEED"]
                                ) )
    conn.commit()
    conn.close()
    await state.clear()
            
            
            