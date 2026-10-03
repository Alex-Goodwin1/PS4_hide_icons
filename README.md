# hide_icons — hide the desktop icons of a PS4 user

The home screen shows one tile per row of `tbl_appbrowse_<user>` with `visible = 1`. `hide_icons`
downloads `/system_data/priv/mms/app.db` from the console over the GoldHEN FTP server and sets
`visible = 0` for the icons you pick — or brings them back with `--show`. The console itself hides
Music Unlimited, PlayStation Video and friends in exactly the same way. Firmware 5.05 – 13.02, no
Python needed: `hide_icons.exe` is prebuilt.

## Quick start

1. Unpack the archive into one folder — the `exe` and the `.bat` files must stay together.
2. Start GoldHEN on the PS4 with its FTP server (port 2121, login `username` / `password`).
3. Double click a launcher and type the IP of the console:

```
run_list.bat   list the icons, nothing is written to the console
run_hide.bat   list + pick the icons to hide (visible = 0)
run_show.bat   list + pick the icons to bring back (visible = 1)
```

After a write **log the PS4 user out or reboot the console**, otherwise PS4 keeps the old app.db in
memory. A copy of the original is kept in `tmp\backup\`.

## Picking the icons

`--pick` (used by `run_hide.bat` / `run_show.bat`) prints every desktop icon with a number and asks
what to change:

```
  1    NPXS20979  1   PlayStation Store  *
  2    NPXS20102  1   Интернет-браузер
  3    NPXS20106  0   Music Unlimited
what to hide?  numbers (1 3 5), a range (3-6), title ids, 'all', 'default'
             Enter = cancel
```

`default` is the usual firmware set: `NPXS20979` Store, `NPXS20108` What's new, `NPXS20105` Live
from PlayStation, `NPXS20104` Capture Gallery, `CUSA00001` THE PLAYROOM. Those rows are marked `*`;
icons the console has already hidden are shown as `visible = 0`. Without a terminal the default set
is used, `--titles NPXS20102,NPXS20104` skips the menu, `--yes` skips the confirmation before the
upload.

## Which user to edit

Every user of the console has its own `tbl_appbrowse_<suffix>` table. The program prints the
suffixes when it starts and, without `--profile`, asks which user to edit:

```
for which user should the icons be changed?
  1    0123456789   (default)
  2    0123456790
  numbers (1 3), a range (1-2), profile tails, 'all' = every user
  Enter = 1, i.e. only the first profile (0123456789)
```

`Enter` and a run without a terminal mean the first profile only, `all` means every user. Set the
user in advance with `--profile` — the other users then notice nothing:

```
hide_icons.exe PS4_IP --list --profile 0123456789
hide_icons.exe PS4_IP --profile 0123456789 --titles NPXS20102 --apply --yes
hide_icons.exe PS4_IP --profile all --pick --apply
```

`--profile` accepts the full suffix (`0123456789`), a unique tail (`789`), the table name
(`tbl_appbrowse_0123456789`), a comma separated list, or `all` / `*`. An unknown value prints the
suffixes that were found and exits with code 1. app.db keeps no user names, so the way to find a
profile is to hide one icon, log out and see which user lost it.

## Command line

`PS4_IP` is the address of the console (the tool cannot download app.db without it).

| command | what it does |
|--|--|
| `hide_icons.exe PS4_IP --list` | list only, nothing is written |
| `hide_icons.exe PS4_IP --pick --apply` | menu + upload |
| `hide_icons.exe PS4_IP --titles NPXS20102 --apply` | no menu: hide the browser |
| `hide_icons.exe --offline --db tmp/app.db --pick` | pick on a local copy, no FTP |
| `fix_db.exe --restore tmp\backup\app.db.<timestamp> --apply --yes` | roll back |

Only the `visible` column is changed and nothing is deleted, so any icon can be brought back.
`--offline --apply` uploads nothing (the report says `offline mode, nothing was uploaded`); send
the prepared `tmp\app.db` later with `fix_db.exe PS4_IP --db tmp\app.db --apply --yes`.

## Files

```
hide_icons.exe    the hide tool (no Python needed)
fix_db.exe        the same engine as a separate program: upload a database, restore a backup
run_list.bat      list the icons
run_hide.bat      list + pick + hide (visible = 0)
run_show.bat      list + pick + bring back (visible = 1)
hide_icons.py     the source of the hide tool (--pick, the profile choice)
fix_db.py         the engine (FTP, param.sfo, row writing)
appinfo.py        a pseudo app.info for tbl_appinfo
sfo\              param.sfo reader (MIT, Copyright (c) 2016 cologler)
build_exe.bat     rebuild hide_icons.exe (PyInstaller)
make_dist.bat     build dist\hide_icons.zip and refresh SHA256SUMS.txt
SHA256SUMS.txt    hashes of hide_icons.exe and fix_db.exe
LICENSE           MIT
tmp\              created on the first run, never committed
```

## Build

| step | what it does |
|--|--|
| `python -m pip install pyinstaller` | install the builder |
| `build_exe.bat` | rebuild `hide_icons.exe` |
| `python hide_icons.py PS4_IP --pick` | run from the sources instead of the exe |
| `make_dist.bat` | build `dist\hide_icons.zip` and refresh `SHA256SUMS.txt` |

The exe files are built with PyInstaller and are not code signed, so SmartScreen may show "Windows
protected your PC": choose More info → Run anyway. Compare the hashes with `SHA256SUMS.txt`
(`certutil -hashfile hide_icons.exe SHA256`). The engine (`fix_db.py`, `appinfo.py`, `sfo\`,
`fix_db.exe`) comes from the companion repository **PS4_db_rebuilder**: when it changes, update
those files here and rebuild `hide_icons.exe`.

## License

MIT, Copyright (c) 2026 Alex Goodwin — see `LICENSE`. Editing `app.db` means touching a system file,
everything is at your own risk.

---

# hide_icons — русская версия

Главный экран PS4 показывает плитку для каждой строки таблицы `tbl_appbrowse_<пользователь>` с
`visible = 1`. `hide_icons` скачивает `/system_data/priv/mms/app.db` с консоли по FTP-серверу GoldHEN
и ставит `visible = 0` для выбранных иконок — а `--show` возвращает их обратно. Сама консоль скрывает
Music Unlimited, PlayStation Video и подобное точно так же. Прошивки 5.05 – 13.02, Python не нужен:
`hide_icons.exe` уже собран.

## Быстрый старт

1. Распакуйте архив в одну папку — `exe` и `.bat` должны лежать рядом.
2. Запустите GoldHEN на PS4 вместе с его FTP-сервером (порт 2121, логин `username` / `password`).
3. Запустите `.bat` и введите IP консоли:

```
run_list.bat   список иконок, на консоль ничего не пишется
run_hide.bat   список + выбор иконок для скрытия (visible = 0)
run_show.bat   список + выбор иконок для возврата (visible = 1)
```

После записи **выйдите из профиля на PS4 или перезагрузите консоль**, иначе PS4 продолжит держать
в памяти старую app.db. Копия оригинала остаётся в `tmp\backup\`.

## Как выбирать иконки

`--pick` (его используют `run_hide.bat` и `run_show.bat`) печатает все иконки рабочего стола с
номерами и спрашивает, что менять:

```
  1    NPXS20979  1   PlayStation Store  *
  2    NPXS20102  1   Интернет-браузер
  3    NPXS20106  0   Music Unlimited
what to hide?  номера (1 3 5), диапазон (3-6), title id, 'all', 'default'
             Enter = отмена
```

`default` — обычный набор прошивки: `NPXS20979` Store, `NPXS20108` Что нового, `NPXS20105` ТВ и
видео, `NPXS20104` Галерея, `CUSA00001` THE PLAYROOM. Эти строки помечены `*`; иконки, которые
консоль уже скрыла, показаны как `visible = 0`. Без терминала используется набор по умолчанию,
`--titles NPXS20102,NPXS20104` пропускает меню, `--yes` — подтверждение перед загрузкой.

## Какого пользователя править

У каждого пользователя консоли своя таблица `tbl_appbrowse_<суффикс>`. Программа печатает суффиксы
при запуске и, если не указан `--profile`, спрашивает, какого пользователя менять:

```
for which user should the icons be changed?
  1    0123456789   (default)
  2    0123456790
  номера (1 3), диапазон (1-2), хвост суффикса, 'all' = все пользователи
  Enter = 1, то есть только первый профиль (0123456789)
```

`Enter` и запуск без терминала означают только первого пользователя, `all` — всех. Пользователя
можно задать заранее через `--profile`, тогда остальные ничего не заметят:

```
hide_icons.exe PS4_IP --list --profile 0123456789
hide_icons.exe PS4_IP --profile 0123456789 --titles NPXS20102 --apply --yes
hide_icons.exe PS4_IP --profile all --pick --apply
```

`--profile` принимает полный суффикс (`0123456789`), однозначный «хвост» (`789`), имя таблицы
(`tbl_appbrowse_0123456789`), список через запятую или `all` / `*`. Неизвестное значение печатает
найденные суффиксы и выходит с кодом 1. Имён пользователей в app.db нет, поэтому профиль ищут так:
скрыть одну иконку, выйти из профиля и посмотреть, у кого она пропала.

## Командная строка

`PS4_IP` — адрес консоли (без него скачать app.db невозможно).

| команда | что делает |
|--|--|
| `hide_icons.exe PS4_IP --list` | только список, ничего не пишется |
| `hide_icons.exe PS4_IP --pick --apply` | меню + загрузка |
| `hide_icons.exe PS4_IP --titles NPXS20102 --apply` | без меню: скрыть браузер |
| `hide_icons.exe --offline --db tmp/app.db --pick` | выбор на локальной копии, без FTP |
| `fix_db.exe --restore tmp\backup\app.db.<время> --apply --yes` | откатить назад |

Меняется только колонка `visible`, ничего не удаляется, поэтому любую иконку можно вернуть.
`--offline --apply` ничего не загружает (в отчёте будет `offline mode, nothing was uploaded`);
подготовленный `tmp\app.db` отправьте позже: `fix_db.exe PS4_IP --db tmp\app.db --apply --yes`.

## Файлы

```
hide_icons.exe    сама программа скрытия (Python не нужен)
fix_db.exe        тот же движок отдельной программой: загрузка базы, восстановление бэкапа
run_list.bat      список иконок
run_hide.bat      список + выбор + скрытие (visible = 0)
run_show.bat      список + выбор + возврат (visible = 1)
hide_icons.py     исходник программы скрытия (--pick, выбор профиля)
fix_db.py         движок (FTP, param.sfo, запись строк)
appinfo.py        псевдо-app.info для tbl_appinfo
sfo\              чтение param.sfo (MIT, Copyright (c) 2016 cologler)
build_exe.bat     пересборка hide_icons.exe (PyInstaller)
make_dist.bat     сборка dist\hide_icons.zip и обновление SHA256SUMS.txt
SHA256SUMS.txt    хэши hide_icons.exe и fix_db.exe
LICENSE           MIT
tmp\              создаётся при первом запуске, в репозиторий не попадает
```

## Сборка

| шаг | что делает |
|--|--|
| `python -m pip install pyinstaller` | поставить сборщик |
| `build_exe.bat` | пересобрать `hide_icons.exe` |
| `python hide_icons.py PS4_IP --pick` | запуск из исходников вместо exe |
| `make_dist.bat` | собрать `dist\hide_icons.zip` и обновить `SHA256SUMS.txt` |

exe собраны PyInstaller и не подписаны, поэтому SmartScreen может показать «Windows защитила ваш
компьютер»: нажмите «Подробнее» → «Выполнить в любом случае». Сверяйте хэши с `SHA256SUMS.txt`
(`certutil -hashfile hide_icons.exe SHA256`). Движок (`fix_db.py`, `appinfo.py`, `sfo\`,
`fix_db.exe`) берётся из соседнего репозитория **PS4_db_rebuilder**: когда он меняется, обновите
эти файлы здесь и пересоберите `hide_icons.exe`.

## Лицензия

MIT, Copyright (c) 2026 Alex Goodwin — см. `LICENSE`. Правка `app.db` — это вмешательство в
системный файл, всё делается на свой страх и риск.
