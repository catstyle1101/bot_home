from enum import StrEnum


class MessageType(StrEnum):
    start_menu = "messages/start_menu.j2"
    help_command = "messages/help_command.j2"
    torrent_settings = "messages/torrent_settings.j2"
    delete_torrent = "messages/delete_torrent.j2"
    confirm_delete_message = "messages/confirm_delete_message.j2"
    download_magnet = "messages/download_magnet.j2"
    format_find_torrent = "messages/format_find_torrent.j2"
    nothing_found = "messages/nothing_found.j2"


class ErrorMessage(StrEnum):
    api_not_found = "Не могу подключиться к API серверу. Он переехал? Попробуй позже."
