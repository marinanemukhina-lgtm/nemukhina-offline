'use strict';
const $ = id => document.getElementById(id);
const token = document.querySelector('meta[name="local-token"]').content;
const strings = {
  ru: {
    skip: 'К содержимому',
    library: 'ВАША БИБЛИОТЕКА',
    add: '＋ Добавить тексты',
    fileHint: 'TXT / Markdown · до 1 МиБ на файл',
    emptyLibrary: 'Здесь появятся ваши источники. Они останутся на этом компьютере.',
    backup: 'Скачать копию',
    restore: 'Восстановить',
    local: 'Работает на вашем компьютере',
    privacy: 'Без аккаунта. Без облака. Без телеметрии.',
    workspace: 'Рабочее пространство / Источники',
    language: 'Язык',
    eyebrow: 'ЗНАНИЯ ПОД РУКОЙ',
    title: 'Ваши тексты.\nЯсные ответы.',
    lead: 'Найдите нужную мысль в своих материалах — с точной цитатой, которую можно проверить.',
    searchLabel: 'Что ищем в источниках?',
    placeholder: 'Например: дробь',
    search: 'Найти цитаты ↗',
    searchHint: 'Ищем все введённые слова в одной строке. Попробуйте короткую фразу.',
    sourceMode: 'Режим источников',
    noModel: 'Поиск работает без нейросети.',
    connect: 'Как подключить модель',
    askTitle: 'Объяснить с локальной моделью',
    question: 'Ваш вопрос к найденным источникам',
    mode: 'Режим',
    general: 'Повседневные задачи',
    school: 'Школьнику',
    university: 'Студенту',
    ask: 'Объяснить',
    start: 'Начните с небольшой идеи',
    samples: 'Встроенные учебные примеры',
    sample1: 'Понять дроби',
    sample1sub: 'Одна мысль. Точный источник.',
    sample2: 'Спланировать исследование',
    sample2sub: 'От вопроса к проверке вывода.',
    sample3: 'Три языка, одна библиотека',
    sample3sub: 'Русский, English, 中文.',
    results: 'Найдено в ваших источниках',
    noResults: 'Совпадений нет. Уберите лишние слова или добавьте источник. Мы не будем придумывать ответ.',
    draft: 'ЧЕРНОВИК МОДЕЛИ · ПРОВЕРЬТЕ ССЫЛКИ',
    foot: 'Сначала источник. Затем вывод.',
    helpTitle: 'Локальная модель',
    helpBody: 'Заранее скачайте llama.cpp и совместимую GGUF-модель. Перезапустите приложение с путями к ним:',
    helpNote: 'Ничего не скачивается автоматически. Генерация экспериментальная: качество и цитаты нужно проверять. Поиск и библиотека уже доступны без модели.',
    working: 'Обработка…',
    thinking: 'Модель готовит черновик. Это может занять до 3 минут…',
    saved: 'Добавлено документов: ',
    removed: 'Документ удалён.',
    copy: 'Копировать',
    copied: 'Цитата скопирована.',
    line: 'строка',
    delete: 'Удалить',
    confirmDelete: 'Удалить документ из библиотеки? Сохраните резервную копию, если он ещё нужен.',
    restoreConfirm: 'Добавить документы из копии? Существующие тексты сохранятся.',
    error: 'Не удалось выполнить действие. Проверьте файл, лимиты и запущенное приложение.',
    file_size: 'Файл превышает 1 МиБ.',
    file_encoding: 'Нужен корректный текст UTF-8.',
    file_name: 'Допускаются имена TXT/MD без пути.',
    checksum: 'Контрольная сумма не совпадает. Копия не импортирована.',
    backup_format: 'Неподдерживаемая резервная копия.',
    library_limit: 'Лимит: 200 документов / 50 МиБ.',
    document_count: 'Не более 200 документов за один импорт.',
    request_size: 'Запрос слишком большой. Импортируйте небольшими группами (до 8 МиБ JSON).',
    session: 'Сессия изменилась. Обновите страницу.',
    busy: 'Модель уже занята. Попробуйте позже.',
    modelReady: 'Модель настроена',
    modelHint: 'Локальная генерация · экспериментально',
    backupDone: 'Копия скачана. Храните её вне репозитория.',
    fraction: 'дробь',
    project: 'проект',
    all: '1/2'
  },
  en: {
    skip: 'Skip to content',
    library: 'YOUR LIBRARY',
    add: '＋ Add texts',
    fileHint: 'TXT / Markdown · up to 1 MiB per file',
    emptyLibrary: 'Your sources will appear here. They stay on this computer.',
    backup: 'Download backup',
    restore: 'Restore',
    local: 'Running on your computer',
    privacy: 'No account. No cloud. No telemetry.',
    workspace: 'Workspace / Sources',
    language: 'Language',
    eyebrow: 'KNOWLEDGE WITHIN REACH',
    title: 'Your sources.\nClearer thinking.',
    lead: 'Find the idea you need in your own material, with an exact quotation you can check.',
    searchLabel: 'What are you looking for?',
    placeholder: 'Try: fraction',
    search: 'Find quotes ↗',
    searchHint: 'All search terms must appear on one line. Try a short phrase.',
    sourceMode: 'Source mode',
    noModel: 'Search works without an AI model.',
    connect: 'Connect a local model',
    askTitle: 'Explain with a local model',
    question: 'Your question about these sources',
    mode: 'Mode',
    general: 'Everyday tasks',
    school: 'School',
    university: 'University',
    ask: 'Explain',
    start: 'Start with a small idea',
    samples: 'Built-in learning examples',
    sample1: 'Make sense of fractions',
    sample1sub: 'One idea. An exact source.',
    sample2: 'Plan a study project',
    sample2sub: 'From question to checked conclusion.',
    sample3: 'Three languages, one library',
    sample3sub: 'Русский, English, 中文.',
    results: 'Found in your sources',
    noResults: 'No matches. Try fewer words or add a source. We will not invent an answer.',
    draft: 'MODEL DRAFT · VERIFY THE CITATIONS',
    foot: 'Source first. Conclusion second.',
    helpTitle: 'A model on your computer',
    helpBody: 'Download llama.cpp and a compatible GGUF model beforehand. Restart with their local paths:',
    helpNote: 'Nothing is downloaded automatically. Generation is experimental: check quality and citations. Search and library features already work without a model.',
    working: 'Working…',
    thinking: 'The model is drafting. This can take up to 3 minutes…',
    saved: 'Documents added: ',
    removed: 'Document deleted.',
    copy: 'Copy',
    copied: 'Quotation copied.',
    line: 'line',
    delete: 'Delete',
    confirmDelete: 'Delete this document? Download a backup first if you still need it.',
    restoreConfirm: 'Merge documents from this backup? Existing texts will be preserved.',
    error: 'Could not complete the action. Check the file, limits and running application.',
    file_size: 'File exceeds 1 MiB.',
    file_encoding: 'Valid UTF-8 text is required.',
    file_name: 'Use a TXT/MD filename without a path.',
    checksum: 'Checksum mismatch. Backup not imported.',
    backup_format: 'Unsupported backup format.',
    library_limit: 'Limit: 200 documents / 50 MiB.',
    document_count: 'Maximum 200 documents per import.',
    request_size: 'Request too large. Import smaller groups (up to 8 MiB JSON).',
    session: 'Session changed. Reload this page.',
    busy: 'Model is busy. Please try later.',
    modelReady: 'Model configured',
    modelHint: 'Local generation · experimental',
    backupDone: 'Backup downloaded. Store it outside the repository.',
    fraction: 'fraction',
    project: 'project',
    all: '1/2'
  },
  zh: {
    skip: '跳到内容',
    library: '您的资料库',
    add: '＋ 添加文本',
    fileHint: 'TXT / Markdown · 每个文件最多 1 MiB',
    emptyLibrary: '您的资料将显示在这里，并保留在此电脑上。',
    backup: '下载备份',
    restore: '恢复',
    local: '在您的电脑上运行',
    privacy: '无需账号。无需云端。无遥测。',
    workspace: '工作区 / 来源',
    language: '语言',
    eyebrow: '知识触手可及',
    title: '您的资料。\n清晰的思路。',
    lead: '从自己的资料中找到所需的观点，并附上可核查的原文引用。',
    searchLabel: '您想查找什么？',
    placeholder: '试试：分数',
    search: '查找引用 ↗',
    searchHint: '所有搜索词必须出现在同一行。请尝试简短词组。',
    sourceMode: '来源模式',
    noModel: '无需 AI 模型即可搜索。',
    connect: '连接本地模型',
    askTitle: '使用本地模型解释',
    question: '关于这些来源，您有什么问题？',
    mode: '模式',
    general: '日常任务',
    school: '中小学',
    university: '大学',
    ask: '解释',
    start: '从一个小想法开始',
    samples: '内置学习示例',
    sample1: '理解分数',
    sample1sub: '一个观点，一个确切来源。',
    sample2: '规划研究项目',
    sample2sub: '从提出问题到核查结论。',
    sample3: '三种语言，一个资料库',
    sample3sub: 'Русский, English, 中文。',
    results: '在您的来源中找到',
    noResults: '没有匹配结果。请减少搜索词或添加来源。我们不会编造答案。',
    draft: '模型草稿 · 请核查引用',
    foot: '先有来源，再下结论。',
    helpTitle: '本地模型',
    helpBody: '请提前下载 llama.cpp 和兼容的 GGUF 模型，使用本地路径重新启动：',
    helpNote: '不会自动下载任何内容。生成属于实验功能，请核查质量和引用。无需模型也能使用搜索和资料库。',
    working: '处理中…',
    thinking: '模型正在起草，可能需要最多 3 分钟…',
    saved: '新增文档：',
    removed: '文档已删除。',
    copy: '复制',
    copied: '引用已复制。',
    line: '行',
    delete: '删除',
    confirmDelete: '删除此文档？如果仍需要，请先下载备份。',
    restoreConfirm: '从备份合并文档？现有文本将保留。',
    error: '操作未完成。请检查文件、大小限制及应用是否在运行。',
    file_size: '文件超过 1 MiB。',
    file_encoding: '需要有效的 UTF-8 文本。',
    file_name: '请使用不含路径的 TXT/MD 文件名。',
    checksum: '校验和不匹配，未导入备份。',
    backup_format: '不支持此备份格式。',
    library_limit: '上限：200 个文档 / 50 MiB。',
    document_count: '每次最多导入 200 个文档。',
    request_size: '请求过大。请分批导入（JSON 最多 8 MiB）。',
    session: '会话已更改，请刷新页面。',
    busy: '模型正在忙，请稍后重试。',
    modelReady: '模型已配置',
    modelHint: '本地生成 · 实验功能',
    backupDone: '已下载备份，请保存在代码库之外。',
    fraction: '分数',
    project: '学习',
    all: '1/2'
  }
};
strings.ru.missing_citations = 'Модель не указала ссылки. Сверьте ответ с цитатами выше.';
strings.ru.invalid_citations = 'Модель указала несуществующие ссылки. Ответ требует проверки.';
strings.en.missing_citations = 'The model omitted citations. Check its answer against the quotes above.';
strings.en.invalid_citations = 'The model cited missing sources. Verify this answer.';
strings.zh.missing_citations = '模型未提供引用，请对照上方原文核查。';
strings.zh.invalid_citations = '模型引用了不存在的来源，请核查回答。';
let lang = 'ru',
  state = {
    documents: [],
    model: false
  },
  lastResults = [],
  busy = false;
const t = k => strings[lang][k] || strings[lang].error;
const el = (tag, text, cls) => {
  const n = document.createElement(tag);
  n.textContent = text;
  if (cls) n.className = cls;
  return n;
};

function message(text, error = false) {
  $('status').textContent = text;
  $('status').className = error ? 'error' : '';
}
async function api(path, data = {}) {
  const response = await fetch('/api/' + path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Local-Token': token
    },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error);
  return result;
}
async function run(action, thinking = false) {
  if (busy) return;
  busy = true;
  document.querySelectorAll('button').forEach(b => b.disabled = true);
  $('main').setAttribute('aria-busy', 'true');
  message(t(thinking ? 'thinking' : 'working'));
  try {
    await action();
  } catch (e) {
    message(t(e.message), true);
  } finally {
    busy = false;
    document.querySelectorAll('button').forEach(b => b.disabled = false);
    $('main').setAttribute('aria-busy', 'false');
  }
}

function translate() {
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-t]').forEach(n => {
    const text = t(n.dataset.t);
    n.textContent = text;
    if (n.tagName === 'H1') {
      n.replaceChildren(...text.split('\n').flatMap((s, i) => i ? [document.createElement('br'), document.createTextNode(s)] : [document.createTextNode(s)]));
    }
  });
  document.querySelectorAll('[data-placeholder]').forEach(n => n.placeholder = t(n.dataset.placeholder));
  renderLibrary();
  renderResults(lastResults);
}

function renderLibrary() {
  const list = $('documents');
  list.replaceChildren();
  $('count').textContent = state.documents.length;
  $('emptyLibrary').hidden = state.documents.length > 0;
  for (const doc of state.documents) {
    const li = el('li', '');
    const open = el('button', doc.name, 'doc-open');
    open.append(el('small', (doc.size / 1024).toFixed(1) + ' KiB'));
    open.onclick = () => run(() => openDocument(doc.id));
    const del = el('button', '×', 'delete');
    del.setAttribute('aria-label', t('delete') + ': ' + doc.name);
    del.onclick = () => run(async () => {
      if (!confirm(t('confirmDelete') + '\n' + doc.name)) {
        message('');
        return;
      }
      await api('delete', {
        id: doc.id
      });
      await refresh();
      lastResults = [];
      renderResults([]);
      $('answerCard').hidden = true;
      message(t('removed'));
    });
    li.append(open, del);
    list.append(li);
  }
  $('modelStatus').textContent = t(state.model ? 'modelReady' : 'sourceMode');
  $('modelHint').textContent = t(state.model ? 'modelHint' : 'noModel');
  $('modelHelp').hidden = state.model;
  $('askPanel').hidden = !state.model;
}
async function refresh() {
  state = await api('state');
  renderLibrary();
}
async function openDocument(id) {
  const {
    document: doc
  } = await api('document', {
    id
  });
  if (!doc) throw new Error('error');
  $('documentName').textContent = doc.name;
  $('documentHash').textContent = 'SHA-256: ' + doc.id;
  $('documentText').textContent = doc.text.split(/\r\n|\n|\r/).map((line, i) => (i + 1) + '  ' + line).join('\n');
  $('documentDialog').showModal();
  message('');
}

function renderResults(results) {
  $('results').replaceChildren();
  $('resultCount').textContent = results.length + (results.length === 20 ? ' / max 20' : '');
  $('noResults').hidden = results.length > 0;
  results.forEach((source, i) => {
    const card = el('article', '', 'result'),
      head = el('div', '', 'result-head');
    const link = el('button', `[${i+1}] ${source.name} · ${t('line')} ${source.line}`, 'source-link');
    link.onclick = () => run(() => openDocument(source.id));
    const copy = el('button', t('copy'), 'copy');
    copy.onclick = () => run(async () => {
      await navigator.clipboard.writeText(`${source.quote}\n[${source.name}:${source.line}; SHA-256: ${source.id}]`);
      message(t('copied'));
    });
    head.append(link, copy);
    card.append(head, el('blockquote', source.quote), el('p', 'SHA-256: ' + source.id, 'hash'));
    $('results').append(card);
  });
}
async function search() {
  const result = await api('search', {
    query: $('query').value
  });
  lastResults = result.sources;
  renderResults(lastResults);
  $('resultsArea').hidden = false;
  $('welcome').hidden = true;
  $('answerCard').hidden = true;
  message('');
}
$('searchForm').onsubmit = event => {
  event.preventDefault();
  run(search);
};
$('lang').onchange = () => {
  lang = $('lang').value;
  translate();
  message('');
};
$('import').onclick = () => $('files').click();
$('files').onchange = () => {
  const files = [...$('files').files];
  $('files').value = '';
  if (!files.length) return;
  run(async () => {
    if (files.length > 200) throw new Error('document_count');
    const documents = [];
    for (const file of files) {
      if (file.size > 1048576) throw new Error('file_size');
      let text;
      try {
        text = new TextDecoder('utf-8', {
          fatal: true,
          ignoreBOM: true
        }).decode(await file.arrayBuffer());
      } catch {
        throw new Error('file_encoding');
      }
      documents.push({
        name: file.name,
        text
      });
    }
    const result = await api('import', {
      documents
    });
    await refresh();
    message(t('saved') + result.added);
  });
};
$('backup').onclick = () => run(async () => {
  const data = await api('backup');
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], {
    type: 'application/json'
  }));
  const a = el('a', '');
  a.href = url;
  a.download = 'nemukhina-library.json';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
  message(t('backupDone'));
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
    } catch {
      throw new Error('backup_format');
    }
    if (!confirm(t('restoreConfirm'))) {
      message('');
      return;
    }
    const result = await api('restore', {
      backup
    });
    await refresh();
    message(t('saved') + result.added);
  });
};
document.querySelectorAll('[data-sample]').forEach(button => button.onclick = () => run(async () => {
  await api('demo');
  await refresh();
  $('query').value = t(button.dataset.sample);
  await search();
}));
$('ask').onclick = () => run(async () => {
  const result = await api('ask', {
    query: $('query').value,
    question: $('question').value,
    mode: $('mode').value,
    lang
  });
  lastResults = result.sources;
  renderResults(lastResults);
  $('resultsArea').hidden = false;
  $('welcome').hidden = true;
  $('answer').textContent = result.answer || '';
  $('answerCard').hidden = !result.answer;
  message(result.warning ? t(result.warning) : '', Boolean(result.warning));
}, true);
$('modelHelp').onclick = () => $('helpDialog').showModal();
$('closeHelp').onclick = () => $('helpDialog').close();
$('closeDocument').onclick = () => $('documentDialog').close();
translate();
run(async () => {
  await refresh();
  message('');
});
