from random import choice

def convert_digits_to_emoji(num: int):
    """
    Convert a given number to emoji representation.

    Args:
        num (int): The number to be converted.

    Returns:
        str: The emoji representation of the number.
    """
    emoji = '0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣'.split()
    return ''.join(emoji[int(i)] for i in str(num))

def random_heart():
    """
    Generate a random heart emoji from a list of heart emojis.

    Returns:
        str: A randomly selected heart emoji.
    """
    hearts = '❤️ 🧡 💛 💚 💙 💜 🤎 🖤 🤍 💟'.split()
    return choice[hearts]

if __name__ == '__main__':
    print(random_heart())
