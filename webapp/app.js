// ==========================================================================
// WOW ENGLISH — TELEGRAM MINI APP CONTROLLER & LOGIC
// ==========================================================================

const tg = window.Telegram?.WebApp;
if (tg) {
  try {
    tg.ready();
    tg.expand();
    if (tg.disableVerticalSwipes) {
      tg.disableVerticalSwipes();
    }
  } catch (e) {
    console.log("Telegram WebApp init:", e);
  }
}

// Global State & Language Config
const SUPPORTED_LANGS = {
  'en': { name: 'English', nativeName: 'English', flag: '🇬🇧', short: 'EN', speechCode: 'en-US' },
  'ru': { name: 'Русский', nativeName: 'Русский', flag: '🇷🇺', short: 'RU', speechCode: 'ru-RU' },
  'uk': { name: 'Українська', nativeName: 'Українська (Украинский)', flag: '🇺🇦', short: 'UK', speechCode: 'uk-UA' },
  'es': { name: 'Español', nativeName: 'Español (Испанский)', flag: '🇪🇸', short: 'ES', speechCode: 'es-ES' },
  'fr': { name: 'Français', nativeName: 'Français (Французский)', flag: '🇫🇷', short: 'FR', speechCode: 'fr-FR' },
  'de': { name: 'Deutsch', nativeName: 'Deutsch (Немецкий)', flag: '🇩🇪', short: 'DE', speechCode: 'de-DE' },
  'it': { name: 'Italiano', nativeName: 'Italiano (Итальянский)', flag: '🇮🇹', short: 'IT', speechCode: 'it-IT' },
  'sl': { name: 'Slovenščina', nativeName: 'Slovenščina (Словенский)', flag: '🇸🇮', short: 'SL', speechCode: 'sl-SI' }
};

const I18N = {
  ru: {
    streakSuffix: "дней",
    streakTitle: "Серия дней обучения",
    langPickerTitle: "Выбрать языки",
    themeToggle: "Переключить тему",
    myVocab: "Мой словарь",
    filterAll: "Все",
    filterLearning: "Учу",
    filterKnown: "Знаю",
    cardOf: "Карточка",
    of: "из",
    stampKnown: "ЗНАЮ",
    stampLearning: "УЧУ",
    hintRememberTrans: "Вспомните перевод (клик для проверки)",
    hintRateResponse: "Оцените ваш ответ:",
    hintListenRate: "Послушайте произношение и оцените ответ:",
    actionLearning: "Учу",
    actionLearningSub: "Свайп вправо",
    actionDelete: "Удалить",
    actionDeleteSub: "Свайп вниз",
    actionKnown: "Знаю",
    actionKnownSub: "Свайп влево",
    hintFlip: "Перевернуть",
    catEmptyTag: "+ Категория",
    catPickerTitle: "Категория карточки",
    catPickerSubtitle: "Выберите тему или введите свою",
    catPickerCustom: "Или введите свою категорию:",
    catPickerRemove: "Без категории",
    catPickerSave: "Сохранить",
    emptyVocabTitle: "Ваш личный словарь пока пуст 🌱",
    emptyVocabSub: "Нажмите «Добавить», чтобы внести первую фразу ✨",
    emptyKnownTitle: "Раздел «Знаю» пуст",
    emptyKnownSub: "Отмечайте карточки кнопкой «Знаю» во время тренировки раздела «Все».",
    emptyLearningTitle: "Все карточки освоены! 🎉",
    emptyLearningSub: "Отличная работа. Переключитесь на «Все» или «Знаю» для повторения.",
    searchPlaceholder: "Поиск слова или перевод...",
    btnAddWord: "Добавить",
    btnExportExcel: "Экспорт в Excel",
    catAll: "Все",
    catGeneral: "Разговорный / Общее",
    catBusiness: "Деловая переписка",
    catLogistics: "Логистика и ВЭД",
    catInterview: "Собеседование",
    dictEmptyTitle: "Ваш личный словарь пуст",
    dictEmptyDesc: "Вы начинаете с чистого листа! Добавляйте свои фразы, и они сохранятся только в вашем личном аккаунте.",
    dictEmptyBtn: "Добавить первую фразу",
    dictSearchEmpty: "Ничего не найдено",
    dictSearchEmptyDesc: "Попробуйте изменить поисковый запрос или фильтр категории.",
    bentoVocab: "Словарь",
    bentoTotalCards: "Всего карточек",
    bentoKnown: "Знаю",
    bentoSolidMastery: "Твердые знания",
    bentoLearning: "Учу",
    bentoInProgress: "В процессе",
    bentoStreak: "Серия",
    bentoDaysInRow: "Дней подряд",
    masteryLabel: "Освоено словаря",
    adminTitle: "Метрики & Аудитория",
    adminExportExcel: "Excel отчёт",
    adminTotalUsers: "Всего пользователей",
    adminNewToday: "сегодня",
    adminLaunchedApp: "Запустили тренажёр",
    adminGrowth7d: "Прирост (7 дней)",
    adminRegistrations7d: "Регистраций за неделю",
    adminActiveToday: "Активных сегодня",
    adminWau: "за 7 дней (WAU)",
    adminTotalCardsInDb: "Всего карточек в базе",
    adminAvgPerUser: "ср./чел",
    adminActivityDynamics: "Динамика активности (последние 7 дней)",
    adminActiveUsersLegend: "Активные пользователи",
    adminLangBreakdown: "🌍 Распределение по изучаемым языкам",
    adminLangsCount: "8 языков",
    adminStudentsList: "Список учеников",
    adminSearchPlaceholder: "Поиск по имени или @нику...",
    adminStudentsNotFound: "Ученики не найдены",
    dockCards: "Карточки",
    dockDict: "Словарь",
    dockProgress: "Прогресс",
    dockAnalytics: "Аналитика",
    modalLangTitle: "Выбор языков",
    modalLangSubtitle: "Родной язык и язык для изучения",
    modalLangSec1: "1. Мой родной язык:",
    modalLangSec2: "2. Я хочу учить:",
    modalLangSave: "Сохранить выбор",
    modalAddSingle: "1 фраза",
    modalAddBulk: "Пачкой (Excel)",
    aiStatusActive: "AI автоперевод активен",
    aiStatusThinking: "AI думает над фразой...",
    aiStatusTranslating: "AI переводит...",
    aiStatusReady: "Живой перевод готов ✨",
    phraseIn: "Фраза на",
    translationIn: "Перевод на",
    btnSwap: "Поменять местами",
    aiAltHeader: "Живые разговорные варианты:",
    categoryLabel: "Категория:",
    btnSaveCard: "Сохранить в карточки",
    bulkLabel: "Вставьте строки из Excel или чата:",
    bulkPlaceholder: "Скопируйте 2 колонки из Excel или текст вида:\nTo keep you posted - Держать в курсе\nShorten the lead time — Сократить срок доставки",
    bulkDetected: "Найдено карточек:",
    btnSaveBulk: "Импортировать все фразы",
    supportBtn: "Помощь",
    supportBtnTitle: "Связь с разработчиком / Помощь",
    modalSupportTitle: "Связь с разработчиком",
    modalSupportSubtitle: "Есть идея, вопрос или нашли ошибку? Напишите нам!",
    supportCatLabel: "Выберите тему:",
    supportMsgLabel: "Ваше сообщение:",
    supportMsgPlaceholder: "Опишите вашу идею, вопрос или пожелание...",
    btnDirectTg: "Написать в Telegram",
    btnSendSupport: "Отправить",
    supportSuccess: "✅ Сообщение отправлено! Разработчик скоро ответит вам.",
    supportEmptyError: "Пожалуйста, введите текст сообщения."
  },
  uk: {
    streakSuffix: "днів",
    streakTitle: "Серія днів навчання",
    langPickerTitle: "Обрати мови",
    themeToggle: "Змінити тему",
    myVocab: "Мій словник",
    filterAll: "Всі",
    filterLearning: "Вчу",
    filterKnown: "Знаю",
    cardOf: "Картка",
    of: "з",
    stampKnown: "ЗНАЮ",
    stampLearning: "ВЧУ",
    hintRememberTrans: "Згадайте переклад (клік для перевірки)",
    hintRateResponse: "Оцініть вашу відповідь:",
    hintListenRate: "Послухайте вимову та оцініть відповідь:",
    actionLearning: "Вчу",
    actionLearningSub: "Свайп вправо",
    actionDelete: "Видалити",
    actionDeleteSub: "Свайп униз",
    actionKnown: "Знаю",
    actionKnownSub: "Свайп вліво",
    hintFlip: "Перевернути",
    catEmptyTag: "+ Категорія",
    catPickerTitle: "Категорія картки",
    catPickerSubtitle: "Оберіть тему або введіть свою",
    catPickerCustom: "Або введіть свою категорію:",
    catPickerRemove: "Без категорії",
    catPickerSave: "Зберегти",
    emptyVocabTitle: "Ваш особистий словник поки що порожній 🌱",
    emptyVocabSub: "Натисніть «Додати», щоб внести першу фразу ✨",
    emptyKnownTitle: "Розділ «Знаю» порожній",
    emptyKnownSub: "Відзначайте картки кнопкою «Знаю» під час тренування розділу «Всі».",
    emptyLearningTitle: "Всі картки засвоєно! 🎉",
    emptyLearningSub: "Чудова робота. Перемкніться на «Всі» або «Знаю» для повторення.",
    searchPlaceholder: "Пошук слова або перекладу...",
    btnAddWord: "Додати",
    btnExportExcel: "Експорт в Excel",
    catAll: "Всі",
    catGeneral: "Розмовна / Загальне",
    catBusiness: "Ділове листування",
    catLogistics: "Логістика та ЗЕД",
    catInterview: "Співбесіда",
    dictEmptyTitle: "Ваш особистий словник порожній",
    dictEmptyDesc: "Ви починаєте з чистого аркуша! Додавайте власні фрази, і вони збережуться у вашому акаунті.",
    dictEmptyBtn: "Додати першу фразу",
    dictSearchEmpty: "Нічого не знайдено",
    dictSearchEmptyDesc: "Спробуйте змінити пошуковий запит або категорію.",
    bentoVocab: "Словник",
    bentoTotalCards: "Всього карток",
    bentoKnown: "Знаю",
    bentoSolidMastery: "Міцні знання",
    bentoLearning: "Вчу",
    bentoInProgress: "У процесі",
    bentoStreak: "Серія",
    bentoDaysInRow: "Днів поспіль",
    masteryLabel: "Освоєно словника",
    adminTitle: "Метрики та Аудиторія",
    adminExportExcel: "Excel звіт",
    adminTotalUsers: "Всього користувачів",
    adminNewToday: "сьогодні",
    adminLaunchedApp: "Запустили тренажер",
    adminGrowth7d: "Приріст (7 днів)",
    adminRegistrations7d: "Реєстрацій за тиждень",
    adminActiveToday: "Активних сьогодні",
    adminWau: "за 7 днів (WAU)",
    adminTotalCardsInDb: "Всього карток у базі",
    adminAvgPerUser: "сер./корист.",
    adminActivityDynamics: "Динаміка активності (останні 7 днів)",
    adminActiveUsersLegend: "Активні користувачі",
    adminLangBreakdown: "🌍 Розподіл за мовами навчання",
    adminLangsCount: "8 мов",
    adminStudentsList: "Список учнів",
    adminSearchPlaceholder: "Пошук за ім'ям або @ніком...",
    adminStudentsNotFound: "Учнів не знайдено",
    dockCards: "Картки",
    dockDict: "Словник",
    dockProgress: "Прогрес",
    dockAnalytics: "Аналітика",
    modalLangTitle: "Вибір мов",
    modalLangSubtitle: "Рідна мова та мова для вивчення",
    modalLangSec1: "1. Моя рідна мова:",
    modalLangSec2: "2. Я хочу вчити:",
    modalLangSave: "Зберегти вибір",
    modalAddSingle: "1 фраза",
    modalAddBulk: "Пачкою (Excel)",
    aiStatusActive: "AI автопереклад активний",
    aiStatusThinking: "AI міркує над фразою...",
    aiStatusTranslating: "AI перекладає...",
    aiStatusReady: "Живий переклад готовий ✨",
    phraseIn: "Фраза мовою",
    translationIn: "Переклад мовою",
    btnSwap: "Поміняти місцями",
    aiAltHeader: "Живі розмовні варіанти:",
    categoryLabel: "Категорія:",
    btnSaveCard: "Зберегти у картки",
    bulkLabel: "Вставте рядки з Excel або чату:",
    bulkPlaceholder: "Скопіюйте 2 колонки з Excel або текст вигляду:\nTo keep you posted - Тримати в курсі\nShorten the lead time — Скоротити термін доставки",
    bulkDetected: "Знайдено карток:",
    btnSaveBulk: "Імпортувати всі фрази",
    supportBtn: "Допомога",
    supportBtnTitle: "Зв'язок з розробником / Допомога",
    modalSupportTitle: "Зв'язок з розробником",
    modalSupportSubtitle: "Є ідея, питання або знайшли помилку? Напишіть нам!",
    supportCatLabel: "Оберіть тему:",
    supportMsgLabel: "Ваше повідомлення:",
    supportMsgPlaceholder: "Опишіть вашу ідею, питання або побажання...",
    btnDirectTg: "Написати в Telegram",
    btnSendSupport: "Надіслати",
    supportSuccess: "✅ Повідомлення надіслано! Розробник незабаром відповість вам.",
    supportEmptyError: "Будь ласка, введіть текст повідомлення."
  },
  en: {
    streakSuffix: "days",
    streakTitle: "Learning Streak Days",
    langPickerTitle: "Choose Languages",
    themeToggle: "Toggle Theme",
    myVocab: "My Vocabulary",
    filterAll: "All",
    filterLearning: "Learning",
    filterKnown: "Mastered",
    cardOf: "Card",
    of: "of",
    stampKnown: "MASTERED",
    stampLearning: "LEARNING",
    hintRememberTrans: "Recall the translation (tap to reveal)",
    hintRateResponse: "Rate your answer:",
    hintListenRate: "Listen to pronunciation and rate your answer:",
    actionLearning: "Learning",
    actionLearningSub: "Swipe right",
    actionDelete: "Delete",
    actionDeleteSub: "Swipe down",
    actionKnown: "Mastered",
    actionKnownSub: "Swipe left",
    hintFlip: "Flip Card",
    catEmptyTag: "+ Category",
    catPickerTitle: "Card Category",
    catPickerSubtitle: "Select topic or create a new one",
    catPickerCustom: "Or enter a custom category:",
    catPickerRemove: "No category",
    catPickerSave: "Save Category",
    emptyVocabTitle: "Your vocabulary is currently empty 🌱",
    emptyVocabSub: "Tap «Add» to create your first flashcard ✨",
    emptyKnownTitle: "Mastered section is empty",
    emptyKnownSub: "Mark cards as «Mastered» during practice to move them here.",
    emptyLearningTitle: "All cards mastered! 🎉",
    emptyLearningSub: "Great job. Switch to «All» or «Mastered» to review.",
    searchPlaceholder: "Search phrase or translation...",
    btnAddWord: "Add",
    btnExportExcel: "Export Excel",
    catAll: "All",
    catGeneral: "General / Conversational",
    catBusiness: "Business & Emails",
    catLogistics: "Logistics & Supply Chain",
    catInterview: "Job Interview",
    dictEmptyTitle: "Your vocabulary is empty",
    dictEmptyDesc: "Start fresh! Add your own custom phrases, stored privately in your account.",
    dictEmptyBtn: "Add First Phrase",
    dictSearchEmpty: "No phrases found",
    dictSearchEmptyDesc: "Try adjusting your search query or category filter.",
    bentoVocab: "Vocabulary",
    bentoTotalCards: "Total Cards",
    bentoKnown: "Mastered",
    bentoSolidMastery: "Solid Mastery",
    bentoLearning: "Learning",
    bentoInProgress: "In Progress",
    bentoStreak: "Streak",
    bentoDaysInRow: "Days in a Row",
    masteryLabel: "Vocabulary Mastered",
    adminTitle: "Metrics & Audience",
    adminExportExcel: "Excel Report",
    adminTotalUsers: "Total Users",
    adminNewToday: "today",
    adminLaunchedApp: "Launched App",
    adminGrowth7d: "Growth (7 Days)",
    adminRegistrations7d: "Registrations this week",
    adminActiveToday: "Active Today",
    adminWau: "last 7 days (WAU)",
    adminTotalCardsInDb: "Total Cards in DB",
    adminAvgPerUser: "avg/user",
    adminActivityDynamics: "Activity Dynamics (Last 7 Days)",
    adminActiveUsersLegend: "Active Users",
    adminLangBreakdown: "🌍 Learning Languages Distribution",
    adminLangsCount: "8 languages",
    adminStudentsList: "Students Roster",
    adminSearchPlaceholder: "Search by name or @username...",
    adminStudentsNotFound: "No students found",
    dockCards: "Cards",
    dockDict: "Dictionary",
    dockProgress: "Progress",
    dockAnalytics: "Analytics",
    modalLangTitle: "Language Settings",
    modalLangSubtitle: "Native language and target language",
    modalLangSec1: "1. My native language:",
    modalLangSec2: "2. I want to learn:",
    modalLangSave: "Save & Apply",
    modalAddSingle: "1 Phrase",
    modalAddBulk: "Bulk (Excel)",
    aiStatusActive: "AI Auto-translate active",
    aiStatusThinking: "AI is thinking...",
    aiStatusTranslating: "AI is translating...",
    aiStatusReady: "Smart translation ready ✨",
    phraseIn: "Phrase in",
    translationIn: "Translation in",
    btnSwap: "Swap Fields",
    aiAltHeader: "Natural conversational alternatives:",
    categoryLabel: "Category:",
    btnSaveCard: "Save to Flashcards",
    bulkLabel: "Paste rows from Excel or chat:",
    bulkPlaceholder: "Copy 2 columns from Excel or text like:\nTo keep you posted - Keep informed\nShorten the lead time — Reduce delivery time",
    bulkDetected: "Cards detected:",
    btnSaveBulk: "Import All Phrases",
    supportBtn: "Help",
    supportBtnTitle: "Contact Developer / Help",
    modalSupportTitle: "Contact Developer",
    modalSupportSubtitle: "Have an idea, question or found a bug? Send us a message!",
    supportCatLabel: "Select topic:",
    supportMsgLabel: "Your message:",
    supportMsgPlaceholder: "Describe your idea, question or feedback...",
    btnDirectTg: "Message on Telegram",
    btnSendSupport: "Send Message",
    supportSuccess: "✅ Message sent! The developer will reply shortly.",
    supportEmptyError: "Please enter your message."
  },
  sl: {
    streakSuffix: "dni",
    streakTitle: "Dnevi učenja zapored",
    langPickerTitle: "Izberi jezike",
    themeToggle: "Preklopi temo",
    myVocab: "Moj besednjak",
    filterAll: "Vse",
    filterLearning: "Učim se",
    filterKnown: "Znam",
    cardOf: "Kartica",
    of: "od",
    stampKnown: "ZNAM",
    stampLearning: "UČIM SE",
    hintRememberTrans: "Spomnite se prevoda (klik za ogled)",
    hintRateResponse: "Ocenite svoj odgovor:",
    hintListenRate: "Poslušajte izgovorjavo in ocenite odgovor:",
    actionLearning: "Učim se",
    actionLearningSub: "Podrsaj desno",
    actionDelete: "Izbriši",
    actionDeleteSub: "Podrsaj navzdol",
    actionKnown: "Znam",
    actionKnownSub: "Podrsaj levo",
    hintFlip: "Obrni",
    catEmptyTag: "+ Kategorija",
    catPickerTitle: "Kategorija kartice",
    catPickerSubtitle: "Izberite temo ali vnesite svojo",
    catPickerCustom: "Ali vnesite svojo kategorijo:",
    catPickerRemove: "Brez kategorije",
    catPickerSave: "Shrani",
    emptyVocabTitle: "Vaš osebni besednjak je trenutno prazen 🌱",
    emptyVocabSub: "Pritisnite «Dodaj», da vnesete prvo frazo ✨",
    emptyKnownTitle: "Razdelek «Znam» je prazen",
    emptyKnownSub: "Označite kartice z «Znam» med vadbo razdelka «Vse».",
    emptyLearningTitle: "Vse kartice so osvojene! 🎉",
    emptyLearningSub: "Odlično delo. Preklopite na «Vse» ali «Znam» za ponavljanje.",
    searchPlaceholder: "Iskanje besede ali prevoda...",
    btnAddWord: "Dodaj",
    btnExportExcel: "Izvozi v Excel",
    catAll: "Vse",
    catGeneral: "Pogovorno / Splošno",
    catBusiness: "Poslovna sporočila",
    catLogistics: "Logistika in dobava",
    catInterview: "Razgovor za službo",
    dictEmptyTitle: "Vaš besednjak je prazen",
    dictEmptyDesc: "Začnite na novo! Dodajte svoje fraze, ki se shranijo v vaš osebni račun.",
    dictEmptyBtn: "Dodaj prvo frazo",
    dictSearchEmpty: "Ni zadetkov",
    dictSearchEmptyDesc: "Poskusite spremeniti iskalni niz ali kategorijo.",
    bentoVocab: "Besednjak",
    bentoTotalCards: "Vseh kartic",
    bentoKnown: "Znam",
    bentoSolidMastery: "Trdno znanje",
    bentoLearning: "Učim se",
    bentoInProgress: "V teku",
    bentoStreak: "Niz",
    bentoDaysInRow: "Dni zapored",
    masteryLabel: "Osvojeno besedišče",
    adminTitle: "Metrike in Obiskovalci",
    adminExportExcel: "Excel poročilo",
    adminTotalUsers: "Vseh uporabnikov",
    adminNewToday: "danes",
    adminLaunchedApp: "Zagnana aplikacija",
    adminGrowth7d: "Rast (7 dni)",
    adminRegistrations7d: "Registracij v tednu",
    adminActiveToday: "Aktivnih danes",
    adminWau: "v 7 dneh (WAU)",
    adminTotalCardsInDb: "Vseh kartic v bazi",
    adminAvgPerUser: "povpr./upor.",
    adminActivityDynamics: "Dinamika aktivnosti (zadnjih 7 dni)",
    adminActiveUsersLegend: "Aktivni uporabniki",
    adminLangBreakdown: "🌍 Porazdelitev po jezikih učenja",
    adminLangsCount: "8 jezikov",
    adminStudentsList: "Seznam učencev",
    adminSearchPlaceholder: "Iskanje po imenu ali @uporabniku...",
    adminStudentsNotFound: "Učenci niso bili najdeni",
    dockCards: "Kartice",
    dockDict: "Besednjak",
    dockProgress: "Napredek",
    dockAnalytics: "Analitika",
    modalLangTitle: "Izbira jezikov",
    modalLangSubtitle: "Materni jezik in ciljni jezik učenja",
    modalLangSec1: "1. Moj materni jezik:",
    modalLangSec2: "2. Želim se učiti:",
    modalLangSave: "Shrani izbiro",
    modalAddSingle: "1 fraza",
    modalAddBulk: "Skupinsko (Excel)",
    aiStatusActive: "AI samodejni prevod aktiven",
    aiStatusThinking: "AI razmišlja...",
    aiStatusTranslating: "AI prevaja...",
    aiStatusReady: "Prevajanje pripravljeno ✨",
    phraseIn: "Fraza v jeziku",
    translationIn: "Prevod v jeziku",
    btnSwap: "Zamenjaj polji",
    aiAltHeader: "Naravne pogovorne alternative:",
    categoryLabel: "Kategorija:",
    btnSaveCard: "Shrani med kartice",
    bulkLabel: "Prilepite vrstice iz Excela ali klepeta:",
    bulkPlaceholder: "Kopirajte 2 stolpca iz Excela ali besedilo oblike:\nTo keep you posted - Obveščati sproti\nShorten the lead time — Skrajšati dobavni rok",
    bulkDetected: "Najdenih kartic:",
    btnSaveBulk: "Uvozi vse fraze",
    supportBtn: "Pomoč",
    supportBtnTitle: "Stik z razvijalcem / Pomoč",
    modalSupportTitle: "Stik z razvijalcem",
    modalSupportSubtitle: "Imate idejo, vprašanje ali ste našli napako? Pišite nam!",
    supportCatLabel: "Izberite temo:",
    supportMsgLabel: "Vaše sporočilo:",
    supportMsgPlaceholder: "Opišite vašo idejo, vprašanje ali predlog...",
    btnDirectTg: "Pišite na Telegram",
    btnSendSupport: "Pošlji",
    supportSuccess: "✅ Sporočilo poslano! Razvijalec vam bo kmalu odgovoril.",
    supportEmptyError: "Prosimo, vnesite besedilo sporočila."
  },
  es: {
    streakSuffix: "días",
    streakTitle: "Racha de días de estudio",
    langPickerTitle: "Elegir idiomas",
    themeToggle: "Cambiar tema",
    myVocab: "Mi vocabulario",
    filterAll: "Todas",
    filterLearning: "Aprendiendo",
    filterKnown: "Dominadas",
    cardOf: "Tarjeta",
    of: "de",
    stampKnown: "DOMINADA",
    stampLearning: "APRENDO",
    hintRememberTrans: "Recuerda la traducción (toca para ver)",
    hintRateResponse: "Evalúa tu respuesta:",
    hintListenRate: "Escucha la pronunciación y evalúa:",
    actionLearning: "Aprendo",
    actionLearningSub: "Desliza izq.",
    actionFlip: "Voltear",
    actionFlipSub: "Toca tarjeta",
    actionKnown: "Dominada",
    actionKnownSub: "Desliza der.",
    emptyVocabTitle: "Tu vocabulario está vacío 🌱",
    emptyVocabSub: "Toca «Añadir» para crear tu primera tarjeta ✨",
    emptyKnownTitle: "La sección «Dominadas» está vacía",
    emptyKnownSub: "Marca tarjetas como «Dominadas» durante la práctica.",
    emptyLearningTitle: "¡Todas las tarjetas dominadas! 🎉",
    emptyLearningSub: "Excelente trabajo. Cambia a «Todas» para repasar.",
    searchPlaceholder: "Buscar palabra o traducción...",
    btnAddWord: "Añadir",
    btnExportExcel: "Exportar Excel",
    catAll: "Todas",
    catGeneral: "Conversacional / General",
    catBusiness: "Negocios y Correos",
    catLogistics: "Logística y Comercio",
    catInterview: "Entrevista de trabajo",
    dictEmptyTitle: "Tu vocabulario está vacío",
    dictEmptyDesc: "¡Empieza de cero! Añade tus propias frases personalizadas.",
    dictEmptyBtn: "Añadir primera frase",
    dictSearchEmpty: "No se encontraron frases",
    dictSearchEmptyDesc: "Prueba ajustando la búsqueda o el filtro.",
    bentoVocab: "Vocabulario",
    bentoTotalCards: "Total tarjetas",
    bentoKnown: "Dominadas",
    bentoSolidMastery: "Conocimiento sólido",
    bentoLearning: "Aprendiendo",
    bentoInProgress: "En proceso",
    bentoStreak: "Racha",
    bentoDaysInRow: "Días seguidos",
    masteryLabel: "Vocabulario dominado",
    adminTitle: "Métricas y Audiencia",
    adminExportExcel: "Informe Excel",
    adminTotalUsers: "Total usuarios",
    adminNewToday: "hoy",
    adminLaunchedApp: "Iniciaron la app",
    adminGrowth7d: "Crecimiento (7 días)",
    adminRegistrations7d: "Registros esta semana",
    adminActiveToday: "Activos hoy",
    adminWau: "en 7 días (WAU)",
    adminTotalCardsInDb: "Total tarjetas en BD",
    adminAvgPerUser: "prom./usuario",
    adminActivityDynamics: "Dinámica de actividad (últimos 7 días)",
    adminActiveUsersLegend: "Usuarios activos",
    adminLangBreakdown: "🌍 Distribución por idiomas de estudio",
    adminLangsCount: "8 idiomas",
    adminStudentsList: "Lista de estudiantes",
    adminSearchPlaceholder: "Buscar por nombre o @usuario...",
    adminStudentsNotFound: "No se encontraron estudiantes",
    dockCards: "Tarjetas",
    dockDict: "Vocabulario",
    dockProgress: "Progreso",
    dockAnalytics: "Analítica",
    modalLangTitle: "Ajustes de idioma",
    modalLangSubtitle: "Idioma nativo e idioma de estudio",
    modalLangSec1: "1. Mi idioma nativo:",
    modalLangSec2: "2. Quiero aprender:",
    modalLangSave: "Guardar selección",
    modalAddSingle: "1 frase",
    modalAddBulk: "En lote (Excel)",
    aiStatusActive: "Traducción AI activa",
    aiStatusThinking: "AI está pensando...",
    aiStatusTranslating: "AI traduciendo...",
    aiStatusReady: "Traducción lista ✨",
    phraseIn: "Frase en",
    translationIn: "Traducción en",
    btnSwap: "Intercambiar",
    aiAltHeader: "Alternativas conversacionales:",
    categoryLabel: "Categoría:",
    btnSaveCard: "Guardar en tarjetas",
    bulkLabel: "Pega filas desde Excel o chat:",
    bulkPlaceholder: "Copia 2 columnas de Excel o texto como:\nTo keep you posted - Mantener informado\nShorten the lead time — Reducir plazo de entrega",
    bulkDetected: "Tarjetas detectadas:",
    btnSaveBulk: "Importar todas las frases",
    supportBtn: "Ayuda",
    supportBtnTitle: "Contacto con el desarrollador / Ayuda",
    modalSupportTitle: "Contacto con el desarrollador",
    modalSupportSubtitle: "¿Tienes una idea, pregunta o error? ¡Escríbenos!",
    supportCatLabel: "Elige un tema:",
    supportMsgLabel: "Tu mensaje:",
    supportMsgPlaceholder: "Describe tu idea, pregunta o sugerencia...",
    btnDirectTg: "Escribir en Telegram",
    btnSendSupport: "Enviar",
    supportSuccess: "✅ ¡Mensaje enviado! El desarrollador responderá pronto.",
    supportEmptyError: "Por favor, escribe un mensaje."
  },
  de: {
    streakSuffix: "Tage",
    streakTitle: "Lernsträhne Tage",
    langPickerTitle: "Sprachen wählen",
    themeToggle: "Design wechseln",
    myVocab: "Mein Wortschatz",
    filterAll: "Alle",
    filterLearning: "Lernen",
    filterKnown: "Gelernt",
    cardOf: "Karte",
    of: "von",
    stampKnown: "GELERNT",
    stampLearning: "LERNEN",
    hintRememberTrans: "Übersetzung erinnern (tippen zum Aufdecken)",
    hintRateResponse: "Bewerte deine Antwort:",
    hintListenRate: "Aussprache anhören und bewerten:",
    actionLearning: "Lernen",
    actionLearningSub: "Nach rechts wischen",
    actionDelete: "Löschen",
    actionDeleteSub: "Nach unten wischen",
    actionKnown: "Gelernt",
    actionKnownSub: "Nach links wischen",
    hintFlip: "Umdrehen",
    catEmptyTag: "+ Kategorie",
    catPickerTitle: "Karten-Kategorie",
    catPickerSubtitle: "Thema wählen oder eigenes eingeben",
    catPickerCustom: "Oder eigene Kategorie eingeben:",
    catPickerRemove: "Keine Kategorie",
    catPickerSave: "Speichern",
    emptyVocabTitle: "Dein Wortschatz ist noch leer 🌱",
    emptyVocabSub: "Tippe auf «Hinzufügen», um deine erste Karte zu erstellen ✨",
    emptyKnownTitle: "Der Bereich «Gelernt» ist leer",
    emptyKnownSub: "Markiere Karten beim Üben als «Gelernt».",
    emptyLearningTitle: "Alle Karten gemeistert! 🎉",
    emptyLearningSub: "Super gemacht. Wechsle zu «Alle», um zu wiederholen.",
    searchPlaceholder: "Wort oder Übersetzung suchen...",
    btnAddWord: "Hinzufügen",
    btnExportExcel: "Excel-Export",
    catAll: "Alle",
    catGeneral: "Alltag / Konversation",
    catBusiness: "Geschäftskommunikation",
    catLogistics: "Logistik & Lieferkette",
    catInterview: "Bewerbungsgespräch",
    dictEmptyTitle: "Dein Wortschatz ist leer",
    dictEmptyDesc: "Starte neu! Füge deine eigenen Ausdrücke hinzu.",
    dictEmptyBtn: "Erste Phrase hinzufügen",
    dictSearchEmpty: "Keine Treffer gefunden",
    dictSearchEmptyDesc: "Passe deine Suchanfrage oder Kategorie an.",
    bentoVocab: "Wortschatz",
    bentoTotalCards: "Karten gesamt",
    bentoKnown: "Gelernt",
    bentoSolidMastery: "Festes Wissen",
    bentoLearning: "Lernen",
    bentoInProgress: "In Bearbeitung",
    bentoStreak: "Strähne",
    bentoDaysInRow: "Tage in Folge",
    masteryLabel: "Wortschatz gemeistert",
    adminTitle: "Metriken & Zielgruppe",
    adminExportExcel: "Excel-Bericht",
    adminTotalUsers: "Benutzer gesamt",
    adminNewToday: "heute",
    adminLaunchedApp: "App gestartet",
    adminGrowth7d: "Zuwachs (7 Tage)",
    adminRegistrations7d: "Registrierungen diese Woche",
    adminActiveToday: "Heute aktiv",
    adminWau: "in 7 Tagen (WAU)",
    adminTotalCardsInDb: "Karten in Datenbank",
    adminAvgPerUser: "Ø/Benutzer",
    adminActivityDynamics: "Aktivitätsdynamik (letzte 7 Tage)",
    adminActiveUsersLegend: "Aktive Benutzer",
    adminLangBreakdown: "🌍 Verteilung nach Lernsprachen",
    adminLangsCount: "8 Sprachen",
    adminStudentsList: "Schülerliste",
    adminSearchPlaceholder: "Nach Name oder @Benutzername suchen...",
    adminStudentsNotFound: "Keine Schüler gefunden",
    dockCards: "Karten",
    dockDict: "Wortschatz",
    dockProgress: "Fortschritt",
    dockAnalytics: "Analytik",
    modalLangTitle: "Spracheinstellungen",
    modalLangSubtitle: "Muttersprache und Zielsprache",
    modalLangSec1: "1. Meine Muttersprache:",
    modalLangSec2: "2. Ich möchte lernen:",
    modalLangSave: "Auswahl speichern",
    modalAddSingle: "1 Phrase",
    modalAddBulk: "Massenimport (Excel)",
    aiStatusActive: "AI-Übersetzung aktiv",
    aiStatusThinking: "AI überlegt...",
    aiStatusTranslating: "AI übersetzt...",
    aiStatusReady: "Übersetzung bereit ✨",
    phraseIn: "Phrase auf",
    translationIn: "Übersetzung auf",
    btnSwap: "Felder tauschen",
    aiAltHeader: "Natürliche Gesprächsvarianten:",
    categoryLabel: "Kategorie:",
    btnSaveCard: "In Karten speichern",
    bulkLabel: "Zeilen aus Excel oder Chat einfügen:",
    bulkPlaceholder: "Kopiere 2 Spalten aus Excel oder Text:\nTo keep you posted - Auf dem Laufenden halten\nShorten the lead time — Lieferzeit verkürzen",
    bulkDetected: "Karten erkannt:",
    btnSaveBulk: "Alle Phrasen importieren",
    supportBtn: "Hilfe",
    supportBtnTitle: "Entwickler kontaktieren / Hilfe",
    modalSupportTitle: "Entwickler kontaktieren",
    modalSupportSubtitle: "Hast du eine Idee, Frage oder einen Fehler gefunden? Schreib uns!",
    supportCatLabel: "Thema wählen:",
    supportMsgLabel: "Deine Nachricht:",
    supportMsgPlaceholder: "Beschreibe deine Idee, Frage oder deinen Wunsch...",
    btnDirectTg: "Auf Telegram schreiben",
    btnSendSupport: "Senden",
    supportSuccess: "✅ Nachricht gesendet! Der Entwickler antwortet in Kürze.",
    supportEmptyError: "Bitte gib eine Nachricht ein."
  },
  fr: {
    streakSuffix: "jours",
    streakTitle: "Jours consécutifs d'étude",
    langPickerTitle: "Choisir les langues",
    themeToggle: "Changer de thème",
    myVocab: "Mon vocabulaire",
    filterAll: "Toutes",
    filterLearning: "En cours",
    filterKnown: "Maîtrisées",
    cardOf: "Carte",
    of: "sur",
    stampKnown: "MAÎTRISÉ",
    stampLearning: "EN COURS",
    hintRememberTrans: "Rappelez-vous la traduction (touchez pour voir)",
    hintRateResponse: "Évaluez votre réponse :",
    hintListenRate: "Écoutez la prononciation et évaluez :",
    actionLearning: "En cours",
    actionLearningSub: "Glisser à droite",
    actionDelete: "Supprimer",
    actionDeleteSub: "Glisser en bas",
    actionKnown: "Maîtrisé",
    actionKnownSub: "Glisser à gauche",
    hintFlip: "Retourner",
    catEmptyTag: "+ Catégorie",
    catPickerTitle: "Catégorie de la carte",
    catPickerSubtitle: "Choisissez un thème ou entrez le vôtre",
    catPickerCustom: "Ou entrez votre propre catégorie :",
    catPickerRemove: "Sans catégorie",
    catPickerSave: "Enregistrer",
    emptyVocabTitle: "Votre vocabulaire est vide 🌱",
    emptyVocabSub: "Appuyez sur «Ajouter» pour créer votre première carte ✨",
    emptyKnownTitle: "La section «Maîtrisées» est vide",
    emptyKnownSub: "Marquez des cartes comme «Maîtrisées» pendant la pratique.",
    emptyLearningTitle: "Toutes les cartes maîtrisées ! 🎉",
    emptyLearningSub: "Excellent travail. Passez à «Toutes» pour réviser.",
    searchPlaceholder: "Rechercher un mot ou une traduction...",
    btnAddWord: "Ajouter",
    btnExportExcel: "Exporter Excel",
    catAll: "Toutes",
    catGeneral: "Conversationnel / Général",
    catBusiness: "Affaires & E-mails",
    catLogistics: "Logistique & Chaîne d'approvisionnement",
    catInterview: "Entretien d'embauche",
    dictEmptyTitle: "Votre vocabulaire est vide",
    dictEmptyDesc: "Commencez à zéro ! Ajoutez vos propres phrases personnalisées.",
    dictEmptyBtn: "Ajouter la première phrase",
    dictSearchEmpty: "Aucune phrase trouvée",
    dictSearchEmptyDesc: "Essayez d'ajuster votre recherche ou votre catégorie.",
    bentoVocab: "Vocabulaire",
    bentoTotalCards: "Total cartes",
    bentoKnown: "Maîtrisées",
    bentoSolidMastery: "Connaissance solide",
    bentoLearning: "En cours",
    bentoInProgress: "En cours",
    bentoStreak: "Série",
    bentoDaysInRow: "Jours d'affilée",
    masteryLabel: "Vocabulaire maîtrisé",
    adminTitle: "Métriques & Audience",
    adminExportExcel: "Rapport Excel",
    adminTotalUsers: "Total utilisateurs",
    adminNewToday: "aujourd'hui",
    adminLaunchedApp: "Ont lancé l'app",
    adminGrowth7d: "Croissance (7 jours)",
    adminRegistrations7d: "Inscriptions cette semaine",
    adminActiveToday: "Actifs aujourd'hui",
    adminWau: "en 7 jours (WAU)",
    adminTotalCardsInDb: "Total cartes en base",
    adminAvgPerUser: "moy./util.",
    adminActivityDynamics: "Dynamique d'activité (7 derniers jours)",
    adminActiveUsersLegend: "Utilisateurs actifs",
    adminLangBreakdown: "🌍 Répartition par langues d'apprentissage",
    adminLangsCount: "8 langues",
    adminStudentsList: "Liste des apprenants",
    adminSearchPlaceholder: "Rechercher par nom ou @identifiant...",
    adminStudentsNotFound: "Aucun apprenant trouvé",
    dockCards: "Cartes",
    dockDict: "Vocabulaire",
    dockProgress: "Progrès",
    dockAnalytics: "Analytique",
    modalLangTitle: "Paramètres de langue",
    modalLangSubtitle: "Langue maternelle et langue cible",
    modalLangSec1: "1. Ma langue maternelle :",
    modalLangSec2: "2. Je veux apprendre :",
    modalLangSave: "Enregistrer le choix",
    modalAddSingle: "1 phrase",
    modalAddBulk: "En masse (Excel)",
    aiStatusActive: "Traduction IA active",
    aiStatusThinking: "L'IA réfléchit...",
    aiStatusTranslating: "L'IA traduit...",
    aiStatusReady: "Traduction prête ✨",
    phraseIn: "Phrase en",
    translationIn: "Traduction en",
    btnSwap: "Inverser les champs",
    aiAltHeader: "Alternatives conversationnelles naturelles :",
    categoryLabel: "Catégorie :",
    btnSaveCard: "Enregistrer dans les cartes",
    bulkLabel: "Collez des lignes depuis Excel ou un chat :",
    bulkPlaceholder: "Copiez 2 colonnes d'Excel ou un texte :\nTo keep you posted - Tenir au courant\nShorten the lead time — Réduire le délai de livraison",
    bulkDetected: "Cartes détectées :",
    btnSaveBulk: "Importer toutes les phrases",
    supportBtn: "Aide",
    supportBtnTitle: "Contacter le développeur / Aide",
    modalSupportTitle: "Contacter le développeur",
    modalSupportSubtitle: "Une idée, une question ou un bug ? Écrivez-nous !",
    supportCatLabel: "Choisissez un sujet :",
    supportMsgLabel: "Votre message :",
    supportMsgPlaceholder: "Décrivez votre idée, question ou suggestion...",
    btnDirectTg: "Écrire sur Telegram",
    btnSendSupport: "Envoyer",
    supportSuccess: "✅ Message envoyé ! Le développeur vous répondra bientôt.",
    supportEmptyError: "Veuillez saisir un message."
  },
  it: {
    streakSuffix: "giorni",
    streakTitle: "Giorni consecutivi di studio",
    langPickerTitle: "Scegli lingue",
    themeToggle: "Cambia tema",
    myVocab: "Il mio vocabolario",
    filterAll: "Tutte",
    filterLearning: "Studio",
    filterKnown: "Conosciute",
    cardOf: "Carta",
    of: "di",
    stampKnown: "CONOSCIUTA",
    stampLearning: "STUDIO",
    hintRememberTrans: "Ricorda la traduzione (tocca per vedere)",
    hintRateResponse: "Valuta la tua risposta:",
    hintListenRate: "Ascolta la pronuncia e valuta:",
    actionLearning: "Studio",
    actionLearningSub: "Scorri a destra",
    actionDelete: "Elimina",
    actionDeleteSub: "Scorri in basso",
    actionKnown: "Conosciuta",
    actionKnownSub: "Scorri a sinistra",
    hintFlip: "Gira",
    catEmptyTag: "+ Categoria",
    catPickerTitle: "Categoria carta",
    catPickerSubtitle: "Scegli un argomento o creane uno",
    catPickerCustom: "Oppure inserisci la tua categoria:",
    catPickerRemove: "Senza categoria",
    catPickerSave: "Salva",
    emptyVocabTitle: "Il tuo vocabolario è vuoto 🌱",
    emptyVocabSub: "Tocca «Aggiungi» per creare la prima carta ✨",
    emptyKnownTitle: "La sezione «Conosciute» è vuota",
    emptyKnownSub: "Segna le carte come «Conosciute» durante la pratica.",
    emptyLearningTitle: "Tutte le carte completate! 🎉",
    emptyLearningSub: "Ottimo lavoro. Passa a «Tutte» per ripassare.",
    searchPlaceholder: "Cerca parola o traduzione...",
    btnAddWord: "Aggiungi",
    btnExportExcel: "Esporta Excel",
    catAll: "Tutte",
    catGeneral: "Conversazione / Generale",
    catBusiness: "Affari & Email",
    catLogistics: "Logistica & Forniture",
    catInterview: "Colloquio di lavoro",
    dictEmptyTitle: "Il tuo vocabolario è vuoto",
    dictEmptyDesc: "Inizia da zero! Aggiungi le tue frasi personalizzate.",
    dictEmptyBtn: "Aggiungi la prima frase",
    dictSearchEmpty: "Nessuna frase trovata",
    dictSearchEmptyDesc: "Prova a modificare la ricerca o la categoria.",
    bentoVocab: "Vocabolario",
    bentoTotalCards: "Totale carte",
    bentoKnown: "Conosciute",
    bentoSolidMastery: "Conoscenza solida",
    bentoLearning: "Studio",
    bentoInProgress: "In corso",
    bentoStreak: "Serie",
    bentoDaysInRow: "Giorni di fila",
    masteryLabel: "Vocabolario padroneggiato",
    adminTitle: "Metriche & Pubblico",
    adminExportExcel: "Report Excel",
    adminTotalUsers: "Totale utenti",
    adminNewToday: "oggi",
    adminLaunchedApp: "Hanno aperto l'app",
    adminGrowth7d: "Crescita (7 giorni)",
    adminRegistrations7d: "Registrazioni questa settimana",
    adminActiveToday: "Attivi oggi",
    adminWau: "in 7 giorni (WAU)",
    adminTotalCardsInDb: "Totale carte nel database",
    adminAvgPerUser: "media/utente",
    adminActivityDynamics: "Dinamica attività (ultimi 7 giorni)",
    adminActiveUsersLegend: "Utenti attivi",
    adminLangBreakdown: "🌍 Distribuzione per lingue di studio",
    adminLangsCount: "8 lingue",
    adminStudentsList: "Elenco studenti",
    adminSearchPlaceholder: "Cerca per nome o @username...",
    adminStudentsNotFound: "Nessuno studente trovato",
    dockCards: "Carte",
    dockDict: "Vocabolario",
    dockProgress: "Progresso",
    dockAnalytics: "Analitica",
    modalLangTitle: "Impostazioni lingua",
    modalLangSubtitle: "Lingua madre e lingua di studio",
    modalLangSec1: "1. La mia lingua madre:",
    modalLangSec2: "2. Voglio imparare:",
    modalLangSave: "Salva selezione",
    modalAddSingle: "1 frase",
    modalAddBulk: "In blocco (Excel)",
    aiStatusActive: "Traduzione AI attiva",
    aiStatusThinking: "L'AI sta pensando...",
    aiStatusTranslating: "L'AI sta traducendo...",
    aiStatusReady: "Traduzione pronta ✨",
    phraseIn: "Frase in",
    translationIn: "Traduzione in",
    btnSwap: "Scambia campi",
    aiAltHeader: "Alternative colloquiali naturali:",
    categoryLabel: "Categoria:",
    btnSaveCard: "Salva nelle carte",
    bulkLabel: "Incolla righe da Excel o chat:",
    bulkPlaceholder: "Copia 2 colonne da Excel o testo:\nTo keep you posted - Tenere aggiornato\nShorten the lead time — Ridurre i tempi di consegna",
    bulkDetected: "Carte rilevate:",
    btnSaveBulk: "Importa tutte le frasi",
    supportBtn: "Aiuto",
    supportBtnTitle: "Contatta lo sviluppatore / Aiuto",
    modalSupportTitle: "Contatta lo sviluppatore",
    modalSupportSubtitle: "Hai un'idea, domanda o hai trovato un bug? Scrivici!",
    supportCatLabel: "Scegli un argomento:",
    supportMsgLabel: "Il tuo messaggio:",
    supportMsgPlaceholder: "Descrivi la tua idea, domanda o suggerimento...",
    btnDirectTg: "Scrivi su Telegram",
    btnSendSupport: "Invia",
    supportSuccess: "✅ Messaggio inviato! Lo sviluppatore risponderà presto.",
    supportEmptyError: "Inserisci un messaggio."
  }
};

let currentNativeLang = localStorage.getItem('wow_native_lang') || 'ru';
let currentTargetLang = localStorage.getItem('wow_target_lang') || 'en';

let allCards = [];
let currentDeck = [];
let currentIndex = 0;
let sessionCounter = 0; // Tracks 1-in-5 rule
let isFlipped = false;
let currentFilter = 'all'; // 'all', 'learning', 'known'
let currentCategory = 'all';
let currentTheme = 'light'; // Always launch in Light theme by default

// --- Theme Controller (Always starts in Light Theme) ---
function applyTheme(theme) {
  currentTheme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  
  const toggleBtn = document.getElementById('themeToggleBtn');
  if (toggleBtn) {
    if (theme === 'dark') {
      // In dark theme -> show Sun icon to switch to light
      toggleBtn.innerHTML = `
        <svg class="theme-svg" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
      `;
      toggleBtn.title = "Включить светлую тему";
    } else {
      // In light theme -> show Moon icon to switch to dark
      toggleBtn.innerHTML = `
        <svg class="theme-svg" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      `;
      toggleBtn.title = "Включить тёмную тему";
    }
  }

  if (tg) {
    try {
      const bgColor = theme === 'dark' ? '#16241B' : '#F6EFE9';
      if (tg.setHeaderColor) tg.setHeaderColor(bgColor);
      if (tg.setBackgroundColor) tg.setBackgroundColor(bgColor);
    } catch (e) {}
  }
}

// Always ensure Light theme on initial launch
applyTheme('light');

const themeToggleBtn = document.getElementById('themeToggleBtn');
if (themeToggleBtn) {
  themeToggleBtn.addEventListener('click', () => {
    haptic('light');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
  });
}

// User Identification (Strict Multi-tenant Isolation)
let userId = null;
const urlParams = new URLSearchParams(window.location.search);
const paramUid = urlParams.get('uid') || urlParams.get('user_id') || urlParams.get('auth');

if (paramUid && !isNaN(parseInt(paramUid))) {
  userId = parseInt(paramUid);
  try { localStorage.setItem('wow_english_user_id', userId.toString()); } catch (e) {}
} else if (tg?.initDataUnsafe?.user?.id) {
  userId = tg.initDataUnsafe.user.id;
  try { localStorage.setItem('wow_english_user_id', userId.toString()); } catch (e) {}
} else if (tg?.initDataUnsafe?.user?.username && tg.initDataUnsafe.user.username.toLowerCase() === 'hitrova_olga') {
  userId = 466788167;
  try { localStorage.setItem('wow_english_user_id', userId.toString()); } catch (e) {}
} else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  // If running locally on development server, default to Admin (Olga)
  userId = 466788167;
  try { localStorage.setItem('wow_english_user_id', userId.toString()); } catch (e) {}
} else {
  try {
    const saved = localStorage.getItem('wow_english_user_id');
    if (saved && !isNaN(parseInt(saved)) && parseInt(saved) !== 1) {
      userId = parseInt(saved);
    }
  } catch (e) {}
  
  if (!userId) {
    // Default to main admin account 466788167
    userId = 466788167;
    try { localStorage.setItem('wow_english_user_id', userId.toString()); } catch (e) {}
  }
}

// User Profile Init in UI Header
function updateUserNameUI() {
  const t = I18N[currentNativeLang] || I18N['ru'];
  if (tg?.initDataUnsafe?.user) {
    const u = tg.initDataUnsafe.user;
    const userNameEl = document.getElementById('userName');
    const userAvatarEl = document.getElementById('userAvatar');
    if (userNameEl) userNameEl.textContent = u.first_name || t.myVocab;
    if (userAvatarEl && u.first_name) {
      userAvatarEl.textContent = u.first_name.charAt(0).toUpperCase();
    }
  } else {
    const userNameEl = document.getElementById('userName');
    if (userNameEl) userNameEl.textContent = t.myVocab;
  }
}


// DOM Elements
const phraseFront = document.getElementById('phraseFront');
const phraseBack = document.getElementById('phraseBack');
const frontLangTag = document.getElementById('frontLangTag');
const backLangTag = document.getElementById('backLangTag');
const frontCategory = document.getElementById('frontCategory');
const backCategory = document.getElementById('backCategory');
const frontCategoryChip = document.getElementById('frontCategoryChip');
const backCategoryChip = document.getElementById('backCategoryChip');
const frontHint = document.getElementById('frontHint');
const backHint = document.getElementById('backHint');
const frontSpeakBtn = document.getElementById('frontSpeakBtn');
const backSpeakBtn = document.getElementById('backSpeakBtn');

const flashcard = document.getElementById('flashcard');
const cardScene = document.getElementById('cardScene');
const btnDeleteCard = document.getElementById('btnDeleteCard');
const btnKnown = document.getElementById('btnKnown');
const btnLearning = document.getElementById('btnLearning');

const stampKnown = document.getElementById('stampKnown');
const stampLearning = document.getElementById('stampLearning');
const stampDelete = document.getElementById('stampDelete');

const dockTabSupport = document.getElementById('dockTabSupport');
const dockTabAnalytics = document.getElementById('dockTabAnalytics');
const categoryFilterCarousel = document.getElementById('categoryFilterCarousel');

// Category Picker Modal Elements
const modalCategoryPicker = document.getElementById('modalCategoryPicker');
const btnCloseCatPickerModal = document.getElementById('btnCloseCatPickerModal');
const catPickerChipsGrid = document.getElementById('catPickerChipsGrid');
const customCategoryInput = document.getElementById('customCategoryInput');
const btnRemoveCategory = document.getElementById('btnRemoveCategory');
const btnSaveCardCategory = document.getElementById('btnSaveCardCategory');

const progressBar = document.getElementById('progressBar');
const cardCounter = document.getElementById('cardCounter');
const modeBadge = document.getElementById('modeBadge');
const streakDays = document.getElementById('streakDays');

// Segmented Filter Elements
const segmentedIndicator = document.getElementById('segmentedIndicator');
const countAll = document.getElementById('countAll');
const countLearning = document.getElementById('countLearning');
const countKnown = document.getElementById('countKnown');

// Dictionary DOM
const dictList = document.getElementById('dictList');
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const dictTotalCount = document.getElementById('dictTotalCount');
const btnExportExcelLink = document.getElementById('btnExportExcelLink');

// Modal DOM & Tabs
const addModal = document.getElementById('addModal');
const btnOpenAddModal = document.getElementById('btnOpenAddModal');
const btnCloseModal = document.getElementById('btnCloseModal');
const tabModeSingle = document.getElementById('tabModeSingle');
const tabModeBulk = document.getElementById('tabModeBulk');
const modalSingleBody = document.getElementById('modalSingleBody');
const modalBulkBody = document.getElementById('modalBulkBody');

const newPhraseEn = document.getElementById('newPhraseEn');
const newPhraseRu = document.getElementById('newPhraseRu');
const newCategorySelect = document.getElementById('newCategorySelect');
const btnSaveNewWord = document.getElementById('btnSaveNewWord');

// AI Translation Elements
const aiStatusBadge = document.getElementById('aiStatusBadge');
const aiStatusText = document.getElementById('aiStatusText');
const aiSpinner = document.getElementById('aiSpinner');
const btnTranslateEn = document.getElementById('btnTranslateEn');
const btnTranslateRu = document.getElementById('btnTranslateRu');
const btnClearEn = document.getElementById('btnClearEn');
const btnClearRu = document.getElementById('btnClearRu');
const btnSwapFields = document.getElementById('btnSwapFields');
const aiAlternativesBox = document.getElementById('aiAlternativesBox');
const aiAltChips = document.getElementById('aiAltChips');
const autoCategoryTag = document.getElementById('autoCategoryTag');

const bulkTextInput = document.getElementById('bulkTextInput');
const bulkCount = document.getElementById('bulkCount');
const btnSaveBulk = document.getElementById('btnSaveBulk');


// Stats DOM
const statTotal = document.getElementById('statTotal');
const statKnown = document.getElementById('statKnown');
const statLearning = document.getElementById('statLearning');
const statStreak = document.getElementById('statStreak');
const circleProgressPath = document.getElementById('circleProgressPath');
const masteryPercent = document.getElementById('masteryPercent');

// --- Haptic Feedback Helper ---
function haptic(type = 'light') {
  if (tg?.HapticFeedback) {
    try {
      if (type === 'success') tg.HapticFeedback.notificationOccurred('success');
      else if (type === 'warning') tg.HapticFeedback.notificationOccurred('warning');
      else tg.HapticFeedback.impactOccurred('light');
    } catch (e) {}
  }
}

// --- Confetti Celebration ---
function launchConfetti() {
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.65 },
      colors: ['#6366F1', '#10B981', '#F59E0B', '#EC4899', '#38BDF8']
    });
  }
}

// Fisher-Yates Shuffle algorithm
function shuffleArray(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// --- Category Dynamic Translator & Localizer ---
function getLocalizedCategoryName(rawCat, lang = currentNativeLang) {
  if (!rawCat || !rawCat.trim() || rawCat.trim() === '—' || rawCat.trim() === '+ Категория') {
    const t = I18N[lang] || I18N.ru;
    return t.catEmptyTag || '+ Категория';
  }
  
  const trimmed = rawCat.trim();
  const lower = trimmed.toLowerCase();
  const t = I18N[lang] || I18N.ru;
  
  if (lower.includes('разговорн') || lower.includes('общее') || lower.includes('general') || lower.includes('splošn') || lower.includes('pogovorno') || lower.includes('alltag') || lower.includes('général') || lower.includes('generale') || lower.includes('загальн') || lower.includes('розмовн')) {
    return t.catGeneral || trimmed;
  }
  if (lower.includes('делов') || lower.includes('business') || lower.includes('poslovn') || lower.includes('geschäft') || lower.includes('affaires') || lower.includes('negocios') || lower.includes('affari') || lower.includes('листуван')) {
    return t.catBusiness || trimmed;
  }
  if (lower.includes('логистик') || lower.includes('logist') || lower.includes('вэд') || lower.includes('oskrba') || lower.includes('forniture') || lower.includes('chaîne') || lower.includes('comercio') || lower.includes('зед')) {
    return t.catLogistics || trimmed;
  }
  if (lower.includes('собеседован') || lower.includes('interview') || lower.includes('razgovor') || lower.includes('vorstellungsgespräch') || lower.includes('entretien') || lower.includes('entrevista') || lower.includes('colloquio') || lower.includes('співбесід')) {
    return t.catInterview || trimmed;
  }
  if (lower.includes('путешеств') || lower.includes('отель') || lower.includes('travel') || lower.includes('potovan') || lower.includes('reisen') || lower.includes('voyage') || lower.includes('viaje') || lower.includes('viaggi') || lower.includes('подорож')) {
    return t.catTravel || trimmed;
  }
  if (lower.includes('it') || lower.includes('технолог') || lower.includes('tech') || lower.includes('tehnolog')) {
    return t.catTech || trimmed;
  }
  if (lower.includes('покупк') || lower.includes('кафе') || lower.includes('shop') || lower.includes('cafe') || lower.includes('nakup') || lower.includes('einkauf') || lower.includes('achats') || lower.includes('acquisti') || lower.includes('compras')) {
    return t.catShopping || trimmed;
  }
  if (lower.includes('эмоци') || lower.includes('мысл') || lower.includes('emotion') || lower.includes('čustv') || lower.includes('gefühle') || lower.includes('pensée') || lower.includes('pensamiento') || lower.includes('думк') || lower.includes('емоці')) {
    return t.catEmotions || trimmed;
  }
  
  return trimmed;
}

// --- Language Controller & Complete Dynamic UI Localization ---
function updateLanguageUI() {
  const t = I18N[currentNativeLang] || I18N['ru'];
  const nativeMeta = SUPPORTED_LANGS[currentNativeLang] || SUPPORTED_LANGS['ru'];
  const targetMeta = SUPPORTED_LANGS[currentTargetLang] || SUPPORTED_LANGS['en'];

  updateUserNameUI();

  // Header & Streak
  const langFlagPair = document.getElementById('langFlagPair');
  const langPairLabel = document.getElementById('langPairLabel');
  if (langFlagPair) langFlagPair.textContent = `${nativeMeta.flag} ➔ ${targetMeta.flag}`;
  if (langPairLabel) langPairLabel.textContent = targetMeta.short;

  const streakText = document.querySelector('.streak-text');
  if (streakText) streakText.textContent = t.streakSuffix;
  const streakPill = document.getElementById('streakPill');
  if (streakPill) streakPill.title = t.streakTitle;
  const langSelectorBtn = document.getElementById('langSelectorBtn');
  if (langSelectorBtn) langSelectorBtn.title = t.langPickerTitle;

  // Filter Segments
  const btnFilterAll = document.querySelector('.segment-btn[data-filter="all"] span:first-child');
  if (btnFilterAll) btnFilterAll.textContent = t.filterAll;
  const btnFilterLearning = document.querySelector('.segment-btn[data-filter="learning"] span:first-child');
  if (btnFilterLearning) btnFilterLearning.textContent = t.filterLearning;
  const btnFilterKnown = document.querySelector('.segment-btn[data-filter="known"] span:first-child');
  if (btnFilterKnown) btnFilterKnown.textContent = t.filterKnown;

  // Gesture Stamps
  const stampKnownEl = document.querySelector('#stampKnown span');
  if (stampKnownEl) stampKnownEl.textContent = t.stampKnown;
  const stampLearningEl = document.querySelector('#stampLearning span');
  if (stampLearningEl) stampLearningEl.textContent = t.stampLearning;

  // Bottom action bar buttons
  const btnLearningAction = document.getElementById('btnLearning');
  if (btnLearningAction) {
    const title = btnLearningAction.querySelector('.action-btn-title');
    const sub = btnLearningAction.querySelector('.action-btn-sub');
    if (title) title.textContent = t.actionLearning;
    if (sub) sub.textContent = t.actionLearningSub;
  }
  const btnDeleteAction = document.getElementById('btnDeleteCard');
  if (btnDeleteAction) {
    const title = btnDeleteAction.querySelector('.action-btn-title');
    const sub = btnDeleteAction.querySelector('.action-btn-sub');
    if (title) title.textContent = t.actionDelete;
    if (sub) sub.textContent = t.actionDeleteSub;
  }
  const btnKnownAction = document.getElementById('btnKnown');
  if (btnKnownAction) {
    const title = btnKnownAction.querySelector('.action-btn-title');
    const sub = btnKnownAction.querySelector('.action-btn-sub');
    if (title) title.textContent = t.actionKnown;
    if (sub) sub.textContent = t.actionKnownSub;
  }

  // Card Hints
  if (frontHint) frontHint.textContent = t.hintFlip || "Перевернуть";
  if (backHint) backHint.textContent = t.hintFlip || "Перевернуть";

  // Category Picker Modal
  const modalCatPickerTitle = document.getElementById('modalCatPickerTitle');
  if (modalCatPickerTitle) modalCatPickerTitle.textContent = t.catPickerTitle || "Категория карточки";
  const modalCatPickerSubtitle = document.getElementById('modalCatPickerSubtitle');
  if (modalCatPickerSubtitle) modalCatPickerSubtitle.textContent = t.catPickerSubtitle || "Выберите тему или введите свою";
  const lblCatPickerCustom = document.getElementById('lblCatPickerCustom');
  if (lblCatPickerCustom) lblCatPickerCustom.textContent = t.catPickerCustom || "Или введите свою категорию:";
  const lblBtnRemoveCategory = document.getElementById('lblBtnRemoveCategory');
  if (lblBtnRemoveCategory) lblBtnRemoveCategory.textContent = t.catPickerRemove || "Без категории";
  const lblBtnSaveCategory = document.getElementById('lblBtnSaveCategory');
  if (lblBtnSaveCategory) lblBtnSaveCategory.textContent = t.catPickerSave || "Сохранить";

  // Dictionary Tab
  if (searchInput) searchInput.placeholder = t.searchPlaceholder;
  if (btnOpenAddModal) {
    const span = btnOpenAddModal.querySelector('span');
    if (span) span.textContent = t.btnAddWord;
  }
  const btnExportExcelLink = document.getElementById('btnExportExcelLink');
  if (btnExportExcelLink) {
    const span = btnExportExcelLink.querySelector('span');
    if (span) span.textContent = t.btnExportExcel;
  }

  // Category Pills in Dictionary
  const catPillAll = document.querySelector('.chip-filter[data-cat="all"]');
  if (catPillAll) catPillAll.textContent = t.catAll;
  const catPillGen = document.querySelector('.chip-filter[data-cat="Разговорный / Общее"]');
  if (catPillGen) catPillGen.textContent = t.catGeneral;
  const catPillBus = document.querySelector('.chip-filter[data-cat="Деловая переписка"]');
  if (catPillBus) catPillBus.textContent = t.catBusiness;
  const catPillLog = document.querySelector('.chip-filter[data-cat="Логистика и ВЭД"]');
  if (catPillLog) catPillLog.textContent = t.catLogistics;
  const catPillInt = document.querySelector('.chip-filter[data-cat="Собеседование"]');
  if (catPillInt) catPillInt.textContent = t.catInterview;

  // Progress Tab Bento Cards
  const bentoTagVocab = document.querySelector('.bento-total .bento-tag');
  if (bentoTagVocab) bentoTagVocab.textContent = t.bentoVocab;
  const bentoLblVocab = document.querySelector('.bento-total .bento-lbl');
  if (bentoLblVocab) bentoLblVocab.textContent = t.bentoTotalCards;

  const bentoTagKnown = document.querySelector('.bento-known .bento-tag');
  if (bentoTagKnown) bentoTagKnown.textContent = t.bentoKnown;
  const bentoLblKnown = document.querySelector('.bento-known .bento-lbl');
  if (bentoLblKnown) bentoLblKnown.textContent = t.bentoSolidMastery;

  const bentoTagLearning = document.querySelector('.bento-learning .bento-tag');
  if (bentoTagLearning) bentoTagLearning.textContent = t.bentoLearning;
  const bentoLblLearning = document.querySelector('.bento-learning .bento-lbl');
  if (bentoLblLearning) bentoLblLearning.textContent = t.bentoInProgress;

  const bentoTagStreak = document.querySelector('.bento-streak .bento-tag');
  if (bentoTagStreak) bentoTagStreak.textContent = t.bentoStreak;
  const bentoLblStreak = document.querySelector('.bento-streak .bento-lbl');
  if (bentoLblStreak) bentoLblStreak.textContent = t.bentoDaysInRow;

  const circleMasteryLabel = document.querySelector('.circle-progress-center .circle-label');
  if (circleMasteryLabel) circleMasteryLabel.textContent = t.masteryLabel;

  // Bottom Navigation Dock
  const dockCardsLabel = document.querySelector('.dock-tab[data-tab="tabPractice"] .dock-label');
  if (dockCardsLabel) dockCardsLabel.textContent = t.dockCards;
  const dockDictLabel = document.querySelector('.dock-tab[data-tab="tabDictionary"] .dock-label');
  if (dockDictLabel) dockDictLabel.textContent = t.dockDict;
  const dockProgressLabel = document.querySelector('.dock-tab[data-tab="tabStats"] .dock-label');
  if (dockProgressLabel) dockProgressLabel.textContent = t.dockProgress;
  const dockAnalyticsLabel = document.querySelector('.dock-tab[data-tab="tabAnalytics"] .dock-label');
  if (dockAnalyticsLabel) dockAnalyticsLabel.textContent = t.dockAnalytics;

  // Admin Analytics Tab
  const adminTitleH2 = document.querySelector('.admin-title-wrap h2');
  if (adminTitleH2) adminTitleH2.textContent = t.adminTitle;
  const btnAdminExcelSpan = document.querySelector('#btnAdminExportExcel span');
  if (btnAdminExcelSpan) btnAdminExcelSpan.textContent = t.adminExportExcel;
  const adminChartHeaderH3 = document.querySelector('.admin-chart-header h3');
  if (adminChartHeaderH3) adminChartHeaderH3.textContent = t.adminActivityDynamics;
  const chartLegend = document.querySelector('.chart-legend');
  if (chartLegend) chartLegend.innerHTML = `<span class="dot-legend"></span> ${t.adminActiveUsersLegend}`;
  const adminLangHeaderH3 = document.querySelector('.admin-lang-breakdown-card h3');
  if (adminLangHeaderH3) adminLangHeaderH3.textContent = t.adminLangBreakdown;
  const adminTotalLangsCount = document.getElementById('adminTotalLangsCount');
  if (adminTotalLangsCount) adminTotalLangsCount.textContent = t.adminLangsCount;
  const adminSearchInput = document.getElementById('adminSearchInput');
  if (adminSearchInput) adminSearchInput.placeholder = t.adminSearchPlaceholder;

  // Language Modal
  const modalLangTitleH3 = document.querySelector('#modalLanguagePicker .modal-title-text h3');
  if (modalLangTitleH3) modalLangTitleH3.textContent = t.modalLangTitle;
  const modalLangSubtitleP = document.querySelector('#modalLanguagePicker .modal-subtitle');
  if (modalLangSubtitleP) modalLangSubtitleP.textContent = t.modalLangSubtitle;
  const langSec1Label = document.querySelector('.lang-modal-section:first-child .lang-section-label');
  if (langSec1Label) langSec1Label.textContent = t.modalLangSec1;
  const langSec2Label = document.querySelector('.lang-modal-section:nth-child(2) .lang-section-label');
  if (langSec2Label) langSec2Label.textContent = t.modalLangSec2;
  const btnSaveLanguagesSpan = document.querySelector('#btnSaveLanguages span');
  if (btnSaveLanguagesSpan) btnSaveLanguagesSpan.textContent = t.modalLangSave;

  // Add Word Modal
  const tabModeSingleBtn = document.getElementById('tabModeSingle');
  if (tabModeSingleBtn) tabModeSingleBtn.textContent = t.modalAddSingle;
  const tabModeBulkBtn = document.getElementById('tabModeBulk');
  if (tabModeBulkBtn) tabModeBulkBtn.textContent = t.modalAddBulk;
  
  const labelEn = document.querySelector('label[for="newPhraseEn"]');
  const tagEn = document.querySelector('#modalSingleBody .form-group:nth-child(2) .field-lang-tag');
  if (labelEn) labelEn.textContent = `${t.phraseIn} ${targetMeta.name} (${targetMeta.short}):`;
  if (tagEn) tagEn.textContent = targetMeta.short;

  const labelRu = document.querySelector('label[for="newPhraseRu"]');
  const tagRu = document.querySelector('#modalSingleBody .form-group:nth-child(4) .field-lang-tag');
  if (labelRu) labelRu.textContent = `${t.translationIn} ${nativeMeta.name} (${nativeMeta.short}):`;
  if (tagRu) tagRu.textContent = nativeMeta.short;

  const btnSwapSpan = document.querySelector('#btnSwapFields span');
  if (btnSwapSpan) btnSwapSpan.textContent = t.btnSwap;

  const aiAltHeaderSpan = document.querySelector('.ai-alt-header span');
  if (aiAltHeaderSpan) aiAltHeaderSpan.textContent = t.aiAltHeader;

  const catLabel = document.querySelector('label[for="newCategorySelect"]');
  if (catLabel) catLabel.textContent = t.categoryLabel;

  const btnSaveNewWordSpan = document.querySelector('#btnSaveNewWord span');
  if (btnSaveNewWordSpan) btnSaveNewWordSpan.textContent = t.btnSaveCard;

  const bulkLabel = document.querySelector('label[for="bulkTextInput"]');
  if (bulkLabel) bulkLabel.textContent = t.bulkLabel;
  if (bulkTextInput) bulkTextInput.placeholder = t.bulkPlaceholder;
  const btnSaveBulkSpan = document.querySelector('#btnSaveBulk span');
  if (btnSaveBulkSpan) btnSaveBulkSpan.textContent = t.btnSaveBulk;

  // Support Button & Modal
  const supportPillLabel = document.querySelector('.support-pill-label');
  if (supportPillLabel) supportPillLabel.textContent = t.supportBtn || "Помощь";
  const btnOpenSupportModal = document.getElementById('btnOpenSupportModal');
  if (btnOpenSupportModal) btnOpenSupportModal.title = t.supportBtnTitle || "Связь с разработчиком";

  const modalSupportTitle = document.getElementById('modalSupportTitle');
  if (modalSupportTitle) modalSupportTitle.textContent = t.modalSupportTitle || "Связь с разработчиком";
  const modalSupportSubtitle = document.getElementById('modalSupportSubtitle');
  if (modalSupportSubtitle) modalSupportSubtitle.textContent = t.modalSupportSubtitle || "Есть идея, вопрос или нашли ошибку? Напишите нам!";

  const supportCatLabel = document.getElementById('supportCatLabel');
  if (supportCatLabel) supportCatLabel.textContent = t.supportCatLabel || "Выберите тему:";
  const supportMsgLabel = document.getElementById('supportMsgLabel');
  if (supportMsgLabel) supportMsgLabel.textContent = t.supportMsgLabel || "Ваше сообщение:";
  const supportMessageInput = document.getElementById('supportMessageInput');
  if (supportMessageInput) supportMessageInput.placeholder = t.supportMsgPlaceholder || "Опишите вашу идею, вопрос или пожелание...";

  const btnDirectTgSpan = document.getElementById('btnDirectTgSpan');
  if (btnDirectTgSpan) btnDirectTgSpan.textContent = t.btnDirectTg || "Написать в Telegram";
  const btnSendSupportSpan = document.getElementById('btnSendSupportSpan');
  if (btnSendSupportSpan) btnSendSupportSpan.textContent = t.btnSendSupport || "Отправить";

  // Active pills highlight in modal
  document.querySelectorAll('#nativeLangGrid .lang-opt-pill').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === currentNativeLang);
  });
  document.querySelectorAll('#targetLangGrid .lang-opt-pill').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === currentTargetLang);
  });
}

function initLanguagePicker() {
  const modal = document.getElementById('modalLanguagePicker');
  const btnOpen = document.getElementById('langSelectorBtn');
  const btnClose = document.getElementById('btnCloseLangModal');
  const btnSave = document.getElementById('btnSaveLanguages');

  if (btnOpen && modal) {
    btnOpen.addEventListener('click', () => {
      haptic('light');
      updateLanguageUI();
      modal.style.display = 'flex';
      setTimeout(() => modal.classList.add('open'), 10);
    });
  }

  if (btnClose && modal) {
    btnClose.addEventListener('click', () => {
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
    });
  }

  document.querySelectorAll('#nativeLangGrid .lang-opt-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      haptic('light');
      currentNativeLang = btn.dataset.lang;
      updateLanguageUI();
    });
  });

  document.querySelectorAll('#targetLangGrid .lang-opt-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      haptic('light');
      currentTargetLang = btn.dataset.lang;
      updateLanguageUI();
    });
  });

  if (btnSave && modal) {
    btnSave.addEventListener('click', async () => {
      haptic('success');
      localStorage.setItem('wow_native_lang', currentNativeLang);
      localStorage.setItem('wow_target_lang', currentTargetLang);

      try {
        await fetch('/api/user/languages', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId, native_lang: currentNativeLang, target_lang: currentTargetLang })
        });
      } catch (e) {}

      updateLanguageUI();
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
      
      await loadData();
    });
  }

  updateLanguageUI();
}

// --- Network Resilience & Safe Fetch ---
async function safeFetch(url, options = {}, retries = 3, delay = 500) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url, options);
      if (res.ok) return res;
      if (res.status >= 400 && res.status < 500 && res.status !== 408) {
        return res; // Client error - do not retry endlessly
      }
    } catch (e) {
      if (i === retries - 1) throw e;
    }
    await new Promise(r => setTimeout(r, delay * Math.pow(1.5, i)));
  }
  return await fetch(url, options);
}

// --- Data Fetching with LocalStorage Cache & Background Sync ---
async function loadData(silent = false) {
  const cacheKey = `wow_cards_cache_${userId}_${currentTargetLang}_${currentNativeLang}`;
  
  // 1. Instant Local Cache Hydration (0ms initial render)
  if (!silent && (!allCards || allCards.length === 0)) {
    try {
      const cached = localStorage.getItem(cacheKey);
      if (cached) {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed) && parsed.length > 0) {
          allCards = parsed;
          updateCounters();
          applyFilter(currentFilter);
          renderDictionary();
        }
      }
    } catch (e) {
      console.warn('Cache read error:', e);
    }
  }

  // 2. Fetch fresh data from API with retry
  try {
    const res = await safeFetch(`/api/cards?user_id=${userId}&target_lang=${currentTargetLang}&native_lang=${currentNativeLang}&shuffle=false`, {}, 3, 400);
    if (res.ok) {
      const freshCards = await res.json();
      allCards = freshCards;
      try {
        localStorage.setItem(cacheKey, JSON.stringify(freshCards));
      } catch (e) {}
    } else {
      console.warn('Cards API returned non-OK status:', res.status);
    }
  } catch (e) {
    console.warn('Network issue fetching cards, keeping cached/existing deck:', e);
    // CRITICAL: NEVER wipe allCards = [] on network error!
  }
  
  updateCounters();
  applyFilter(currentFilter);
  await fetchAndRenderCategories();
  await fetchAndRenderGroups();
  await loadRedWords();
  renderDictionary();
  await loadStats();
  if (typeof currentTrainerStep !== 'undefined' && currentTrainerStep === 2) {
    renderTrainerGroupsChecklist();
    updateStep2SelectionSummary();
  }
  updateStartButtonLabel();
}

function updateCounters() {
  const total = allCards.length;
  const known = allCards.filter(c => c.status === 'known').length;
  const learning = allCards.filter(c => c.status === 'learning' || !c.status).length;

  if (countAll) countAll.textContent = total;
  if (countLearning) countLearning.textContent = learning;
  if (countKnown) countKnown.textContent = known;

  if (statTotal) statTotal.textContent = total;
  if (statKnown) statKnown.textContent = known;
  if (statLearning) statLearning.textContent = learning;

  const pct = total > 0 ? Math.round((known / total) * 100) : 0;
  if (masteryPercent) masteryPercent.textContent = `${pct}%`;
  if (circleProgressPath) {
    circleProgressPath.setAttribute('stroke-dasharray', `${pct}, 100`);
  }
}

async function loadStats() {
  const statsKey = `wow_stats_cache_${userId}_${currentTargetLang}_${currentNativeLang}`;
  
  // Hydrate stats from cache first
  try {
    const cachedStats = localStorage.getItem(statsKey);
    if (cachedStats) {
      const s = JSON.parse(cachedStats);
      if (statStreak) statStreak.textContent = s.streak || 1;
      if (streakDays) streakDays.textContent = s.streak || 1;
    }
  } catch (e) {}

  try {
    const res = await safeFetch(`/api/stats?user_id=${userId}&target_lang=${currentTargetLang}&native_lang=${currentNativeLang}`, {}, 2, 400);
    if (res.ok) {
      const s = await res.json();
      try { localStorage.setItem(statsKey, JSON.stringify(s)); } catch (e) {}
      if (statStreak) statStreak.textContent = s.streak || 1;
      if (streakDays) streakDays.textContent = s.streak || 1;
      if (s.native_lang && !localStorage.getItem('wow_native_lang')) {
        currentNativeLang = s.native_lang;
      }
      if (s.target_lang && !localStorage.getItem('wow_target_lang')) {
        currentTargetLang = s.target_lang;
      }
      updateLanguageUI();
    }
  } catch (e) {}
}

// --- FILTER SWITCHING (FIXED & FULLY WORKING) ---
function applyFilter(filter) {
  currentFilter = filter;
  let filtered = [];

  if (filter === 'all') {
    filtered = [...allCards];
  } else if (filter === 'learning') {
    filtered = allCards.filter(c => c.status === 'learning' || !c.status);
  } else if (filter === 'known') {
    filtered = allCards.filter(c => c.status === 'known');
  }

  // Segmented control UI updates
  const segmentBtns = document.querySelectorAll('.segment-btn');
  segmentBtns.forEach(btn => {
    if (btn.dataset.filter === filter) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  if (segmentedIndicator) {
    if (filter === 'all') segmentedIndicator.style.transform = 'translateX(0%)';
    else if (filter === 'learning') segmentedIndicator.style.transform = 'translateX(100%)';
    else if (filter === 'known') segmentedIndicator.style.transform = 'translateX(200%)';
  }

  currentDeck = shuffleArray(filtered);
  currentIndex = 0;
  sessionCounter = 0;
  isFlipped = false;
  if (flashcard) flashcard.classList.remove('is-flipped');
  displayCard();
}

// Segmented filter click listeners
document.querySelectorAll('.segment-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    haptic('light');
    const f = btn.dataset.filter;
    applyFilter(f);
  });
});

// --- DISPLAY CURRENT CARD ---
function displayCard() {
  const t = I18N[currentNativeLang] || I18N['ru'];
  const nativeMeta = SUPPORTED_LANGS[currentNativeLang] || SUPPORTED_LANGS['ru'];
  const targetMeta = SUPPORTED_LANGS[currentTargetLang] || SUPPORTED_LANGS['en'];

  if (!allCards || allCards.length === 0) {
    const testWords = {
      'ru': 'Тест', 'uk': 'Тест', 'en': 'Test', 'sl': 'Test',
      'es': 'Prueba', 'de': 'Test', 'fr': 'Test', 'it': 'Test'
    };
    const sampleNative = testWords[currentNativeLang] || 'Тест';
    const sampleTarget = testWords[currentTargetLang] || 'Test';

    if (phraseFront) {
      phraseFront.textContent = sampleNative;
      phraseFront.className = "card-phrase-text card-phrase-sample";
    }
    if (phraseBack) {
      phraseBack.textContent = sampleTarget;
      phraseBack.className = "card-phrase-text card-phrase-sample";
    }
    if (frontCategory) frontCategory.textContent = t.catGeneral || t.catEmptyTag || "+ Категория";
    if (backCategory) backCategory.textContent = t.catGeneral || t.catEmptyTag || "+ Категория";
    if (frontLangTag) {
      frontLangTag.textContent = nativeMeta.name.toUpperCase();
      frontLangTag.className = "lang-pill";
    }
    if (backLangTag) {
      backLangTag.textContent = targetMeta.name.toUpperCase();
      backLangTag.className = "lang-pill pill-en";
    }
    if (frontHint) frontHint.textContent = `${t.hintFlip || "Перевернуть"} • ${t.emptyVocabTitle || "Словарь пуст"}`;
    if (backHint) backHint.textContent = t.emptyVocabSub || "Нажмите «Добавить», чтобы внести первую фразу ✨";
    if (cardCounter) cardCounter.textContent = `0 ${t.of} 0`;
    if (progressBar) progressBar.style.width = "0%";
    if (modeBadge) modeBadge.textContent = "0";
    isFlipped = false;
    if (flashcard) {
      flashcard.style.transform = '';
      flashcard.classList.remove('is-flipped');
    }

    // Trigger onboarding spotlight guide
    checkAndShowOnboarding(1);
    return;
  }

  // If cards exist, hide onboarding guide
  hideOnboardingSpotlight();

  if (!currentDeck || currentDeck.length === 0) {
    let emptyTitle = t.dictSearchEmpty;
    let emptySub = t.dictSearchEmptyDesc;
    if (currentFilter === 'known') {
      emptyTitle = t.emptyKnownTitle;
      emptySub = t.emptyKnownSub;
    } else if (currentFilter === 'learning') {
      emptyTitle = t.emptyLearningTitle;
      emptySub = t.emptyLearningSub;
      launchConfetti();
    }
    
    if (phraseFront) {
      phraseFront.textContent = emptyTitle;
      phraseFront.className = "card-phrase-text";
    }
    if (phraseBack) {
      phraseBack.textContent = "";
      phraseBack.className = "card-phrase-text";
    }
    if (frontCategory) frontCategory.textContent = t.catGeneral;
    if (backCategory) backCategory.textContent = "";
    if (frontLangTag) {
      frontLangTag.textContent = nativeMeta.name.toUpperCase();
      frontLangTag.className = "lang-pill";
    }
    if (frontHint) frontHint.textContent = emptySub;
    if (cardCounter) cardCounter.textContent = `0 ${t.of} 0`;
    if (progressBar) progressBar.style.width = "100%";
    if (modeBadge) modeBadge.textContent = "—";
    isFlipped = false;
    if (flashcard) flashcard.classList.remove('is-flipped');
    return;
  }

  if (currentIndex >= currentDeck.length) {
    launchConfetti();
    currentDeck = shuffleArray(currentDeck);
    currentIndex = 0;
  }

  const card = currentDeck[currentIndex];
  const hasCategory = Boolean(card.category && card.category.trim() && card.category.trim() !== '—');
  const catDisplay = hasCategory ? getLocalizedCategoryName(card.category, currentNativeLang) : (t.catEmptyTag || '+ Категория');
  
  // Rule: 4 out of 5 cards Native -> Target, 1 out of 5 cards Target -> Native
  const isTargetToNative = (sessionCounter % 5 === 4);

  if (phraseFront) phraseFront.className = "card-phrase-text";
  if (phraseBack) phraseBack.className = "card-phrase-text en-glow";

  if (frontCategory) frontCategory.textContent = catDisplay;
  if (frontCategoryChip) {
    if (hasCategory) frontCategoryChip.classList.remove('is-empty');
    else frontCategoryChip.classList.add('is-empty');
  }

  if (backCategory) backCategory.textContent = catDisplay;
  if (backCategoryChip) {
    if (hasCategory) backCategoryChip.classList.remove('is-empty');
    else backCategoryChip.classList.add('is-empty');
  }

  if (frontHint) frontHint.textContent = t.hintFlip || "Перевернуть";
  if (backHint) backHint.textContent = t.hintFlip || "Перевернуть";

  if (isTargetToNative) {
    if (frontLangTag) {
      frontLangTag.textContent = targetMeta.name.toUpperCase();
      frontLangTag.className = "lang-pill pill-en";
    }
    if (phraseFront) phraseFront.textContent = card.phrase_en;

    if (backLangTag) {
      backLangTag.textContent = nativeMeta.name.toUpperCase();
      backLangTag.className = "lang-pill";
    }
    if (phraseBack) phraseBack.textContent = card.phrase_ru;

    if (modeBadge) modeBadge.textContent = `${targetMeta.short} ➔ ${nativeMeta.short} (1 ${t.of} 5)`;
  } else {
    if (frontLangTag) {
      frontLangTag.textContent = nativeMeta.name.toUpperCase();
      frontLangTag.className = "lang-pill";
    }
    if (phraseFront) phraseFront.textContent = card.phrase_ru;

    if (backLangTag) {
      backLangTag.textContent = targetMeta.name.toUpperCase();
      backLangTag.className = "lang-pill pill-en";
    }
    if (phraseBack) phraseBack.textContent = card.phrase_en;

    if (modeBadge) modeBadge.textContent = `${nativeMeta.short} ➔ ${targetMeta.short}`;
  }

  if (cardCounter) cardCounter.textContent = `${t.cardOf} ${currentIndex + 1} ${t.of} ${currentDeck.length}`;
  const progressPercent = Math.round(((currentIndex + 1) / currentDeck.length) * 100);
  if (progressBar) progressBar.style.width = `${progressPercent}%`;

  isFlipped = false;
  if (flashcard) {
    flashcard.style.transform = '';
    flashcard.classList.remove('is-flipped');
  }
}

// Flip Card Action
function flipCard() {
  haptic('light');
  isFlipped = !isFlipped;
  if (flashcard) {
    flashcard.classList.remove('dragging');
    flashcard.style.transform = '';
    if (isFlipped) {
      flashcard.classList.add('is-flipped');
    } else {
      flashcard.classList.remove('is-flipped');
    }
  }
}

// --- High-Quality Speech Synthesis Engine with Accurate Language Matching ---
let isWorkoutMuted = false;
try {
  isWorkoutMuted = localStorage.getItem('wow_english_workout_muted') === 'true';
} catch (e) {}

function speakPhrase(text, langCode = null, btnElement = null, isWorkoutCall = false) {
  if (!text) return;
  // If in workout and muted, skip voice playback
  if (isWorkoutMuted && (isWorkoutCall || currentTrainerStep === 'workout')) return;

  const targetLang = langCode || currentTargetLang;
  
  if (btnElement) {
    btnElement.classList.add('is-playing');
    setTimeout(() => btnElement.classList.remove('is-playing'), 1500);
  }

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const speechCode = SUPPORTED_LANGS[targetLang]?.speechCode || 'en-US';
    utterance.lang = speechCode;
    utterance.rate = 0.82; // Natural and clear speed
    utterance.pitch = 1.0;
    
    // Select natural voice matching requested language
    const voices = window.speechSynthesis.getVoices();
    const voicePrefix = targetLang.toLowerCase();
    const matchVoice = voices.find(v => v.lang.toLowerCase().startsWith(voicePrefix) && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Siri') || v.name.includes('Samantha') || v.name.includes('Neural')));
    if (matchVoice) {
      utterance.voice = matchVoice;
    } else {
      const anyVoice = voices.find(v => v.lang.toLowerCase().startsWith(voicePrefix));
      if (anyVoice) utterance.voice = anyVoice;
    }

    utterance.onend = () => {
      if (btnElement) btnElement.classList.remove('is-playing');
    };
    
    window.speechSynthesis.speak(utterance);
  }
}

// Bottom Bar Delete Button
if (btnDeleteCard) {
  btnDeleteCard.addEventListener('click', () => {
    deleteCardAction();
  });
}

// Category Chips click listeners on flashcard
if (frontCategoryChip) {
  frontCategoryChip.addEventListener('click', (e) => {
    e.stopPropagation();
    if (currentDeck.length > 0 && currentDeck[currentIndex]) {
      openCategoryPickerModal(currentDeck[currentIndex]);
    }
  });
}

if (backCategoryChip) {
  backCategoryChip.addEventListener('click', (e) => {
    e.stopPropagation();
    if (currentDeck.length > 0 && currentDeck[currentIndex]) {
      openCategoryPickerModal(currentDeck[currentIndex]);
    }
  });
}

// Speaker Buttons: front speaks front phrase in its language, back speaks back phrase in its language
if (frontSpeakBtn) {
  frontSpeakBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    haptic('light');
    if (currentDeck.length > 0 && currentDeck[currentIndex]) {
      const isTargetToNative = (sessionCounter % 5 === 4);
      const text = isTargetToNative ? currentDeck[currentIndex].phrase_en : currentDeck[currentIndex].phrase_ru;
      const lang = isTargetToNative ? currentTargetLang : currentNativeLang;
      speakPhrase(text, lang, frontSpeakBtn);
    } else if (allCards.length === 0) {
      const testWords = { 'ru': 'Тест', 'uk': 'Тест', 'en': 'Test', 'sl': 'Test', 'es': 'Prueba', 'de': 'Test', 'fr': 'Test', 'it': 'Test' };
      speakPhrase(testWords[currentNativeLang] || 'Тест', currentNativeLang, frontSpeakBtn);
    }
  });
}

if (backSpeakBtn) {
  backSpeakBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    haptic('light');
    if (currentDeck.length > 0 && currentDeck[currentIndex]) {
      const isTargetToNative = (sessionCounter % 5 === 4);
      const text = isTargetToNative ? currentDeck[currentIndex].phrase_ru : currentDeck[currentIndex].phrase_en;
      const lang = isTargetToNative ? currentNativeLang : currentTargetLang;
      speakPhrase(text, lang, backSpeakBtn);
    } else if (allCards.length === 0) {
      const testWords = { 'ru': 'Тест', 'uk': 'Тест', 'en': 'Test', 'sl': 'Test', 'es': 'Prueba', 'de': 'Test', 'fr': 'Test', 'it': 'Test' };
      speakPhrase(testWords[currentTargetLang] || 'Test', currentTargetLang, backSpeakBtn);
    }
  });
}

// --- ACTION: "ЗНАЮ" (Mark as Known / Swipe Left) ---
if (btnKnown) {
  btnKnown.addEventListener('click', async () => {
    haptic('success');
    if (currentDeck.length === 0) return;
    
    const card = currentDeck[currentIndex];
    card.status = 'known';
    
    const globalCard = allCards.find(c => c.id === card.id);
    if (globalCard) globalCard.status = 'known';

    try {
      fetch('/api/card_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: card.id, status: 'known', user_id: userId })
      });
    } catch (e) {}

    updateCounters();

    // If filtering only 'learning', remove card from view
    if (currentFilter === 'learning') {
      currentDeck.splice(currentIndex, 1);
    } else {
      currentIndex++;
    }

    sessionCounter++;
    displayCard();
    renderDictionary();
  });
}

// --- ACTION: "УЧУ" (Mark as Learning / Repeat / Swipe Right) ---
if (btnLearning) {
  btnLearning.addEventListener('click', async () => {
    haptic('warning');
    if (currentDeck.length === 0) return;
    
    const card = currentDeck[currentIndex];
    card.status = 'learning';
    
    const globalCard = allCards.find(c => c.id === card.id);
    if (globalCard) globalCard.status = 'learning';

    try {
      fetch('/api/card_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: card.id, status: 'learning', user_id: userId })
      });
    } catch (e) {}

    updateCounters();

    // If filtering only 'known', remove card from view
    if (currentFilter === 'known') {
      currentDeck.splice(currentIndex, 1);
    } else {
      // Re-insert at end of queue for repetition
      const cur = currentDeck.splice(currentIndex, 1)[0];
      currentDeck.push(cur);
    }

    sessionCounter++;
    displayCard();
    renderDictionary();
  });
}

// --- ACTION: DELETE CARD (Swipe Down) ---
async function deleteCardAction() {
  if (currentDeck.length === 0 || !currentDeck[currentIndex]) return;
  const card = currentDeck[currentIndex];
  const cardId = card.id;

  haptic('heavy');
  
  // Remove from arrays
  allCards = allCards.filter(c => c.id !== cardId);
  currentDeck.splice(currentIndex, 1);
  if (currentIndex >= currentDeck.length) {
    currentIndex = 0;
  }

  updateCounters();
  displayCard();
  renderDictionary();

  try {
    await fetch('/api/card/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card_id: cardId, user_id: userId })
    });
  } catch (e) {
    console.error('Delete card failed:', e);
  }
}

// --- SMOOTH & SENSITIVE SWIPE GESTURES & TAP CONTROLLER (POINTER & TOUCH) ---
let touchStartX = 0;
let touchStartY = 0;
let touchMoveX = 0;
let touchMoveY = 0;
let touchStartTime = 0;
let isDraggingCard = false;
let lastTouchEndTime = 0;

if (cardScene && flashcard) {
  // Tap / Click handler (with gesture debounce)
  cardScene.addEventListener('click', (e) => {
    if (allCards.length === 0) return;
    if (e.target.closest('.speaker-circle-btn') || e.target.closest('button') || e.target.closest('.category-chip') || e.target.closest('.swipe-stamp')) return;
    if (Date.now() - lastTouchEndTime < 600) return;
    flipCard();
  });

  const onPointerStart = (clientX, clientY, target) => {
    if (allCards.length === 0) return false;
    if (target.closest('.speaker-circle-btn') || target.closest('button') || target.closest('.category-chip')) return false;
    touchStartX = clientX;
    touchStartY = clientY;
    touchMoveX = 0;
    touchMoveY = 0;
    touchStartTime = Date.now();
    isDraggingCard = true;
    flashcard.classList.add('dragging');
    return true;
  };

  const onPointerMove = (clientX, clientY, e) => {
    if (!isDraggingCard) return;
    touchMoveX = clientX - touchStartX;
    touchMoveY = clientY - touchStartY;
    
    const absX = Math.abs(touchMoveX);
    const absY = Math.abs(touchMoveY);

    if (absX > 5 || absY > 5) {
      if (e && e.cancelable && (absX > absY || touchMoveY > 12)) {
        e.preventDefault();
      }
      
      const rotY = isFlipped ? 180 : 0;
      
      // Check downward drag (Delete action)
      if (touchMoveY > 18 && touchMoveY > absX * 0.9) {
        const tilt = touchMoveX * 0.05;
        flashcard.style.transform = `translate3d(${touchMoveX * 0.2}px, ${touchMoveY}px, 0) rotateZ(${tilt + touchMoveY * 0.04}deg) rotateY(${rotY}deg)`;
        
        const opacity = Math.min(1, (touchMoveY - 18) / 40);
        if (stampDelete) {
          stampDelete.style.opacity = opacity;
          stampDelete.classList.add('visible');
        }
        if (stampLearning) { stampLearning.style.opacity = 0; stampLearning.classList.remove('visible'); }
        if (stampKnown) { stampKnown.style.opacity = 0; stampKnown.classList.remove('visible'); }
      }
      // Check right drag (УЧУ)
      else if (touchMoveX > 12) {
        const tilt = touchMoveX * 0.07;
        flashcard.style.transform = `translate3d(${touchMoveX}px, ${touchMoveY * 0.15}px, 0) rotateZ(${tilt}deg) rotateY(${rotY}deg)`;
        const opacity = Math.min(1, (touchMoveX - 12) / 30);
        if (stampLearning) {
          stampLearning.style.opacity = opacity;
          stampLearning.classList.add('visible');
        }
        if (stampKnown) { stampKnown.style.opacity = 0; stampKnown.classList.remove('visible'); }
        if (stampDelete) { stampDelete.style.opacity = 0; stampDelete.classList.remove('visible'); }
      }
      // Check left drag (ЗНАЮ)
      else if (touchMoveX < -12) {
        const tilt = touchMoveX * 0.07;
        flashcard.style.transform = `translate3d(${touchMoveX}px, ${touchMoveY * 0.15}px, 0) rotateZ(${tilt}deg) rotateY(${rotY}deg)`;
        const opacity = Math.min(1, (-touchMoveX - 12) / 30);
        if (stampKnown) {
          stampKnown.style.opacity = opacity;
          stampKnown.classList.add('visible');
        }
        if (stampLearning) { stampLearning.style.opacity = 0; stampLearning.classList.remove('visible'); }
        if (stampDelete) { stampDelete.style.opacity = 0; stampDelete.classList.remove('visible'); }
      } else {
        flashcard.style.transform = `translate3d(${touchMoveX}px, ${touchMoveY * 0.15}px, 0) rotateY(${rotY}deg)`;
        if (stampKnown) { stampKnown.style.opacity = 0; stampKnown.classList.remove('visible'); }
        if (stampLearning) { stampLearning.style.opacity = 0; stampLearning.classList.remove('visible'); }
        if (stampDelete) { stampDelete.style.opacity = 0; stampDelete.classList.remove('visible'); }
      }
    }
  };

  const finishSwipe = (direction) => {
    if (!flashcard) return;
    flashcard.classList.remove('dragging');
    
    if (direction === 'tap') {
      flashcard.style.transform = '';
      flipCard();
    } else if (direction === 'right') {
      // Swiped Right -> УЧУ
      flashcard.classList.add('swiping-right');
      haptic('warning');
      setTimeout(() => {
        flashcard.classList.remove('swiping-right');
        flashcard.style.transform = '';
        if (btnLearning) btnLearning.click();
      }, 160);
    } else if (direction === 'left') {
      // Swiped Left -> ЗНАЮ
      flashcard.classList.add('swiping-left');
      haptic('success');
      setTimeout(() => {
        flashcard.classList.remove('swiping-left');
        flashcard.style.transform = '';
        if (btnKnown) btnKnown.click();
      }, 160);
    } else if (direction === 'down') {
      // Swiped Down -> УДАЛИТЬ
      flashcard.style.transition = 'transform 0.22s ease, opacity 0.22s ease';
      flashcard.style.transform = 'translateY(550px) rotate(20deg)';
      flashcard.style.opacity = '0';
      haptic('heavy');
      setTimeout(() => {
        flashcard.style.transition = '';
        flashcard.style.opacity = '1';
        flashcard.style.transform = '';
        deleteCardAction();
      }, 220);
    } else {
      flashcard.style.transition = 'transform 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      flashcard.style.transform = isFlipped ? 'rotateY(180deg)' : '';
      setTimeout(() => {
        if (flashcard) {
          flashcard.style.transition = '';
          if (!isFlipped) flashcard.style.transform = '';
        }
      }, 230);
    }

    if (stampKnown) { stampKnown.style.opacity = ''; stampKnown.classList.remove('visible'); }
    if (stampLearning) { stampLearning.style.opacity = ''; stampLearning.classList.remove('visible'); }
    if (stampDelete) { stampDelete.style.opacity = ''; stampDelete.classList.remove('visible'); }
  };

  const onPointerEnd = () => {
    if (!isDraggingCard) return;
    isDraggingCard = false;
    lastTouchEndTime = Date.now();
    
    const timeDelta = Math.max(1, Date.now() - touchStartTime);
    const absX = Math.abs(touchMoveX);
    const absY = Math.abs(touchMoveY);
    const velocityX = absX / timeDelta;
    const velocityY = absY / timeDelta;

    // Detect Tap (short duration, small displacement)
    if (absX < 18 && absY < 18 && timeDelta < 400) {
      finishSwipe('tap');
      return;
    }

    // Detect Swipe Down (Delete)
    if (touchMoveY > 55 || (touchMoveY > 30 && velocityY > 0.3 && touchMoveY > absX)) {
      finishSwipe('down');
      return;
    }

    // Detect Swipe Right (Учу) or Left (Знаю)
    if (touchMoveX > 30 || (touchMoveX > 14 && velocityX > 0.25)) {
      finishSwipe('right');
    } else if (touchMoveX < -30 || (touchMoveX < -14 && velocityX > 0.25)) {
      finishSwipe('left');
    } else {
      finishSwipe('center');
    }
  };

  // Touch Listeners
  cardScene.addEventListener('touchstart', (e) => {
    const t = e.touches[0];
    onPointerStart(t.clientX, t.clientY, e.target);
  }, { passive: true });

  cardScene.addEventListener('touchmove', (e) => {
    const t = e.touches[0];
    onPointerMove(t.clientX, t.clientY, e);
  }, { passive: false });

  cardScene.addEventListener('touchend', () => {
    onPointerEnd();
  });

  cardScene.addEventListener('touchcancel', () => {
    if (!isDraggingCard) return;
    isDraggingCard = false;
    lastTouchEndTime = Date.now();
    finishSwipe('center');
  });

  // Mouse Pointer Listeners (Desktop / Simulator support)
  cardScene.addEventListener('mousedown', (e) => {
    if (e.button !== 0) return; // Left click only
    if (onPointerStart(e.clientX, e.clientY, e.target)) {
      const moveHandler = (moveEvt) => {
        onPointerMove(moveEvt.clientX, moveEvt.clientY, moveEvt);
      };
      const upHandler = () => {
        document.removeEventListener('mousemove', moveHandler);
        document.removeEventListener('mouseup', upHandler);
        onPointerEnd();
      };
      document.addEventListener('mousemove', moveHandler);
      document.addEventListener('mouseup', upHandler);
    }
  });
}


// --- KEYBOARD SHORTCUTS ---
window.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  
  if (e.code === 'Space' || e.code === 'Enter') {
    e.preventDefault();
    flipCard();
  } else if (e.code === 'ArrowRight') {
    e.preventDefault();
    if (btnKnown) btnKnown.click();
  } else if (e.code === 'ArrowLeft') {
    e.preventDefault();
    if (btnLearning) btnLearning.click();
  } else if (e.code === 'KeyA') {
    e.preventDefault();
    if (currentDeck.length > 0 && currentDeck[currentIndex]) {
      speakPhrase(currentDeck[currentIndex].phrase_en);
    }
  }
});

// --- ONBOARDING GUIDE CONTROLLER ---
function checkAndShowOnboarding(step = 1) {
  if (allCards.length > 0) {
    hideOnboardingSpotlight();
    return;
  }

  const overlay = document.getElementById('onboardingSpotlight');
  const dockDict = document.getElementById('dockTabDictionary');
  const btnAdd = document.getElementById('btnOpenAddModal');
  const btnEmptyAdd = document.getElementById('btnEmptyAddWord');

  if (!overlay) return;

  if (step === 1) {
    overlay.style.display = 'block';
    document.body.classList.remove('onboarding-step-2');
    document.body.classList.add('onboarding-step-1');
    if (dockDict) dockDict.classList.add('dock-tab-spotlight');
    if (btnAdd) btnAdd.classList.remove('btn-add-spotlight');
    if (btnEmptyAdd) btnEmptyAdd.classList.remove('btn-add-spotlight');
  } else if (step === 2) {
    overlay.style.display = 'block';
    document.body.classList.remove('onboarding-step-1');
    document.body.classList.add('onboarding-step-2');
    if (dockDict) dockDict.classList.remove('dock-tab-spotlight');
    if (btnAdd) btnAdd.classList.add('btn-add-spotlight');
    if (btnEmptyAdd) btnEmptyAdd.classList.add('btn-add-spotlight');
  }
}

function hideOnboardingSpotlight() {
  const overlay = document.getElementById('onboardingSpotlight');
  const dockDict = document.getElementById('dockTabDictionary');
  const btnAdd = document.getElementById('btnOpenAddModal');
  const btnEmptyAdd = document.getElementById('btnEmptyAddWord');
  
  if (overlay) overlay.style.display = 'none';
  document.body.classList.remove('onboarding-step-1', 'onboarding-step-2');
  if (dockDict) dockDict.classList.remove('dock-tab-spotlight');
  if (btnAdd) btnAdd.classList.remove('btn-add-spotlight');
  if (btnEmptyAdd) btnEmptyAdd.classList.remove('btn-add-spotlight');
}

// --- DYNAMIC AI CATEGORIES CONTROLLER (>= 30 cards) ---
let userCategories = [];

async function fetchAndRenderCategories() {
  if (!categoryFilterCarousel) return;
  
  if (allCards.length < 30) {
    categoryFilterCarousel.style.display = 'none';
    currentCategory = 'all';
    return;
  }

  const catKey = `wow_categories_cache_${userId}_${currentTargetLang}_${currentNativeLang}`;
  try {
    const cached = localStorage.getItem(catKey);
    if (cached && (!userCategories || userCategories.length === 0)) {
      userCategories = JSON.parse(cached);
    }
  } catch (e) {}

  try {
    const res = await safeFetch(`/api/categories?user_id=${userId}&target_lang=${currentTargetLang}&native_lang=${currentNativeLang}`, {}, 2, 400);
    if (res.ok) {
      const data = await res.json();
      userCategories = data.categories || [];
      try { localStorage.setItem(catKey, JSON.stringify(userCategories)); } catch (e) {}
    }
  } catch (e) {
    console.error('Error fetching categories:', e);
  }

  if (userCategories && userCategories.length > 0) {
    categoryFilterCarousel.style.display = 'flex';
    categoryFilterCarousel.innerHTML = '';
    
    const allBtn = document.createElement('button');
    allBtn.className = `chip-filter ${currentCategory === 'all' ? 'active' : ''}`;
    allBtn.dataset.cat = 'all';
    allBtn.textContent = 'Все категории';
    allBtn.addEventListener('click', () => {
      haptic('light');
      document.querySelectorAll('.chip-filter').forEach(c => c.classList.remove('active'));
      allBtn.classList.add('active');
      currentCategory = 'all';
      renderDictionary();
    });
    categoryFilterCarousel.appendChild(allBtn);

    userCategories.forEach(cat => {
      const btn = document.createElement('button');
      btn.className = `chip-filter ${currentCategory === cat ? 'active' : ''}`;
      btn.dataset.cat = cat;
      btn.textContent = cat;
      btn.addEventListener('click', () => {
        haptic('light');
        document.querySelectorAll('.chip-filter').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = cat;
        renderDictionary();
      });
      categoryFilterCarousel.appendChild(btn);
    });
  } else {
    categoryFilterCarousel.style.display = 'none';
    currentCategory = 'all';
  }
}

// --- NAVIGATION DOCK TABS ---
document.querySelectorAll('.dock-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    haptic('light');
    document.querySelectorAll('.dock-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    tab.classList.add('active');
    const tabId = tab.dataset.tab;
    const targetContent = document.getElementById(tabId);
    if (targetContent) targetContent.classList.add('active');
    
    if (tabId === 'tabPractice') {
      if (allCards.length === 0) {
        checkAndShowOnboarding(1);
      }
    }
    if (tabId === 'tabDictionary') {
      if (activeDictSubtab === 'groups') {
        fetchAndRenderGroups();
      } else {
        renderDictionary();
      }
      if (allCards.length === 0) {
        checkAndShowOnboarding(2);
      }
    }
    if (tabId === 'tabTrainer') {
      loadTrainerSetup();
    }
    if (tabId === 'tabStats') loadStats();
    if (tabId === 'tabSupport') updateSupportTabUI();
    if (tabId === 'tabAnalytics') loadAdminAnalytics();
  });
});

// --- RENDER DICTIONARY ---
function renderDictionary() {
  if (!dictList) return;
  dictList.innerHTML = '';
  const t = I18N[currentNativeLang] || I18N['ru'];

  if (!allCards || allCards.length === 0) {
    dictList.innerHTML = `
      <div class="dict-empty-state">
        <div class="dict-empty-icon">🌱</div>
        <div class="dict-empty-title">${t.dictEmptyTitle}</div>
        <div class="dict-empty-desc">${t.dictEmptyDesc}</div>
        <button class="dict-empty-btn" id="btnEmptyAddWord">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.2" fill="none"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          <span>${t.dictEmptyBtn}</span>
        </button>
      </div>
    `;
    const btnEmptyAdd = document.getElementById('btnEmptyAddWord');
    if (btnEmptyAdd) {
      btnEmptyAdd.addEventListener('click', () => {
        hideOnboardingSpotlight();
        haptic('light');
        resetModalAddForm();
        if (addModal) addModal.classList.add('open');
      });
    }
    if (dictTotalCount) dictTotalCount.textContent = '0';
    return;
  }

  const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
  let filtered = allCards.filter(c => {
    const matchCat = (currentCategory === 'all' || c.category === currentCategory);
    const matchQuery = !query || 
      (c.phrase_en && c.phrase_en.toLowerCase().includes(query)) || 
      (c.phrase_ru && c.phrase_ru.toLowerCase().includes(query));
    return matchCat && matchQuery;
  });

  if (dictTotalCount) dictTotalCount.textContent = filtered.length;

  if (clearSearchBtn) {
    clearSearchBtn.style.display = query ? 'block' : 'none';
  }

  if (filtered.length === 0) {
    dictList.innerHTML = `
      <div class="dict-empty-state">
        <div class="dict-empty-icon">🔍</div>
        <div class="dict-empty-title">${t.dictSearchEmpty}</div>
        <div class="dict-empty-desc">${t.dictSearchEmptyDesc}</div>
      </div>
    `;
    return;
  }

  filtered.forEach(card => {
    const isK = card.status === 'known';
    const hasCat = Boolean(card.category && card.category.trim() && card.category.trim() !== '—');
    const catText = hasCat ? getLocalizedCategoryName(card.category, currentNativeLang) : (t.catEmptyTag || '+ Категория');
    const trainerSt = card.trainer_status || 'neutral';
    const dotClass = trainerSt === 'green' ? 'dot-green' : (trainerSt === 'red' ? 'dot-red' : 'dot-neutral');
    
    const item = document.createElement('div');
    item.className = 'dict-item-card';
    item.innerHTML = `
      <div class="dict-card-header">
        <div>
          <div class="dict-en-text">${card.phrase_en}</div>
          <div class="dict-ru-text">${card.phrase_ru}</div>
        </div>
        <button class="dict-speaker-mini" title="${t.hintListenRate}" aria-label="${t.hintListenRate}">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
          </svg>
        </button>
      </div>
      <div class="dict-card-footer">
        <div class="dict-tags-group">
          <div class="knowledge-dot-wrap" data-status="${trainerSt}" title="Индикатор знаний в тренажёре (клик для подсказки)">
            <span class="knowledge-dot ${dotClass}"></span>
            <span class="knowledge-dot-help">?</span>
          </div>
          <span class="status-pill ${isK ? 'status-pill-known' : 'status-pill-learning'}">
            ${isK ? t.filterKnown : t.filterLearning}
          </span>
          <span class="category-tag-mini ${hasCat ? '' : 'is-empty'}" title="Нажмите, чтобы изменить категорию">${catText}</span>
        </div>
        <button class="dict-delete-btn" title="${t.actionDelete || 'Удалить'}" aria-label="${t.actionDelete || 'Удалить'}">
          <svg viewBox="0 0 24 24" width="15" height="15" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            <line x1="10" y1="11" x2="10" y2="17"></line>
            <line x1="14" y1="11" x2="14" y2="17"></line>
          </svg>
        </button>
      </div>
    `;
    
    // Knowledge dot click listener
    const kDot = item.querySelector('.knowledge-dot-wrap');
    if (kDot) {
      kDot.addEventListener('click', (e) => {
        e.stopPropagation();
        haptic('light');
        showKnowledgeTooltip(e, trainerSt);
      });
    }
    
    // Mini speaker listener
    const speakBtn = item.querySelector('.dict-speaker-mini');
    if (speakBtn) {
      speakBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        haptic('light');
        speakPhrase(card.phrase_en, currentTargetLang, speakBtn);
      });
    }

    // Interactive category chip listener in dictionary
    const catChip = item.querySelector('.category-tag-mini');
    if (catChip) {
      catChip.addEventListener('click', (e) => {
        e.stopPropagation();
        haptic('light');
        openCategoryPickerModal(card);
      });
    }

    // Delete button in dictionary card footer
    const deleteBtn = item.querySelector('.dict-delete-btn');
    if (deleteBtn) {
      deleteBtn.addEventListener('click', async (e) => {
        e.stopPropagation();
        haptic('heavy');
        
        item.style.transition = 'all 0.25s ease';
        item.style.opacity = '0';
        item.style.transform = 'scale(0.9) translateY(-10px)';
        
        setTimeout(async () => {
          allCards = allCards.filter(c => c.id !== card.id);
          currentDeck = currentDeck.filter(c => c.id !== card.id);
          if (currentIndex >= currentDeck.length) {
            currentIndex = Math.max(0, currentDeck.length - 1);
          }
          updateCounters();
          renderDictionary();
          displayCard();
        }, 240);

        try {
          fetch('/api/card/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ card_id: card.id, user_id: userId })
          });
        } catch (err) {}
      });
    }

    // Toggle status listener
    const statusPill = item.querySelector('.status-pill');
    if (statusPill) {
      statusPill.addEventListener('click', async (e) => {
        e.stopPropagation();
        haptic('light');
        const newSt = card.status === 'known' ? 'learning' : 'known';
        card.status = newSt;
        const gc = allCards.find(c => c.id === card.id);
        if (gc) gc.status = newSt;

        try {
          fetch('/api/card_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ card_id: card.id, status: newSt, user_id: userId })
          });
        } catch (e) {}

        updateCounters();
        renderDictionary();
        applyFilter(currentFilter);
      });
    }

    dictList.appendChild(item);
  });

  setTimeout(updateFastScroller, 100);
}

// --- TOUCH-FRIENDLY INTERACTIVE FAST SCROLLER ---
let isFastScrollerDragging = false;

function updateFastScroller() {
  const track = document.getElementById('dictFastScrollerTrack');
  const thumb = document.getElementById('dictFastScrollerThumb');
  const appMain = document.querySelector('.app-main');
  const tabDict = document.getElementById('tabDictionary');
  const subviewList = document.getElementById('dictSubviewList');

  if (!track || !thumb || !appMain || !tabDict) return;

  const isDictActive = tabDict.classList.contains('active') && (!subviewList || subviewList.classList.contains('active'));
  if (!isDictActive || isFastScrollerDragging) {
    if (!isDictActive) track.style.display = 'none';
    return;
  }

  const scrollHeight = appMain.scrollHeight;
  const clientHeight = appMain.clientHeight;
  const maxScroll = scrollHeight - clientHeight;

  if (maxScroll <= 30) {
    track.style.display = 'none';
    return;
  }

  track.style.display = 'flex';
  const trackHeight = track.clientHeight - thumb.clientHeight;
  if (trackHeight <= 0) return;

  const scrollRatio = Math.min(1, Math.max(0, appMain.scrollTop / maxScroll));
  const thumbTop = scrollRatio * trackHeight;
  thumb.style.transform = `translateY(${thumbTop}px)`;
}

function initFastScroller() {
  const track = document.getElementById('dictFastScrollerTrack');
  const thumb = document.getElementById('dictFastScrollerThumb');
  const bubble = document.getElementById('scrollerBubble');
  const appMain = document.querySelector('.app-main');

  if (!track || !thumb || !appMain) return;

  function updateBubble(ratio) {
    if (!bubble) return;
    const total = allCards.length || 0;
    if (total === 0) {
      bubble.textContent = '0 фраз';
      return;
    }
    const currentNum = Math.min(total, Math.max(1, Math.round(ratio * total)));
    bubble.textContent = `${currentNum} из ${total}`;
  }

  function handleScrollerMove(clientY) {
    const rect = track.getBoundingClientRect();
    const trackTop = rect.top;
    const trackHeight = rect.height - thumb.clientHeight;
    if (trackHeight <= 0) return;

    const targetTop = Math.min(trackHeight, Math.max(0, clientY - trackTop - thumb.clientHeight / 2));
    const ratio = targetTop / trackHeight;

    thumb.style.transform = `translateY(${targetTop}px)`;
    const maxScroll = appMain.scrollHeight - appMain.clientHeight;
    appMain.scrollTop = ratio * maxScroll;

    updateBubble(ratio);
  }

  function onPointerDown(e) {
    e.preventDefault();
    e.stopPropagation();
    isFastScrollerDragging = true;
    thumb.classList.add('dragging');
    haptic('medium');

    const clientY = e.clientY ?? (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
    handleScrollerMove(clientY);

    if (thumb.setPointerCapture && e.pointerId !== undefined) {
      try { thumb.setPointerCapture(e.pointerId); } catch (err) {}
    }
  }

  function onPointerMove(e) {
    if (!isFastScrollerDragging) return;
    e.preventDefault();
    e.stopPropagation();

    const clientY = e.clientY ?? (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
    handleScrollerMove(clientY);
  }

  function onPointerUp(e) {
    if (!isFastScrollerDragging) return;
    isFastScrollerDragging = false;
    thumb.classList.remove('dragging');
    haptic('light');
    updateFastScroller();
  }

  // Pointer Events (Mouse, Pen, Touch)
  thumb.addEventListener('pointerdown', onPointerDown);
  track.addEventListener('pointerdown', onPointerDown);

  window.addEventListener('pointermove', onPointerMove, { passive: false });
  window.addEventListener('pointerup', onPointerUp);
  window.addEventListener('pointercancel', onPointerUp);

  // Fallback direct touch listeners for iOS / Android WebViews
  thumb.addEventListener('touchstart', onPointerDown, { passive: false });
  track.addEventListener('touchstart', onPointerDown, { passive: false });
  window.addEventListener('touchmove', onPointerMove, { passive: false });
  window.addEventListener('touchend', onPointerUp);

  appMain.addEventListener('scroll', updateFastScroller, { passive: true });
}

if (searchInput) searchInput.addEventListener('input', renderDictionary);
if (clearSearchBtn) {
  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    renderDictionary();
    searchInput.focus();
  });
}

if (btnExportExcelLink) {
  btnExportExcelLink.addEventListener('click', () => {
    window.open(`/api/cards?user_id=${userId}&shuffle=false`, '_blank');
  });
}

// --- MODAL: ADD PHRASES & AI AUTO-TRANSLATION ---
if (btnOpenAddModal) {
  btnOpenAddModal.addEventListener('click', () => {
    hideOnboardingSpotlight();
    haptic('light');
    resetModalAddForm();
    if (addModal) addModal.classList.add('open');
    setTimeout(() => { if (newPhraseEn) newPhraseEn.focus(); }, 150);
  });
}

if (btnCloseModal) {
  btnCloseModal.addEventListener('click', () => {
    if (addModal) addModal.classList.remove('open');
  });
}

if (tabModeSingle && tabModeBulk) {
  tabModeSingle.addEventListener('click', () => {
    haptic('light');
    tabModeSingle.classList.add('active');
    tabModeBulk.classList.remove('active');
    if (modalSingleBody) modalSingleBody.style.display = 'flex';
    if (modalBulkBody) modalBulkBody.style.display = 'none';
  });

  tabModeBulk.addEventListener('click', () => {
    haptic('light');
    tabModeBulk.classList.add('active');
    tabModeSingle.classList.remove('active');
    if (modalSingleBody) modalSingleBody.style.display = 'none';
    if (modalBulkBody) modalBulkBody.style.display = 'flex';
  });
}

let translateDebounceTimer = null;
let isProgrammaticUpdate = false;


function setAiStatus(state, text) {
  if (!aiStatusBadge) return;
  aiStatusBadge.classList.remove('loading', 'success');
  
  if (state === 'loading') {
    aiStatusBadge.classList.add('loading');
    if (aiSpinner) aiSpinner.style.display = 'block';
    if (aiStatusText) aiStatusText.textContent = text || 'AI переводит...';
  } else if (state === 'success') {
    aiStatusBadge.classList.add('success');
    if (aiSpinner) aiSpinner.style.display = 'none';
    if (aiStatusText) aiStatusText.textContent = text || 'Живой перевод готов ✨';
  } else {
    if (aiSpinner) aiSpinner.style.display = 'none';
    if (aiStatusText) aiStatusText.textContent = text || 'AI автоперевод активен';
  }
}

function renderAlternativeChips(alternatives, targetField) {
  if (!aiAlternativesBox || !aiAltChips) return;
  
  if (!alternatives || alternatives.length === 0) {
    aiAlternativesBox.style.display = 'none';
    aiAltChips.innerHTML = '';
    return;
  }
  
  aiAltChips.innerHTML = '';
  alternatives.forEach(alt => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'ai-chip';
    chip.textContent = alt;
    chip.title = 'Нажмите, чтобы применить этот вариант';
    
    chip.addEventListener('click', (e) => {
      e.preventDefault();
      haptic('light');
      
      // Clean up bracket notes like "(разговорное)" if user clicks
      let cleanText = alt.replace(/\s*\([^)]*\)/g, '').trim();
      if (!cleanText) cleanText = alt;
      
      if (targetField === 'ru' && newPhraseRu) {
        newPhraseRu.value = cleanText;
        if (btnClearRu) btnClearRu.style.display = 'flex';
      } else if (targetField === 'en' && newPhraseEn) {
        newPhraseEn.value = cleanText;
        if (btnClearEn) btnClearEn.style.display = 'flex';
      }
      
      setAiStatus('success', 'Выбран вариант ✨');
    });
    
    aiAltChips.appendChild(chip);
  });
  
  aiAlternativesBox.style.display = 'flex';
}

let currentTranslationRequestId = 0;

async function triggerAiTranslation(sourceField = 'en') {
  if (isProgrammaticUpdate) return;
  
  const srcInput = sourceField === 'en' ? newPhraseEn : newPhraseRu;
  const tgtInput = sourceField === 'en' ? newPhraseRu : newPhraseEn;
  const val = srcInput ? srcInput.value.trim() : '';
  
  if (!val) {
    if (tgtInput && !tgtInput.value.trim()) {
      if (aiAlternativesBox) aiAlternativesBox.style.display = 'none';
      if (autoCategoryTag) autoCategoryTag.style.display = 'none';
      setAiStatus('idle', 'AI автоперевод активен');
    }
    return;
  }
  
  const reqId = ++currentTranslationRequestId;
  setAiStatus('loading', 'AI переводит...');
  
  try {
    const res = await fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: val,
        source_field: sourceField,
        native_lang: currentNativeLang,
        target_lang: currentTargetLang
      })
    });
    
    if (reqId !== currentTranslationRequestId) return;

    if (res.ok) {
      const data = await res.json();
      if (reqId !== currentTranslationRequestId) return;

      if (data.status === 'ok') {
        isProgrammaticUpdate = true;
        
        let targetFieldForChips = 'ru';
        
        if (data.field_corrected) {
          if (sourceField === 'en') {
            if (newPhraseRu) newPhraseRu.value = data.original;
            if (newPhraseEn) newPhraseEn.value = data.translation;
            targetFieldForChips = 'en';
          } else {
            if (newPhraseEn) newPhraseEn.value = data.original;
            if (newPhraseRu) newPhraseRu.value = data.translation;
            targetFieldForChips = 'ru';
          }
        } else {
          if (tgtInput) {
            tgtInput.value = data.translation;
          }
          targetFieldForChips = sourceField === 'en' ? 'ru' : 'en';
        }
        
        // Auto category selection
        if (data.category && newCategorySelect) {
          for (let i = 0; i < newCategorySelect.options.length; i++) {
            if (newCategorySelect.options[i].value === data.category || data.category.includes(newCategorySelect.options[i].value)) {
              newCategorySelect.selectedIndex = i;
              break;
            }
          }
          if (autoCategoryTag) {
            autoCategoryTag.textContent = `✨ ${data.category}`;
            autoCategoryTag.style.display = 'inline-block';
          }
        }
        
        // Render alternatives suggestions
        renderAlternativeChips(data.alternatives, targetFieldForChips);
        
        // Update clear button visibility
        if (btnClearEn && newPhraseEn) btnClearEn.style.display = newPhraseEn.value ? 'flex' : 'none';
        if (btnClearRu && newPhraseRu) btnClearRu.style.display = newPhraseRu.value ? 'flex' : 'none';
        
        setAiStatus('success', 'Живой перевод готов ✨');
        haptic('light');
        
        setTimeout(() => { isProgrammaticUpdate = false; }, 80);
      } else {
        setAiStatus('idle', 'AI автоперевод активен');
      }
    } else {
      if (reqId === currentTranslationRequestId) setAiStatus('idle', 'AI автоперевод активен');
    }
  } catch (err) {
    console.error("Translation API error:", err);
    if (reqId === currentTranslationRequestId) setAiStatus('idle', 'AI автоперевод активен');
  }
}

function handleInputWithDebounce(sourceField) {
  if (isProgrammaticUpdate) return;
  
  const srcInput = sourceField === 'en' ? newPhraseEn : newPhraseRu;
  const val = srcInput ? srcInput.value.trim() : '';

  if (sourceField === 'en') {
    if (btnClearEn && newPhraseEn) btnClearEn.style.display = newPhraseEn.value ? 'flex' : 'none';
  } else {
    if (btnClearRu && newPhraseRu) btnClearRu.style.display = newPhraseRu.value ? 'flex' : 'none';
  }

  if (val.length > 0) {
    setAiStatus('loading', 'AI думает над фразой...');
  } else {
    currentTranslationRequestId++;
    if (aiAlternativesBox) aiAlternativesBox.style.display = 'none';
    if (autoCategoryTag) autoCategoryTag.style.display = 'none';
    setAiStatus('idle', 'AI автоперевод активен');
    clearTimeout(translateDebounceTimer);
    return;
  }
  
  clearTimeout(translateDebounceTimer);
  translateDebounceTimer = setTimeout(() => {
    triggerAiTranslation(sourceField);
  }, 500);
}

// Input Event Listeners
if (newPhraseEn) {
  newPhraseEn.addEventListener('input', () => handleInputWithDebounce('en'));
}

if (newPhraseRu) {
  newPhraseRu.addEventListener('input', () => handleInputWithDebounce('ru'));
}

// Manual Sparkle AI Translate Buttons
if (btnTranslateEn) {
  btnTranslateEn.addEventListener('click', (e) => {
    e.preventDefault();
    haptic('light');
    clearTimeout(translateDebounceTimer);
    triggerAiTranslation('en');
  });
}

if (btnTranslateRu) {
  btnTranslateRu.addEventListener('click', (e) => {
    e.preventDefault();
    haptic('light');
    clearTimeout(translateDebounceTimer);
    triggerAiTranslation('ru');
  });
}

// Clear Buttons
if (btnClearEn) {
  btnClearEn.addEventListener('click', (e) => {
    e.preventDefault();
    if (newPhraseEn) newPhraseEn.value = '';
    btnClearEn.style.display = 'none';
    if (aiAlternativesBox) aiAlternativesBox.style.display = 'none';
    if (autoCategoryTag) autoCategoryTag.style.display = 'none';
    setAiStatus('idle', 'AI автоперевод активен');
    if (newPhraseEn) newPhraseEn.focus();
  });
}

if (btnClearRu) {
  btnClearRu.addEventListener('click', (e) => {
    e.preventDefault();
    if (newPhraseRu) newPhraseRu.value = '';
    btnClearRu.style.display = 'none';
    if (aiAlternativesBox) aiAlternativesBox.style.display = 'none';
    if (autoCategoryTag) autoCategoryTag.style.display = 'none';
    setAiStatus('idle', 'AI автоперевод активен');
    if (newPhraseRu) newPhraseRu.focus();
  });
}

// Swap Fields Button
if (btnSwapFields) {
  btnSwapFields.addEventListener('click', (e) => {
    e.preventDefault();
    haptic('light');
    if (!newPhraseEn || !newPhraseRu) return;
    
    isProgrammaticUpdate = true;
    const temp = newPhraseEn.value;
    newPhraseEn.value = newPhraseRu.value;
    newPhraseRu.value = temp;
    
    if (btnClearEn) btnClearEn.style.display = newPhraseEn.value ? 'flex' : 'none';
    if (btnClearRu) btnClearRu.style.display = newPhraseRu.value ? 'flex' : 'none';
    
    setTimeout(() => {
      isProgrammaticUpdate = false;
      if (newPhraseEn.value.trim()) {
        triggerAiTranslation('en');
      }
    }, 50);
  });
}

function resetModalAddForm() {
  isProgrammaticUpdate = true;
  if (newPhraseEn) newPhraseEn.value = '';
  if (newPhraseRu) newPhraseRu.value = '';
  if (btnClearEn) btnClearEn.style.display = 'none';
  if (btnClearRu) btnClearRu.style.display = 'none';
  if (aiAlternativesBox) aiAlternativesBox.style.display = 'none';
  if (autoCategoryTag) autoCategoryTag.style.display = 'none';
  if (newCategorySelect) newCategorySelect.value = 'Разговорный / Общее';
  setAiStatus('idle', 'AI автоперевод активен');
  setTimeout(() => { isProgrammaticUpdate = false; }, 50);
}

// Save Single Phrase
if (btnSaveNewWord) {
  btnSaveNewWord.addEventListener('click', async () => {
    const en = newPhraseEn ? newPhraseEn.value.trim() : '';
    const ru = newPhraseRu ? newPhraseRu.value.trim() : '';
    const cat = newCategorySelect ? newCategorySelect.value : 'Разговорный / Общее';

    if (!en) {
      const targetMeta = SUPPORTED_LANGS[currentTargetLang] || SUPPORTED_LANGS['en'];
      alert(`Пожалуйста, введите фразу на ${targetMeta.name.toLowerCase()}`);
      return;
    }

    try {
      const res = await fetch('/api/cards', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          phrase_en: en,
          phrase_ru: ru,
          category: cat,
          target_lang: currentTargetLang,
          native_lang: currentNativeLang
        })
      });
      if (res.ok) {
        haptic('success');
        resetModalAddForm();
        if (addModal) addModal.classList.remove('open');
        await loadData();
      }
    } catch (e) {
      alert("Ошибка при сохранении карточки");
    }
  });
}


// Bulk Import Input Tracker
if (bulkTextInput && bulkCount) {
  bulkTextInput.addEventListener('input', () => {
    const lines = bulkTextInput.value.split('\n').filter(l => l.trim().length > 1);
    bulkCount.textContent = lines.length;
  });
}

if (btnSaveBulk) {
  btnSaveBulk.addEventListener('click', async () => {
    const text = bulkTextInput ? bulkTextInput.value.trim() : '';
    if (!text) {
      alert("Вставьте фразы из таблицы Excel или списка");
      return;
    }

    try {
      const res = await fetch('/api/cards/bulk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          raw_text: text,
          target_lang: currentTargetLang,
          native_lang: currentNativeLang
        })
      });
      if (res.ok) {
        const data = await res.json();
        haptic('success');
        launchConfetti();
        alert(`✅ Успешно добавлено ${data.added_count} карточек!`);
        if (bulkTextInput) bulkTextInput.value = '';
        if (addModal) addModal.classList.remove('open');
        await loadData();
      }
    } catch (e) {
      alert("Ошибка при пакетном импорте карточек");
    }
  });
}

// --- ADMIN ANALYTICS CONTROLLER ---
let adminAnalyticsData = null;

async function checkAdminAccess() {
  const isDirectAdm = Boolean(
    userId === 466788167 || 
    tg?.initDataUnsafe?.user?.id === 466788167 || 
    tg?.initDataUnsafe?.user?.username?.toLowerCase() === 'hitrova_olga' ||
    window.location.hostname === 'localhost' || 
    window.location.hostname === '127.0.0.1'
  );
  const dockTabAnalytics = document.getElementById('dockTabAnalytics');
  const dockTabSupport = document.getElementById('dockTabSupport');
  const dockTabTrainer = document.getElementById('dockTabTrainer');

  // Trainer tab is a core feature and is ALWAYS visible for ALL users
  if (dockTabTrainer) dockTabTrainer.style.display = 'flex';

  if (isDirectAdm) {
    if (dockTabAnalytics) dockTabAnalytics.style.display = 'flex';
    if (dockTabSupport) dockTabSupport.style.display = 'none';
  }

  try {
    const res = await fetch(`/api/admin/check?user_id=${userId}`);
    if (res.ok) {
      const data = await res.json();
      const isAdm = Boolean(data.is_admin || isDirectAdm);

      if (isAdm) {
        if (dockTabAnalytics) dockTabAnalytics.style.display = 'flex';
        if (dockTabSupport) dockTabSupport.style.display = 'none';
        
        // If opened with ?tab=trainer or ?tab=analytics, open tab directly
        const tabParam = urlParams.get('tab');
        if (tabParam === 'trainer' && dockTabTrainer) {
          dockTabTrainer.click();
        } else if (tabParam === 'analytics' && dockTabAnalytics) {
          dockTabAnalytics.click();
        }
      } else {
        if (dockTabAnalytics) dockTabAnalytics.style.display = 'none';
        if (dockTabSupport) dockTabSupport.style.display = 'flex';
      }
    }
  } catch (e) {
    console.log('Admin check:', e);
  }
}

async function loadAdminAnalytics() {
  try {
    const res = await fetch(`/api/admin/analytics?user_id=${userId}`);
    if (!res.ok) return;
    adminAnalyticsData = await res.json();
    renderAdminAnalytics(adminAnalyticsData);
  } catch (e) {
    console.error('Error loading admin analytics:', e);
  }
}

function renderAdminAnalytics(data) {
  if (!data) return;

  // KPIs
  const elTotal = document.getElementById('adminTotalUsers');
  const elNewToday = document.getElementById('adminNewTodayTag');
  const elNew7d = document.getElementById('adminNew7d');
  const elActiveToday = document.getElementById('adminActiveToday');
  const elActive7d = document.getElementById('adminActive7d');
  const elTotalCards = document.getElementById('adminTotalCards');
  const elAvgCards = document.getElementById('adminAvgCardsTag');
  const elKnownCards = document.getElementById('adminKnownCards');
  const elLearningCards = document.getElementById('adminLearningCards');
  const elUsersCount = document.getElementById('adminUsersCount');

  if (elTotal) elTotal.textContent = data.total_users || 0;
  if (elNewToday) elNewToday.textContent = `+${data.new_users_today || 0} сегодня`;
  if (elNew7d) elNew7d.textContent = `+${data.new_users_7d || 0}`;
  if (elActiveToday) elActiveToday.textContent = data.active_today || 0;
  if (elActive7d) elActive7d.textContent = `${data.active_7d || 0}`;
  if (elTotalCards) elTotalCards.textContent = data.total_cards || 0;
  if (elAvgCards) elAvgCards.textContent = `${data.avg_cards_per_user || 0} ср./чел`;
  if (elKnownCards) elKnownCards.textContent = `${data.known_cards || 0}`;
  if (elLearningCards) elLearningCards.textContent = `${data.learning_cards || 0}`;
  if (elUsersCount) elUsersCount.textContent = (data.users_list || []).length;

  // Activity 7-Day Chart
  renderAdminActivityChart(data.daily_stats || []);

  // Language Breakdown
  renderAdminLanguageDistribution(data.language_stats || []);

  // Users List
  renderAdminUsersList(data.users_list || []);
}

function renderAdminLanguageDistribution(langs) {
  const container = document.getElementById('adminLangDistributionList');
  if (!container) return;
  container.innerHTML = '';

  const totalUsersInLangs = langs.reduce((sum, l) => sum + (l.users_count || 0), 0) || 1;

  langs.forEach(l => {
    const row = document.createElement('div');
    row.className = 'admin-lang-row';
    const pct = Math.round((l.users_count / totalUsersInLangs) * 100);
    row.innerHTML = `
      <div class="admin-lang-meta">
        <span class="admin-lang-flag">${l.flag}</span>
        <span class="admin-lang-name">${l.name}</span>
      </div>
      <div class="admin-lang-track">
        <div class="admin-lang-fill" style="width: ${Math.max(pct, 4)}%;"></div>
      </div>
      <div class="admin-lang-stat">
        <span>👥 ${l.users_count}</span>
        <span style="opacity: 0.6; font-size: 10px; margin-left: 4px;">(${l.cards_count} карт.)</span>
      </div>
    `;
    container.appendChild(row);
  });
}

function renderAdminActivityChart(dailyStats) {
  const container = document.getElementById('adminActivityBars');
  if (!container) return;
  container.innerHTML = '';

  const maxVal = Math.max(...dailyStats.map(d => Math.max(d.active_users, d.new_users, 1)), 5);

  dailyStats.forEach(d => {
    const activeHeight = Math.max(Math.round((d.active_users / maxVal) * 56), 4);
    const col = document.createElement('div');
    col.className = 'admin-bar-col';
    col.innerHTML = `
      <span class="admin-bar-val">${d.active_users}</span>
      <div class="admin-bar-track">
        <div class="admin-bar-fill" style="height: ${activeHeight}px;"></div>
      </div>
      <span class="admin-bar-label">${d.label}</span>
    `;
    container.appendChild(col);
  });
}

function renderAdminUsersList(users) {
  const listEl = document.getElementById('adminUsersList');
  if (!listEl) return;
  const t = I18N[currentNativeLang] || I18N['ru'];
  
  const search = (document.getElementById('adminSearchInput')?.value || '').toLowerCase().trim();
  const filtered = users.filter(u => {
    if (!search) return true;
    return (u.full_name || '').toLowerCase().includes(search) || (u.username || '').toLowerCase().includes(search) || String(u.user_id).includes(search);
  });

  listEl.innerHTML = '';
  if (filtered.length === 0) {
    listEl.innerHTML = `
      <div style="text-align: center; padding: 20px; color: var(--text-tertiary); font-size: 13px;">
        ${t.adminStudentsNotFound}
      </div>
    `;
    return;
  }

  filtered.forEach(u => {
    const card = document.createElement('div');
    card.className = 'admin-user-card';
    
    const initials = (u.full_name && u.full_name !== 'Без имени') 
      ? u.full_name.charAt(0).toUpperCase() 
      : (u.username ? u.username.charAt(0).toUpperCase() : 'U');
      
    const handle = u.username ? `@${u.username}` : (u.full_name || 'Без имени');
    const streak = u.streak_days > 1 ? `🔥 ${u.streak_days} дн.` : `🌱 1 дн.`;
    const langPairStr = u.lang_pair_str || '🇷🇺 ➔ 🇬🇧 EN';
    
    card.innerHTML = `
      <div class="admin-user-left">
        <div class="admin-user-avatar">${initials}</div>
        <div class="admin-user-meta">
          <div class="admin-user-name">${handle}</div>
          <div class="admin-user-details">
            <span>${streak}</span>
            <span>•</span>
            <span style="font-weight: 600;">${langPairStr}</span>
            <span>•</span>
            <span>📚 ${u.total_cards} сл.</span>
          </div>
        </div>
      </div>
      <div class="admin-user-right">
        <div class="admin-user-cards-badge">${u.total_cards} карточек</div>
        <div class="admin-user-date">${u.created_at ? u.created_at.split(' ')[0] : 'сегодня'}</div>
      </div>
    `;
    listEl.appendChild(card);
  });
}

// Search input listener
const adminSearchInput = document.getElementById('adminSearchInput');
if (adminSearchInput) {
  adminSearchInput.addEventListener('input', () => {
    if (adminAnalyticsData) {
      renderAdminUsersList(adminAnalyticsData.users_list || []);
    }
  });
}

// Export Excel Button
const btnAdminExportExcel = document.getElementById('btnAdminExportExcel');
if (btnAdminExportExcel) {
  btnAdminExportExcel.addEventListener('click', () => {
    haptic('success');
    window.location.href = `/api/admin/export-excel?user_id=${userId}`;
  });
}

// --- Support & Developer Contact Modal Controller ---
let currentSupportCategory = '💡 Идея / Предложение';

function initSupportModal() {
  const modal = document.getElementById('modalSupport');
  const btnOpen = document.getElementById('btnOpenSupportModal');
  const btnClose = document.getElementById('btnCloseSupportModal');
  const btnSend = document.getElementById('btnSendSupport');
  const btnDirect = document.getElementById('btnDirectTg');
  const messageInput = document.getElementById('supportMessageInput');

  if (btnOpen && modal) {
    btnOpen.addEventListener('click', () => {
      haptic('light');
      updateLanguageUI();
      modal.style.display = 'flex';
      setTimeout(() => modal.classList.add('open'), 10);
      if (messageInput) messageInput.focus();
    });
  }

  if (btnClose && modal) {
    btnClose.addEventListener('click', () => {
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
    });
  }

  // Support category chips
  document.querySelectorAll('#supportChipsGrid .support-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      haptic('light');
      document.querySelectorAll('#supportChipsGrid .support-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentSupportCategory = btn.dataset.cat;
    });
  });

  // Direct Telegram contact button
  if (btnDirect) {
    btnDirect.addEventListener('click', () => {
      haptic('light');
      if (tg?.openTelegramLink) {
        tg.openTelegramLink('https://t.me/Hitrova_Olga');
      } else {
        window.open('https://t.me/Hitrova_Olga', '_blank');
      }
    });
  }

  // Send support message
  if (btnSend && modal) {
    btnSend.addEventListener('click', async () => {
      const t = I18N[currentNativeLang] || I18N['ru'];
      const msg = messageInput ? messageInput.value.trim() : '';
      if (!msg) {
        alert(t.supportEmptyError || "Пожалуйста, введите текст сообщения.");
        return;
      }

      btnSend.disabled = true;
      const sendSpan = document.getElementById('btnSendSupportSpan');
      if (sendSpan) sendSpan.textContent = "...";

      try {
        const res = await fetch('/api/support', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: userId,
            message: msg,
            category: currentSupportCategory,
            native_lang: currentNativeLang,
            target_lang: currentTargetLang
          })
        });

        if (res.ok) {
          haptic('success');
          launchConfetti();
          alert(t.supportSuccess || "✅ Сообщение отправлено! Разработчик скоро ответит вам.");
          if (messageInput) messageInput.value = '';
          modal.classList.remove('open');
          setTimeout(() => modal.style.display = 'none', 200);
        } else {
          alert("Не удалось отправить сообщение. Попробуйте написать напрямую @Hitrova_Olga.");
        }
      } catch (e) {
        alert("Ошибка сети при отправке сообщения.");
      } finally {
        btnSend.disabled = false;
        if (sendSpan) sendSpan.textContent = t.btnSendSupport || "Отправить";
      }
    });
  }
}

// --- Support Tab in Main Content Controller ---
let currentSupportTabCategory = '💡 Идея / Предложение';

function updateSupportTabUI() {
  const t = I18N[currentNativeLang] || I18N['ru'];
  const title = document.getElementById('supportTabTitle');
  if (title) title.textContent = t.modalSupportTitle || "Связь с разработчиком & Поддержка";
  const sub = document.getElementById('supportTabSubtitle');
  if (sub) sub.textContent = t.modalSupportSubtitle || "Есть идея, вопрос или нашли ошибку? Напишите нам!";
  const catLabel = document.getElementById('supportTabCatLabel');
  if (catLabel) catLabel.textContent = t.supportCatLabel || "Выберите тему:";
  const msgLabel = document.getElementById('supportTabMsgLabel');
  if (msgLabel) msgLabel.textContent = t.supportMsgLabel || "Ваше сообщение:";
  const input = document.getElementById('supportTabMessageInput');
  if (input) input.placeholder = t.supportMsgPlaceholder || "Опишите вашу идею, вопрос или пожелание...";
  const tgSpan = document.getElementById('btnTabDirectTgSpan');
  if (tgSpan) tgSpan.textContent = t.btnDirectTg || "Написать в Telegram";
  const sendSpan = document.getElementById('btnSendTabSupportSpan');
  if (sendSpan) sendSpan.textContent = t.btnSendSupport || "Отправить";
}

function initSupportTab() {
  // Support category chips in Tab 4
  document.querySelectorAll('#supportTabChipsGrid .support-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      haptic('light');
      document.querySelectorAll('#supportTabChipsGrid .support-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentSupportTabCategory = btn.dataset.cat;
    });
  });

  // Direct Telegram contact button in Tab 4
  const btnDirect = document.getElementById('btnTabDirectTg');
  if (btnDirect) {
    btnDirect.addEventListener('click', () => {
      haptic('light');
      if (tg?.openTelegramLink) {
        tg.openTelegramLink('https://t.me/Hitrova_Olga');
      } else {
        window.open('https://t.me/Hitrova_Olga', '_blank');
      }
    });
  }

  // Send support message from Tab 4
  const btnSend = document.getElementById('btnSendTabSupport');
  const messageInput = document.getElementById('supportTabMessageInput');

  if (btnSend) {
    btnSend.addEventListener('click', async () => {
      const t = I18N[currentNativeLang] || I18N['ru'];
      const msg = messageInput ? messageInput.value.trim() : '';
      if (!msg) {
        alert(t.supportEmptyError || "Пожалуйста, введите текст сообщения.");
        return;
      }

      btnSend.disabled = true;
      const sendSpan = document.getElementById('btnSendTabSupportSpan');
      if (sendSpan) sendSpan.textContent = "...";

      try {
        const res = await fetch('/api/support', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: userId,
            message: msg,
            category: currentSupportTabCategory,
            native_lang: currentNativeLang,
            target_lang: currentTargetLang
          })
        });

        if (res.ok) {
          haptic('success');
          launchConfetti();
          alert(t.supportSuccess || "✅ Сообщение отправлено! Разработчик скоро ответит вам.");
          if (messageInput) messageInput.value = '';
        } else {
          alert("Не удалось отправить сообщение. Попробуйте написать напрямую @Hitrova_Olga.");
        }
      } catch (e) {
        alert("Ошибка сети при отправке сообщения.");
      } finally {
        btnSend.disabled = false;
        if (sendSpan) sendSpan.textContent = t.btnSendSupport || "Отправить";
      }
    });
  }
}

// --- CATEGORY PICKER & EDITOR CONTROLLER ---
let activeCardForCategory = null;
let selectedCategoryChoice = '';

function openCategoryPickerModal(card) {
  if (!card) return;
  activeCardForCategory = card;
  selectedCategoryChoice = (card.category && card.category.trim() !== '—') ? card.category.trim() : '';
  
  const modal = document.getElementById('modalCategoryPicker');
  const preview = document.getElementById('catPickerPhrasePreview');
  const chipsGrid = document.getElementById('catPickerChipsGrid');
  const customInput = document.getElementById('customCategoryInput');

  if (preview) {
    preview.textContent = `${card.phrase_ru || ''} — ${card.phrase_en || ''}`;
  }
  if (customInput) {
    customInput.value = '';
  }

  // Build standard list of categories + user's existing categories
  const standardCategories = [
    'Деловая переписка',
    'Логистика и ВЭД',
    'Собеседование',
    'Разговорный / Общее',
    'Путешествия и отель',
    'IT и технологии',
    'Покупки и кафе',
    'Эмоции и мысли'
  ];

  const existingInUser = allCards
    .map(c => (c.category || '').trim())
    .filter(c => c && c !== '—' && !standardCategories.includes(c));
  const allChoices = Array.from(new Set([...standardCategories, ...existingInUser]));

  if (chipsGrid) {
    chipsGrid.innerHTML = '';
    allChoices.forEach(catName => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = `cat-picker-chip ${selectedCategoryChoice === catName ? 'active' : ''}`;
      chip.textContent = getLocalizedCategoryName(catName, currentNativeLang);
      chip.addEventListener('click', () => {
        haptic('light');
        document.querySelectorAll('#catPickerChipsGrid .cat-picker-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        selectedCategoryChoice = catName;
        if (customInput) customInput.value = '';
      });
      chipsGrid.appendChild(chip);
    });
  }

  if (modal) {
    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('open'), 10);
  }
}

function initCategoryPickerModal() {
  const modal = document.getElementById('modalCategoryPicker');
  const btnClose = document.getElementById('btnCloseCatPickerModal');
  const btnRemove = document.getElementById('btnRemoveCategory');
  const btnSave = document.getElementById('btnSaveCardCategory');
  const customInput = document.getElementById('customCategoryInput');

  if (btnClose && modal) {
    btnClose.addEventListener('click', () => {
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
    });
  }

  if (btnRemove && modal) {
    btnRemove.addEventListener('click', async () => {
      if (!activeCardForCategory) return;
      haptic('warning');
      await applyCategoryUpdate(activeCardForCategory.id, '');
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
    });
  }

  if (btnSave && modal) {
    btnSave.addEventListener('click', async () => {
      if (!activeCardForCategory) return;
      haptic('success');
      let finalCat = selectedCategoryChoice;
      if (customInput && customInput.value.trim()) {
        finalCat = customInput.value.trim();
      }
      await applyCategoryUpdate(activeCardForCategory.id, finalCat);
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
    });
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('open');
        setTimeout(() => modal.style.display = 'none', 200);
      }
    });
  }
}

async function applyCategoryUpdate(cardId, newCat) {
  const card = allCards.find(c => c.id === cardId);
  if (card) card.category = newCat;
  const deckCard = currentDeck.find(c => c.id === cardId);
  if (deckCard) deckCard.category = newCat;

  displayCard();
  renderDictionary();
  await fetchAndRenderCategories();

  try {
    await fetch('/api/card/category', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card_id: cardId, category: newCat, user_id: userId })
    });
  } catch (err) {
    console.error('Failed to update category:', err);
  }
}

// ==========================================================================
// GROUPS & KNOWLEDGE STATUS MODULE
// ==========================================================================
let activeDictSubtab = 'list'; // 'list' or 'groups'
let userGroups = [];
let groupSearchQuery = '';
let editingGroupId = null;

function initDictSubtabs() {
  const btnList = document.getElementById('subtabDictList');
  const btnGroups = document.getElementById('subtabDictGroups');
  const viewList = document.getElementById('dictSubviewList');
  const viewGroups = document.getElementById('dictSubviewGroups');

  if (btnList && btnGroups) {
    btnList.addEventListener('click', () => {
      haptic('light');
      activeDictSubtab = 'list';
      btnList.classList.add('active');
      btnGroups.classList.remove('active');
      if (viewList) {
        viewList.classList.add('active');
        viewList.style.display = 'block';
      }
      if (viewGroups) {
        viewGroups.classList.remove('active');
        viewGroups.style.display = 'none';
      }
      renderDictionary();
    });

    btnGroups.addEventListener('click', () => {
      haptic('light');
      activeDictSubtab = 'groups';
      btnGroups.classList.add('active');
      btnList.classList.remove('active');
      if (viewList) {
        viewList.classList.remove('active');
        viewList.style.display = 'none';
      }
      if (viewGroups) {
        viewGroups.classList.add('active');
        viewGroups.style.display = 'block';
      }
      fetchAndRenderGroups();
    });
  }

  // Group search input
  const groupsSearchInput = document.getElementById('groupsSearchInput');
  const clearGroupsSearchBtn = document.getElementById('clearGroupsSearchBtn');
  if (groupsSearchInput) {
    groupsSearchInput.addEventListener('input', () => {
      groupSearchQuery = groupsSearchInput.value.trim().toLowerCase();
      if (clearGroupsSearchBtn) {
        clearGroupsSearchBtn.style.display = groupSearchQuery ? 'block' : 'none';
      }
      renderGroupsList();
    });
  }

  if (clearGroupsSearchBtn && groupsSearchInput) {
    clearGroupsSearchBtn.addEventListener('click', () => {
      groupsSearchInput.value = '';
      groupSearchQuery = '';
      clearGroupsSearchBtn.style.display = 'none';
      renderGroupsList();
    });
  }

  // Rename group modal listeners
  const btnCloseRename = document.getElementById('btnCloseRenameModal');
  const btnCancelRename = document.getElementById('btnCancelRenameGroup');
  const btnSaveRename = document.getElementById('btnSaveGroupName');
  const modalRename = document.getElementById('modalEditGroupName');

  if (btnCloseRename && modalRename) {
    btnCloseRename.addEventListener('click', () => {
      modalRename.classList.remove('open');
      setTimeout(() => modalRename.style.display = 'none', 200);
    });
  }

  if (btnCancelRename && modalRename) {
    btnCancelRename.addEventListener('click', () => {
      modalRename.classList.remove('open');
      setTimeout(() => modalRename.style.display = 'none', 200);
    });
  }

  if (btnSaveRename && modalRename) {
    btnSaveRename.addEventListener('click', () => {
      saveGroupName();
    });
  }
}

async function fetchAndRenderGroups() {
  const groupsKey = `wow_groups_cache_${userId}_${currentTargetLang}_${currentNativeLang}`;
  try {
    const cached = localStorage.getItem(groupsKey);
    if (cached && (!userGroups || userGroups.length === 0)) {
      userGroups = JSON.parse(cached);
      renderGroupsList();
    }
  } catch (e) {}

  try {
    const res = await safeFetch(`/api/groups?user_id=${userId}&target_lang=${currentTargetLang}&native_lang=${currentNativeLang}`, {}, 2, 400);
    if (res.ok) {
      userGroups = await res.json();
      try { localStorage.setItem(groupsKey, JSON.stringify(userGroups)); } catch (e) {}
      renderGroupsList();
    }
  } catch (e) {
    console.error('Error fetching groups:', e);
  }
}

function renderGroupsList() {
  const container = document.getElementById('groupsListContainer');
  const countEl = document.getElementById('groupsTotalCount');
  if (!container) return;

  if (countEl) countEl.textContent = userGroups.length;

  if (userGroups.length === 0) {
    container.innerHTML = `
      <div class="dict-empty-state">
        <div class="dict-empty-icon">📁</div>
        <div class="dict-empty-title">Группы пока не сформированы</div>
        <div class="dict-empty-desc">Добавьте фразы в словарь, и они автоматически разделятся на группы по 10 штук.</div>
      </div>
    `;
    return;
  }

  const query = groupSearchQuery;
  container.innerHTML = '';

  let visibleGroupsCount = 0;

  userGroups.forEach(group => {
    const cards = group.cards || [];
    
    // Check search match
    let matchGroup = false;
    if (!query) {
      matchGroup = true;
    } else {
      const nameMatch = group.name.toLowerCase().includes(query);
      const cardMatch = cards.some(c => 
        (c.phrase_en && c.phrase_en.toLowerCase().includes(query)) ||
        (c.phrase_ru && c.phrase_ru.toLowerCase().includes(query))
      );
      matchGroup = nameMatch || cardMatch;
    }

    if (!matchGroup) return;
    visibleGroupsCount++;

    const status = group.status || 'new';
    const statusClass = `group-status-${status}`;
    const totalCards = group.total_cards || cards.length;
    const greenCount = group.green_count || 0;
    const redCount = group.red_count || 0;

    const cardEl = document.createElement('div');
    cardEl.className = `group-accordion-card ${statusClass} ${query ? 'open' : ''}`;
    cardEl.id = `groupCard_${group.id}`;

    // Subtitle meta text
    let statusText = 'Не изучена';
    if (status === 'in_progress') statusText = `В процессе (${greenCount}/${totalCards} выучено)`;
    if (status === 'mastered') statusText = `Изучена 🏆 (${totalCards}/${totalCards})`;

    cardEl.innerHTML = `
      <div class="group-card-header" onclick="toggleGroupAccordion(${group.id})">
        <div class="group-header-left">
          <div class="group-status-icon-dot"></div>
          <div class="group-title-wrap">
            <span class="group-title-name">${escapeHtml(group.name)}</span>
            <span class="group-meta-sub">
              <span>${totalCards} фраз</span>
              <span>•</span>
              <span>${statusText}</span>
              ${redCount > 0 ? `<span style="color:#E53935; font-weight:700;">(🔴 ${redCount} ошибок)</span>` : ''}
            </span>
          </div>
        </div>
        <div class="group-header-actions">
          <button type="button" class="btn-icon-sm" title="Переименовать" onclick="event.stopPropagation(); openEditGroupNameModal(${group.id})">
            <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
          </button>
          <button type="button" class="btn-icon-sm group-toggle-chevron-btn" title="Раскрыть список" onclick="event.stopPropagation(); toggleGroupAccordion(${group.id})">
            <svg class="group-chevron-icon" style="pointer-events:none;" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.2" fill="none"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
        </div>
      </div>

      <div class="group-card-body">
        <div class="group-body-controls-row">
          <div class="group-status-select-wrap">
            <span>Статус:</span>
            <select class="group-status-select" onchange="handleGroupStatusChange(${group.id}, this.value)">
              <option value="new" ${status === 'new' ? 'selected' : ''}>⬛ Не изучена</option>
              <option value="in_progress" ${status === 'in_progress' ? 'selected' : ''}>🟧 В процессе</option>
              <option value="mastered" ${status === 'mastered' ? 'selected' : ''}>🟩 Изучена</option>
            </select>
          </div>
          <button type="button" class="btn-group-reset-link" onclick="handleGroupReset(${group.id})">
            🔄 Сбросить результат
          </button>
        </div>

        <div class="group-phrases-inner-list" id="groupPhrasesList_${group.id}">
          <!-- Injected via cards loop -->
        </div>
      </div>
    `;

    // Populate phrases inside group
    const phrasesList = cardEl.querySelector(`#groupPhrasesList_${group.id}`);
    cards.forEach(c => {
      const cTrainerSt = c.trainer_status || 'neutral';
      const cDotClass = cTrainerSt === 'green' ? 'dot-green' : (cTrainerSt === 'red' ? 'dot-red' : 'dot-neutral');
      
      const isHighlighted = query && (
        (c.phrase_en && c.phrase_en.toLowerCase().includes(query)) ||
        (c.phrase_ru && c.phrase_ru.toLowerCase().includes(query))
      );

      const pRow = document.createElement('div');
      pRow.className = 'group-phrase-row';
      if (isHighlighted) pRow.style.background = 'rgba(99, 102, 241, 0.1)';

      pRow.innerHTML = `
        <div class="group-phrase-info">
          <div class="knowledge-dot-wrap" onclick="showKnowledgeTooltip(event, '${cTrainerSt}')" title="Индикатор знаний">
            <span class="knowledge-dot ${cDotClass}"></span>
            <span class="knowledge-dot-help">?</span>
          </div>
          <div class="group-phrase-texts">
            <div class="group-phrase-en">${escapeHtml(c.phrase_en)}</div>
            <div class="group-phrase-ru">${escapeHtml(c.phrase_ru)}</div>
          </div>
        </div>
        <button type="button" class="btn-phrase-delete-mini" title="Удалить из группы" onclick="handleDeleteCardFromGroup(${c.id}, ${group.id})">
          <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        </button>
      `;
      phrasesList.appendChild(pRow);
    });

    container.appendChild(cardEl);
  });

  if (visibleGroupsCount === 0) {
    container.innerHTML = `
      <div class="dict-empty-state">
        <div class="dict-empty-icon">🔍</div>
        <div class="dict-empty-title">Фразы не найдены</div>
        <div class="dict-empty-desc">По запросу «${escapeHtml(query)}» ничего не найдено в группах.</div>
      </div>
    `;
  }
}

function toggleGroupAccordion(groupId) {
  haptic('light');
  const card = document.getElementById(`groupCard_${groupId}`);
  if (card) {
    card.classList.toggle('open');
  }
}

function openEditGroupNameModal(groupId) {
  const group = userGroups.find(g => g.id === groupId);
  if (!group) return;
  editingGroupId = groupId;

  const modal = document.getElementById('modalEditGroupName');
  const input = document.getElementById('editGroupNameInput');
  if (input) input.value = group.name;

  if (modal) {
    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('open'), 10);
    if (input) input.focus();
  }
}

async function saveGroupName() {
  if (!editingGroupId) return;
  const input = document.getElementById('editGroupNameInput');
  const modal = document.getElementById('modalEditGroupName');
  const newName = input ? input.value.trim() : '';

  if (!newName) return;
  haptic('success');

  try {
    const res = await fetch('/api/group/name', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ group_id: editingGroupId, name: newName, user_id: userId })
    });
    if (res.ok) {
      const g = userGroups.find(x => x.id === editingGroupId);
      if (g) g.name = newName;
      renderGroupsList();
      renderTrainerGroupsChecklist();
    }
  } catch (e) {
    console.error('Error saving group name:', e);
  } finally {
    if (modal) {
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
    }
    editingGroupId = null;
  }
}

async function handleGroupStatusChange(groupId, newStatus) {
  haptic('light');
  try {
    const res = await fetch('/api/group/status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ group_id: groupId, status: newStatus, user_id: userId })
    });
    if (res.ok) {
      const g = userGroups.find(x => x.id === groupId);
      if (g) g.status = newStatus;
      renderGroupsList();
      renderTrainerGroupsChecklist();
    }
  } catch (e) {
    console.error('Error updating group status:', e);
  }
}

async function handleGroupReset(groupId) {
  haptic('warning');
  try {
    const res = await fetch('/api/group/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ group_id: groupId, user_id: userId })
    });
    if (res.ok) {
      await fetchAndRenderGroups();
      await loadData();
    }
  } catch (e) {
    console.error('Error resetting group:', e);
  }
}

async function handleDeleteCardFromGroup(cardId, groupId) {
  haptic('heavy');
  try {
    const res = await fetch('/api/card/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card_id: cardId, user_id: userId })
    });
    if (res.ok) {
      // Remove card from local list
      allCards = allCards.filter(c => c.id !== cardId);
      currentDeck = currentDeck.filter(c => c.id !== cardId);
      const grp = userGroups.find(g => g.id === groupId);
      if (grp) {
        grp.cards = (grp.cards || []).filter(c => c.id !== cardId);
        grp.total_cards = grp.cards.length;
      }
      renderGroupsList();
      renderDictionary();
      updateCounters();
    }
  } catch (e) {
    console.error('Error deleting card from group:', e);
  }
}

// --- Knowledge Tooltip Popup Controller ---
let tooltipTimer = null;
function showKnowledgeTooltip(event, status) {
  event.stopPropagation();
  const tooltip = document.getElementById('knowledgeTooltip');
  const body = document.getElementById('knowledgeTooltipBody');
  if (!tooltip || !body) return;

  let text = '';
  if (status === 'green') {
    text = '🟢 <b>Изучена</b>: фраза успешно и правильно пройдена в тренажёре.';
  } else if (status === 'red') {
    text = '🔴 <b>Требует повторения</b>: в тренажёре была допущена ошибка.';
  } else {
    text = '⭕ <b>Не проходила тренажёр</b>: фраза ещё не тренировалась.';
  }

  body.innerHTML = text;

  const rect = event.currentTarget.getBoundingClientRect();
  const top = rect.bottom + 6;
  const left = Math.min(Math.max(10, rect.left - 40), window.innerWidth - 230);

  tooltip.style.top = `${top}px`;
  tooltip.style.left = `${left}px`;
  tooltip.style.display = 'block';
  tooltip.style.opacity = '1';

  clearTimeout(tooltipTimer);
  tooltipTimer = setTimeout(() => {
    tooltip.style.opacity = '0';
    setTimeout(() => { tooltip.style.display = 'none'; }, 180);
  }, 2800);
}

document.addEventListener('click', () => {
  const tooltip = document.getElementById('knowledgeTooltip');
  if (tooltip) {
    tooltip.style.opacity = '0';
    setTimeout(() => { tooltip.style.display = 'none'; }, 150);
  }
});

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ==========================================================================
// INTENSIVE TRAINER MODULE (6 Mechanics + Batches + Mistakes Loop)
// ==========================================================================
// ==========================================================================
// INTENSIVE TRAINER MODULE (Step Wizard: Step 1 -> Step 2 -> Step 3 -> Workout -> Completion)
// ==========================================================================
let currentTrainerStep = 1;
let trainerMode = 'groups'; // 'groups' or 'red_words'
let selectedGroupIds = new Set();
let redCardsList = [];
let activeMechanics = {
  cards: true,
  builder: true,
  cloze: true,
  sprint: true,
  audio: false,
  voice: false,
  news: true
};
let workoutSession = null;

function goToTrainerStep(stepNum) {
  currentTrainerStep = stepNum;
  
  const s1 = document.getElementById('trainerStep1View');
  const s2 = document.getElementById('trainerStep2View');
  const s3 = document.getElementById('trainerStep3View');
  const sWorkout = document.getElementById('trainerWorkoutView');
  const sComp = document.getElementById('trainerCompletionView');

  const steps = [
    { el: s1, isTarget: stepNum === 1 },
    { el: s2, isTarget: stepNum === 2 },
    { el: s3, isTarget: stepNum === 3 },
    { el: sWorkout, isTarget: stepNum === 'workout' },
    { el: sComp, isTarget: stepNum === 'completion' }
  ];

  steps.forEach(s => {
    if (s.el) {
      if (s.isTarget) {
        s.el.classList.add('active');
        s.el.style.display = 'block';
      } else {
        s.el.classList.remove('active');
        s.el.style.display = 'none';
      }
    }
  });

  if (stepNum === 1) {
    loadRedWords();
  } else if (stepNum === 2) {
    renderTrainerGroupsChecklist();
    updateStep2SelectionSummary();
  } else if (stepNum === 3) {
    const pill = document.getElementById('step3IndicatorPill');
    if (pill) {
      pill.textContent = (trainerMode === 'red_words') ? 'Шаг 2 из 2' : 'Шаг 3 из 3';
    }
    updateStartButtonLabel();
  }
}

function updateStep2SelectionSummary() {
  const lbl = document.getElementById('step2SelectedCountLabel');
  if (!lbl) return;
  const count = selectedGroupIds.size;
  let totalPhrases = 0;
  userGroups.filter(g => selectedGroupIds.has(g.id)).forEach(g => {
    totalPhrases += (g.cards || []).length;
  });
  lbl.textContent = `Выбрано групп: ${count} (${totalPhrases} фраз)`;
}

function initTrainerModule() {
  // Step 1: Option Cards Click
  const btnChooseGroups = document.getElementById('btnSelectModeGroups');
  if (btnChooseGroups) {
    btnChooseGroups.addEventListener('click', () => {
      haptic('light');
      trainerMode = 'groups';
      if (selectedGroupIds.size === 0 && userGroups.length > 0) {
        selectedGroupIds.add(userGroups[0].id);
      }
      goToTrainerStep(2);
    });
  }

  const btnChooseRed = document.getElementById('btnSelectModeRedWords');
  if (btnChooseRed) {
    btnChooseRed.addEventListener('click', async () => {
      haptic('light');
      await loadRedWords();
      if (redCardsList.length === 0) {
        alert("У вас пока нет карточек с ошибками! Все группы чисты 🎉");
        return;
      }
      trainerMode = 'red_words';
      goToTrainerStep(3); // Skip Step 2 as requested!
    });
  }

  // Step 2: Navigation Buttons
  const btnStep2Back = document.getElementById('btnStep2Back');
  if (btnStep2Back) {
    btnStep2Back.addEventListener('click', () => {
      haptic('light');
      goToTrainerStep(1);
    });
  }

  const btnStep2Next = document.getElementById('btnStep2Next');
  if (btnStep2Next) {
    btnStep2Next.addEventListener('click', () => {
      haptic('light');
      if (selectedGroupIds.size === 0) {
        alert("Пожалуйста, выберите хотя бы одну группу для тренировки.");
        return;
      }
      goToTrainerStep(3);
    });
  }

  // Toggle All Groups button in Step 2
  const btnToggleAll = document.getElementById('btnToggleAllGroups');
  if (btnToggleAll) {
    btnToggleAll.addEventListener('click', () => {
      haptic('light');
      if (selectedGroupIds.size === userGroups.length) {
        selectedGroupIds.clear();
      } else {
        selectedGroupIds = new Set(userGroups.map(g => g.id));
      }
      renderTrainerGroupsChecklist();
      updateStep2SelectionSummary();
    });
  }

  // Step 3: Navigation Buttons
  const btnStep3Back = document.getElementById('btnStep3Back');
  if (btnStep3Back) {
    btnStep3Back.addEventListener('click', () => {
      haptic('light');
      if (trainerMode === 'red_words') {
        goToTrainerStep(1);
      } else {
        goToTrainerStep(2);
      }
    });
  }

  // Select All Mechanics button
  const btnSelectAllMech = document.getElementById('btnSelectAllMechanics');
  if (btnSelectAllMech) {
    btnSelectAllMech.addEventListener('click', () => {
      haptic('light');
      ['mechCards', 'mechBuilder', 'mechCloze', 'mechSprint', 'mechAudio', 'mechVoice', 'mechNews'].forEach(id => {
        const chk = document.getElementById(id);
        if (chk) chk.checked = true;
      });
      activeMechanics = { cards: true, builder: true, cloze: true, sprint: true, audio: true, voice: true, news: true };
    });
  }

  // Mechanics checkboxes change listeners
  ['cards', 'builder', 'cloze', 'sprint', 'audio', 'voice', 'news'].forEach(m => {
    const chk = document.getElementById(`mech${m.charAt(0).toUpperCase() + m.slice(1)}`);
    if (chk) {
      chk.addEventListener('change', () => {
        activeMechanics[m] = chk.checked;
      });
    }
  });

  // Start workout button on Step 3
  const btnStart = document.getElementById('btnStartWorkout');
  if (btnStart) {
    btnStart.addEventListener('click', () => {
      startWorkoutSession();
    });
  }

  // Back button in workout (Instant and seamless return)
  const btnBack = document.getElementById('btnWorkoutBack');
  if (btnBack) {
    btnBack.addEventListener('click', async () => {
      haptic('light');
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      workoutSession = null;
      goToTrainerStep(trainerMode === 'red_words' ? 1 : (selectedGroupIds.size > 0 ? 2 : 1));
      await fetchAndRenderGroups();
    });
  }

  initExitWorkoutModal();
  initWorkoutSoundToggle();

  // Completion screen buttons
  const btnNextGroups = document.getElementById('btnNextGroupSelection');
  if (btnNextGroups) {
    btnNextGroups.addEventListener('click', () => {
      haptic('light');
      loadTrainerSetup();
    });
  }

  const btnResetProgress = document.getElementById('btnResetGroupProgress');
  if (btnResetProgress) {
    btnResetProgress.addEventListener('click', () => {
      resetWorkoutGroupProgress();
    });
  }

  // Close toast button
  const btnCloseToast = document.getElementById('btnCloseGroupToast');
  if (btnCloseToast) {
    btnCloseToast.addEventListener('click', () => {
      const toast = document.getElementById('popupGroupCompleted');
      if (toast) toast.style.display = 'none';
    });
  }
}

async function loadTrainerSetup() {
  await fetchAndRenderGroups();
  await loadRedWords();
  
  // Default select 1st group if none selected
  if (selectedGroupIds.size === 0 && userGroups.length > 0) {
    selectedGroupIds.add(userGroups[0].id);
  }

  goToTrainerStep(1);
}

async function loadRedWords() {
  const redKey = `wow_red_cards_cache_${userId}_${currentTargetLang}_${currentNativeLang}`;
  try {
    const cached = localStorage.getItem(redKey);
    if (cached && (!redCardsList || redCardsList.length === 0)) {
      redCardsList = JSON.parse(cached);
      const badgeStep1 = document.getElementById('badgeRedCardsStep1');
      if (badgeStep1) badgeStep1.textContent = `${redCardsList.length} фраз`;
    }
  } catch (e) {}

  try {
    const res = await safeFetch(`/api/cards/red?user_id=${userId}&target_lang=${currentTargetLang}&native_lang=${currentNativeLang}`, {}, 2, 400);
    if (res.ok) {
      redCardsList = await res.json();
      try { localStorage.setItem(redKey, JSON.stringify(redCardsList)); } catch (e) {}
      const badgeStep1 = document.getElementById('badgeRedCardsStep1');
      if (badgeStep1) badgeStep1.textContent = `${redCardsList.length} фраз`;
    }
  } catch (e) {
    console.error('Error loading red cards:', e);
  }
}

function renderTrainerGroupsChecklist() {
  const container = document.getElementById('trainerGroupsChecklist');
  if (!container) return;
  container.innerHTML = '';

  if (userGroups.length === 0) {
    container.innerHTML = `<div style="color: var(--text-tertiary); font-size: 12.5px;">Группы пока не созданы. Добавьте фразы в словарь!</div>`;
    return;
  }

  userGroups.forEach(g => {
    const isChecked = selectedGroupIds.has(g.id);
    const status = g.status || 'new';
    
    let statusLabel = 'Не изучена';
    let statusTagClass = 'status-tag-new';
    if (status === 'in_progress') {
      statusLabel = 'В процессе';
      statusTagClass = 'status-tag-progress';
    } else if (status === 'mastered') {
      statusLabel = 'Изучена 🏆';
      statusTagClass = 'status-tag-mastered';
    }

    const row = document.createElement('div');
    row.className = `trainer-group-chk-card ${isChecked ? 'selected' : ''}`;
    row.innerHTML = `
      <div class="chk-left">
        <input type="checkbox" class="custom-chk" ${isChecked ? 'checked' : ''} onchange="toggleGroupSelection(${g.id}, this.checked)" />
        <span class="chk-group-name">${escapeHtml(g.name)} (${g.total_cards} фраз)</span>
      </div>
      <span class="chk-group-status-tag ${statusTagClass}">${statusLabel}</span>
    `;

    row.addEventListener('click', (e) => {
      if (e.target.tagName !== 'INPUT') {
        const chk = row.querySelector('input');
        if (chk) {
          chk.checked = !chk.checked;
          toggleGroupSelection(g.id, chk.checked);
        }
      }
    });

    container.appendChild(row);
  });
}

function toggleGroupSelection(groupId, isSelected) {
  haptic('light');
  if (isSelected) {
    selectedGroupIds.add(groupId);
  } else {
    selectedGroupIds.delete(groupId);
  }
  renderTrainerGroupsChecklist();
  updateStep2SelectionSummary();
  updateStartButtonLabel();
}

function updateStartButtonLabel() {
  const btnText = document.getElementById('btnStartWorkoutText');
  const btn = document.getElementById('btnStartWorkout');
  if (!btnText || !btn) return;

  let totalCount = 0;
  if (trainerMode === 'groups') {
    userGroups.filter(g => selectedGroupIds.has(g.id)).forEach(g => {
      totalCount += (g.cards || []).length;
    });
  } else {
    totalCount = redCardsList.length;
  }

  btnText.textContent = `🚀 Начать тренировку (${totalCount} фраз)`;
  btn.disabled = totalCount === 0;
  btn.style.opacity = totalCount === 0 ? '0.5' : '1';
}

function showTrainerSetupView() {
  goToTrainerStep(1);
}

// --- WORKOUT ENGINE ---
function startWorkoutSession() {
  haptic('medium');
  let sessionCards = [];

  if (trainerMode === 'groups') {
    userGroups.filter(g => selectedGroupIds.has(g.id)).forEach(g => {
      sessionCards.push(...(g.cards || []));
    });
  } else {
    sessionCards = [...redCardsList];
  }

  if (sessionCards.length === 0) {
    alert("Пожалуйста, выберите хотя бы одну группу или режим фраз с ошибками.");
    return;
  }

  // Ensure at least 1 mechanic is active
  const enabledMechs = Object.keys(activeMechanics).filter(k => activeMechanics[k]);
  if (enabledMechs.length === 0) {
    activeMechanics.cards = true;
    const chk = document.getElementById('mechCards');
    if (chk) chk.checked = true;
  }

  workoutSession = {
    orderedCards: [...sessionCards],
    queue: shuffleArray([...sessionCards]),
    phraseStates: {}, // card.id -> 'neutral', 'green', 'red'
    currentCard: null,
    round: 1,
    activeMechanicsList: Object.keys(activeMechanics).filter(k => activeMechanics[k]),
    isProcessing: false,
    newsStories: [],
    isLoadingNews: false
  };

  if (activeMechanics.news) {
    preloadWorkoutNewsStories(sessionCards);
  }

  // Every card in this workout session MUST start as 'neutral' so all phrases must be answered
  sessionCards.forEach(c => {
    workoutSession.phraseStates[c.id] = 'neutral';
  });

  goToTrainerStep('workout');

  renderWorkoutIndicatorCircles();
  presentNextExercise();
}

function renderWorkoutIndicatorCircles() {
  const bars = document.querySelectorAll('.workout-circles-bar');
  if (!bars || bars.length === 0 || !workoutSession) return;

  bars.forEach(bar => {
    bar.innerHTML = '';
    const cards = workoutSession.orderedCards || [];
    
    // Chunk cards into rows of 10 items
    const chunkSize = 10;
    const rows = [];
    for (let i = 0; i < cards.length; i += chunkSize) {
      rows.push(cards.slice(i, i + chunkSize));
    }

    rows.forEach((rowCards, rowIdx) => {
      const rowEl = document.createElement('div');
      rowEl.className = 'workout-circles-row';

      rowCards.forEach((c, colIdx) => {
        const globalIdx = rowIdx * chunkSize + colIdx;
        const st = workoutSession.phraseStates[c.id] || 'neutral';
        let circleClass = 'circle-neutral';
        if (st === 'green') circleClass = 'circle-green';
        if (st === 'red') circleClass = 'circle-red';
        if (workoutSession.currentCard && workoutSession.currentCard.id === c.id) {
          circleClass += ' circle-current';
        }

        const dot = document.createElement('div');
        dot.className = `phrase-circle-indicator ${circleClass}`;
        dot.title = `Фраза ${globalIdx + 1}: ${c.phrase_en}`;
        dot.addEventListener('click', (e) => {
          e.stopPropagation();
          showKnowledgeTooltip(e, st);
        });
        rowEl.appendChild(dot);
      });

      bar.appendChild(rowEl);
    });
  });
}

function presentNextExercise() {
  if (!workoutSession) return;
  workoutSession.isProcessing = false;

  // If current round queue is empty: check if any cards are NOT green yet
  if (workoutSession.queue.length === 0) {
    const remainingCards = workoutSession.orderedCards.filter(c => workoutSession.phraseStates[c.id] !== 'green');
    if (remainingCards.length === 0) {
      showWorkoutCompletion();
      return;
    }

    // Populate queue with all unmastered cards for next round
    workoutSession.round++;
    workoutSession.queue = shuffleArray([...remainingCards]);
  }

  const roundBadge = document.getElementById('workoutRoundBadge');
  if (roundBadge) {
    roundBadge.textContent = workoutSession.round === 1 
      ? `Раунд 1` 
      : `Раунд ${workoutSession.round} (Осталось: ${workoutSession.queue.length + 1})`;
  }

  workoutSession.currentCard = workoutSession.queue.shift();
  if (!workoutSession.currentCard) {
    showWorkoutCompletion();
    return;
  }

  // Pick mechanic
  const mechs = workoutSession.activeMechanicsList;
  const pickedMech = mechs[Math.floor(Math.random() * mechs.length)] || 'cards';

  const arena = document.getElementById('workoutArena');
  if (!arena) return;
  arena.innerHTML = '';

  switch (pickedMech) {
    case 'builder':
      renderExercise_Builder(workoutSession.currentCard);
      break;
    case 'cloze':
      renderExercise_Cloze(workoutSession.currentCard);
      break;
    case 'sprint':
      renderExercise_Sprint(workoutSession.currentCard);
      break;
    case 'audio':
      renderExercise_Audio(workoutSession.currentCard);
      break;
    case 'voice':
      renderExercise_Voice(workoutSession.currentCard);
      break;
    case 'news':
      renderExercise_News(workoutSession.currentCard);
      break;
    case 'cards':
    default:
      renderExercise_3DCards(workoutSession.currentCard);
      break;
  }

  renderWorkoutIndicatorCircles();
}

// 1. 3D Flashcard Exercise
function renderExercise_3DCards(card) {
  const arena = document.getElementById('workoutArena');
  const wrap = document.createElement('div');
  wrap.className = 'exercise-card-container';
  wrap.innerHTML = `
    <!-- Top Centered Circles Row(s) -->
    <div class="workout-circles-bar" id="workoutCirclesBar"></div>

    <!-- Mechanic & Instruction in Top-Left (below indicators) -->
    <div class="exercise-meta-top-left">
      <span class="exercise-type-tag">🃏 3D-Карточка</span>
      <div class="exercise-prompt-title">Вспомните перевод фразы на английский:</div>
    </div>

    <!-- Target Phrase (with 3x spacing above) -->
    <div class="exercise-target-phrase">${escapeHtml(card.phrase_ru)}</div>

    <div class="builder-target-zone is-flipped-preview" id="cardFlipPreview" style="display:none; padding:16px; background:rgba(99,102,241,0.06); border-color:var(--accent-primary); border-style:solid; cursor:pointer; margin-bottom:16px;">
      <strong style="font-size:16px; color:var(--text-primary);">${escapeHtml(card.phrase_en)}</strong>
    </div>

    <div class="self-assess-row" id="cardAssessButtons" style="display:none; margin-top:auto;">
      <button type="button" class="btn-assess-fail" id="btnAssessFail">🔴 Не помню</button>
      <button type="button" class="btn-assess-pass" id="btnAssessPass">🟢 Знаю</button>
    </div>

    <button type="button" class="btn-trainer-start" id="btnRevealCard" style="margin-top:auto;">
      <span>👁️ Показать перевод & озвучить</span>
    </button>
  `;

  const btnReveal = wrap.querySelector('#btnRevealCard');
  const preview = wrap.querySelector('#cardFlipPreview');
  const assessRow = wrap.querySelector('#cardAssessButtons');

  btnReveal.addEventListener('click', () => {
    haptic('light');
    btnReveal.style.display = 'none';
    preview.style.display = 'block';
    assessRow.style.display = 'flex';
    speakPhrase(card.phrase_en, currentTargetLang, null, true);
  });

  preview.addEventListener('click', () => {
    speakPhrase(card.phrase_en, currentTargetLang, null, true);
  });

  wrap.querySelector('#btnAssessFail').addEventListener('click', () => {
    if (workoutSession && workoutSession.isProcessing) return;
    assessRow.style.pointerEvents = 'none';
    handleExerciseResult(card, false);
  });

  wrap.querySelector('#btnAssessPass').addEventListener('click', () => {
    if (workoutSession && workoutSession.isProcessing) return;
    assessRow.style.pointerEvents = 'none';
    handleExerciseResult(card, true);
  });

  arena.appendChild(wrap);
}

// 2. Word Builder (Sentence Scramble)
function renderExercise_Builder(card) {
  const arena = document.getElementById('workoutArena');
  const rawWords = card.phrase_en.trim().split(/\s+/).filter(Boolean);
  const shuffledWords = shuffleArray(rawWords.map((w, idx) => ({ word: w, originalIdx: idx })));
  const placedWords = [];

  const wrap = document.createElement('div');
  wrap.className = 'exercise-card-container';
  wrap.innerHTML = `
    <!-- Top Centered Circles Row(s) -->
    <div class="workout-circles-bar" id="workoutCirclesBar"></div>

    <!-- Mechanic & Instruction in Top-Left (below indicators) -->
    <div class="exercise-meta-top-left">
      <span class="exercise-type-tag">🧩 Конструктор предложений</span>
      <div class="exercise-prompt-title">Соберите фразу на английском:</div>
    </div>

    <!-- Target Phrase (with 3x spacing above) -->
    <div class="exercise-target-phrase">${escapeHtml(card.phrase_ru)}</div>

    <div class="builder-target-zone ${placedWords.length === 0 ? 'is-empty' : ''}" id="builderTargetZone"></div>

    <div class="builder-word-bank" id="builderWordBank"></div>

    <div class="self-assess-row" style="margin-top:auto;">
      <button type="button" class="btn-cancel-action" id="btnResetBuilder" style="max-width:100px;">Сбросить</button>
      <button type="button" class="btn-trainer-start" id="btnCheckBuilder" style="flex:1;">
        <span>Проверить</span>
      </button>
    </div>
  `;

  const targetZone = wrap.querySelector('#builderTargetZone');
  const wordBank = wrap.querySelector('#builderWordBank');
  const btnCheck = wrap.querySelector('#btnCheckBuilder');
  const btnReset = wrap.querySelector('#btnResetBuilder');

  function renderTiles() {
    targetZone.innerHTML = '';
    targetZone.className = `builder-target-zone ${placedWords.length === 0 ? 'is-empty' : ''}`;
    placedWords.forEach((item, pIdx) => {
      const tile = document.createElement('div');
      tile.className = 'word-chip-tile in-target';
      tile.textContent = item.word;
      tile.addEventListener('click', () => {
        haptic('light');
        placedWords.splice(pIdx, 1);
        renderTiles();
      });
      targetZone.appendChild(tile);
    });

    wordBank.innerHTML = '';
    shuffledWords.forEach((item) => {
      const isUsed = placedWords.some(p => p.originalIdx === item.originalIdx);
      const tile = document.createElement('div');
      tile.className = `word-chip-tile ${isUsed ? 'used' : ''}`;
      tile.textContent = item.word;
      tile.addEventListener('click', () => {
        if (!isUsed) {
          haptic('light');
          placedWords.push(item);
          renderTiles();
        }
      });
      wordBank.appendChild(tile);
    });
  }

  btnReset.addEventListener('click', () => {
    haptic('light');
    placedWords.length = 0;
    renderTiles();
  });

  btnCheck.addEventListener('click', () => {
    if (workoutSession && workoutSession.isProcessing) return;
    btnCheck.style.pointerEvents = 'none';
    const built = placedWords.map(p => p.word).join(' ').trim().toLowerCase();
    const correct = card.phrase_en.trim().toLowerCase();
    
    // Normalize punctuation
    const cleanBuilt = built.replace(/[.,\/#!$%^&*;:{}=\-_`~()]/g, '');
    const cleanCorrect = correct.replace(/[.,\/#!$%^&*;:{}=\-_`~()]/g, '');

    const isMatch = cleanBuilt === cleanCorrect;
    handleExerciseResult(card, isMatch);
  });

  renderTiles();
  arena.appendChild(wrap);
}

// 3. Cloze (Fill-in) Exercise
function renderExercise_Cloze(card) {
  const arena = document.getElementById('workoutArena');
  const enText = (card.phrase_en || '').trim();
  const words = enText.split(/\s+/).filter(Boolean);
  
  if (words.length === 0) {
    renderExercise_3DCards(card);
    return;
  }

  // Pick a word >= 3 chars if possible
  let targetIdx = 0;
  for (let i = 0; i < words.length; i++) {
    if (words[i].length >= 4) { targetIdx = i; break; }
  }

  const hiddenWord = (words[targetIdx] || '').replace(/[.,\/#!$%^&*;:{}=\-_`~()]/g, '');
  if (!hiddenWord) {
    renderExercise_3DCards(card);
    return;
  }
  const promptEn = words.map((w, i) => i === targetIdx ? '_____' : w).join(' ');

  // Create distractors
  const defaultDistractors = ['about', 'into', 'with', 'through', 'make', 'take', 'look', 'keep', 'give', 'hold', 'time', 'work', 'place', 'order', 'deal'];
  const distractors = defaultDistractors
    .filter(d => d.toLowerCase() !== hiddenWord.toLowerCase())
    .slice(0, 3);
  const options = shuffleArray([hiddenWord, ...distractors]);

  const wrap = document.createElement('div');
  wrap.className = 'exercise-card-container';
  wrap.innerHTML = `
    <!-- Top Centered Circles Row(s) -->
    <div class="workout-circles-bar" id="workoutCirclesBar"></div>

    <!-- Mechanic & Instruction in Top-Left (below indicators) -->
    <div class="exercise-meta-top-left">
      <span class="exercise-type-tag">✍️ Пропущенное слово</span>
      <div class="exercise-prompt-title">Вставьте пропущенное слово:</div>
    </div>

    <!-- Target Phrase (with 3x spacing above) -->
    <div class="exercise-target-phrase">${escapeHtml(promptEn)}</div>
    <div style="font-size:13.5px; color:var(--text-secondary); margin-bottom:18px;">🇷🇺 ${escapeHtml(card.phrase_ru || '')}</div>

    <div class="quiz-options-stack" id="clozeOptionsStack"></div>
  `;

  const stack = wrap.querySelector('#clozeOptionsStack');
  options.forEach(opt => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'quiz-option-btn';
    btn.textContent = opt;
    btn.addEventListener('click', () => {
      if (workoutSession && workoutSession.isProcessing) return;
      stack.style.pointerEvents = 'none';
      const isCorrect = opt.toLowerCase() === hiddenWord.toLowerCase();
      if (isCorrect) {
        btn.classList.add('opt-correct');
      } else {
        btn.classList.add('opt-incorrect');
      }
      setTimeout(() => handleExerciseResult(card, isCorrect), 320);
    });
    stack.appendChild(btn);
  });

  arena.appendChild(wrap);
}

// 4. Sprint Quiz Exercise
function renderExercise_Sprint(card) {
  const arena = document.getElementById('workoutArena');
  const fallbackTrans = [
    "Давай встретимся завтра",
    "Я извиняюсь за неудобства",
    "Это зависит от времени",
    "Груз застрял на таможне",
    "Нам нужно сократить сроки",
    "Я считаю себя ответственным",
    "С нетерпением жду ответа"
  ];
  
  // Pick 3 random distractors from allCards or fallback
  const otherTranslations = (allCards || [])
    .filter(c => c.id !== card.id && c.phrase_ru && c.phrase_ru !== card.phrase_ru)
    .map(c => c.phrase_ru);
    
  let pickedDistractors = shuffleArray(otherTranslations).slice(0, 3);
  if (pickedDistractors.length < 3) {
    const pool = fallbackTrans.filter(f => f !== card.phrase_ru && !pickedDistractors.includes(f));
    pickedDistractors = [...pickedDistractors, ...shuffleArray(pool).slice(0, 3 - pickedDistractors.length)];
  }
  const options = shuffleArray([card.phrase_ru || '—', ...pickedDistractors]);

  const wrap = document.createElement('div');
  wrap.className = 'exercise-card-container';
  wrap.innerHTML = `
    <!-- Top Centered Circles Row(s) -->
    <div class="workout-circles-bar" id="workoutCirclesBar"></div>

    <!-- Mechanic & Instruction in Top-Left (below indicators) -->
    <div class="exercise-meta-top-left">
      <span class="exercise-type-tag">⚡ Спринт-квиз</span>
      <div class="exercise-prompt-title">Выберите правильный перевод:</div>
    </div>

    <!-- Target Phrase (with 3x spacing above) -->
    <div class="exercise-target-phrase">${escapeHtml(card.phrase_en || '')}</div>

    <div class="quiz-options-stack" id="sprintOptionsStack"></div>
  `;

  const stack = wrap.querySelector('#sprintOptionsStack');
  options.forEach(opt => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'quiz-option-btn';
    btn.textContent = opt;
    btn.addEventListener('click', () => {
      if (workoutSession && workoutSession.isProcessing) return;
      stack.style.pointerEvents = 'none';
      const isCorrect = opt === (card.phrase_ru || '—');
      if (isCorrect) {
        btn.classList.add('opt-correct');
      } else {
        btn.classList.add('opt-incorrect');
      }
      setTimeout(() => handleExerciseResult(card, isCorrect), 320);
    });
    stack.appendChild(btn);
  });

  arena.appendChild(wrap);
}

// 5. Audio Dictation Exercise
function renderExercise_Audio(card) {
  const arena = document.getElementById('workoutArena');
  const fallbackTrans = [
    "Давай встретимся завтра",
    "Я извиняюсь за неудобства",
    "Это зависит от времени",
    "Груз застрял на таможне",
    "Нам нужно сократить сроки",
    "Я считаю себя ответственным",
    "С нетерпением жду ответа"
  ];
  
  const otherTranslations = (allCards || [])
    .filter(c => c.id !== card.id && c.phrase_ru && c.phrase_ru !== card.phrase_ru)
    .map(c => c.phrase_ru);
    
  let pickedDistractors = shuffleArray(otherTranslations).slice(0, 3);
  if (pickedDistractors.length < 3) {
    const pool = fallbackTrans.filter(f => f !== card.phrase_ru && !pickedDistractors.includes(f));
    pickedDistractors = [...pickedDistractors, ...shuffleArray(pool).slice(0, 3 - pickedDistractors.length)];
  }
  const options = shuffleArray([card.phrase_ru || '—', ...pickedDistractors]);

  const wrap = document.createElement('div');
  wrap.className = 'exercise-card-container';
  wrap.innerHTML = `
    <!-- Top Centered Circles Row(s) -->
    <div class="workout-circles-bar" id="workoutCirclesBar"></div>

    <!-- Mechanic & Instruction in Top-Left (below indicators) -->
    <div class="exercise-meta-top-left">
      <span class="exercise-type-tag">🎧 Аудио-диктант</span>
      <div class="exercise-prompt-title">Послушайте фразу и выберите перевод:</div>
    </div>

    <!-- Audio Player (with 3x spacing above) -->
    <div class="audio-exercise-center" style="margin-top: 10px; margin-bottom: 22px;">
      <button type="button" class="btn-big-speaker" id="btnPlayWorkoutAudio" title="Послушать">
        <svg viewBox="0 0 24 24" width="30" height="30" stroke="currentColor" stroke-width="2" fill="none"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path></svg>
      </button>
      <span style="font-size:12px; color:var(--text-tertiary); margin-top: 6px;">Нажмите для повтора</span>
    </div>

    <div class="quiz-options-stack" id="audioOptionsStack"></div>
  `;

  const playBtn = wrap.querySelector('#btnPlayWorkoutAudio');
  playBtn.addEventListener('click', () => {
    speakPhrase(card.phrase_en, currentTargetLang, playBtn, true);
  });

  // Auto-play audio on presentation if not muted
  setTimeout(() => speakPhrase(card.phrase_en, currentTargetLang, playBtn, true), 250);

  const stack = wrap.querySelector('#audioOptionsStack');
  options.forEach(opt => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'quiz-option-btn';
    btn.textContent = opt;
    btn.addEventListener('click', () => {
      if (workoutSession && workoutSession.isProcessing) return;
      stack.style.pointerEvents = 'none';
      const isCorrect = opt === card.phrase_ru;
      if (isCorrect) {
        btn.classList.add('opt-correct');
      } else {
        btn.classList.add('opt-incorrect');
      }
      setTimeout(() => handleExerciseResult(card, isCorrect), 320);
    });
    stack.appendChild(btn);
  });

  arena.appendChild(wrap);
}

// 6. Voice Pronunciation Exercise
function renderExercise_Voice(card) {
  const arena = document.getElementById('workoutArena');
  const wrap = document.createElement('div');
  wrap.className = 'exercise-card-container';
  wrap.innerHTML = `
    <!-- Top Centered Circles Row(s) -->
    <div class="workout-circles-bar" id="workoutCirclesBar"></div>

    <!-- Mechanic & Instruction in Top-Left (below indicators) -->
    <div class="exercise-meta-top-left">
      <span class="exercise-type-tag">🎙️ Разговорный тренажёр</span>
      <div class="exercise-prompt-title">Проговорите фразу вслух:</div>
    </div>

    <!-- Target Phrase (with 3x spacing above) -->
    <div class="exercise-target-phrase">${escapeHtml(card.phrase_en)}</div>
    <div style="font-size:13.5px; color:var(--text-secondary); margin-bottom:18px;">🇷🇺 ${escapeHtml(card.phrase_ru)}</div>

    <div class="audio-exercise-center">
      <button type="button" class="btn-big-mic" id="btnWorkoutMic" title="Сказать">
        <svg viewBox="0 0 24 24" width="28" height="28" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
      </button>
      <span id="micStatusLabel" style="font-size:12px; color:var(--text-tertiary); margin-top: 6px;">Нажмите микрофон и повторите вслух</span>
    </div>

    <div class="self-assess-row" style="margin-top:auto;">
      <button type="button" class="btn-assess-fail" id="btnVoiceFail">🔴 Повторить</button>
      <button type="button" class="btn-assess-pass" id="btnVoicePass">🟢 Получилось!</button>
    </div>
  `;

  const micBtn = wrap.querySelector('#btnWorkoutMic');
  const micLabel = wrap.querySelector('#micStatusLabel');

  micBtn.addEventListener('click', () => {
    haptic('light');
    micBtn.classList.add('recording');
    if (micLabel) micLabel.textContent = "Слушаю ваше произношение...";
    speakPhrase(card.phrase_en, currentTargetLang, null, true);

    setTimeout(() => {
      micBtn.classList.remove('recording');
      if (micLabel) micLabel.textContent = "Отлично! Оцените, как прозвучало:";
    }, 2200);
  });

  wrap.querySelector('#btnVoiceFail').addEventListener('click', () => {
    if (workoutSession && workoutSession.isProcessing) return;
    wrap.querySelector('.self-assess-row').style.pointerEvents = 'none';
    handleExerciseResult(card, false);
  });

  wrap.querySelector('#btnVoicePass').addEventListener('click', () => {
    if (workoutSession && workoutSession.isProcessing) return;
    wrap.querySelector('.self-assess-row').style.pointerEvents = 'none';
    handleExerciseResult(card, true);
  });

  arena.appendChild(wrap);
}

// 7. News / Context Texts Exercise
let activeNewsPopoverEl = null;

function closeActiveNewsPopover() {
  if (activeNewsPopoverEl) {
    activeNewsPopoverEl.remove();
    activeNewsPopoverEl = null;
  }
}

function showNewsPhrasePopover(anchorEl, wordObj) {
  closeActiveNewsPopover();
  haptic('light');

  const rect = anchorEl.getBoundingClientRect();
  const popover = document.createElement('div');
  popover.className = 'news-popover-card';
  popover.innerHTML = `
    <div class="news-popover-head">
      <span class="news-popover-target">${escapeHtml(wordObj.phrase_target)}</span>
      <button type="button" class="btn-text-link" id="btnPopSpeak" style="font-size:16px; padding:0 4px;" title="Озвучить">🔊</button>
    </div>
    <div class="news-popover-native">🇷🇺 ${escapeHtml(wordObj.phrase_native || '—')}</div>
    <div class="news-popover-actions">
      <button type="button" class="news-popover-btn fail" id="btnPopFail">🔴 Учу</button>
      <button type="button" class="news-popover-btn pass" id="btnPopPass">🟢 Знаю</button>
    </div>
  `;

  document.body.appendChild(popover);
  activeNewsPopoverEl = popover;

  const top = Math.min(window.innerHeight - 140, Math.max(10, rect.bottom + 6));
  const left = Math.min(window.innerWidth - 300, Math.max(12, rect.left - 20));
  popover.style.top = `${top}px`;
  popover.style.left = `${left}px`;

  popover.querySelector('#btnPopSpeak').addEventListener('click', (e) => {
    e.stopPropagation();
    speakPhrase(wordObj.phrase_target, currentTargetLang, null, true);
  });

  popover.querySelector('#btnPopFail').addEventListener('click', (e) => {
    e.stopPropagation();
    if (workoutSession && wordObj.id) {
      workoutSession.phraseStates[wordObj.id] = 'red';
      renderWorkoutIndicatorCircles();
      try {
        fetch('/api/card/trainer_status', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ card_id: wordObj.id, trainer_status: 'red', user_id: userId })
        });
      } catch (err) {}
    }
    closeActiveNewsPopover();
  });

  popover.querySelector('#btnPopPass').addEventListener('click', (e) => {
    e.stopPropagation();
    if (workoutSession && wordObj.id) {
      workoutSession.phraseStates[wordObj.id] = 'green';
      renderWorkoutIndicatorCircles();
      try {
        fetch('/api/card/trainer_status', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ card_id: wordObj.id, trainer_status: 'green', user_id: userId })
        });
      } catch (err) {}
    }
    closeActiveNewsPopover();
  });

  setTimeout(() => {
    const handleOutsideClick = (evt) => {
      if (activeNewsPopoverEl && !activeNewsPopoverEl.contains(evt.target)) {
        closeActiveNewsPopover();
        document.removeEventListener('click', handleOutsideClick);
      }
    };
    document.addEventListener('click', handleOutsideClick);
  }, 100);
}

function highlightStoryWords(text, targetWords) {
  if (!text) return '';
  let cleanText = text;
  
  const sorted = [...(targetWords || [])].sort((a, b) => (b.phrase_target || '').length - (a.phrase_target || '').length);

  sorted.forEach(w => {
    const phrase = (w.phrase_target || '').trim();
    if (phrase.length >= 2) {
      const escaped = phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`(?:"|«)?\\b(${escaped})\\b(?:"|»)?`, 'gi');
      cleanText = cleanText.replace(regex, (match, p1) => {
        const isCurr = (workoutSession && workoutSession.currentCard && workoutSession.currentCard.id === w.id);
        return `___HL_START___${w.id}___${encodeURIComponent(w.phrase_target)}___${encodeURIComponent(w.phrase_native || '')}___${isCurr ? 'curr' : 'norm'}___${p1}___HL_END___`;
      });
    }
  });

  let escapedHtml = escapeHtml(cleanText);
  escapedHtml = escapedHtml.replace(/___HL_START___(\d+)___(.*?)___(.*?)___(curr|norm)___(.*?)___HL_END___/g, (m, id, tEnc, nEnc, mode, text) => {
    const t = decodeURIComponent(tEnc);
    const n = decodeURIComponent(nEnc);
    const isCurr = mode === 'curr';
    return `<span class="news-phrase-pill ${isCurr ? 'active-focused' : ''}" data-card-id="${id}" data-target="${escapeHtml(t)}" data-native="${escapeHtml(n)}">${text}</span>`;
  });

  return escapedHtml;
}

async function preloadWorkoutNewsStories(cards) {
  if (!workoutSession || !cards || cards.length === 0) return;
  workoutSession.isLoadingNews = true;
  try {
    const wordsPayload = cards.map(c => ({
      id: c.id,
      phrase_en: c.phrase_en || '',
      phrase_ru: c.phrase_ru || ''
    }));
    const res = await fetch('/api/trainer/news_context', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        target_lang: currentTargetLang,
        native_lang: currentNativeLang,
        words: wordsPayload
      })
    });
    if (res.ok) {
      const data = await res.json();
      if (workoutSession && data.stories) {
        workoutSession.newsStories = data.stories;
      }
    }
  } catch (e) {
    console.error('Error loading workout news stories:', e);
  } finally {
    if (workoutSession) {
      workoutSession.isLoadingNews = false;
    }
  }
}

function renderExercise_News(card) {
  const arena = document.getElementById('workoutArena');
  if (!arena || !workoutSession || !card) return;

  let stories = workoutSession.newsStories || [];
  let story = stories.find(s => s.word_ids && s.word_ids.includes(card.id));
  
  if (!story && stories.length > 0) {
    story = stories[0];
  }

  if (!story) {
    story = {
      id: 'story_fallback',
      title: '🎬 Hollywood & Culture News: Behind the Scenes',
      topic: '🎬 Звёзды & Шоубиз',
      source: 'People Magazine',
      text_target: `At the recent international film festival, the crew spoke about their new project. The lead actor remarked: "${card.phrase_en}". The director agreed that this shared vision helped them succeed.`,
      text_native: `На недавнем международном кинофестивале съемочная группа рассказала о своем проекте. Главный актер отметил: «${card.phrase_ru || card.phrase_en}». Режиссер согласился, что это общее видение помогло им добиться успеха.`,
      target_words: [{ id: card.id, phrase_target: card.phrase_en, phrase_native: card.phrase_ru || '' }],
      word_ids: [card.id]
    };
  }

  const targetWords = story.target_words || [{ id: card.id, phrase_target: card.phrase_en, phrase_native: card.phrase_ru || '' }];
  const highlightedHtml = highlightStoryWords(story.text_target, targetWords);

  const wrap = document.createElement('div');
  wrap.className = 'exercise-card-container';
  wrap.innerHTML = `
    <!-- Top Centered Circles Row(s) -->
    <div class="workout-circles-bar" id="workoutCirclesBar"></div>

    <!-- Mechanic & Instruction in Top-Left -->
    <div class="exercise-meta-top-left" style="margin-bottom: 14px;">
      <div style="display:flex; align-items:center; justify-content:space-between; width:100%; gap:8px;">
        <span class="exercise-type-tag">📰 Новости / тексты</span>
        <span class="news-source-tag">🌐 ${escapeHtml(story.source || 'Live News')}</span>
      </div>
      <div class="exercise-prompt-title">Найдите изучаемые фразы в живом контексте новости:</div>
    </div>

    <!-- News Article Card -->
    <div class="news-exercise-container">
      <div class="news-article-header">
        <div class="news-meta-pills-row">
          <span class="news-topic-badge">${escapeHtml(story.topic || 'Новости')}</span>
        </div>
        <div class="news-headline">${escapeHtml(story.title || 'Breaking News Story')}</div>
      </div>

      <!-- Main News Passage with Highlighted Interactive Words -->
      <div class="news-article-body" id="newsArticleBody">
        ${highlightedHtml}
      </div>

      <!-- Control Buttons: Listen Audio & Show Translation -->
      <div class="news-controls-row">
        <button type="button" class="btn-news-ctrl" id="btnSpeakNewsStory" title="Озвучить новость">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
          <span>Слушать новость</span>
        </button>
        <button type="button" class="btn-news-ctrl" id="btnToggleNewsTrans" title="Показать перевод статьи">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          <span id="lblNewsTransBtn">Перевод статьи</span>
        </button>
      </div>

      <!-- Hidden Expandable Translation Box -->
      <div class="news-translation-box" id="newsTranslationBox" style="display:none;">
        <div style="font-weight:700; font-size:12px; margin-bottom:4px; color:var(--text-tertiary);">ПЕРЕВОД:</div>
        <div>${escapeHtml(story.text_native || '')}</div>
      </div>

      <!-- Covered Phrases in this Story -->
      <div class="news-words-deck-title">Фразы в этом тексте (нажмите для перевода):</div>
      <div class="news-words-chips-grid" id="newsWordsChipsGrid"></div>
    </div>

    <!-- Self-assessment Action Row at the bottom -->
    <div class="self-assess-row" style="margin-top:auto;">
      <button type="button" class="btn-assess-fail" id="btnNewsFail">🔴 Сложно (Повторить)</button>
      <button type="button" class="btn-assess-pass" id="btnNewsPass">🟢 Текст понятен! (Знаю)</button>
    </div>
  `;

  const chipsGrid = wrap.querySelector('#newsWordsChipsGrid');
  targetWords.forEach(w => {
    const st = (workoutSession.phraseStates[w.id]) || 'neutral';
    const chip = document.createElement('div');
    chip.className = `news-word-chip ${st}`;
    chip.innerHTML = `
      <span class="chip-status-dot"></span>
      <span>${escapeHtml(w.phrase_target)}</span>
    `;
    chip.addEventListener('click', (e) => {
      e.stopPropagation();
      showNewsPhrasePopover(e.currentTarget, w);
    });
    chipsGrid.appendChild(chip);
  });

  const pills = wrap.querySelectorAll('.news-phrase-pill');
  pills.forEach(p => {
    p.addEventListener('click', (e) => {
      e.stopPropagation();
      const wordObj = {
        id: parseInt(p.getAttribute('data-card-id') || '0', 10),
        phrase_target: p.getAttribute('data-target') || p.textContent,
        phrase_native: p.getAttribute('data-native') || ''
      };
      showNewsPhrasePopover(p, wordObj);
    });
  });

  const btnSpeak = wrap.querySelector('#btnSpeakNewsStory');
  btnSpeak.addEventListener('click', () => {
    haptic('light');
    if ('speechSynthesis' in window) {
      if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
        btnSpeak.classList.remove('active');
        return;
      }
      speakPhrase(story.text_target, currentTargetLang, btnSpeak, true);
    }
  });

  const btnTrans = wrap.querySelector('#btnToggleNewsTrans');
  const transBox = wrap.querySelector('#newsTranslationBox');
  const lblTrans = wrap.querySelector('#lblNewsTransBtn');
  btnTrans.addEventListener('click', () => {
    haptic('light');
    if (transBox.style.display === 'none') {
      transBox.style.display = 'block';
      lblTrans.textContent = 'Скрыть перевод';
    } else {
      transBox.style.display = 'none';
      lblTrans.textContent = 'Перевод статьи';
    }
  });

  wrap.querySelector('#btnNewsFail').addEventListener('click', () => {
    if (workoutSession && workoutSession.isProcessing) return;
    wrap.querySelector('.self-assess-row').style.pointerEvents = 'none';
    closeActiveNewsPopover();
    handleExerciseResult(card, false);
  });

  wrap.querySelector('#btnNewsPass').addEventListener('click', () => {
    if (workoutSession && workoutSession.isProcessing) return;
    wrap.querySelector('.self-assess-row').style.pointerEvents = 'none';
    closeActiveNewsPopover();
    
    targetWords.forEach(w => {
      if (w.id && workoutSession.phraseStates[w.id] !== 'green') {
        workoutSession.phraseStates[w.id] = 'green';
        try {
          fetch('/api/card/trainer_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ card_id: w.id, trainer_status: 'green', user_id: userId })
          });
        } catch (e) {}
      }
    });

    handleExerciseResult(card, true);
  });

  arena.appendChild(wrap);
}

// Result Handler for Workout
async function handleExerciseResult(card, isCorrect) {
  if (!workoutSession || !card) return;
  if (workoutSession.isProcessing) return; // Prevent double execution and card skipping
  workoutSession.isProcessing = true;

  // Immediately disable all interactive elements in arena
  const arena = document.getElementById('workoutArena');
  if (arena) {
    const clickables = arena.querySelectorAll('button, .quiz-option-btn, .word-chip-tile, .btn-assess-pass, .btn-assess-fail, .btn-trainer-start');
    clickables.forEach(el => {
      el.style.pointerEvents = 'none';
    });
  }

  if (isCorrect) {
    workoutSession.phraseStates[card.id] = 'green';
    haptic('success');
    
    // Save green status to database
    try {
      const res = await fetch('/api/card/trainer_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: card.id, trainer_status: 'green', user_id: userId })
      });
      if (res.ok) {
        const data = await res.json();
        // Check if group completed popup should be shown
        if (data.group_completed) {
          showGroupMasteredToast(data.group_completed);
        }
      }
    } catch (e) {
      console.error('Failed to update trainer status:', e);
    }
  } else {
    workoutSession.phraseStates[card.id] = 'red';
    haptic('warning');
    
    // Save red status to database
    try {
      fetch('/api/card/trainer_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card_id: card.id, trainer_status: 'red', user_id: userId })
      });
    } catch (e) {}
  }

  renderWorkoutIndicatorCircles();
  setTimeout(() => {
    if (workoutSession) {
      presentNextExercise();
    }
  }, 380);
}

function showGroupMasteredToast(groupInfo) {
  const toast = document.getElementById('popupGroupCompleted');
  const title = document.getElementById('toastGroupTitle');
  if (title) title.textContent = `Вы выучили «${groupInfo.name}»! 🎉`;
  if (toast) {
    toast.style.display = 'flex';
    launchConfetti();
    setTimeout(() => {
      toast.style.display = 'none';
    }, 5000);
  }
}

async function showWorkoutCompletion() {
  haptic('success');
  launchConfetti();

  goToTrainerStep('completion');

  const total = workoutSession ? workoutSession.orderedCards.length : 0;
  const green = total;

  const numGreen = document.getElementById('compGreenCount');
  const numTotal = document.getElementById('compTotalCount');
  if (numGreen) numGreen.textContent = green;
  if (numTotal) numTotal.textContent = total;

  // Refresh groups in background so their green/mastered status is updated immediately
  await fetchAndRenderGroups();
}

async function resetWorkoutGroupProgress() {
  if (!workoutSession) return;
  haptic('warning');

  // Reset all trained groups
  if (trainerMode === 'groups') {
    for (const gid of selectedGroupIds) {
      await handleGroupReset(gid);
    }
  } else {
    // Reset red cards to neutral
    for (const c of workoutSession.orderedCards) {
      try {
        await fetch('/api/card/trainer_status', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ card_id: c.id, trainer_status: 'neutral', user_id: userId })
        });
      } catch (e) {}
    }
  }

  await loadTrainerSetup();
}

function initExitWorkoutModal() {
  const modal = document.getElementById('modalExitWorkoutConfirm');
  const btnClose = document.getElementById('btnCloseExitModal');
  const btnCancel = document.getElementById('btnExitWorkoutCancel');
  const btnConfirm = document.getElementById('btnExitWorkoutConfirm');

  function closeModal() {
    if (modal) {
      modal.classList.remove('open');
      setTimeout(() => modal.style.display = 'none', 200);
    }
  }

  if (btnClose) btnClose.addEventListener('click', closeModal);
  if (btnCancel) btnCancel.addEventListener('click', closeModal);

  if (btnConfirm) {
    btnConfirm.addEventListener('click', async () => {
      closeModal();
      haptic('light');
      showTrainerSetupView();
      await loadTrainerSetup();
    });
  }
}

function initWorkoutSoundToggle() {
  const btn = document.getElementById('btnWorkoutMuteToggle');
  const iconOn = document.getElementById('workoutSoundOnIcon');
  const iconOff = document.getElementById('workoutSoundOffIcon');

  function updateSoundUI() {
    if (btn) {
      if (isWorkoutMuted) {
        btn.classList.add('muted');
        btn.title = "Звук выключен (нажмите, чтобы включить)";
        if (iconOn) iconOn.style.display = 'none';
        if (iconOff) iconOff.style.display = 'block';
      } else {
        btn.classList.remove('muted');
        btn.title = "Звук включен (нажмите, чтобы выключить)";
        if (iconOn) iconOn.style.display = 'block';
        if (iconOff) iconOff.style.display = 'none';
      }
    }
  }

  updateSoundUI();

  if (btn) {
    btn.addEventListener('click', () => {
      haptic('light');
      isWorkoutMuted = !isWorkoutMuted;
      try { localStorage.setItem('wow_english_workout_muted', isWorkoutMuted.toString()); } catch (e) {}
      if (isWorkoutMuted && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      updateSoundUI();
    });
  }
}

// --- Continuous Lifecycle Sync & Re-entry Handler ---
let syncDebounceTimer = null;
function syncDataInBackground() {
  clearTimeout(syncDebounceTimer);
  syncDebounceTimer = setTimeout(() => {
    loadData(true);
  }, 300);
}

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    syncDataInBackground();
  }
});
window.addEventListener('pageshow', () => {
  syncDataInBackground();
});
window.addEventListener('focus', () => {
  syncDataInBackground();
});
window.addEventListener('online', () => {
  syncDataInBackground();
});

// Initialize on Load
initLanguagePicker();
initSupportModal();
initSupportTab();
initCategoryPickerModal();
initDictSubtabs();
initTrainerModule();
initFastScroller();
loadData();
checkAdminAccess();


