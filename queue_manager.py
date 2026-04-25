# queue_manager.py

from collections import deque

music_queue = deque()
repeat_mode = False


def add_to_queue(song_data):
    music_queue.append(song_data)


def get_next_song():
    if music_queue:
        return music_queue.popleft()
    return None


def view_queue():
    return list(music_queue)


def clear_queue():
    music_queue.clear()


def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    return repeat_mode


def is_repeat():
    return repeat_mode
