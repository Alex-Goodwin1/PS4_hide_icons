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
  1    0473217505   (default)
  2    0473217511
  numbers (1 3), a range (1-2), profile tails, 'all' = every user
  Enter = 1, i.e. only the first profile (0473217505)
```

`Enter` and a run without a terminal mean the first profile only, `all` means every user. Set the
user in advance with `--profile` — the other users then notice nothing:

```
hide_icons.exe 192.0.2.10 --list --profile 0473217505
hide_icons.exe 192.0.2.10 --profile 0473217505 --titles NPXS20102 --apply --yes
hide_icons.exe 192.0.2.10 --profile all --pick --apply
```

`--profile` accepts the full suffix (`0473217505`), a unique tail (`512`), the table name
(`tbl_appbrowse_0473217505`), a comma separated list, or `all` / `*`. An unknown value prints the
suffixes that were found and exits with code 1. app.db keeps no user names, so the way to find a
profile is to hide one icon, log out and see which user lost it.

## Command line

```
hide_icons.exe 192.0.2.10 --list                            # list only
hide_icons.exe 192.0.2.10 --pick --apply                    # menu + upload
hide_icons.exe 192.0.2.10 --titles NPXS20102 --apply        # no menu: hide the browser
hide_icons.exe --offline --db tmp/app.db --pick             # pick on a local copy, no FTP
fix_db.exe --restore tmp\backup\app.db.<timestamp> --apply --yes   # roll back
```

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

```
python -m pip install pyinstaller
build_exe.bat                            # rebuild hide_icons.exe
python hide_icons.py 192.0.2.10 --pick   # run from the sources
make_dist.bat                            # dist\hide_icons.zip + SHA256SUMS.txt
```

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

Домашний экран показывает по плитке на каждую строку `tbl_appbrowse_<пользователь>` с
`visible = 1`. `hide_icons` скачивает `/system_data/priv/mms/app.db` с консоли через FTP-сервер
GoldHEN и ставит `visible = 0` для выбранных значков, а ключ `--show` возвращает их обратно. Сама
консоль прячет Music Unlimited, PlayStation Video и прочие точно так же. Прошивки 5.05 – 13.02,
Python не нужен: `hide_icons.exe` уже собран.

## Быстрый старт

1. Распакуйте архив в одну папку — `exe` и `.bat` должны лежать рядом.
2. Запустите на PS4 GoldHEN с FTP-сервером (порт 2121, логин `username` / `password`).
3. Двойной щелчок по лаунчеру и введите IP консоли:

```
run_list.bat   список значков, на консоль ничего не пишется
run_hide.bat   список + выбор значков, скрыть их (visible = 0)
run_show.bat   список + выбор значков, вернуть их (visible = 1)
```

После записи **выйдите из пользователя PS4 или перезагрузите консоль** — иначе система оставит
в памяти старую копию app.db. Копия оригинала складывается в `tmp\backup\`.

## Выбор значков

`--pick` (его используют `run_hide.bat` / `run_show.bat`) печатает все значки домашнего экрана с
номерами и спрашивает, что изменить:

```
  1    NPXS20979  1   PlayStation Store  *
  2    NPXS20102  1   Интернет-браузер
  3    NPXS20106  0   Music Unlimited
what to hide?  numbers (1 3 5), a range (3-6), title ids, 'all', 'default'
             Enter = отмена
```

`default` — стандартный набор прошивки: `NPXS20979` Store, `NPXS20108` «Что нового?»,
`NPXS20105` «Прямой эфир с PlayStation», `NPXS20104` «Галерея снимков и клипов», `CUSA00001`
THE PLAYROOM. Они помечены `*`; значки, которые консоль уже скрыла, показываются с
`visible = 0`. Если терминала нет, берётся стандартный набор; `--titles NPXS20102,NPXS20104`
отменяет меню, `--yes` — подтверждение перед загрузкой.

## Для какого пользователя

У каждого пользователя консоли своя таблица `tbl_appbrowse_<суффикс>`. Программа печатает список
суффиксов при запуске и без `--profile` спрашивает, кого править:

```
for which user should the icons be changed?
  1    0473217505   (default)
  2    0473217511
  numbers (1 3), a range (1-2), profile tails, 'all' = every user
  Enter = 1, i.e. only the first profile (0473217505)
```

`Enter` и запуск без терминала = только первый профиль, `all` = все пользователи. Ключ
`--profile` задаёт пользователя заранее — остальные тогда ничего не замечают:

```
hide_icons.exe 192.0.2.10 --list --profile 0473217505
hide_icons.exe 192.0.2.10 --profile 0473217505 --titles NPXS20102 --apply --yes
hide_icons.exe 192.0.2.10 --profile all --pick --apply
```

`--profile` принимает полный суффикс (`0473217505`), однозначный «хвост» (`512`), имя таблицы
(`tbl_appbrowse_0473217505`), список через запятую или `all` / `*`. Неизвестное значение печатает
найденные суффиксы и выходит с кодом 1. Имён пользователей в app.db нет, поэтому нужный профиль
проще найти так: скройте значок, выйдите из пользователя — значок исчезнет именно у него.

## Командная строка

```
hide_icons.exe 192.0.2.10 --list                            # только список
hide_icons.exe 192.0.2.10 --pick --apply                    # меню + загрузка
hide_icons.exe 192.0.2.10 --titles NPXS20102 --apply        # без меню: скрыть браузер
hide_icons.exe --offline --db tmp/app.db --pick             # выбор по локальной копии, без FTP
fix_db.exe --restore tmp\backup\app.db.<дата> --apply --yes # откат
```

Меняется только колонка `visible`, ничего не удаляется и не отключается, поэтому любой значок
можно вернуть. `--offline --apply` ничего не загружает (в отчёте `offline mode, nothing was
uploaded`); готовую `tmp\app.db` отправьте позже командой
`fix_db.exe PS4_IP --db tmp\app.db --apply --yes`.

## Файлы

```
hide_icons.exe    сам скрыватель (Python не нужен)
fix_db.exe        тот же движок отдельной программой: залить базу, вернуть бэкап
run_list.bat      список значков
run_hide.bat      список + выбор + скрыть (visible = 0)
run_show.bat      список + выбор + вернуть (visible = 1)
hide_icons.py     исходник скрывателя (--pick, выбор профиля)
fix_db.py         движок (FTP, param.sfo, запись строк)
appinfo.py        псевдо-app.info для tbl_appinfo
sfo\              разбор param.sfo (MIT, Copyright (c) 2016 cologler)
build_exe.bat     пересобрать hide_icons.exe (PyInstaller)
make_dist.bat     собрать dist\hide_icons.zip и обновить SHA256SUMS.txt
SHA256SUMS.txt    хэши hide_icons.exe и fix_db.exe
LICENSE           MIT
tmp\              создаётся при первом запуске, в git не попадает
```

## Сборка

```
python -m pip install pyinstaller
build_exe.bat                            # пересобрать hide_icons.exe
python hide_icons.py 192.0.2.10 --pick   # запуск без сборки
make_dist.bat                            # dist\hide_icons.zip + SHA256SUMS.txt
```

exe собраны PyInstaller и не подписаны, поэтому SmartScreen может показать «Windows защитила ваш
компьютер»: «Подробнее» → «Выполнить в любом случае». Сверьте хэши с `SHA256SUMS.txt`
(`certutil -hashfile hide_icons.exe SHA256`). Движок (`fix_db.py`, `appinfo.py`, `sfo\`,
`fix_db.exe`) — из соседнего репозитория **PS4_db_rebuilder**: если он менялся, обновите эти файлы
здесь и пересоберите `hide_icons.exe`.

## Лицензия

MIT, Copyright (c) 2026 Alex Goodwin — см. `LICENSE`. Правка `app.db` — вмешательство в системный
файл консоли, всё делается на ваш риск.

