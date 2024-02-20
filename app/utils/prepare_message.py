from io import StringIO


def prepare_message(message: str, delimiter: str) -> list[str]:
    """
    split message into chunks based on delimiter for limit of 4096 symbols.
    :param message:
    :param delimiter: delimiter for message
    :return: list of chunks
    """
    result = []
    if len(message) > 4096:
        message_list = message.split(delimiter)
        reply_message = StringIO()
        len_reply_message = 0
        for line in message_list:
            if len_reply_message + len(line) > 4096:
                result.append(reply_message.getvalue())
                reply_message = StringIO()
            else:
                reply_message.write(line)
                len_reply_message += len(line)
        if last := reply_message.getvalue():
            result.append(last)
    else:
        result.append(message.replace(delimiter, ""))
    return result
