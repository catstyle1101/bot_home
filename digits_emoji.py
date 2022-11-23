
def convert_digits_to_emoji(num: int):
    emoji = '0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣'.split()
    num=str(num)
    return ''.join(emoji[int(i)] for i in num)

def random_heart():
    from random import randint
    hearts = '❤️ 🧡 💛 💚 💙 💜 🤎 🖤 🤍 💟'.split()
    return hearts[randint(0, len(hearts))]

if __name__ == '__main__':
    print(random_heart())    