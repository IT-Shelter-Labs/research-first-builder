# Research First Builder

**Скилл, который помогает coding agent обосновать архитектуру реальными источниками до разработки.**

Don't build from vibes. Build from evidence.

Проект [IT Shelter](https://github.com/IT-Shelter-Labs). Один переносимый скилл и небольшой Python helper
без сторонних библиотек, серверов и аккаунта RFB.
Канал IT Shelter в [Telegram](https://t.me/+ihTcvubt-_BhZTQ6).

Агент изучает подходящие аналоги, фиксирует доказательства, принимает **ADOPT / REJECT / DEFER** решения,
создаёт минимальный план, реализует его и сохраняет реальные результаты проверок.
Простое решение **NO-PATTERN** допустимо. Популярность репозитория не доказывает пригодность его архитектуры.

**Версия 0.1.0 — release candidate.** Локальные проверки, примеры и [полный тест в приложении](docs/acceptance/DESKTOP_BOOKMARKS.md)
пройдены. Последний использовал прямое чтение скилла; вызов через встроенный список и сравнительный эксперимент ещё не подтверждены.
[Точный статус](docs/COMPATIBILITY.md) · [Полная документация на английском](README.md).

## Установка в приложение

Скопируйте всю папку `skills/research-first-build` в проект, с которым работает агент:

- Codex в приложении: `.agents/skills/research-first-build`.
- Claude Code: `.claude/skills/research-first-build`.
- Cursor/OpenCode: `.agents/skills/research-first-build`, пока beta.

Отдельный Codex CLI для этого не нужен. Откройте именно папку целевого проекта с `.agents/skills` в локальном режиме работы с кодом,
выберите скилл или вызовите `$research-first-build`. Если он не появился, перезапустите сессию/приложение.
Для выполнения проверок нужен Python 3.11+, для исследования — доступ агента к источникам и файлам.
Обычный чат без доступа к локальному проекту не сможет выполнить этот workflow.

Можно начать без установки, явно указав агенту путь к `skills/research-first-build/SKILL.md` и попросив прочитать
его и нужные ссылки. Это проверяет работу инструкций, но не нативное обнаружение установленного скилла.

## Первый запрос

```text
$research-first-build Исследуй аналоги локального webhook inbox и реализуй
минимальный вариант для одного процесса. Сначала реальные источники,
потом доказательства, решения Adopt/Reject, план, код и проверки.
Артефакты сохраняй в docs/research-first/inbox.
```

Для исследования без кода добавьте: `research-only, quick depth; реализацию пока не начинай`.

Результат: `RESEARCH.md`, `PLAN.md`, `VERIFICATION.md`, `evidence.json`, заметки источников и реальные
выводы проверок. Helper проверяет связи, полноту записей и актуальность предоставленных snapshots.
Он не доказывает истинность источников и не запускает команды из JSON.

## Примеры и проверка

[Три работающих примера и отдельный research-only запуск](examples/README.md).
Все примеры учебные, с явно ограниченным scope.

Из корня репозитория:

```text
python -m unittest discover -s tests -v
python tools/verify_examples.py
python tools/check_repository.py
```

Исходники опубликованы на [GitHub](https://github.com/IT-Shelter-Labs/research-first-builder).
Фактические результаты автоматических проверок смотрите в [GitHub Actions](https://github.com/IT-Shelter-Labs/research-first-builder/actions/workflows/check.yml).
MIT покрывает наш оригинальный код и материалы. Лицензии изученных проектов записаны отдельно;
их код не переносился. [Установка](docs/QUICKSTART.md) · [Ограничения](docs/CONTRACT.md).
