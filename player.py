# player.py

from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

vc_client = None


async def init_player(app):
    global vc_client
    vc_client = PyTgCalls(app)
    await vc_client.start()


async def play_song(chat_id, file_path):
    await vc_client.join_group_call(
        chat_id,
        AudioPiped(file_path)
    )


async def stop_song(chat_id):
    await vc_client.leave_group_call(chat_id)


async def pause_song(chat_id):
    await vc_client.pause_stream(chat_id)


async def resume_song(chat_id):
    await vc_client.resume_stream(chat_id)
