# Как опубликовать Research First Builder на GitHub

Инструкция подготовлена 1 октября 2026 года.
Будущий репозиторий: **IT-Shelter-Labs/research-first-builder**.
Выбранный автор коммитов: [melroncod](https://github.com/melroncod).

Локальные коммиты уже созданы. Для этого репозитория настроен GitHub noreply-адрес автора,
поэтому личный почтовый адрес не попадает в коммиты. Владельцем репозитория будет организация IT-Shelter-Labs.
Пользователь уже отправил исходники на GitHub. Для публичного open-source запуска проверьте,
что у репозитория стоит видимость **Public**; отправка исходников сама по себе этого не гарантирует.

## Что готово

Реализация, локальные проверки, реальные примеры, документация и демо готовы для предварительного
релиза **0.1.0-rc1**. [Полный тест в приложении](acceptance/DESKTOP_BOOKMARKS.md) прошёл через прямое
чтение файла скилла. Перед стабильным релизом остаются проверка вызова через встроенный список скиллов
в папке целевого проекта и успешный запуск проверок GitHub Actions.

Полный нативный тест Claude Code и сравнительный эксперимент ещё не выполнены.
[Подробный статус готовности](RELEASE_STATUS.md).

## Вариант 1: через GitHub Desktop

Этот способ позволяет опубликовать готовый локальный репозиторий через интерфейс.
Названия кнопок ниже оставлены на английском, чтобы их было проще найти в приложении.

1. Войдите в GitHub Desktop под аккаунтом, которому разрешено создавать репозитории в **IT-Shelter-Labs**.
2. Выберите **File → Add local repository** и укажите папку самого продукта `research-first-builder`.
   Не выбирайте родительскую папку Content OS или GitHubRepoDev.
3. Просмотрите локальные коммиты и список файлов. Архивы и временные файлы исключены из Git.
4. Нажмите **Publish repository**. Укажите:
   - **Name:** `research-first-builder`.
   - **Organization:** `IT-Shelter-Labs`.
   - **Description:** `Make your coding agent justify architecture with real sources before it builds.`
5. Для публичного open-source репозитория снимите галочку **Keep this code private**.
   При желании сначала проверить GitHub Actions без публичного запуска можно оставить репозиторий приватным.
6. Нажмите **Publish repository** и откройте опубликованный репозиторий на GitHub.
7. Перейдите во вкладку **Actions** и дождитесь завершения проверок Windows, Linux и форматирования.
   Если есть ошибки, исправьте их до объявления успешного релиза.

Если организации нет в списке, проверьте выбранный аккаунт и его право создавать репозитории в организации.

Официальные инструкции GitHub: [добавление локального репозитория](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-a-repository-from-your-local-computer-to-github-desktop),
[публикация существующего проекта](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop).

## Вариант 2: через сайт GitHub и Git

На сайте GitHub создайте **пустой** репозиторий:

- **Owner:** `IT-Shelter-Labs`.
- **Repository name:** `research-first-builder`.
- **Visibility:** `Public` для публичного запуска.
- Не добавляйте README, лицензию и .gitignore при создании: они уже есть в локальном проекте.

Откройте PowerShell в папке `research-first-builder`. После обычной авторизации Git выполните:

```powershell
git remote add origin https://github.com/IT-Shelter-Labs/research-first-builder.git
git push -u origin main
```

Команды рассчитаны на уже созданные локальные коммиты и отсутствие подключённого `origin`.
Если Git сообщает, что `origin` уже существует, сначала проверьте его адрес командой `git remote -v`.
Не заменяйте адрес автоматически. Принудительная отправка `--force` здесь не нужна.

Отправляйте только репозиторий продукта. Весь Content OS и ZIP-архив в качестве исходного репозитория
загружать не нужно. После отправки проверьте вкладку **Actions**.
[Официальная инструкция для существующего кода](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github?platform=windows).

## Что сделать после публикации

1. Добавьте темы репозитория: `ai`, `coding-agents`, `agent-skills`, `claude-code`, `codex`,
   `developer-tools`, `software-architecture`, `research`, `open-source`.
2. В настройках включите приватную отправку сообщений об уязвимостях и обновите SECURITY.md,
   указав реально доступный способ связи.
3. В README уже добавлены ссылки на GitHub, Telegram IT Shelter и фактические результаты Actions.
4. Проверьте установку из GitHub в новом чистом проекте, прежде чем рекомендовать эту команду пользователям:

```text
npx skills@1.7.0 add IT-Shelter-Labs/research-first-builder --skill research-first-build --agent codex --copy
```

5. Создайте черновик релиза:
   - **Tag:** `v0.1.0-rc1`.
   - **Target:** `main`.
   - **Title:** `Research First Builder 0.1.0-rc1`.
   - **Description:** содержимое [подготовленных release notes](RELEASE_NOTES_0.1.0_RC1.md).
   - Отметьте **This is a pre-release** — это предварительный релиз.
6. Прикрепите из папки `dist` два ZIP-архива и файл `SHA256SUMS.txt`, затем опубликуйте релиз.
   Если включены неизменяемые релизы, добавьте все вложения до публикации черновика.

[Официальная инструкция по релизам](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## Что нужно предоставить

Организация, профиль автора и результаты теста в приложении уже получены и проверены.
Адрес репозитория уже известен. Остаётся проверить доступ без авторизации, результаты GitHub Actions
и установку скилла из GitHub в чистом проекте.

Для самой публикации нужен обычный доступ к GitHub с правом записи в организацию.
Ссылка на профиль сама по себе такого доступа не даёт.

Фотографии, дополнительные скриншоты и новый дизайн не обязательны: в репозитории уже есть оригинальное демо GIF.
Существующий логотип IT Shelter и ссылка на бренд пригодятся для дополнительного оформления.
Скриншот нужен только при непонятной ошибке интерфейса. Пароли, токены и коды восстановления в чат отправлять не нужно.
