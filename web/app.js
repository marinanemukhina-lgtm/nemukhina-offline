'use strict';
const $ = id => document.getElementById(id);
const token = document.querySelector('meta[name="local-token"]').content;
const strings = {
    ru: {
        discoverModels: "Найти подготовленные файлы",
        discoveryHint: "Можно положить распакованный движок в папку runtime, а модель — в models рядом с server.py. Поиск проверяет только эти папки.",
        manualPath: "Указать путь вручную",
        foundEngine: "Найденные движки",
        foundModel: "Найденные модели",
        nothingFound: "В папках runtime и models ничего не найдено. Укажите пути вручную или положите файлы туда и повторите поиск.",
        filesFound: "Найденные файлы доступны в списках ниже.",
        checkModel: "Проверить подключённую модель",
        checkRunning: "Проверяю модель на коротком вопросе… До 60 секунд.",
        checkPassed: "Модель ответила на контрольный вопрос.",
        checkUnexpected: "Модель запустилась, но ответ отличается от ожидаемого. Проверьте её на своей задаче.",
        checkHint: "Вопрос: 2 + 2. Ожидаемый ответ: 4. Это проверка запуска, а не оценка качества всех ответов. В историю диалогов она не добавляется.",
        checkTime: "Время, с:",
        checkAnswer: "Ответ модели",
        checkCancel: "Остановить проверку",
        verified: "Модель прошла проверку запуска в этой сессии.",
        model_changed: "Файлы модели изменились во время проверки. Подключите их заново.",
        engine_timeout: "Модель не успела ответить. Попробуйте меньшую модель или более короткий вопрос.",
        skip: 'К диалогу',
        navigation: 'Навигация',
        actions: 'Действия',
        tagline: 'ИИ-помощник без интернета',
        history: 'Диалоги',
        materials: 'Материалы',
        language: 'Язык',
        new: 'Новый диалог',
        settings: 'Настройки',
        messages: 'Сообщения',
        start: 'С чего начнём?',
        intro: 'Опишите задачу своими словами. Можно уточнять и развивать ответ.',
        question: 'Что вы хотите сделать?',
        mode: 'Режим',
        chatMode: 'Диалог',
        sourceMode: 'По источникам',
        send: 'Отправить',
        stop: 'Остановить',
        noModel: 'Для ответов нужна локальная модель',
        connect: 'Подключить модель',
        configured: 'Локальные файлы подключены. Совместимость проверяется при ответе.',
        eyebrow: 'ЛИЧНЫЙ ИИ НА ВАШЕМ КОМПЬЮТЕРЕ',
        title: 'ИИ без\nинтернета.\nДля ваших задач.',
        lead: 'Объяснить сложное, придумать новое, написать текст, разобрать код — начните с вопроса.',
        example1: 'Разобраться',
        example2: 'Придумать',
        example3: 'Спланировать',
        conversationLabel: 'ДИАЛОГ',
        freedom: 'СВОБОДА МЫСЛИ',
        storyTitle: 'Ваши идеи.\nВаше пространство.',
        openSource: 'Открытый исходный код',
        privacy: 'Диалоги и материалы остаются на этом компьютере.',
        result: 'РЕЗУЛЬТАТ',
        copy: 'Копировать',
        save: 'Сохранить .md',
        close: 'Закрыть',
        showArchived: 'Показать архив',
        exportChat: 'Скачать текущий диалог',
        materialsIntro: 'Добавьте свои тексты, чтобы искать цитаты и задавать вопросы по источникам. Для обычного диалога документы не обязательны.',
        add: 'Добавить тексты',
        demo: 'Загрузить примеры',
        fileHint: 'TXT / Markdown · UTF-8 · до 1 МиБ на файл',
        useSources: 'Перейти к поиску по источникам',
        queryLabel: 'Ключевые слова в материалах',
        queryPlaceholder: 'Короткая фраза для точного поиска',
        queryHint: 'Все слова должны встретиться в одной строке. Поиск цитат доступен и без модели.',
        search: 'Найти цитаты',
        localModel: 'Локальная модель',
        setupIntro: 'Один раз подготовьте llama.cpp и модель GGUF. После этого можно работать без интернета. Качество и скорость ответов зависят от модели и компьютера.',
        setupGuide: 'Где взять движок и модель',
        setupSteps: 'Скачайте официальный выпуск llama.cpp для своей системы и распакуйте архив. Выберите совместимую инструктивную модель GGUF, проверьте её лицензию и требования к памяти. Укажите полные пути к файлам ниже. При первой загрузке модели нужен интернет; приложение ничего не скачивает автоматически.',
        enginePath: 'Путь к llama-completion',
        modelPath: 'Путь к модели .gguf',
        saveModel: "Подключить и проверить",
        yourData: 'Ваши данные',
        backupHint: 'Резервная копия включает диалоги и материалы. Восстановление добавляет отсутствующие записи, сохраняя текущие. Храните копию в безопасном месте.',
        backup: 'Скачать копию',
        restore: 'Восстановить',
        limits: 'Данные хранятся без шифрования. Нет аккаунта и телеметрии. Приложение не выполняет код и действия из ответов модели.',
        you: 'Вы',
        assistant: 'Nemukhina Offline',
        viewAnswer: 'Открыть ответ',
        thinking: 'Модель готовит ответ… Можно остановить.',
        stopping: 'Останавливаю…',
        copied: 'Скопировано',
        saved: 'Файл подготовлен к скачиванию',
        imported: 'Материалы добавлены',
        restored: 'Копия объединена с текущими данными',
        emptyHistory: 'Здесь появятся ваши диалоги после первого ответа.',
        emptyLibrary: 'Материалов пока нет. Обычный диалог работает и без них.',
        rename: 'Переименовать',
        archive: 'В архив',
        unarchive: 'Вернуть из архива',
        saveTitle: 'Сохранить',
        cancel: 'Отмена',
        modelKnowledge: 'Ответ на основе знаний модели. Проверяйте важные сведения.',
        sourceKnowledge: 'Ответ по найденным источникам. Проверяйте ссылки и выводы.',
        missing_citations: 'Модель не указала ссылки на источники. Сверьте ответ с цитатами ниже.',
        invalid_citations: 'В ответе есть ссылки на отсутствующие источники. Сверьте ответ с цитатами ниже.',
        omitted: 'Часть старых сообщений не вошла в контекст. Пропущено обменов: ',
        sources: 'Источники',
        line: 'строка',
        found: 'Найденные цитаты',
        noResults: 'Совпадений нет. Попробуйте более короткую фразу или добавьте материал.',
        query: 'Введите короткую фразу: до 24 слов и 1000 символов.',
        no_model: 'Подключите локальную модель в настройках. Ваш вопрос сохранён в поле ввода.',
        no_sources: 'Совпадений в материалах нет. Измените ключевые слова или выберите обычный диалог.',
        engine_path: 'Нужен существующий исполняемый файл llama-completion или llama-completion.exe.',
        model_path: 'Укажите существующую модель GGUF с корректным заголовком файла.',
        engine: 'Модель не ответила. Проверьте совместимость файлов, доступную память и версию llama.cpp. Ваш вопрос остался в поле ввода.',
        busy: 'Модель уже отвечает на другой запрос. Дождитесь завершения.',
        cancelled: 'Генерация остановлена. Вопрос остался в поле ввода.',
        conversation_changed: 'Диалог изменился в другом окне. Откройте его заново из истории.',
        conversation_missing: 'Диалог не найден. Обновите историю.',
        conversation_archived: 'Сначала верните диалог из архива.',
        context_limit: 'Вопрос или источники слишком объёмные для контекста модели. Сократите вопрос или поиск.',
        turn_limit: 'Достигнут предел 100 ответов в диалоге. Сохраните результат и начните новый.',
        history_limit: 'Достигнут предел истории: 500 диалогов или 20 МиБ. Экспортируйте данные и используйте отдельную базу.',
        answer_limit: 'Ответ превысил допустимый размер. Задайте более короткую задачу.',
        file_size: 'Файл больше 1 МиБ.',
        file_encoding: 'Нужен текст в кодировке UTF-8.',
        file_name: 'Поддерживаются только TXT и Markdown с обычным именем файла.',
        document_count: 'Можно добавить до 200 документов.',
        library_limit: 'Предел библиотеки: 200 документов или 50 МиБ.',
        backup_format: 'Формат резервной копии не поддерживается или повреждён.',
        checksum: 'Проверка целостности документа не пройдена.',
        request_size: 'Выбранные данные слишком объёмные.',
        session: 'Сессия сервера изменилась. Обновите страницу.',
        storage: 'Хранилище недоступно. Проверьте свободное место и права доступа.',
        network: 'Нет связи с локальным сервером. Проверьте, что он запущен. После восстановления связи загляните в историю: ответ мог сохраниться.',
        invalid_request: 'Не удалось обработать запрос. Проверьте введённые данные.',
        understand: 'Помоги разобраться в следующем вопросе: ',
        create: 'Помоги придумать и развить идею: ',
        plan: 'Помоги продумать следующие шаги для задачи: ',
        emptyExport: 'Сначала откройте диалог.',
        documentMissing: 'Исходный документ недоступен. Сохранённая цитата:',
        archived: 'В архиве',
        setupSaved: 'Файлы подключены. Задайте вопрос, чтобы проверить работу модели.',
        sourceCount: 'Найдено цитат: ',
        clipboard: 'Не удалось скопировать автоматически. Выделите текст ответа и скопируйте его.'
    },
    en: {
        discoverModels: "Find prepared files",
        discoveryHint: "Place the extracted engine in runtime and the model in models beside server.py. Discovery checks only these folders.",
        manualPath: "Enter path manually",
        foundEngine: "Detected engines",
        foundModel: "Detected models",
        nothingFound: "No files found in runtime or models. Enter paths manually, or place files there and search again.",
        filesFound: "Detected files are available in the lists below.",
        checkModel: "Check connected model",
        checkRunning: "Checking the model with a short question… Up to 60 seconds.",
        checkPassed: "The model answered the check question.",
        checkUnexpected: "The model ran, but its answer differs from the expected result. Test it on your own task.",
        checkHint: "Question: 2 + 2. Expected answer: 4. This checks startup, not overall answer quality. It is not added to conversation history.",
        checkTime: "Time, seconds:",
        checkAnswer: "Model answer",
        checkCancel: "Stop check",
        verified: "The model passed a startup check in this session.",
        model_changed: "Model files changed during the check. Connect them again.",
        engine_timeout: "The model did not answer in time. Try a smaller model or a shorter question.",
        skip: 'Go to conversation',
        navigation: 'Navigation',
        actions: 'Actions',
        tagline: 'Offline AI assistant',
        history: 'Conversations',
        materials: 'Materials',
        language: 'Language',
        new: 'New conversation',
        settings: 'Settings',
        messages: 'Messages',
        start: 'Where shall we start?',
        intro: 'Describe your task in your own words. Ask follow-up questions and develop the answer.',
        question: 'What would you like to do?',
        mode: 'Mode',
        chatMode: 'Conversation',
        sourceMode: 'From sources',
        send: 'Send',
        stop: 'Stop',
        noModel: 'Connect a local model to get answers',
        connect: 'Connect a model',
        configured: 'Local files connected. Compatibility is checked when generating an answer.',
        eyebrow: 'PERSONAL AI ON YOUR COMPUTER',
        title: 'AI without internet.\nFor your tasks.',
        lead: 'Understand something, imagine something new, write a text, work through code — start with a question.',
        example1: 'Understand',
        example2: 'Imagine',
        example3: 'Plan ahead',
        conversationLabel: 'CONVERSATION',
        freedom: 'FREEDOM TO THINK',
        storyTitle: 'Your ideas.\nYour space.',
        openSource: 'Open source',
        privacy: 'Conversations and materials stay on this computer.',
        result: 'RESULT',
        copy: 'Copy',
        save: 'Save .md',
        close: 'Close',
        showArchived: 'Show archive',
        exportChat: 'Download current conversation',
        materialsIntro: 'Add your texts to find quotes and ask questions grounded in sources. Documents are optional for ordinary conversations.',
        add: 'Add texts',
        demo: 'Load examples',
        fileHint: 'TXT / Markdown · UTF-8 · up to 1 MiB each',
        useSources: 'Search your sources',
        queryLabel: 'Keywords in your materials',
        queryPlaceholder: 'A short phrase for exact search',
        queryHint: 'All words must appear on the same line. Quote search also works without a model.',
        search: 'Find quotes',
        localModel: 'Local model',
        setupIntro: 'Prepare llama.cpp and a GGUF model once, then work without internet. Answer quality and speed depend on your model and computer.',
        setupGuide: 'Get an engine and a model',
        setupSteps: 'Download and extract an official llama.cpp release for your system. Choose a compatible GGUF instruction model and check its license and memory requirements. Enter absolute file paths below. Initial downloads require internet; this app never downloads automatically.',
        enginePath: 'Path to llama-completion',
        modelPath: 'Path to the .gguf model',
        saveModel: "Connect and check",
        yourData: 'Your data',
        backupHint: 'Backups include conversations and materials. Restore merges missing records and preserves existing data. Keep backups somewhere safe.',
        backup: 'Download backup',
        restore: 'Restore',
        limits: 'Data is stored without encryption. No account or telemetry. The app does not execute code or actions suggested by the model.',
        you: 'You',
        assistant: 'Nemukhina Offline',
        viewAnswer: 'Open answer',
        thinking: 'The model is preparing an answer… You can stop it.',
        stopping: 'Stopping…',
        copied: 'Copied',
        saved: 'File prepared for download',
        imported: 'Materials added',
        restored: 'Backup merged with current data',
        emptyHistory: 'Your conversations will appear here after the first answer.',
        emptyLibrary: 'No materials yet. Ordinary conversations do not require them.',
        rename: 'Rename',
        archive: 'Archive',
        unarchive: 'Unarchive',
        saveTitle: 'Save',
        cancel: 'Cancel',
        modelKnowledge: 'Based on model knowledge. Verify important information.',
        sourceKnowledge: 'Based on matched sources. Verify citations and conclusions.',
        missing_citations: 'The model did not cite sources. Check the answer against the quotes below.',
        invalid_citations: 'The answer refers to missing sources. Check the quotes below.',
        omitted: 'Some earlier messages did not fit the context. Exchanges omitted: ',
        sources: 'Sources',
        line: 'line',
        found: 'Matched quotes',
        noResults: 'No matches. Try a shorter phrase or add material.',
        query: 'Use a short phrase: up to 24 words and 1000 characters.',
        no_model: 'Connect a local model in settings. Your question remains in the input.',
        no_sources: 'No source matches. Change the keywords or use ordinary conversation mode.',
        engine_path: 'Select an existing executable named llama-completion or llama-completion.exe.',
        model_path: 'Select an existing GGUF model with a valid file header.',
        engine: 'The model did not answer. Check file compatibility, available memory and llama.cpp version. Your question remains in the input.',
        busy: 'The model is processing another request. Wait for it to finish.',
        cancelled: 'Generation stopped. Your question remains in the input.',
        conversation_changed: 'This conversation changed in another window. Open it again from history.',
        conversation_missing: 'Conversation not found. Refresh history.',
        conversation_archived: 'Unarchive the conversation first.',
        context_limit: 'The question or sources exceed model context. Shorten the question or narrow your search.',
        turn_limit: 'This conversation reached 100 answers. Export it and start a new one.',
        history_limit: 'History limit reached: 500 conversations or 20 MiB. Export your data and use a separate database.',
        answer_limit: 'The answer was too large. Ask a shorter task.',
        file_size: 'File exceeds 1 MiB.',
        file_encoding: 'UTF-8 text is required.',
        file_name: 'Only TXT and Markdown files with ordinary names are supported.',
        document_count: 'You can add up to 200 documents.',
        library_limit: 'Library limit: 200 documents or 50 MiB.',
        backup_format: 'Unsupported or damaged backup format.',
        checksum: 'Document integrity check failed.',
        request_size: 'The selected data is too large.',
        session: 'The server session changed. Refresh this page.',
        storage: 'Storage unavailable. Check free space and permissions.',
        network: 'Cannot reach the local server. Check that it is running. Once connected, check history: your answer may have been saved.',
        invalid_request: 'Could not process this request. Check the input.',
        understand: 'Help me understand this question: ',
        create: 'Help me imagine and develop an idea: ',
        plan: 'Help me plan the next steps for this task: ',
        emptyExport: 'Open a conversation first.',
        documentMissing: 'The original document is unavailable. Saved quote:',
        archived: 'Archived',
        setupSaved: 'Files connected. Ask a question to check the model.',
        sourceCount: 'Quotes found: ',
        clipboard: 'Automatic copy failed. Select and copy the answer text.'
    },
    zh: {
        discoverModels: "查找已准备的文件",
        discoveryHint: "将解压后的运行程序放入 server.py 旁的 runtime 文件夹，将模型放入 models 文件夹。仅搜索这两个文件夹。",
        manualPath: "手动输入路径",
        foundEngine: "找到的运行程序",
        foundModel: "找到的模型",
        nothingFound: "runtime 和 models 中没有找到文件。请手动输入路径，或放入文件后重新搜索。",
        filesFound: "找到的文件已列在下方。",
        checkModel: "检查已连接的模型",
        checkRunning: "正在用简短问题检查模型… 最长 60 秒。",
        checkPassed: "模型已回答检查问题。",
        checkUnexpected: "模型已运行，但答案与预期不同。请用自己的任务进一步测试。",
        checkHint: "问题：2 + 2。预期答案：4。这只检查运行情况，不代表整体回答质量。不会加入对话历史。",
        checkTime: "耗时（秒）：",
        checkAnswer: "模型回答",
        checkCancel: "停止检查",
        verified: "模型已通过本次会话的启动检查。",
        model_changed: "检查期间模型文件发生了变化。请重新连接。",
        engine_timeout: "模型未能及时回答。请尝试更小的模型或更短的问题。",
        skip: '跳转到对话',
        navigation: '导航',
        actions: '操作',
        tagline: '离线 AI 助手',
        history: '对话',
        materials: '资料',
        language: '语言',
        new: '新对话',
        settings: '设置',
        messages: '消息',
        start: '从哪里开始？',
        intro: '用自己的话描述任务。可以继续提问，逐步完善回答。',
        question: '您想做什么？',
        mode: '模式',
        chatMode: '对话',
        sourceMode: '依据来源',
        send: '发送',
        stop: '停止',
        noModel: '连接本地模型后即可获得回答',
        connect: '连接模型',
        configured: '已连接本地文件。生成回答时将检查兼容性。',
        eyebrow: '在您电脑上运行的个人 AI',
        title: '无需联网的 AI。\n为您的任务而来。',
        lead: '理解复杂问题、构思新想法、撰写文字、分析代码——从一个问题开始。',
        example1: '理解问题',
        example2: '构思创意',
        example3: '规划下一步',
        conversationLabel: '对话',
        freedom: '自由思考',
        storyTitle: '你的想法。\n你的空间。',
        openSource: '开放源代码',
        privacy: '对话和资料保存在这台电脑上。',
        result: '结果',
        copy: '复制',
        save: '保存 .md',
        close: '关闭',
        showArchived: '显示归档',
        exportChat: '下载当前对话',
        materialsIntro: '添加文本，查找原文引用并依据来源提问。普通对话不需要文档。',
        add: '添加文本',
        demo: '加载示例',
        fileHint: 'TXT / Markdown · UTF-8 · 每个文件不超过 1 MiB',
        useSources: '搜索来源',
        queryLabel: '资料中的关键词',
        queryPlaceholder: '输入简短的精确搜索词',
        queryHint: '所有词语必须出现在同一行。没有模型也能搜索引用。',
        search: '查找引用',
        localModel: '本地模型',
        setupIntro: '首次准备好 llama.cpp 和 GGUF 模型后，即可离线使用。回答质量和速度取决于模型及电脑。',
        setupGuide: '获取运行程序和模型',
        setupSteps: '下载适合系统的官方 llama.cpp 版本并解压。选择兼容的 GGUF 指令模型，检查许可证及内存要求。在下方输入完整文件路径。首次下载需要网络；本应用不会自动下载。',
        enginePath: 'llama-completion 路径',
        modelPath: '.gguf 模型路径',
        saveModel: "连接并检查",
        yourData: '您的数据',
        backupHint: '备份包含对话和资料。恢复时添加缺少的记录，保留现有数据。请妥善保管备份。',
        backup: '下载备份',
        restore: '恢复',
        limits: '数据未加密存储。无需账号，无遥测。本应用不会执行模型建议的代码或操作。',
        you: '您',
        assistant: 'Nemukhina Offline',
        viewAnswer: '打开回答',
        thinking: '模型正在生成回答……可以停止。',
        stopping: '正在停止……',
        copied: '已复制',
        saved: '文件已准备下载',
        imported: '已添加资料',
        restored: '已将备份与现有数据合并',
        emptyHistory: '首次获得回答后，对话将出现在这里。',
        emptyLibrary: '暂无资料。普通对话不需要资料。',
        rename: '重命名',
        archive: '归档',
        unarchive: '取消归档',
        saveTitle: '保存',
        cancel: '取消',
        modelKnowledge: '依据模型知识生成，请核实重要信息。',
        sourceKnowledge: '依据匹配来源生成，请核实引用和结论。',
        missing_citations: '模型未标注来源。请与下方原文核对。',
        invalid_citations: '回答引用了不存在的来源。请与下方原文核对。',
        omitted: '部分较早的消息未纳入上下文。省略的问答数：',
        sources: '来源',
        line: '行',
        found: '匹配的引用',
        noResults: '没有匹配结果。请缩短关键词或添加资料。',
        query: '请输入简短搜索词：最多 24 个词、1000 个字符。',
        no_model: '请在设置中连接本地模型。问题仍保留在输入框中。',
        no_sources: '资料中没有匹配结果。请调整关键词或使用普通对话模式。',
        engine_path: '请选择名为 llama-completion 或 llama-completion.exe 的可执行文件。',
        model_path: '请选择文件头有效的现有 GGUF 模型。',
        engine: '模型未能回答。请检查文件兼容性、可用内存和 llama.cpp 版本。问题仍保留在输入框中。',
        busy: '模型正在处理其他请求，请等待完成。',
        cancelled: '已停止生成。问题仍保留在输入框中。',
        conversation_changed: '其他窗口已修改此对话，请从历史记录重新打开。',
        conversation_missing: '找不到对话，请刷新历史记录。',
        conversation_archived: '请先取消归档。',
        context_limit: '问题或来源超过上下文限制，请缩短问题或搜索范围。',
        turn_limit: '此对话已达到 100 次回答，请导出后开始新对话。',
        history_limit: '已达到历史记录上限：500 个对话或 20 MiB。请导出数据并使用另一个数据库。',
        answer_limit: '回答过长，请缩小任务范围。',
        file_size: '文件超过 1 MiB。',
        file_encoding: '需要 UTF-8 编码文本。',
        file_name: '仅支持名称有效的 TXT 和 Markdown 文件。',
        document_count: '最多可添加 200 个文档。',
        library_limit: '资料库上限：200 个文档或 50 MiB。',
        backup_format: '备份格式不受支持或已损坏。',
        checksum: '文档完整性检查失败。',
        request_size: '所选数据过大。',
        session: '服务器会话已更改，请刷新页面。',
        storage: '存储不可用，请检查空间和权限。',
        network: '无法连接本地服务器，请检查是否已启动。恢复连接后请查看历史记录，回答可能已经保存。',
        invalid_request: '无法处理请求，请检查输入。',
        understand: '请帮我理解这个问题：',
        create: '请帮我构思并完善这个想法：',
        plan: '请帮我规划这项任务的下一步：',
        emptyExport: '请先打开对话。',
        documentMissing: '原始文档不可用。已保存的引用：',
        archived: '已归档',
        setupSaved: '已连接文件，请提问以检查模型。',
        sourceCount: '找到的引用数：',
        clipboard: '自动复制失败，请选中并复制回答文本。'
    }
};
let lang = 'ru';
try {
    const saved = localStorage.getItem('nemukhina-language');
    if (strings[saved]) lang = saved;
} catch (_) {}
let state = {
        documents: [],
        conversations: [],
        model: false
    },
    current = null,
    selected = null,
    pending = null,
    toastTimer;
const t = key => strings[lang][key] || strings[lang].invalid_request;
const el = (tag, text, cls) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (cls) node.className = cls;
    return node;
};

function notify(text) {
    $('toast').textContent = text;
    $('toast').hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        $('toast').hidden = true;
    }, 6000);
}
async function api(path, data = {}) {
    let response;
    try {
        response = await fetch('/api/' + path, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Local-Token': token
            },
            body: JSON.stringify(data)
        });
    } catch (_) {
        throw new Error('network');
    }
    let result;
    try {
        result = await response.json();
    } catch (_) {
        throw new Error('network');
    }
    if (!response.ok) throw new Error(result.error || 'invalid_request');
    return result;
}
async function run(fn) {
    try {
        await fn();
    } catch (error) {
        notify(t(error.message));
    }
}
async function refresh() {
    state = await api('state');
    renderModel();
    renderDocuments();
    renderHistory();
}

function translate() {
    document.documentElement.lang = lang;
    document.title = 'Nemukhina Offline — ' + t('tagline');
    $('lang').value = lang;
    document.querySelectorAll('[data-t]').forEach(n => {
        n.textContent = t(n.dataset.t);
    });
    document.querySelectorAll('[data-placeholder]').forEach(n => n.placeholder = t(n.dataset.placeholder));
    document.querySelectorAll('[data-aria]').forEach(n => n.setAttribute('aria-label', t(n.dataset.aria)));
    document.querySelectorAll('[data-title]').forEach(n => n.title = t(n.dataset.title));
    renderModel();
    renderMessages();
    renderDocuments();
    renderHistory();
    if (selected) showResult(selected);
}

function renderModel() {
    $('modelHint').textContent = t(state.model_check?.status === 'passed' ? 'verified' : state.model ? 'configured' : 'noModel');
    $('modelLabel').textContent = state.model ? state.model_name : t('connect');
    $('checkModel').disabled = !state.model || !!pending;
    renderModelCheck();
}

function renderMessages() {
    $('chatTitle').textContent = current ? current.title : t('new');
    const box = $('messages');
    box.replaceChildren();
    if (!current) {
        const intro = el('div');
        intro.append(el('h3', t('start')), el('p', t('intro')));
        box.append(intro);
        return;
    }
    current.turns.forEach(turn => {
        const user = el('div', undefined, 'message user');
        user.append(el('div', t('you'), 'speaker'), el('p', turn.question));
        const assistant = el('div', undefined, 'message');
        assistant.append(el('div', t('assistant'), 'speaker'), el('p', turn.answer.length > 220 ? turn.answer.slice(0, 220) + '…' : turn.answer));
        const view = el('button', t('viewAnswer'));
        view.onclick = () => {
            showResult(turn);
            if (window.innerWidth <= 680) $('result').scrollIntoView({
                behavior: 'smooth'
            });
        };
        assistant.append(view);
        box.append(user, assistant);
    });
    box.scrollTop = box.scrollHeight;
}

function markdown(text, container) {
    container.replaceChildren();
    const lines = text.replace(/\r\n/g, '\n').split('\n');
    let paragraph = [],
        code = null,
        list = null;
    const flush = () => {
        if (paragraph.length) {
            container.append(el('p', paragraph.join('\n')));
            paragraph = [];
        }
        list = null;
    };
    for (const line of lines) {
        if (line.trimStart().startsWith('```')) {
            flush();
            if (code !== null) {
                const pre = el('pre');
                pre.append(el('code', code.join('\n')));
                container.append(pre);
                code = null;
            } else code = [];
            continue;
        }
        if (code !== null) {
            code.push(line);
            continue;
        }
        const heading = line.match(/^(#{1,6})\s+(.+)$/);
        const item = line.match(/^\s*(?:[-*+]\s+|\d+[.)]\s+)(.+)$/);
        if (heading) {
            flush();
            container.append(el(heading[1].length <= 2 ? 'h2' : 'h3', heading[2]));
        } else if (item) {
            if (paragraph.length) flush();
            const kind = /^\s*\d/.test(line) ? 'ol' : 'ul';
            if (!list || list.tagName.toLowerCase() !== kind) {
                list = el(kind);
                if (kind === 'ol') list.start = parseInt(line.trim(), 10);
                container.append(list);
            }
            list.append(el('li', item[1]));
        } else if (!line.trim()) flush();
        else if (line.startsWith('> ')) {
            flush();
            container.append(el('blockquote', line.slice(2)));
        } else {
            list = null;
            paragraph.push(line);
        }
    }
    flush();
    if (code !== null) {
        const pre = el('pre');
        pre.append(el('code', code.join('\n')));
        container.append(pre);
    }
}

function showResult(turn) {
    selected = turn;
    document.body.dataset.view = 'workspace';
    $('welcome').hidden = true;
    $('result').hidden = false;
    $('resultTitle').textContent = turn.search ? t('found') : (turn.question.length > 140 ? turn.question.slice(0, 140) + '…' : turn.question);
    $('resultMeta').textContent = turn.search ? t('sourceCount') + turn.sources.length : t(turn.mode === 'sources' ? 'sourceKnowledge' : 'modelKnowledge');
    markdown(turn.answer || (turn.sources.length ? '' : t('noResults')), $('answer'));
    const warnings = [];
    if (turn.warning) warnings.push(t(turn.warning));
    if (turn.context_omitted) warnings.push(t('omitted') + turn.context_omitted);
    $('warning').textContent = warnings.join(' ');
    $('warning').hidden = !warnings.length;
    $('copy').disabled = !turn.answer;
    $('download').disabled = !turn.answer;
    renderSources(turn.sources || []);
}

function renderSources(sources) {
    const box = $('sources');
    box.replaceChildren();
    if (!sources.length) return;
    box.append(el('h2', t('sources')));
    sources.forEach((source, i) => {
        const row = el('div', undefined, 'source');
        const open = el('button', '[' + (i + 1) + '] ' + source.name + ' · ' + t('line') + ' ' + source.line);
        open.onclick = () => run(() => openDocument(source.id, source));
        row.append(open, el('blockquote', source.quote), el('div', 'SHA-256: ' + source.id, 'hash'));
        box.append(row);
    });
}

function newConversation() {
    current = null;
    selected = null;
    document.body.dataset.view = 'home';
    $('result').hidden = true;
    $('welcome').hidden = false;
    $('question').value = '';
    $('status').textContent = '';
    renderMessages();
    $('question').focus();
}

function setBusy(value) {
    ['new', 'history', 'materials', 'attach', 'settings', 'lang', 'mode', 'modelHelp', 'search'].forEach(id => $(id).disabled = value);
    document.querySelectorAll('[data-example]').forEach(button => button.disabled = value);
    $('question').readOnly = value;
    $('query').readOnly = value;
    $('send').hidden = value;
    $('stop').hidden = !value;
    $('stop').disabled = false;
    $('chatForm').setAttribute('aria-busy', String(value));
}
$('chatForm').onsubmit = event => {
    event.preventDefault();
    if (pending) return;
    run(async () => {
        if (!state.model) {
            $('status').textContent = t('no_model');
            await openSettings();
            return;
        }
        const question = $('question').value.trim();
        if (!question) return;
        pending = crypto.randomUUID().replaceAll('-', '');
        setBusy(true);
        $('status').textContent = t('thinking');
        try {
            const result = await api('chat', {
                id: current ? current.id : null,
                revision: current ? current.revision : null,
                request_id: pending,
                question,
                lang,
                mode: $('mode').value,
                query: $('query').value.trim()
            });
            current = result.conversation;
            $('question').value = '';
            $('status').textContent = '';
            renderMessages();
            showResult(current.turns[current.turns.length - 1]);
            if (window.innerWidth <= 680) $('result').scrollIntoView({
                behavior: 'smooth'
            });
            await refresh();
        } catch (error) {
            $('status').textContent = t(error.message);
        } finally {
            pending = null;
            setBusy(false);
            $('question').focus({
                preventScroll: true
            });
        }
    });
};
$('question').onkeydown = event => {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        $('chatForm').requestSubmit();
    }
};
$('stop').onclick = () => run(async () => {
    if (!pending) return;
    $('stop').disabled = true;
    $('status').textContent = t('stopping');
    await api('chat/cancel', {
        request_id: pending
    });
});
$('new').onclick = newConversation;
$('mode').onchange = () => {
    $('sourceQuery').hidden = $('mode').value !== 'sources';
};
$('search').onclick = () => run(async () => {
    const result = await api('search', {
        query: $('query').value.trim()
    });
    showResult({
        search: true,
        answer: null,
        sources: result.sources
    });
    if (innerWidth <= 680) $('result').scrollIntoView({
        behavior: 'smooth'
    });
});
document.querySelectorAll('[data-example]').forEach(button => {
    button.onclick = () => {
        $('question').value = t(button.dataset.example);
        $('question').focus();
        $('question').setSelectionRange($('question').value.length, $('question').value.length);
    };
});
$('lang').onchange = () => {
    lang = $('lang').value;
    try {
        localStorage.setItem('nemukhina-language', lang);
    } catch (_) {}
    translate();
};
document.querySelectorAll('dialog .close').forEach(button => button.onclick = () => button.closest('dialog').close());
$('settings').onclick = $('modelHelp').onclick = () => run(openSettings);
$('materials').onclick = $('attach').onclick = () => run(async () => {
    await refresh();
    $('materialsDialog').showModal();
});
$('history').onclick = () => run(async () => {
    await refresh();
    $('historyDialog').showModal();
});
$('showArchived').onchange = renderHistory;
async function openConversation(id) {
    const result = await api('conversation', {
        id
    });
    current = result.conversation;
    $('historyDialog').close();
    $('question').value = '';
    $('status').textContent = '';
    renderMessages();
    showResult(current.turns[current.turns.length - 1]);
    if (window.innerWidth <= 680) $('result').scrollIntoView({
        behavior: 'smooth'
    });
}

function renderHistory() {
    const box = $('historyList');
    box.replaceChildren();
    const rows = state.conversations.filter(c => Boolean(c.archived) === $('showArchived').checked);
    if (!rows.length) box.append(el('p', t('emptyHistory'), 'muted'));
    rows.forEach(chat => {
        const row = el('div', undefined, 'item');
        const content = el('div');
        const title = el('button', chat.title, 'item-title');
        title.onclick = () => run(() => openConversation(chat.id));
        content.append(title);
        if (chat.archived) content.append(el('small', t('archived')));
        const actions = el('div', undefined, 'item-actions');
        const rename = el('button', t('rename'), 'secondary');
        rename.onclick = () => {
            const form = el('form', undefined, 'rename-field');
            const input = el('input');
            input.value = chat.title;
            input.maxLength = 100;
            input.required = true;
            input.setAttribute('aria-label', t('rename'));
            const save = el('button', t('saveTitle'), 'secondary');
            const cancel = el('button', t('cancel'));
            cancel.type = 'button';
            cancel.onclick = renderHistory;
            form.append(input, save, cancel);
            content.append(form);
            rename.disabled = true;
            input.focus();
            form.onsubmit = e => {
                e.preventDefault();
                run(async () => {
                    const result = await api('conversation/update', {
                        id: chat.id,
                        revision: chat.revision,
                        title: input.value
                    });
                    if (current && current.id === chat.id) {
                        current = result.conversation;
                        renderMessages();
                    }
                    await refresh();
                });
            };
        };
        const archive = el('button', t(chat.archived ? 'unarchive' : 'archive'), 'secondary');
        archive.onclick = () => run(async () => {
            const result = await api('conversation/update', {
                id: chat.id,
                revision: chat.revision,
                archived: !chat.archived
            });
            if (current && current.id === chat.id) {
                if (result.conversation.archived) newConversation();
                else current = result.conversation;
            }
            await refresh();
        });
        actions.append(rename, archive);
        row.append(content, actions);
        box.append(row);
    });
    $('exportChat').disabled = !current;
}

function renderDocuments() {
    const box = $('documents');
    box.replaceChildren();
    if (!state.documents.length) box.append(el('p', t('emptyLibrary'), 'muted'));
    state.documents.forEach(doc => {
        const row = el('div', undefined, 'item');
        const content = el('div');
        const title = el('button', doc.name, 'item-title');
        title.onclick = () => run(() => openDocument(doc.id));
        content.append(title, el('small', (doc.size / 1024).toFixed(1) + ' KiB'));
        row.append(content);
        box.append(row);
    });
}
async function openDocument(id, source) {
    const result = await api('document', {
        id
    });
    $('documentTitle').textContent = result.document ? result.document.name : source ? source.name : t('materials');
    $('documentText').textContent = result.document ? result.document.text : t('documentMissing') + '\n' + (source ? source.quote : '');
    $('documentDialog').showModal();
}
$('import').onclick = () => $('files').click();
$('files').onchange = () => {
    const files = [...$('files').files];
    $('files').value = '';
    run(async () => {
        if (files.length > 200) throw new Error('document_count');
        const documents = [];
        let total = 0;
        for (const file of files) {
            if (file.size > 1024 * 1024) throw new Error('file_size');
            total += file.size;
            if (total > 6 * 1024 * 1024) throw new Error('request_size');
            let text;
            try {
                text = new TextDecoder('utf-8', {
                    fatal: true
                }).decode(await file.arrayBuffer());
            } catch (_) {
                throw new Error('file_encoding');
            }
            documents.push({
                name: file.name,
                text
            });
        }
        await api('import', {
            documents
        });
        await refresh();
        notify(t('imported'));
    });
};
$('demo').onclick = () => run(async () => {
    await api('demo');
    await refresh();
    notify(t('imported'));
});
$('useSources').onclick = () => {
    $('materialsDialog').close();
    $('mode').value = 'sources';
    $('mode').onchange();
    $('query').focus();
};
function renderModelCheck() {
    const result = state.model_check;
    $('probeResult').hidden = !result;
    if (!result) return;
    $('probeSummary').textContent = t(result.status === 'passed' ? 'checkPassed' : 'checkUnexpected');
    $('probeTime').textContent = result.model_name + ' · ' + t('checkTime') + ' ' + result.elapsed_seconds;
    $('probeAnswer').textContent = result.answer;
}
function setupStatus(key) {
    const status = $('settingsStatus');
    if (key) status.dataset.t = key;
    else delete status.dataset.t;
    status.textContent = key ? t(key) : '';
}
async function openSettings() {
    $('settingsDialog').showModal();
    const options = await api('model/options');
    if (!$('enginePath').value) $('enginePath').value = options.configuration.engine;
    if (!$('modelPath').value) $('modelPath').value = options.configuration.model;
}
$('discoverModels').onclick = () => run(async () => {
    const options = await api('model/options');
    for (const [key, selectId] of [['engines', 'engineChoice'], ['models', 'modelChoice']]) {
        const select = $(selectId);
        select.replaceChildren();
        const manual = el('option', t('manualPath'));
        manual.dataset.t = 'manualPath';
        manual.value = '';
        select.append(manual);
        for (const file of options[key]) {
            const option = el('option', file.name);
            option.value = file.path;
            select.append(option);
        }
    }
    const found = options.engines.length + options.models.length > 0;
    $('discoveredModels').hidden = !found;
    setupStatus(found ? 'filesFound' : 'nothingFound');
});
$('engineChoice').onchange = () => {
    if ($('engineChoice').value) $('enginePath').value = $('engineChoice').value;
};
$('modelChoice').onchange = () => {
    if ($('modelChoice').value) $('modelPath').value = $('modelChoice').value;
};
async function checkConnectedModel() {
    if (pending || !state.model) return;
    pending = crypto.randomUUID().replaceAll('-', '');
    setBusy(true);
    $('modelForm').querySelectorAll('input, button').forEach(n => n.disabled = true);
    ['discoverModels', 'engineChoice', 'modelChoice', 'checkModel'].forEach(id => $(id).disabled = true);
    $('cancelCheck').hidden = false;
    $('cancelCheck').disabled = false;
    $('probeResult').hidden = true;
    setupStatus('checkRunning');
    $('status').textContent = t('checkRunning');
    try {
        await api('model/check', {request_id: pending});
        await refresh();
        setupStatus();
        $('status').textContent = '';
    } catch (error) {
        await refresh().catch(() => {});
        setupStatus(error.message);
        $('status').textContent = t(error.message);
    } finally {
        pending = null;
        setBusy(false);
        $('modelForm').querySelectorAll('input, button').forEach(n => n.disabled = false);
        ['discoverModels', 'engineChoice', 'modelChoice'].forEach(id => $(id).disabled = false);
        $('cancelCheck').hidden = true;
        renderModel();
    }
}
$('cancelCheck').onclick = () => run(async () => {
    if (!pending) return;
    await api('chat/cancel', {request_id: pending});
    $('cancelCheck').disabled = true;
    setupStatus('stopping');
});
$('checkModel').onclick = () => run(checkConnectedModel);
$('modelForm').onsubmit = event => {
    event.preventDefault();
    if (pending) return;
    run(async () => {
        try {
            await api('model', {
                engine: $('enginePath').value.trim(),
                model: $('modelPath').value.trim()
            });
            await refresh();
            await checkConnectedModel();
        } catch (error) {
            setupStatus(error.message);
        }
    });
};

function download(name, data, type) {
    const url = URL.createObjectURL(new Blob([data], {
        type
    }));
    const a = el('a');
    a.href = url;
    a.download = name;
    document.body.append(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    notify(t('saved'));
}

function turnText(turn) {
    let text = '# ' + turn.question + '\n\n' + turn.answer + '\n';
    if (turn.sources && turn.sources.length) text += '\n## ' + t('sources') + '\n\n' + turn.sources.map((s, i) => '[' + (i + 1) + '] ' + s.name + ':' + s.line + '\n' + s.quote + '\nSHA-256: ' + s.id).join('\n\n');
    return text;
}
$('copy').onclick = () => run(async () => {
    if (!selected || !selected.answer) return;
    try {
        await navigator.clipboard.writeText(selected.answer);
        notify(t('copied'));
    } catch (_) {
        throw new Error('clipboard');
    }
});
$('download').onclick = () => {
    if (selected && selected.answer) download('nemukhina-result.md', turnText(selected), 'text/markdown;charset=utf-8');
};
$('exportChat').onclick = () => {
    if (current) download('nemukhina-conversation.md', '# ' + current.title + '\n\n' + current.turns.map(turnText).join('\n\n---\n\n'), 'text/markdown;charset=utf-8');
};
$('backup').onclick = () => run(async () => {
    const data = await api('backup');
    download('nemukhina-backup.json', JSON.stringify(data, null, 2), 'application/json');
});
$('restore').onclick = () => $('restoreFile').click();
$('restoreFile').onchange = () => {
    const file = $('restoreFile').files[0];
    $('restoreFile').value = '';
    if (!file) return;
    run(async () => {
        if (file.size > 320 * 1024 * 1024) throw new Error('request_size');
        let backup;
        try {
            backup = JSON.parse(new TextDecoder('utf-8', {
                fatal: true
            }).decode(await file.arrayBuffer()));
        } catch (_) {
            throw new Error('backup_format');
        }
        await api('restore', {
            backup
        });
        await refresh();
        notify(t('restored'));
    });
};
translate();
run(refresh);
