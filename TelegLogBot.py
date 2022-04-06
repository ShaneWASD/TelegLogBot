import config
import logging
import os
import urllib
from aiogram import Bot, Dispatcher, executor, types

if (os.path.exists('Data')) == False:
    os.mkdir('Data')
if (os.path.exists('Data\Chat')) == False:
    os.mkdir('Data\Chat')
if (os.path.exists('Data\Group')) == False:
    os.mkdir('Data\Group')

logging.basicConfig(level=logging.INFO)

#initialization botyari
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

#echobase_logging_text
@dp.message_handler()
async def echo(message: types.message):
    mestext = str(message.text)
    dattext = str(message.date)
    namtext = str(message.from_user.first_name)
    FolPath = (three_folder(message))
    f = open(FolPath + "\index.html", "a")
    f.write(dattext + '   ' + namtext + '    :' + mestext + '<br> \n')

#docloader 20 mb limit?
@dp.message_handler(content_types=['document'])
async def scan_message(message: types.Message):
    FolPath = (three_folder(message))
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    name = message.document.file_name
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{config.TOKEN}/{fi}',f'{FolPath}/{name}')
    FilPath = os.path.abspath(FolPath + '\\' + name)
    f = open(FolPath + "\index.html", "a")
    creator_file(FolPath, message.from_user.first_name, FilPath, name, 'Document ')

#photoloader
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    name = (str(message.photo[-1].file_id))
    name2 = (str(message.caption))
    if name2 == 'None':
        name2 = name
    FolPath = (three_folder(message))
    await message.photo[-1].download(FolPath + '\\' + name + '.jpg')
    FilPath = os.path.abspath(FolPath + '\\' + name + '.jpg')
    creator_file(FolPath, message.from_user.first_name, FilPath, name2, 'Image ')

#videoloader
@dp.message_handler(content_types=['video'])
async def handle_docs_video(message):
    name = (str(message.video.file_id))
    name2 = (str(message.caption))
    if name2 == 'None':
        name2 = name
    FolPath = (three_folder(message))
    await message.video.download(FolPath + '\\' + name + '.mp4')
    FilPath = os.path.abspath(FolPath + '\\' + name + '.mp4')
    creator_file(FolPath, message.from_user.first_name, FilPath, name2, 'Video ')

#tree
def three_folder (a):
    if a.chat.id < 0:
        FolPath = (str('Data\Group\\' + a.chat.title))
        if (os.path.exists(FolPath)) == False:
            os.mkdir(FolPath)
    else:
        FolPath = (str('Data\Chat\\' + a.chat.first_name))
        if (os.path.exists(FolPath)) == False:
            os.mkdir(FolPath)
    return FolPath

#filecreator for html
def creator_file (FolPath, sender, FilPath, name, typemes):
    f = open(FolPath + "\index.html", "a")
    f.write((typemes + sender + '    <a href="' + FilPath + '">' + name + '</a> <br> \n'))

#true = not vajno, false = vajno
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=config.Vajno)