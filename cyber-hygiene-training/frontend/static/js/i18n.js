/**
 * Cyber Hygiene Training — UZ / RU / EN translations
 */

const LANG_KEY = 'cht_lang';
const SUPPORTED_LANGS = ['uz', 'ru', 'en'];
const DEFAULT_LANG = 'uz';

const translations = {
  uz: {
    common: {
      lang_uz: 'UZ',
      lang_ru: 'RU',
      lang_en: 'EN',
    },
    landing: {
      title: 'MEGA LUCKY WIN — Mukofotingizni oling!',
      marquee: '🔥 SHOSHILINCH! Faqat 3 ta sovrin qoldi! Vaqt tugashidan oldin ulguring! 🔥',
      congrats: "🏆 TABRIKLAYMIZ! SIZ G'OLIB BO'LDINGIZ! 🏆",
      subtitle: "Siz maxsus mukofot uchun tanlandingiz! Bu imkoniyatni qo'ldan boy bermang!!!",
      countdown_label: '⏰ TAKLIF TUGASHIGA QOLDI:',
      ticker_loading: 'Yuklanmoqda...',
      prize_apartment: 'Kvartira',
      winners_today: '🔥 BUGUN 2 847 kishi mukofotini oldi!',
      trust_line: "✅ Xavfsiz to'lov • ✅ Tez yetkazib berish • ✅ 100% kafolat",
      claim_btn: "🎁 HOZIR OLISH — BEPUL! 🎁",
      badge_bank: '🏦 Bank kafolati',
      badge_ssl: '🔐 SSL himoya',
      badge_rating: '⭐ 4.9/5 ishonch',
      ticker_1: 'Akmal T. BYD Champion yutdi!',
      ticker_2: 'Dilnoza K. iPhone 17 oldi!',
      ticker_3: "Jasur M. 5 000 000 UZS yutdi!",
      ticker_4: "Nodira S. kvartira sohibi bo'ldi!",
      ticker_5: 'Bobur R. 5 000 000 UZS yutdi!',
      ticker_6: "Malika H. iPhone 17 qo'lga kiritdi!",
      ticker_7: 'Sardor A. 5 000 000 UZS oldi!',
      ticker_8: 'Gulnoza P. BYD Champion yutib oldi!',
    },
    simulation: {
      title: "Milliy Bank — To'lovni tasdiqlash",
      bank_name: '🏦 Milliy Bank',
      secure: '🔒 Xavfsiz ulanish',
      form_title: 'Mukofotni tasdiqlash',
      form_subtitle: "To'lov kartangiz ma'lumotlarini kiriting",
      card_label: 'Karta raqami',
      card_placeholder: '0000 0000 0000 0000',
      expiry_label: 'Amal qilish muddati',
      expiry_placeholder: 'MM/YY',
      cvv_label: 'CVV',
      cvv_placeholder: '•••',
      next_btn: 'Davom etish →',
      footer_encrypt: "🔐 Ma'lumotlaringiz shifrlangan holda uzatiladi",
      sms_header: '📱 SMS xabar',
      sms_prefix: 'Milliy Bank: Tasdiqlash kodi —',
      sms_suffix: 'Hech kimga bermang! Kod 5 daqiqa amal qiladi.',
      otp_label: 'SMS tasdiqlash kodi',
      otp_placeholder: '• • • • • •',
      submit_btn: 'Tasdiqlash va mukofotni olish',
      resend: 'Kod kelmadimi? <a href="#" class="bank-link">Qayta yuborish</a>',
      trust_cards: 'Visa • Mastercard • Uzcard • Humo',
      err_card_rejected: "Karta ma'lumotlari qabul qilinmadi. Iltimos, boshqa karta kiriting yoki ma'lumotlarni tekshiring.",
      err_card_invalid: "Iltimos, to'g'ri karta raqamini kiriting.",
      err_expiry_invalid: "Amal qilish muddatini MM/YY formatida kiriting (masalan: 09/30).",
      err_cvv_invalid: 'CVV 3 ta raqamdan iborat bo\'lishi kerak.',
      err_otp_wrong: 'Noto\'g\'ri tasdiqlash kodi. Qayta urinib ko\'ring.',
      err_otp_empty: '6 xonali SMS kodni kiriting.',
      checking: 'Tekshirilmoqda...',
    },
    reveal: {
      title: '⚠️ DIQQAT!',
      heading: 'DIQQAT!',
      stop: "TO'XTANG!",
      main_msg: "Bu kiberxavfsizlik bo'yicha ta'lim simulyatsiyasi edi.",
      detail_msg: "Agar bu haqiqiy firibgarlik sayti bo'lganida, shaxsiy ma'lumotlaringiz, bank karta raqamingiz va SMS kodlaringiz kiberjinoyatchilarga <strong>o'g'irlanishi</strong> mumkin edi.",
      remember_title: '⚠️ Esda tuting:',
      tip1: "Noma'lum saytlarda bank karta raqamini kiritmang",
      tip2: 'SMS tasdiqlash kodlarini hech kimga bermang',
      tip3: "Haqiqatda bo'lishi mumkin bo'lmagan sovrinlarga ishonmang",
      tip4: "Sayt manzilini doim tekshiring (firibgarlar o'xshash domen ishlatadi)",
      tip5: 'HTTPS borligi yetarli emas — domen ham muhim',
      tip6: 'Telegramdagi shubhali havolalarni bosmang',
      tip7: 'Shoshilish hissi yaratish — firibgarlar usuli',
      tip8: 'Raqamli shaxsingizni himoya qiling',
      disclaimer: "🛡️ <strong>Muhim:</strong> Bu faqat ta'lim maqsadidagi simulyatsiya edi. Hech qanday haqiqiy to'lov kartasi, parol yoki SMS kodi yig'ilmadi va saqlanmadi.",
      learn_btn: "📚 Batafsil o'rganish",
      quiz_btn: '📝 Bilim testi',
    },
    learn: {
      title: '🛡️ Kiberxavfsizlik bo\'yicha ta\'lim',
      subtitle: 'Onlayn tahdidlarni aniqlash va ulardan himoyalanishni o\'rganing',
      phishing_title: '🎣 Fishing qanday ishlaydi',
      phishing_text: 'Fishing — firibgarlar ishonchli tashkilotlarni taqlid qilib, maxfiy ma\'lumotlarni olishga undaydigan kiberhujum. Yolg\'on xatlar, xabarlar va saytlar ishlatiladi. Maqsad — parollar, to\'lov kartalari yoki zararli dasturlarni o\'rnatish.',
      lottery_title: '🎰 Soxta lotereyalar',
      lottery_text: 'Firibgarlar siz hech qachon qatnashmagan tanlovda g\'olib bo\'lganingizni e\'lon qiladi. Shaxsiy ma\'lumot yoki kichik "rasmiylashtirish to\'lovi" so\'rashadi. Haqiqiy lotereyalar g\'olibdan oldindan to\'lov yoki bank ma\'lumotlarini talab qilmaydi.',
      telegram_title: '📱 Telegram firibgarliklari',
      telegram_text: 'Telegram mashhurligi tufayli firibgarlar uchun qulay. Soxta mukofot xabarlari, investitsiya va qo\'llab-quvvatlash xodimini taqlid qilish uchraydi. Botlarni tekshiring va tasdiqlash kodlarini hech kimga bermang.',
      qr_title: '📷 QR-kod hujumlari (Quishing)',
      qr_text: 'Zararli QR-kodlar fishing saytlarga yoki zararli dastur yuklashga olib boradi. Havolani ochishdan oldin manzilini tekshiring. Jamoat joylari va noma\'lum xabarlardagi QR-kodlarga ehtiyot bo\'ling.',
      payment_title: '💳 Soxta to\'lov sahifalari',
      payment_text: 'Firibgar saytlar haqiqiy bank interfeyslarini taqlid qiladi. Shubhali domenlar, xavfsizlik belgilarining yo\'qligi, grammatik xatolar va SMS kod so\'rash — ogohlantirish belgilari.',
      social_title: '🧠 Ijtimoiy muhandislik',
      social_text: 'Hujumchilar texnik emas, inson psixologiyasini manipulyatsiya qiladi — ishonch, shoshilish, qiziqish. Eng yaxshi himoya — shubha va rasmiy kanallar orqali tekshirish.',
      urgency_title: '⏰ Shoshilish taktikasi',
      urgency_text: 'Taymerlar, "cheklangan joylar" va "hoziroq harakat qiling" xabarlari tekshirishni o\'tkazib yuborishga majbur qiladi. Haqiqiy tashkilotlar vaqt beradi.',
      fear_title: '😨 Qo\'rquv taktikasi',
      fear_text: 'Hisob yopilishi, huquqiy choralar yoki mukofot yo\'qolishi haqidagi xabarlar panika yaratadi. To\'xtang, tekshiring, to\'g\'ridan-to\'g\'ri bog\'laning.',
      reward_title: '🎁 Mukofot manipulyatsiyasi',
      reward_text: 'Juda yaxshi bo\'lib tuyuladigan sovrinlar ochko\'zlik va hayajonni suiiste\'mol qiladi. Tanlovga qatnashmagan bo\'lsangiz, g\'olib bo\'lmagansiz.',
      otp_title: '📲 OTP o\'g\'irlash',
      otp_text: 'SMS tasdiqlash kodlari hisoblaringiz kaliti. Firibgarlar kartadan keyin kodni so\'raydi. Banklar hech qachon OTP so\'ramaydi.',
      identity_title: '🪪 Shaxsni o\'g\'irlash',
      identity_text: 'Firibgarlik orqali yig\'ilgan ma\'lumotlar shaxsiy firibgarlikka olib keladi — hisob ochish, kredit olish. Ism, ID va aloqa ma\'lumotlarini himoya qiling.',
      fraud_title: '💸 Karta firibgarligi',
      fraud_text: 'Soxta saytlarda karta kiritish ruxsatsiz xaridlar uchun yetarli. OTP bilan birga daqiqalar ichida hisob bo\'shatilishi mumkin.',
      quiz_btn: '📝 Bilimingizni sinang — Testni boshlang',
    },
    quiz: {
      title: '📝 Kiberxavfsizlik testi',
      subtitle: '10 ta savol — ongli fikrlashni tekshiring',
      loading: 'Yuklanmoqda...',
      progress: 'Savol {current} / {total}',
      prev: '← Oldingi',
      next: 'Keyingi →',
      submit: 'Testni yakunlash',
      submitting: 'Yuborilmoqda...',
      select_answer: 'Davom etishdan oldin javob tanlang.',
      submit_fail: 'Test yuborilmadi. Qayta urinib ko\'ring.',
      load_fail: 'Test yuklanmadi. Sahifani yangilang.',
      complete: 'Test yakunlandi!',
      score: '{score} / {total} ({percent}%)',
      explanations_title: 'Batafsil tushuntirishlar:',
      your_answer: 'Sizning javobingiz:',
      correct_answer: 'To\'g\'ri javob:',
      cert_btn: '🏆 Sertifikatni ko\'rish',
    },
    certificate: {
      title: 'Tugatish sertifikati',
      header: 'KIBERGIYENA BO\'YICHA TA\'LIM',
      cert_title: 'Tugatish sertifikati',
      certifies: 'Quyidagi shaxs',
      completed: 'muvaffaqiyatli tugatdi',
      program: 'Kiberxavfsizlik ongini oshirish dasturi',
      includes: 'fishing simulyatsiyasi, ta\'lim modullari va bilim baholashni o\'z ichiga oladi.',
      score_label: 'Ball',
      id_label: 'Sertifikat ID',
      date_label: 'Sana',
      footer: 'Bu sertifikat ta\'lim simulyatsiyasida ishtirok etganingizni tasdiqlaydi. Haqiqiy shaxsiy yoki moliyaviy ma\'lumot yig\'ilmagan.',
      print_btn: '🖨️ Sertifikatni chop etish',
      review_btn: '📚 O\'quv materiallarini ko\'rib chiqish',
      disclaimer: '🛡️ TA\'LIM SIMULYATSIYASI YAKUNLANDI — Ehtiyot bo\'ling va raqamli shaxsingizni himoya qiling',
      trainee: 'Ishtirokchi',
    },
  },
  ru: {
    common: {
      lang_uz: 'UZ',
      lang_ru: 'RU',
      lang_en: 'EN',
    },
    landing: {
      title: 'MEGA LUCKY WIN — Получите свой приз!',
      marquee: '🔥 СРОЧНО! Осталось только 3 приза! Успейте до окончания времени! 🔥',
      congrats: '🏆 ПОЗДРАВЛЯЕМ! ВЫ ПОБЕДИТЕЛЬ! 🏆',
      subtitle: 'Вы выбраны для специального приза! Не упустите эту возможность!!!',
      countdown_label: '⏰ ДО ОКОНЧАНИЯ ПРЕДЛОЖЕНИЯ:',
      ticker_loading: 'Загрузка...',
      prize_apartment: 'Квартира',
      winners_today: '🔥 СЕГОДНЯ 2 847 человек получили приз!',
      trust_line: '✅ Безопасная оплата • ✅ Быстрая доставка • ✅ 100% гарантия',
      claim_btn: '🎁 ПОЛУЧИТЬ СЕЙЧАС — БЕСПЛАТНО! 🎁',
      badge_bank: '🏦 Банковская гарантия',
      badge_ssl: '🔐 SSL защита',
      badge_rating: '⭐ 4.9/5 доверие',
      ticker_1: 'Акмаль Т. выиграл BYD Champion!',
      ticker_2: 'Дилноза К. получила iPhone 17!',
      ticker_3: 'Жасур М. выиграл 5 000 000 UZS!',
      ticker_4: 'Нодира С. стала владельцем квартиры!',
      ticker_5: 'Бобур Р. выиграл 5 000 000 UZS!',
      ticker_6: 'Малика Х. получила iPhone 17!',
      ticker_7: 'Сардор А. получил 5 000 000 UZS!',
      ticker_8: 'Гульноза П. выиграла BYD Champion!',
    },
    simulation: {
      title: 'Национальный Банк — Подтверждение оплаты',
      bank_name: '🏦 Национальный Банк',
      secure: '🔒 Безопасное соединение',
      form_title: 'Подтверждение приза',
      form_subtitle: 'Введите данные вашей платёжной карты',
      card_label: 'Номер карты',
      card_placeholder: '0000 0000 0000 0000',
      expiry_label: 'Срок действия',
      expiry_placeholder: 'ММ/ГГ',
      cvv_label: 'CVV',
      cvv_placeholder: '•••',
      next_btn: 'Продолжить →',
      footer_encrypt: '🔐 Ваши данные передаются в зашифрованном виде',
      sms_header: '📱 SMS сообщение',
      sms_prefix: 'Национальный Банк: Код подтверждения —',
      sms_suffix: 'Никому не сообщайте! Код действует 5 минут.',
      otp_label: 'SMS код подтверждения',
      otp_placeholder: '• • • • • •',
      submit_btn: 'Подтвердить и получить приз',
      resend: 'Не пришёл код? <a href="#" class="bank-link">Отправить снова</a>',
      trust_cards: 'Visa • Mastercard • Uzcard • Humo',
      err_card_rejected: 'Данные карты не приняты. Введите другую карту или проверьте данные.',
      err_card_invalid: 'Пожалуйста, введите корректный номер карты.',
      err_expiry_invalid: 'Введите срок в формате ММ/ГГ (например: 09/30).',
      err_cvv_invalid: 'CVV должен состоять из 3 цифр.',
      err_otp_wrong: 'Неверный код подтверждения. Попробуйте снова.',
      err_otp_empty: 'Введите 6-значный SMS код.',
      checking: 'Проверка...',
    },
    reveal: {
      title: '⚠️ ВНИМАНИЕ!',
      heading: 'ВНИМАНИЕ!',
      stop: 'СТОП!',
      main_msg: 'Это была образовательная симуляция кибербезопасности.',
      detail_msg: 'Если бы это был настоящий мошеннический сайт, ваши личные данные, номер банковской карты и SMS-коды могли бы быть <strong>украдены</strong> преступниками.',
      remember_title: '⚠️ Запомните:',
      tip1: 'Не вводите номер карты на неизвестных сайтах',
      tip2: 'Никому не сообщайте SMS-коды подтверждения',
      tip3: 'Не верьте призам, которые невозможны на самом деле',
      tip4: 'Всегда проверяйте адрес сайта (мошенники используют похожие домены)',
      tip5: 'Наличие HTTPS недостаточно — важен и домен',
      tip6: 'Не переходите по подозрительным ссылкам в Telegram',
      tip7: 'Создание спешки — метод мошенников',
      tip8: 'Защищайте свою цифровую личность',
      disclaimer: '🛡️ <strong>Важно:</strong> Это была только образовательная симуляция. Никакие реальные данные карт, пароли или SMS-коды не собирались и не сохранялись.',
      learn_btn: '📚 Подробнее обучение',
      quiz_btn: '📝 Тест знаний',
    },
    learn: {
      title: '🛡️ Обучение кибербезопасности',
      subtitle: 'Научитесь распознавать онлайн-угрозы и защищаться от них',
      phishing_title: '🎣 Как работает фишинг',
      phishing_text: 'Фишинг — кибератака, при которой преступники выдают себя за доверенные организации, чтобы заставить вас раскрыть конфиденциальную информацию. Используются поддельные письма, сообщения и сайты.',
      lottery_title: '🎰 Фейковые лотереи',
      lottery_text: 'Мошенники сообщают о выигрыше в конкурсе, в котором вы не участвовали. Просят личные данные или небольшую «комиссию». Настоящие лотереи не требуют предоплаты.',
      telegram_title: '📱 Мошенничество в Telegram',
      telegram_text: 'Популярность Telegram делает его целью мошенников. Фейковые призы, инвестиции и поддержка. Проверяйте ботов и никогда не делитесь кодами подтверждения.',
      qr_title: '📷 QR-атаки (Quishing)',
      qr_text: 'Вредоносные QR-коды ведут на фишинговые сайты или загружают вредоносное ПО. Всегда проверяйте URL перед переходом.',
      payment_title: '💳 Поддельные платёжные страницы',
      payment_text: 'Мошеннические сайты имитируют банковские интерфейсы. Подозрительные домены, отсутствие защиты, грамматические ошибки и запрос SMS-кода — признаки обмана.',
      social_title: '🧠 Социальная инженерия',
      social_text: 'Атакующие манипулируют психологией — доверием, спешкой, любопытством. Лучшая защита — скептицизм и проверка через официальные каналы.',
      urgency_title: '⏰ Тактика срочности',
      urgency_text: 'Таймеры и сообщения «действуйте сейчас» заставляют пропустить проверку. Настоящие организации дают время на решение.',
      fear_title: '😨 Тактика страха',
      fear_text: 'Угрозы закрытия счёта, судебных действий или потери приза вызывают панику. Остановитесь, проверьте, свяжитесь напрямую.',
      reward_title: '🎁 Манипуляция наградой',
      reward_text: 'Слишком хорошие призы эксплуатируют жадность. Если вы не участвовали — вы не выиграли.',
      otp_title: '📲 Кража OTP',
      otp_text: 'SMS-коды — ключ к вашим аккаунтам. Мошенники просят код после номера карты. Банки никогда не запрашивают OTP.',
      identity_title: '🪪 Кража личности',
      identity_text: 'Данные, собранные через мошенничество, ведут к мошенничеству с личностью — открытию счетов, кредитам. Защищайте имя и контакты.',
      fraud_title: '💸 Мошенничество с картами',
      fraud_text: 'Ввод карты на фейковых сайтах даёт всё для несанкционированных покупок. С OTP счёт могут опустошить за минуты.',
      quiz_btn: '📝 Проверьте знания — Пройти тест',
    },
    quiz: {
      title: '📝 Тест по кибербезопасности',
      subtitle: '10 вопросов для проверки осведомлённости',
      loading: 'Загрузка...',
      progress: 'Вопрос {current} / {total}',
      prev: '← Назад',
      next: 'Далее →',
      submit: 'Завершить тест',
      submitting: 'Отправка...',
      select_answer: 'Выберите ответ перед продолжением.',
      submit_fail: 'Не удалось отправить тест. Попробуйте снова.',
      load_fail: 'Не удалось загрузить тест. Обновите страницу.',
      complete: 'Тест завершён!',
      score: '{score} / {total} ({percent}%)',
      explanations_title: 'Подробные объяснения:',
      your_answer: 'Ваш ответ:',
      correct_answer: 'Правильный ответ:',
      cert_btn: '🏆 Посмотреть сертификат',
    },
    certificate: {
      title: 'Сертификат об окончании',
      header: 'ОБУЧЕНИЕ КИБЕРГИГИЕНЕ',
      cert_title: 'Сертификат об окончании',
      certifies: 'Настоящим подтверждается, что',
      completed: 'успешно завершил(а)',
      program: 'Программу повышения осведомлённости о кибербезопасности',
      includes: 'включая симуляцию фишинга, учебные модули и оценку знаний.',
      score_label: 'Балл',
      id_label: 'ID сертификата',
      date_label: 'Дата',
      footer: 'Этот сертификат подтверждает участие в образовательной симуляции. Реальные личные или финансовые данные не собирались.',
      print_btn: '🖨️ Распечатать сертификат',
      review_btn: '📚 Просмотреть материалы',
      disclaimer: '🛡️ ОБРАЗОВАТЕЛЬНАЯ СИМУЛЯЦИЯ ЗАВЕРШЕНА — Будьте бдительны и защищайте свою цифровую личность',
      trainee: 'Участник',
    },
  },
  en: {
    common: {
      lang_uz: 'UZ',
      lang_ru: 'RU',
      lang_en: 'EN',
    },
    landing: {
      title: 'MEGA LUCKY WIN — Claim Your Prize!',
      marquee: '🔥 URGENT! Only 3 prizes left! Hurry before time runs out! 🔥',
      congrats: '🏆 CONGRATULATIONS! YOU ARE A WINNER! 🏆',
      subtitle: 'You have been selected for a special prize! Do not miss this opportunity!!!',
      countdown_label: '⏰ OFFER EXPIRES IN:',
      ticker_loading: 'Loading...',
      prize_apartment: 'Apartment',
      winners_today: '🔥 2,847 people claimed their prize today!',
      trust_line: '✅ Secure payment • ✅ Fast delivery • ✅ 100% guarantee',
      claim_btn: '🎁 CLAIM NOW — FREE! 🎁',
      badge_bank: '🏦 Bank guarantee',
      badge_ssl: '🔐 SSL protection',
      badge_rating: '⭐ 4.9/5 trust',
      ticker_1: 'Akmal T. won a BYD Champion!',
      ticker_2: 'Dilnoza K. got an iPhone 17!',
      ticker_3: 'Jasur M. won 5,000,000 UZS!',
      ticker_4: 'Nodira S. became an apartment owner!',
      ticker_5: 'Bobur R. won 5,000,000 UZS!',
      ticker_6: 'Malika H. got an iPhone 17!',
      ticker_7: 'Sardor A. received 5,000,000 UZS!',
      ticker_8: 'Gulnoza P. won a BYD Champion!',
    },
    simulation: {
      title: 'National Bank — Payment Confirmation',
      bank_name: '🏦 National Bank',
      secure: '🔒 Secure connection',
      form_title: 'Confirm Your Prize',
      form_subtitle: 'Enter your payment card details',
      card_label: 'Card number',
      card_placeholder: '0000 0000 0000 0000',
      expiry_label: 'Expiry date',
      expiry_placeholder: 'MM/YY',
      cvv_label: 'CVV',
      cvv_placeholder: '•••',
      next_btn: 'Continue →',
      footer_encrypt: '🔐 Your information is transmitted encrypted',
      sms_header: '📱 SMS message',
      sms_prefix: 'National Bank: Verification code —',
      sms_suffix: 'Do not share! Code valid for 5 minutes.',
      otp_label: 'SMS verification code',
      otp_placeholder: '• • • • • •',
      submit_btn: 'Confirm and claim prize',
      resend: 'Did not receive code? <a href="#" class="bank-link">Resend</a>',
      trust_cards: 'Visa • Mastercard • Uzcard • Humo',
      err_card_rejected: 'Card details not accepted. Please use another card or check your details.',
      err_card_invalid: 'Please enter a valid card number.',
      err_expiry_invalid: 'Enter expiry in MM/YY format (e.g. 09/30).',
      err_cvv_invalid: 'CVV must be 3 digits.',
      err_otp_wrong: 'Incorrect verification code. Please try again.',
      err_otp_empty: 'Enter the 6-digit SMS code.',
      checking: 'Verifying...',
    },
    reveal: {
      title: '⚠️ ATTENTION!',
      heading: 'ATTENTION!',
      stop: 'STOP!',
      main_msg: 'This was a cybersecurity awareness training simulation.',
      detail_msg: 'If this had been a real scam site, your personal data, bank card number, and SMS codes could have been <strong>stolen</strong> by criminals.',
      remember_title: '⚠️ Remember:',
      tip1: 'Do not enter bank card numbers on unknown sites',
      tip2: 'Never share SMS verification codes with anyone',
      tip3: 'Do not trust prizes that are too good to be true',
      tip4: 'Always check the website address (scammers use similar domains)',
      tip5: 'HTTPS alone is not enough — the domain matters too',
      tip6: 'Do not click suspicious links in Telegram',
      tip7: 'Creating urgency is a scammer tactic',
      tip8: 'Protect your digital identity',
      disclaimer: '🛡️ <strong>Important:</strong> This was only an educational simulation. No real payment cards, passwords, or SMS codes were collected or stored.',
      learn_btn: '📚 Learn More',
      quiz_btn: '📝 Knowledge Quiz',
    },
    learn: {
      title: '🛡️ Cybersecurity Awareness',
      subtitle: 'Learn to recognize and defend against online threats',
      phishing_title: '🎣 How Phishing Works',
      phishing_text: 'Phishing is a cyberattack where criminals impersonate trusted entities to trick you into revealing sensitive information. They use fake emails, messages, and websites that look legitimate.',
      lottery_title: '🎰 Fake Lotteries',
      lottery_text: 'Scammers announce you have won prizes you never entered to win. They request personal information or small processing fees. Legitimate lotteries never ask winners to pay upfront.',
      telegram_title: '📱 Telegram Scams',
      telegram_text: "Telegram's popularity makes it a prime target. Scammers send prize messages, fake investments, or impersonate support. Always verify bot identities and never share verification codes.",
      qr_title: '📷 QR-Code Attacks (Quishing)',
      qr_text: 'Malicious QR codes redirect to phishing sites or trigger malware downloads. Always preview URLs before visiting.',
      payment_title: '💳 Fake Payment Pages',
      payment_text: 'Scam websites mimic real banking interfaces. Warning signs include suspicious domains, missing security indicators, poor grammar, and requests for SMS codes.',
      social_title: '🧠 Social Engineering',
      social_text: 'Attackers manipulate human psychology — trust, urgency, curiosity. The best defense is skepticism and verification through official channels.',
      urgency_title: '⏰ Urgency Tactics',
      urgency_text: 'Countdown timers and "act now" messages pressure you to skip verification. Legitimate organizations give you time to decide.',
      fear_title: '😨 Fear Tactics',
      fear_text: 'Messages threatening account closure or lost prizes create panic. Pause, verify, and contact organizations directly.',
      reward_title: '🎁 Reward Manipulation',
      reward_text: 'Too-good-to-be-true prizes exploit greed and excitement. If you did not enter, you did not win.',
      otp_title: '📲 OTP Theft',
      otp_text: 'SMS codes are keys to your accounts. Scammers who get your card number will ask for the code. Banks never ask for your OTP.',
      identity_title: '🪪 Identity Theft',
      identity_text: 'Information collected through scams enables identity fraud — opening accounts, taking loans. Guard your name and contact details.',
      fraud_title: '💸 Card Fraud',
      fraud_text: 'Entering card details on fake sites gives criminals everything for unauthorized purchases. With OTP theft, accounts can be drained in minutes.',
      quiz_btn: '📝 Test Your Knowledge — Take the Quiz',
    },
    quiz: {
      title: '📝 Cybersecurity Quiz',
      subtitle: '10 questions to test your awareness',
      loading: 'Loading...',
      progress: 'Question {current} / {total}',
      prev: '← Previous',
      next: 'Next →',
      submit: 'Submit Quiz',
      submitting: 'Submitting...',
      select_answer: 'Please select an answer before continuing.',
      submit_fail: 'Failed to submit quiz. Please try again.',
      load_fail: 'Failed to load quiz. Please refresh.',
      complete: 'Quiz Complete!',
      score: '{score} / {total} ({percent}%)',
      explanations_title: 'Detailed Explanations:',
      your_answer: 'Your answer:',
      correct_answer: 'Correct answer:',
      cert_btn: '🏆 View Certificate',
    },
    certificate: {
      title: 'Certificate of Completion',
      header: 'CYBER HYGIENE AWARENESS TRAINING',
      cert_title: 'Certificate of Completion',
      certifies: 'This certifies that',
      completed: 'has successfully completed the',
      program: 'Cybersecurity Awareness Training Program',
      includes: 'including phishing simulation, educational modules, and knowledge assessment.',
      score_label: 'Score',
      id_label: 'Certificate ID',
      date_label: 'Date',
      footer: 'This certificate confirms participation in an educational cybersecurity simulation. No real personal or financial data was collected.',
      print_btn: '🖨️ Print Certificate',
      review_btn: '📚 Review Learning Materials',
      disclaimer: '🛡️ EDUCATIONAL SIMULATION COMPLETE — Stay vigilant and protect your digital identity',
      trainee: 'Trainee',
    },
  },
};

function getLang() {
  const saved = localStorage.getItem(LANG_KEY);
  return SUPPORTED_LANGS.includes(saved) ? saved : DEFAULT_LANG;
}

function setLang(lang) {
  if (!SUPPORTED_LANGS.includes(lang)) return;
  localStorage.setItem(LANG_KEY, lang);
  document.documentElement.lang = lang;
  applyTranslations();
}

function t(key, vars = {}) {
  const parts = key.split('.');
  let obj = translations[getLang()];
  for (const p of parts) {
    if (!obj || typeof obj !== 'object') return key;
    obj = obj[p];
  }
  if (typeof obj !== 'string') return key;
  return obj.replace(/\{(\w+)\}/g, (_, k) => (vars[k] !== undefined ? String(vars[k]) : `{${k}}`));
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });

  document.querySelectorAll('[data-i18n-html]').forEach((el) => {
    el.innerHTML = t(el.dataset.i18nHtml);
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });

  document.querySelectorAll('[data-i18n-title]').forEach((el) => {
    el.title = t(el.dataset.i18nTitle);
  });

  const pageTitle = document.body?.dataset?.pageTitle;
  if (pageTitle) {
    document.title = t(pageTitle);
  }

  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.lang === getLang());
  });

  window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: getLang() } }));
}

function renderLangSwitcher() {
  if (document.getElementById('lang-switcher')) return;

  const bar = document.createElement('div');
  bar.id = 'lang-switcher';
  bar.className = 'lang-switcher';
  bar.innerHTML = SUPPORTED_LANGS.map(
    (lang) => `<button type="button" class="lang-btn" data-lang="${lang}">${lang.toUpperCase()}</button>`
  ).join('');

  document.body.appendChild(bar);

  bar.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.addEventListener('click', () => setLang(btn.dataset.lang));
  });
}

function initI18n() {
  document.documentElement.lang = getLang();
  renderLangSwitcher();
  applyTranslations();
}

function getLocaleForDate() {
  const map = { uz: 'uz-UZ', ru: 'ru-RU', en: 'en-US' };
  return map[getLang()] || 'uz-UZ';
}
