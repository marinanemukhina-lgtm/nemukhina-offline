# Дизайн: от референсов к работающему продукту

Проверено 10 ноября 2026. Главная задача — дать человеку начать любой разговор с локальным ИИ, а затем продолжить работу с ответом. Обучение, тексты, идеи, код и планирование — примеры применения, а не ограничения аудитории.

## Проверенные референсы

| Референс | Подтверждённое отличие | Что применено |
| --- | --- | --- |
| [Superlist](https://www.awwwards.com/sites/superlist) | Site of the Day, 19.04.2021; [Site of the Month, апрель 2021](https://www.awwwards.com/superlist.html) | Большой типографический жест, один связный образ, визуальная уверенность вместо перечня функций. Просмотрена сохранённая [награждённая версия](https://superlist.craftedbygc.com/). |
| [Fourmula AI](https://www.awwwards.com/sites/fourmula-ai) | Site of the Day, 02.05.2026 | Действие на первом экране и объяснение возможностей через результат. Просмотрены [живой сайт](https://fourmula.ai/) и его секция рабочего процесса. |
| [Reflect](https://www.awwwards.com/sites/reflect) | Honorable Mention, 11.05.2023; это не Site of the Day | Ясная подача личного инструмента для мыслей и видимый следующий шаг. Просмотрен [нынешний сайт](https://reflect.app/); его содержание уже отличается от версии 2023 года. |

Это преимущественно сайты представления продуктов. Их выразительность перенесена на вход в приложение; рабочее пространство строится вокруг вопроса, истории и результата. Награды принадлежат перечисленным сайтам, не Nemukhina Offline. Чужие код, логотипы, фотографии и иллюстрации не включены.

## Реализация

- Первый экран: крупная фраза «ИИ без интернета. Для ваших задач.», один работающий ввод и три необязательные подсказки. Материалы не нужны для начала обычного разговора.
- После ответа: тёмная область переписки и светлая область результата с копированием и Markdown-экспортом. На телефоне результат появляется ниже, переход к нему прокручивает страницу.
- Образ раскрывающейся бумаги связывает свободную мысль с осязаемым результатом. Это самостоятельный растровый актив, не изображение всего интерфейса: текст, формы и кнопки остаются настоящими HTML-элементами.
- Lora используется для крупных заголовков, системный sans-serif — для ввода и длинных ответов. Кремовый `#faf7f2`, графитовый `#232329`, коралловый `#f46550`.
- Короткое появление иллюстрации и результата; нет непрерывной фоновой анимации, перехвата скролла, тяжёлого WebGL или загрузочного спектакля. `prefers-reduced-motion` отключает движение.
- Шрифт, иконки, иллюстрация и скрипты загружаются локально. Переходы на внешние страницы происходят только по нажатию ссылки.

[Реальный первый экран](images/assistant.jpg) · [Результат](images/result.jpg) · [Телефон](images/mobile.jpg) · [Визуальная проверка](../design-qa.md)

## Происхождение активов

`web/assets/possibility.png` создан встроенным Imagegen по новой композиции. Финальный промпт:

> Use case: precise-object-edit / production web illustration. Reference is the approved-direction UI concept. Produce ONLY its right-hand sculptural artwork as a standalone high-quality portrait asset, no UI, no text, no letters, no logos, no borders. Reconstruct the tactile coral-red continuous paper ribbon unfolding into a fan of ivory pages, same character, elegant large curving surface, fine visible paper texture and warm light. Charcoal studio backdrop EXACT #232329 with very subtle natural shadows. Portrait 1024x1536. The sculpture fills the top 75% and enters from the top edge and lower-left; bottom 25% is plain charcoal negative space to place real HTML text later. Keep page fan centered at x55% y35%, same dramatic angled fan, detailed beautiful sculptural ribbons. No extra objects, no book cover, no type anywhere. This is an asset extraction/reconstruction for the real webpage.

Референсом для актива был [сгенерированный макет](images/design-reference.png). При подготовке макета Imagegen получил снимки Superlist и Fourmula как композиционные ориентиры, предыдущую выбранную концепцию и широкое описание назначения приложения. Наличие этих референсов не означает использование их иллюстраций в поставляемом продукте.

Lora — [Google Fonts](https://github.com/google/fonts/tree/main/ofl/lora), SIL OFL. Tabler — MIT; закреплённая ревизия указана в `web/assets/SOURCES.md`, лицензия — в `web/assets/icons/LICENSE`. В готовом интерфейсе нет шрифтов или библиотек с CDN.
