# hide_icons — скрыть значки домашнего экрана PS4

Домашний экран показывает по плитке на каждую строку `tbl_appbrowse_<user>` с
`visible = 1`. Сама консоль прячет ненужные плитки (Music Unlimited, PlayStation Video,
ТВ и видео, USB-плеер, Share Play, PS5 Remote Play ...) именно так: в app.db они лежат
с `visible = 0`. Скрипт выставляет тот же флаг для указанных title id — и наоборот,
возвращает значки ключом `--show`.

По умолчанию (ответ `default` в меню, а также запуск без терминала) скрываются:

| titleId | значок |
|--|--|
| `NPXS20979` | PlayStation Store |
| `NPXS20108` | Что нового? |
| `NPXS20105` | Прямой эфир с PlayStation |
| `NPXS20104` | Галерея снимков и клипов |
| `CUSA00001` | THE PLAYROOM |

## Как выбрать, что скрывать

Запустите `run_hide.bat` (он берёт `hide_icons.exe` из этой же папки) или вручную
`hide_icons.exe 192.0.2.10 --pick` — скрипт скачает
app.db, покажет **все** значки домашнего экрана с номерами и спросит, что скрыть:

```
tbl_appbrowse tables: tbl_appbrowse_0473217505, tbl_appbrowse_0473217511, tbl_appbrowse_0473217512, tbl_appbrowse_0473217513
profiles: 0473217505 0473217511 0473217512 0473217513   (--profile <suffix>, 'all' = every user)
for which user should the icons be changed?
  1    0473217505   (default)
  2    0473217511
  3    0473217512
  4    0473217513
  numbers (1 3), a range (1-2), profile tails, 'all' = every user
  Enter = 1, i.e. only the first profile (0473217505)
> 1
editing profile(s): 0473217505
desktop icons -- visible is shown per table (0473217505):
  #    titleId    visible        titleName
  1    NPXS20979  1              PlayStation Store  *
  2    NPXS20108  1              Что нового?  *
  3    NPXS20105  1              Прямой эфир с PlayStation  *
  4    NPXS20104  1              Галерея снимков и клипов  *
  5    NPXS20102  1              Интернет-браузер
  6    NPXS20106  0              Music Unlimited
  7    CUSA00102  1              Demo game, external
  ...

  * = part of the default list NPXS20979,NPXS20108,NPXS20105,NPXS20104,CUSA00001
what to hide?  numbers (1 3 5), a range (3-6), title ids, 'all', 'default'
             Enter = cancel
>
```

Что можно ввести вместо `>`:

| ответ | что будет скрыто |
|--|--|
| `1,5,7` | значки 1, 5 и 7 из списка (номера через запятую — как они показаны) |
| `3-6` | все номера из диапазона |
| `NPXS20102` | конкретный title id (можно смешивать с номерами: `1 NPXS20102`) |
| `all` | все значки из списка |
| `default` | стандартный набор из таблицы выше (только те значки, что есть в этой базе) |
| Enter | отмена — база не меняется, ничего не загружается |

Перед этим задаётся вопрос о пользователе (если в `--profile` не указано иное), его ответы:

| ответ | кого затронет |
|--|--|
| `1`, `2`, `3`, `4` | профиль с этим номером из списка |
| `1 2` / `1,2` | несколько номеров сразу |
| `1-2` | диапазон номеров |
| `0473217505` | суффикс таблицы (подойдёт и однозначный «хвост», например `512`) |
| `all` | все пользователи консоли |
| Enter | первый профиль из списка (вариант по умолчанию) |

Дальше скрипт печатает `icons to be hidden (visible -> 0): ...`, по каждой таблице
показывает `visible 1 -> 0` и (с `--apply`) спрашивает подтверждение перед загрузкой.
`run_show.bat` (или `--show --pick`) делает то же самое в обратную сторону: `visible = 1`,
в вопросе будет `what to show?`.

## Что нужно

* Windows. Готовая сборка `hide_icons.exe` — Python на компьютере не нужен, рядом с ней
  создаётся только рабочая папка `tmp\`. Архив распаковывайте целиком: `hide_icons.exe`,
  `fix_db.exe` и `run_*.bat` должны лежать в одной папке. `fix_db.exe` — та же сборка
  отдельной программой: ею удобно залить готовую базу (см. `--offline` ниже).
* На PS4 запущен GoldHEN с FTP (порт 2121, логин/пароль по умолчанию
  `username` / `password`).

## Как пользоваться

Двойной щелчок по `run_hide.bat` — выбрать и скрыть значки (`visible = 0`),
`run_show.bat` — выбрать и вернуть их обратно, `run_list.bat` — только посмотреть
список. Все три спросят IP консоли (в примерах ниже он заменён на условный
`192.0.2.10`) и запустят `hide_icons.exe` из этой же папки.

Вручную:

```
hide_icons.exe 192.0.2.10 --list                             # только список значков
hide_icons.exe 192.0.2.10 --pick                             # список + выбор, ничего не пишется
hide_icons.exe 192.0.2.10 --pick --apply                     # список + выбор + загрузка
hide_icons.exe 192.0.2.10 --titles NPXS20102 --apply          # без меню: скрыть браузер
hide_icons.exe 192.0.2.10 --show --titles NPXS20102 --apply   # без меню: вернуть браузер
hide_icons.exe 192.0.2.10 --apply                             # без терминала: стандартный набор, первый профиль
hide_icons.exe 192.0.2.10 --profile all --apply                # все пользователи консоли, без вопросов
hide_icons.exe --offline --db tmp/app.db --pick               # выбор по локальной копии базы
```

После `--apply`: **выйдите из пользователя PS4 или перезагрузите консоль** — только тогда
система перечитает app.db. Перед загрузкой скрипт спрашивает подтверждение (`--yes` —
не спрашивать), сверяет md5 загруженного файла и делает копию исходной базы в
`tmp\backup\`.

Если IP неверный или консоль недоступна, вместо простыни трассировки печатается одна
строка и код возврата 1:

```
cannot connect to PS4 at 192.0.2.10:2121 -- [WinError 10061] соединение не установлено
  check that the IP is right and that GoldHEN runs its FTP server on this port
  (if the login was changed, pass --user/--password)
```

## Только один пользователь (`--profile`)

У каждого пользователя консоли в app.db своя таблица `tbl_appbrowse_<суффикс>`, и список этих
суффиксов программа печатает сама (см. вывод выше). Если `--profile` не указан, программа
спрашивает, для кого править базу, и **по умолчанию (просто Enter) берёт первый профиль из
списка**; при запуске без терминала (вывод перенаправлен, планировщик задач) вопросов нет —
тоже первый профиль. Остальные пользователи продолжают видеть значки как раньше, в `--list`
у колонки `visible` остаётся один столбец.

```
hide_icons.exe 192.0.2.10 --list --profile 0473217505
hide_icons.exe 192.0.2.10 --profile 0473217505 --titles NPXS20102 --apply --yes
hide_icons.exe 192.0.2.10 --profile 0473217505,0473217513 --pick --apply
run_hide.bat 192.0.2.10 0473217505
```

Что можно указать в `--profile`:

| значение | что будет изменено |
|--|--|
| `0473217505` | полный суффикс таблицы `tbl_appbrowse_<суффикс>` |
| `512` | однозначный «хвост» суффикса, если он подходит только одной таблице |
| `tbl_appbrowse_0473217505` | имя таблицы целиком |
| `0473217505,0473217513` | несколько профилей (через запятую или пробел) |
| `all` / `*` | все таблицы, то есть все пользователи консоли |

Если подходящей таблицы нет, скрипт перечисляет найденные суффиксы и выходит с кодом 1:

```
no tbl_appbrowse table matches '999', found: 0473217505, 0473217511, 0473217512, 0473217513
```

Имён пользователей в базе нет — профиль это только суффикс таблицы. Найти нужный проще всего
так: скройте значок для одного профиля, выйдите из пользователя и посмотрите, у кого значок
пропал. Если профиль ещё ни разу не входил на этой прошивке, своей таблицы у него может не
быть: система создаст её позже, и тогда значок у него останется видимым — скройте его ещё раз.

## Мелочи, которые стоит знать

* Изменяется **только** колонка `visible` в таблицах `tbl_appbrowse_*` (в 13.02 их четыре —
  по одной на пользователя/профиль; по умолчанию правится первый профиль, другой выбирается
  ответом на вопрос или ключом `--profile`). Остальные строки базы остаются как есть.
* Список значков берётся из скачанной app.db, поэтому в нём видно и то, что консоль
  прячет сама: такие значки уже имеют `visible=0`. Звёздочка `*` отмечает значки из
  стандартного набора (ответ `default`).
* Игра не удаляется и не отключается: вернуть значок можно в любой момент тем же
  списком (`--show --pick`) или без меню — `--titles <ID> --show --apply`.
* `--titles NPXS20102,NPXS20104` вообще не показывает меню: удобно для .bat-скриптов
  и повторных запусков. Если запустить без `--titles`, когда ввода нет (вывод
  перенаправлен в файл, запуск из планировщика), скрипт молча берёт стандартный набор.
* Меню (`--pick`) работает и в `--offline`-режиме: список строится по локальной копии.
  Ответ с опечаткой (например `x`) скрипт не примет: скажет `could not understand ...`
  и спросит снова; пустой Enter — отмена, база не меняется.
* `run_list.bat` показывает значение `visible` по каждой таблице: если числа разные,
  значит база правилась вручную или для разных профилей.
* `--offline --apply` ничего не загружает на консоль (FTP не используется вообще):
  изменённая база остаётся в `tmp\app.db`, в отчёте будет
  `offline mode, nothing was uploaded`. Залить её можно общим модулем:
  `fix_db.exe PS4_IP --db tmp\app.db --apply --yes`.
* Если база повреждена или что-то пошло не так — верните app.db из `tmp\backup\`:
  `fix_db.exe --restore tmp\backup\app.db.ГГГГММДД-ЧЧММСС --apply --yes`
  (`tmp\app.db.orig` — копия того файла, который скачал этот скрипт).

## Файлы

```
hide_icons.exe    готовая сборка скрывателя: run_*.bat запускают её с нужным ключом,
                  Python на компьютере не требуется
fix_db.exe        та же сборка отдельной программой: залить готовую базу
                  (fix_db.exe PS4_IP --db tmp\app.db --apply --yes), вернуть бэкап
run_list.bat      список значков (ничего не пишется на консоль)
run_hide.bat      список + выбор значков, скрыть их (visible = 0)
run_show.bat      список + выбор значков, вернуть их (visible = 1)
README.md         этот файл
LICENSE           лицензия MIT
tmp\              создаётся при первом запуске: app.db, app.db.orig, backup\, отчёты

hide_icons.py     исходник скрывателя: меню --pick, выбор профиля, visible = 0/1
fix_db.py         движок (FTP, param.sfo, запись строк) — тот же, что в PS4_db_rebuilder
appinfo.py        псевдо-app.info для tbl_appinfo
sfo\              библиотека разбора param.sfo (MIT, Copyright (c) 2016 cologler)
build_exe.bat     пересобрать hide_icons.exe (PyInstaller)
make_dist.bat     собрать архив релиза в dist\ и обновить SHA256SUMS.txt
make_dist.ps1     то, что вызывает make_dist.bat
SHA256SUMS.txt    хэши hide_icons.exe и fix_db.exe
```

Репозиторий называется **PS4_hide_icons**. Движок `fix_db.py` и вспомогательная сборка
`fix_db.exe` — из соседнего репозитория **PS4_db_rebuilder** (там же основная программа
регистрации игр в `app.db`). Если движок менялся, обновите `fix_db.py`, `appinfo.py`,
`sfo\` и `fix_db.exe` в обоих репозиториях и пересоберите `hide_icons.exe` (`build_exe.bat`).

## Сборка exe из исходников

Нужен Python 3.8+ и PyInstaller:

```
python -m pip install pyinstaller
build_exe.bat
```

Скрипт собирает `hide_icons.exe` рядом с исходниками (`pyinstaller --onefile --console
--clean`), служебная папка `build\` в git не попадает. Запуск без сборки:
`python hide_icons.py 192.0.2.10 --pick`.

Архив для раздела Releases собирается отдельно:

```
make_dist.bat   -> dist\hide_icons.zip, dist\SHA256SUMS.txt
```

## Проверка хэшей

```
certutil -hashfile hide_icons.exe SHA256
```

Сверьте результат с `SHA256SUMS.txt`. exe собран PyInstaller и не подписан, поэтому
SmartScreen может показать «Windows защитила ваш компьютер»: «Подробнее» → «Выполнить
в любом случае».

---

## English

The home screen shows one tile per row of `tbl_appbrowse_<user>` with `visible = 1`. The console
itself hides unwanted tiles (Music Unlimited, PlayStation Video, TV & Video, USB player, Share
Play, PS5 Remote Play ...) exactly the same way: those rows have `visible = 0` in app.db. The
script sets the same flag for the title ids you choose, and `--show` brings the icons back.

The default list (answer `default` in the menu, or a run without a terminal) is `NPXS20979`
PlayStation Store, `NPXS20108` What's New, `NPXS20105` Live from PlayStation, `NPXS20104`
Capture Gallery, `CUSA00001` THE PLAYROOM.

### Requirements

* Windows. The prebuilt `hide_icons.exe` needs no Python; only a `tmp\` folder is created next to
  it. Unpack the whole archive: `hide_icons.exe`, `fix_db.exe` and the `run_*.bat` files must stay
  in one folder. `fix_db.exe` is the same engine as a separate program: use it to upload a
  prepared database (see `--offline` below).
* GoldHEN with its FTP server on the PS4 (port 2121, default login `username` / `password`).

### Usage

Double click `run_hide.bat` to pick and hide icons (`visible = 0`), `run_show.bat` to bring them
back, `run_list.bat` to only list them. All three ask for the IP of the console (the examples use
`192.0.2.10`) and start `hide_icons.exe` from the same folder. `run_hide.bat` and `run_show.bat`
then ask which user to edit (Enter = the first profile); an optional second argument is a profile
suffix and skips that question.

```
hide_icons.exe 192.0.2.10 --list                             # list only
hide_icons.exe 192.0.2.10 --pick                             # list + pick, nothing is written
hide_icons.exe 192.0.2.10 --pick --apply                     # list + pick + upload
hide_icons.exe 192.0.2.10 --titles NPXS20102 --apply          # no menu: hide the browser
hide_icons.exe 192.0.2.10 --show --titles NPXS20102 --apply   # no menu: bring it back
hide_icons.exe 192.0.2.10 --apply                             # no terminal: the default list, first profile
hide_icons.exe 192.0.2.10 --profile all --apply                # every user, no questions
hide_icons.exe --offline --db tmp/app.db --pick               # pick on a local copy of app.db
```

What you can type instead of `>`: `1,5,7` (numbers from the list), `3-6` (a range), `NPXS20102`
(a title id, mixed with numbers works too), `all`, `default` (the list above), or Enter to cancel.
The question about the user comes first (unless `--profile` is given); it takes a number (`2`),
several numbers (`1 3`), a range (`1-2`), a profile suffix (`0473217505`, a unique tail such as
`512` works too), `all` for every user, or Enter for the first profile of the list.

After `--apply` **log the PS4 user out or reboot the console**, otherwise PS4 keeps the old copy
of app.db in memory. Before uploading, the script asks for confirmation (`--yes` skips it),
compares the md5 of the uploaded file and keeps a copy of the original database in `tmp\backup\`.

### A single user (`--profile`)

Every user of the console has its own table `tbl_appbrowse_<suffix>` and the program prints the
list of suffixes when it starts (`profiles: 0473217505 0473217511 0473217512 0473217513`).
Without `--profile` it asks which user to edit and **Enter takes the first profile of the list**;
when there is no terminal (output redirected, started from the task scheduler) there is no
question either — the first profile is used. The other users keep their icons, and the `visible`
column of `--list` shows a single value.

```
hide_icons.exe 192.0.2.10 --list --profile 0473217505
hide_icons.exe 192.0.2.10 --profile 0473217505 --titles NPXS20102 --apply --yes
hide_icons.exe 192.0.2.10 --profile 0473217505,0473217513 --pick --apply
run_hide.bat 192.0.2.10 0473217505
```

`--profile` accepts the full suffix (`0473217505`), a unique tail (`512`), the whole table name
(`tbl_appbrowse_0473217505`), a comma separated list, or `all` / `*` for every user of the
console. An unknown value prints the suffixes that were found and exits with code 1. app.db stores
no user names, only these suffixes: hide one icon for one profile, log out and see which user
lost it. A profile that never logged in on this firmware may not have its table yet; PS4 creates
it later, so hide the icon again when that table appears.

### Notes

* Only the `visible` column of the `tbl_appbrowse_*` tables is changed (app.db of 13.02 has four of
  them, one per user/profile; the first profile is edited by default, another one is chosen by
  answering the question or with `--profile`).
* The icon list comes from the downloaded app.db, so it also shows what the console hides itself
  (those rows already have `visible=0`). The asterisk `*` marks the default list.
* No game is deleted or disabled: an icon can be brought back at any time (`--show --pick` or
  `--titles <ID> --show --apply`).
* `--titles NPXS20102,NPXS20104` never shows a menu: handy for .bat scripts and repeat runs.
  Without `--titles` and without a terminal (output redirected, started from the task scheduler) the
  default list is used.
* `--pick` works in `--offline` mode too: the list is built from the local copy of app.db. A typo
  (for example `x`) is rejected with `could not understand ...` and asked again; an empty Enter
  cancels and changes nothing.
* `run_list.bat` shows `visible` per table: different numbers mean the database was edited by hand
  or for different profiles.
* `--offline --apply` never uploads anything (FTP is not used at all): the changed database stays in
  `tmp\app.db` and the report says `offline mode, nothing was uploaded`. Upload it with
  `fix_db.exe PS4_IP --db tmp\app.db --apply --yes`.
* To roll back, restore app.db from `tmp\backup\`:
  `fix_db.exe --restore tmp\backup\app.db.<timestamp> --apply --yes` (`tmp\app.db.orig` is the file
  this script had downloaded).

### Files

```
hide_icons.exe    the hide tool: the run_*.bat files start it with the right options
fix_db.exe        the same engine as a separate program: upload a prepared database, restore a backup
run_list.bat      list the icons (nothing is written to the console)
run_hide.bat      list + pick icons, hide them (visible = 0)
run_show.bat      list + pick icons, bring them back (visible = 1)
README.md         this file
LICENSE           MIT license
tmp\              created on the first run: app.db, app.db.orig, backup\, reports

hide_icons.py     the source of the hide tool: the --pick menu, the profile choice, visible = 0/1
fix_db.py         the engine (FTP, param.sfo, row writing) — the same file as in PS4_db_rebuilder
appinfo.py        a pseudo app.info for tbl_appinfo
sfo\              param.sfo reader (MIT, Copyright (c) 2016 cologler)
build_exe.bat     rebuild hide_icons.exe (PyInstaller)
make_dist.bat     build the release archive in dist\ and refresh SHA256SUMS.txt
make_dist.ps1     what make_dist.bat calls
SHA256SUMS.txt    the hashes of hide_icons.exe and fix_db.exe
```

This repository is called **PS4_hide_icons**. The engine (`fix_db.py`) and the helper build
(`fix_db.exe`) come from the companion repository **PS4_db_rebuilder**, which also holds the main
tool that registers games in `app.db`. When the engine changes, update `fix_db.py`, `appinfo.py`,
`sfo\` and `fix_db.exe` in both repositories and rebuild `hide_icons.exe` (`build_exe.bat`).

## Building the exe file

Python 3.8+ and PyInstaller are required:

```
python -m pip install pyinstaller
build_exe.bat
```

The script builds `hide_icons.exe` next to the sources (`pyinstaller --onefile --console --clean`);
the `build\` folder is not committed. To run from the sources:
`python hide_icons.py 192.0.2.10 --pick`.

The archive of the Releases section is built separately:

```
make_dist.bat   -> dist\hide_icons.zip, dist\SHA256SUMS.txt
```

## Checksums

```
certutil -hashfile hide_icons.exe SHA256
```

Compare the result with `SHA256SUMS.txt`. The exe is built with PyInstaller and is not code
signed, so SmartScreen may show "Windows protected your PC": choose More info → Run anyway.