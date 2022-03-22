from base64 import b64encode
from secrets import choice
from typing import TypeVar
from uuid import uuid4

from captcha.image import ImageCaptcha

from db.tables import Captcha


K = TypeVar("K")  # Key
V = TypeVar("V")  # Value


CAPTCHA_TEXT_LENGTH = 6
ALPHABET: tuple[str, ...] = (
    "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
)
MAX_CAPTCHAS = 1000


ImageCaptchaHandler = ImageCaptcha()


async def create_captcha_token_and_jpeg_str() -> tuple[str, str]:
    token = generate_captcha_token()
    answer = generate_captcha_random_chars()

    jpeg_bytes_io = ImageCaptchaHandler.generate(answer, format="jpeg").getvalue()
    jpeg_str = b64encode(jpeg_bytes_io).decode()

    await Captcha.insert(Captcha(token=token, answer=answer))

    await reduce_token_to_captcha_text_mapping_to_max_size()

    return token, jpeg_str


def generate_captcha_token() -> str:
    return str(uuid4())


def generate_captcha_random_chars() -> str:
    return "".join(choice(ALPHABET) for _ in range(CAPTCHA_TEXT_LENGTH))


async def check_captcha_answer_and_delete(token: str, answer: str) -> bool:
    is_correct = False

    async with Captcha._meta.db.transaction():
        entry = await Captcha.objects().where(Captcha.token == token).first()

        if entry is None:
            return False

        is_correct = entry.answer == answer

        await entry.remove()

    return is_correct


async def reduce_token_to_captcha_text_mapping_to_max_size():
    count = int((await Captcha.raw("select count(*) from captcha"))[0]["count"])

    if count <= MAX_CAPTCHAS:
        return

    await Captcha.raw(
        f"delete from captcha where id in (select id from captcha order by id asc limit {count - MAX_CAPTCHAS + (MAX_CAPTCHAS // 10)})"
    )
