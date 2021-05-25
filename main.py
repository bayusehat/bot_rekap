import logging
import psycopg2
# from os import fspath
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from psycopg2 import Error
from datetime import datetime
import requests
import re

#Connecting database
try:
    connection = psycopg2.connect(user="ccoper",password="ccoper2019",host="10.60.170.169",port="5432",database="ccoper")
    cursor = connection.cursor()
    print("PostgreSQL server information")
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    print("PostgreSQL connection is closed")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# def get_url():
#     contents = requests.get('https://random.dog/woof.json').json()    
#     url = contents['url']
#     return url

def done(update, context):
    url = open('./logs.png','rb')
    rep = update.message.reply_to_message
    if rep is None:
        message_id = update.message.message_id
        chat_id = update.message.chat_id
        user = update.message.text
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
        last_name = update.message.from_user.last_name
        name = "{} {}".format(first_name,last_name)
        date = update.message.date
        tipe = update.message.chat.type
        is_reply = 2
    else:
        message_id = rep.message_id
        chat_id = rep.chat_id
        user = rep.text
        username = rep.from_user.username
        first_name = rep.from_user.first_name
        last_name =rep.from_user.last_name
        name = "{} {}".format(first_name,last_name)
        date = rep.date
        tipe = rep.chat.type
        is_reply = 1
        
        #query
        select_query = "select message_id from tbl_rekap_bot where message_id = '%s'"
        sc = connection.cursor()
        sc.execute(select_query,(message_id,))
        row = sc.fetchall()
        rowcount = len(row)
        if rowcount > 0 :
            if row[0][0] == message_id:
                return context.bot.send_message(chat_id=chat_id,text="Pesan ini sudah di reply, failed insert to Database!")

    pesan = "{}".format(user.replace('/done',''))
    insert_query = """insert into tbl_rekap_bot(nama,username,message,type,tgl,is_reply,message_id) 
        values('{}','{}','{}','{}','{}',{},{})""".format(name,username,pesan,tipe,date,is_reply,message_id)
    cursor.execute(insert_query)
    connection.commit()
    notif = "Stored in Database,successfully! \n[Pesan dari : {} ; Text : {} ; Tanggal : {} ]".format(name,pesan,date)
    return context.bot.send_message(chat_id=chat_id,text=notif)

def main():
    updater = Updater('1894704804:AAGa7tvFU-WyJyAWWhz6ho_cuudcbQe7OdA',use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('done',done))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()