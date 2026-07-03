"""
Quiz question bank — uz / ru / en translations.
Grading uses option indices (language-independent).
"""

SUPPORTED_LANGS = {"uz", "ru", "en"}
DEFAULT_LANG = "uz"


def _normalize_lang(lang: str) -> str:
    code = (lang or DEFAULT_LANG).lower()[:2]
    return code if code in SUPPORTED_LANGS else DEFAULT_LANG


QUIZ_QUESTIONS = [
    {
        "id": 1,
        "correct": 1,
        "translations": {
            "en": {
                "question": "You receive a Telegram message claiming you won an iPhone. What should you do first?",
                "options": [
                    "Click the link and enter your details to claim the prize",
                    "Verify the sender and never trust unbelievable prizes",
                    "Forward the message to friends so they can win too",
                    "Reply with your phone number immediately",
                ],
                "explanation": "Unbelievable prizes are a classic scam tactic. Always verify sources and never trust unsolicited win notifications.",
            },
            "uz": {
                "question": "Telegramda iPhone yutganingiz haqida xabar keldi. Birinchi navbatda nima qilasiz?",
                "options": [
                    "Havolani bosib, mukofotni olish uchun ma'lumotlarni kiritaman",
                    "Yuboruvchini tekshiraman va ishonib bo'lmaydigan sovrinlarga ishonmayman",
                    "Do'stlarga yuboraman, ular ham yutishi uchun",
                    "Darhol telefon raqamimni yuboraman",
                ],
                "explanation": "Ishonib bo'lmaydigan sovrinlar — klassik firibgarlik usuli. Manbani tekshiring va kutilmagan g'alaba xabarlariga ishonmang.",
            },
            "ru": {
                "question": "Вы получили в Telegram сообщение о выигрыше iPhone. Что делать в первую очередь?",
                "options": [
                    "Перейти по ссылке и ввести данные для получения приза",
                    "Проверить отправителя и не доверять невероятным призам",
                    "Переслать друзьям, чтобы они тоже выиграли",
                    "Сразу ответить своим номером телефона",
                ],
                "explanation": "Невероятные призы — классическая тактика мошенников. Всегда проверяйте источник.",
            },
        },
    },
    {
        "id": 2,
        "correct": 1,
        "translations": {
            "en": {
                "question": "What does HTTPS in a website URL primarily indicate?",
                "options": [
                    "The website is definitely legitimate and safe",
                    "Encrypted connection between your browser and the server",
                    "The website cannot be a phishing site",
                    "Your payment card is automatically protected",
                ],
                "explanation": "HTTPS encrypts data in transit, but scammers can also obtain HTTPS certificates. Always verify the domain name carefully.",
            },
            "uz": {
                "question": "Sayt manzilidagi HTTPS asosan nimani anglatadi?",
                "options": [
                    "Sayt albatta haqiqiy va xavfsiz",
                    "Brauzer va server o'rtasida shifrlangan aloqa",
                    "Sayt fishing bo'lishi mumkin emas",
                    "To'lov kartangiz avtomatik himoyalangan",
                ],
                "explanation": "HTTPS ma'lumotni shifrlaydi, lekin firibgarlar ham sertifikat olishi mumkin. Domen nomini diqqat bilan tekshiring.",
            },
            "ru": {
                "question": "Что в основном означает HTTPS в адресе сайта?",
                "options": [
                    "Сайт точно настоящий и безопасный",
                    "Зашифрованное соединение между браузером и сервером",
                    "Сайт не может быть фишинговым",
                    "Ваша карта автоматически защищена",
                ],
                "explanation": "HTTPS шифрует данные, но мошенники тоже могут получить сертификаты. Проверяйте домен.",
            },
        },
    },
    {
        "id": 3,
        "correct": 1,
        "translations": {
            "en": {
                "question": "A website asks for your SMS verification code to 'confirm your prize.' What do you do?",
                "options": [
                    "Enter the code — they need it to verify you",
                    "Never share SMS codes — this is OTP theft",
                    "Share only the last 3 digits",
                    "Ask them to send a new code first",
                ],
                "explanation": "SMS verification codes are for YOUR authentication only. Sharing them lets criminals access your accounts.",
            },
            "uz": {
                "question": "Sayt mukofotni tasdiqlash uchun SMS kodini so'raydi. Nima qilasiz?",
                "options": [
                    "Kodni kiritaman — ularga tekshirish kerak",
                    "SMS kodlarni hech kimga bermayman — bu OTP o'g'irlash",
                    "Faqat oxirgi 3 raqamni beraman",
                    "Avval yangi kod yuborishlarini so'rayman",
                ],
                "explanation": "SMS kodlar faqat SIZNING autentifikatsiyangiz uchun. Ularni berish jinoyatchilarga hisobingizga kirish imkonini beradi.",
            },
            "ru": {
                "question": "Сайт просит SMS-код для «подтверждения приза». Что делать?",
                "options": [
                    "Ввести код — им нужно для проверки",
                    "Никому не сообщать SMS-коды — это кража OTP",
                    "Сообщить только последние 3 цифры",
                    "Попросить отправить новый код",
                ],
                "explanation": "SMS-коды только для ВАШЕЙ аутентификации. Их передача даёт преступникам доступ к аккаунтам.",
            },
        },
    },
    {
        "id": 4,
        "correct": 1,
        "translations": {
            "en": {
                "question": "Which is a common sign of a phishing website?",
                "options": [
                    "Professional design and branding",
                    "Urgency messages like 'Claim in 5 minutes or lose prize!'",
                    "Clear contact information",
                    "Proper spelling and grammar",
                ],
                "explanation": "Scammers create urgency to bypass your critical thinking. Legitimate organizations rarely pressure immediate action.",
            },
            "uz": {
                "question": "Fishing saytning qaysi belgisi keng tarqalgan?",
                "options": [
                    "Professional dizayn va brend",
                    "'5 daqiqada oling yoki yo'qotasiz!' kabi shoshilish xabarlari",
                    "Aniq aloqa ma'lumotlari",
                    "To'g'ri imlo va grammatika",
                ],
                "explanation": "Firibgarlar shoshilish yaratib, muhim fikrlashni o'tkazib yuborishga majbur qiladi.",
            },
            "ru": {
                "question": "Какой признак фишингового сайта встречается чаще всего?",
                "options": [
                    "Профессиональный дизайн",
                    "Сообщения о срочности: «Заберите за 5 минут!»",
                    "Чёткие контакты",
                    "Правильная грамматика",
                ],
                "explanation": "Мошенники создают срочность, чтобы вы не успели подумать.",
            },
        },
    },
    {
        "id": 5,
        "correct": 1,
        "translations": {
            "en": {
                "question": "What is social engineering in cybersecurity?",
                "options": [
                    "Building secure software systems",
                    "Manipulating people into revealing information or taking unsafe actions",
                    "Encrypting social media messages",
                    "Engineering social network algorithms",
                ],
                "explanation": "Social engineering exploits human psychology — trust, fear, greed, and urgency — rather than technical vulnerabilities.",
            },
            "uz": {
                "question": "Kiberxavfsizlikda ijtimoiy muhandislik nima?",
                "options": [
                    "Xavfsiz dasturiy tizimlar qurish",
                    "Odamlarni ma'lumot berish yoki xavfli harakat qilishga majburlash",
                    "Ijtimoiy tarmoq xabarlarini shifrlash",
                    "Ijtimoiy tarmoq algoritmlarini loyihalash",
                ],
                "explanation": "Ijtimoiy muhandislik inson psixologiyasini — ishonch, qo'rquv, ochko'zlik va shoshilishni suiiste'mol qiladi.",
            },
            "ru": {
                "question": "Что такое социальная инженерия в кибербезопасности?",
                "options": [
                    "Создание защищённых систем",
                    "Манипулирование людьми для раскрытия информации",
                    "Шифрование сообщений в соцсетях",
                    "Разработка алгоритмов соцсетей",
                ],
                "explanation": "Социальная инженерия эксплуатирует психологию — доверие, страх, жадность и спешку.",
            },
        },
    },
    {
        "id": 6,
        "correct": 1,
        "translations": {
            "en": {
                "question": "You scan a QR code from a poster offering free prizes. What risk does this pose?",
                "options": [
                    "No risk — QR codes are always safe",
                    "QR codes can redirect to malicious phishing websites",
                    "QR codes only open legitimate apps",
                    "QR codes cannot steal information",
                ],
                "explanation": "QR-code attacks (quishing) hide malicious URLs. Always preview the destination before proceeding.",
            },
            "uz": {
                "question": "Bepul sovrin taklif qiluvchi plakatdagi QR-kodni skanerlaysiz. Qanday xavf bor?",
                "options": [
                    "Xavf yo'q — QR-kodlar doim xavfsiz",
                    "QR-kodlar zararli fishing saytlarga yo'naltirishi mumkin",
                    "QR-kodlar faqat haqiqiy ilovalarni ochadi",
                    "QR-kodlar ma'lumot o'g'irlolmaydi",
                ],
                "explanation": "QR-kod hujumlari (quishing) yashirin zararli havolalarni beradi. Ochishdan oldin manzilni tekshiring.",
            },
            "ru": {
                "question": "Вы сканируете QR-код с плаката о бесплатных призах. Какой риск?",
                "options": [
                    "Нет риска — QR всегда безопасны",
                    "QR может вести на вредоносные фишинговые сайты",
                    "QR открывает только легитимные приложения",
                    "QR не может украсть информацию",
                ],
                "explanation": "QR-атаки скрывают вредоносные URL. Всегда проверяйте адрес перед переходом.",
            },
        },
    },
    {
        "id": 7,
        "correct": 1,
        "translations": {
            "en": {
                "question": "A countdown timer on a lottery website pressures you to act fast. This is an example of:",
                "options": [
                    "Good user experience design",
                    "Urgency tactic used in scams",
                    "Legal requirement for online lotteries",
                    "Standard e-commerce practice",
                ],
                "explanation": "Artificial urgency prevents you from researching the site or consulting others — a hallmark of fraud.",
            },
            "uz": {
                "question": "Lotereya saytidagi taymer sizni tez harakat qilishga majbur qiladi. Bu nima misoli?",
                "options": [
                    "Yaxshi foydalanuvchi tajribasi dizayni",
                    "Firibgarlikda ishlatiladigan shoshilish taktikasi",
                    "Onlayn lotereyalar uchun qonuniy talab",
                    "Standart elektron savdo amaliyoti",
                ],
                "explanation": "Sun'iy shoshilish saytni tekshirish yoki maslahatlashishga vaqt bermaydi — firibgarlik belgisi.",
            },
            "ru": {
                "question": "Таймер на сайте лотереи заставляет действовать быстро. Это пример:",
                "options": [
                    "Хорошего UX-дизайна",
                    "Тактики срочности в мошенничестве",
                    "Законного требования для лотерей",
                    "Стандартной практики e-commerce",
                ],
                "explanation": "Искусственная срочность не даёт времени проверить сайт — признак мошенничества.",
            },
        },
    },
    {
        "id": 8,
        "correct": 1,
        "translations": {
            "en": {
                "question": "Which information should you NEVER enter on an unknown website?",
                "options": [
                    "Your favorite color",
                    "Payment card number, CVV, and SMS verification codes",
                    "A made-up username for a game",
                    "Your city name",
                ],
                "explanation": "Financial credentials and OTP codes on untrusted sites lead directly to card fraud and account takeover.",
            },
            "uz": {
                "question": "Noma'lum saytda qaysi ma'lumotni HECH QACHON kiritmaslik kerak?",
                "options": [
                    "Sevimli rangingiz",
                    "To'lov karta raqami, CVV va SMS tasdiqlash kodlari",
                    "O'yin uchun o'ylab topilgan foydalanuvchi nomi",
                    "Shahringiz nomi",
                ],
                "explanation": "Ishonchsiz saytlarda moliyaviy ma'lumotlar va OTP kodlari to'g'ridan-to'g'ri karta firibgarligiga olib keladi.",
            },
            "ru": {
                "question": "Какую информацию НИКОГДА не вводить на неизвестном сайте?",
                "options": [
                    "Любимый цвет",
                    "Номер карты, CVV и SMS-коды",
                    "Выдуманное имя для игры",
                    "Название города",
                ],
                "explanation": "Финансовые данные и OTP на ненадёжных сайтах ведут к мошенничеству с картами.",
            },
        },
    },
    {
        "id": 9,
        "correct": 1,
        "translations": {
            "en": {
                "question": "How can you verify if a website address is suspicious?",
                "options": [
                    "Check if it has many images",
                    "Look for misspellings, unusual domains, or extra subdomains",
                    "See if the page loads quickly",
                    "Count the number of buttons on the page",
                ],
                "explanation": "Phishing domains often mimic real sites with subtle changes like 'paypa1.com' instead of 'paypal.com'.",
            },
            "uz": {
                "question": "Sayt manzili shubhali ekanini qanday tekshirasiz?",
                "options": [
                    "Ko'p rasm bor-yo'qligini tekshirish",
                    "Imlo xatolari, g'ayrioddiy domenlar yoki ortiqcha subdomenlarni qidirish",
                    "Sahifa tez yuklanishini ko'rish",
                    "Tugmalar sonini sanash",
                ],
                "explanation": "Fishing domenlari haqiqiy saytlarni taqlid qiladi — masalan 'paypa1.com' o'rniga 'paypal.com'.",
            },
            "ru": {
                "question": "Как проверить, подозрителен ли адрес сайта?",
                "options": [
                    "Проверить количество картинок",
                    "Искать опечатки, необычные домены или лишние поддомены",
                    "Смотреть скорость загрузки",
                    "Считать кнопки на странице",
                ],
                "explanation": "Фишинговые домены имитируют настоящие — например 'paypa1.com' вместо 'paypal.com'.",
            },
        },
    },
    {
        "id": 10,
        "correct": 1,
        "translations": {
            "en": {
                "question": "What is the safest action after recognizing a phishing attempt?",
                "options": [
                    "Enter fake information to trick the scammers",
                    "Close the page, do not interact, and report it",
                    "Complete the form to see what happens",
                    "Share it on social media without context",
                ],
                "explanation": "Do not engage with phishing sites. Close immediately, report to relevant authorities, and warn others responsibly.",
            },
            "uz": {
                "question": "Fishing urinishini aniqlaganingizdan keyin eng xavfsiz harakat qaysi?",
                "options": [
                    "Firibgarlarni aldash uchun yolg'on ma'lumot kiritish",
                    "Sahifani yopish, muloqot qilmaslik va xabar berish",
                    "Nima bo'lishini ko'rish uchun formani to'ldirish",
                    "Kontekstsiz ijtimoiy tarmoqlarda ulashish",
                ],
                "explanation": "Fishing saytlar bilan muloqot qilmang. Darhol yoping, tegishli organlarga xabar bering.",
            },
            "ru": {
                "question": "Какое действие безопаснее всего после обнаружения фишинга?",
                "options": [
                    "Ввести ложные данные, чтобы обмануть мошенников",
                    "Закрыть страницу, не взаимодействовать и сообщить",
                    "Заполнить форму, чтобы посмотреть что будет",
                    "Поделиться в соцсетях без контекста",
                ],
                "explanation": "Не взаимодействуйте с фишинговыми сайтами. Закройте, сообщите в органы и предупредите других.",
            },
        },
    },
]

NO_ANSWER = {
    "en": "No answer",
    "uz": "Javob berilmagan",
    "ru": "Нет ответа",
}


def _localized(q: dict, lang: str) -> dict:
    return q["translations"][lang]


def get_questions_for_client(lang: str = "uz"):
    """Return questions without correct answers for the client."""
    lang = _normalize_lang(lang)
    return [
        {
            "id": q["id"],
            "question": _localized(q, lang)["question"],
            "options": _localized(q, lang)["options"],
        }
        for q in QUIZ_QUESTIONS
    ]


def grade_quiz(answers: dict, lang: str = "uz") -> tuple:
    """Grade quiz answers and return score with explanations."""
    lang = _normalize_lang(lang)
    results = []
    score = 0
    for q in QUIZ_QUESTIONS:
        loc = _localized(q, lang)
        qid = str(q["id"])
        selected = answers.get(qid)
        correct = q["correct"]
        is_correct = selected == correct
        if is_correct:
            score += 1
        options = loc["options"]
        results.append(
            {
                "question_id": q["id"],
                "question": loc["question"],
                "your_answer": options[selected] if selected is not None and 0 <= selected < len(options) else NO_ANSWER[lang],
                "correct_answer": options[correct],
                "is_correct": is_correct,
                "explanation": loc["explanation"],
            }
        )
    return score, len(QUIZ_QUESTIONS), results
