# hide_icons — hide the desktop icons of a PS4 user
The PS4 home screen displays a tile for each row in the tbl_appbrowse_<user> table with visible = 1.
hide_icons downloads /system_data/priv/mms/app.db from the console via the GoldHEN FTP server and sets visible = 0 for selected icons,
while --show restores them. The console itself hides Music Unlimited, PlayStation Video, and similar apps in the exact same way.
Firmwares 5.05 – 13.02; likely to work on firmwares up to 13.52 inclusive.

Quick Start
Extract the archive into a single folder — the exe and .bat files must be in the same directory.
Launch GoldHEN on the PS4 along with its FTP server (port 2121, login username / password).
Run the .bat file and enter the console's IP address:
run_list.bat lists icons for viewing; no changes are written to the console
run_hide.bat lists + allows selecting icons to hide (visible = 0)
run_show.bat lists + allows selecting icons to restore (visible = 1)

After writing, log out of the PS4 profile or reboot the console, otherwise the PS4 will keep the old app.db in memory. A copy of the original remains in tmp\backup\.

How to select icons
--pick (used by run_hide.bat and run_show.bat) prints all home screen icons with numbers and asks what to change:
  1    NPXS20979  1   PlayStation Store  *
  2    NPXS20102  1   Internet Browser
  3    NPXS20106  0   Music Unlimited
  
what to hide? numbers (1 3 5), range (3-6), title id, 'all', 'default'
             Enter = cancel
default — the standard firmware set: NPXS20979 Store, NPXS20108 What's New, NPXS20105 TV & Video, NPXS20104 Gallery, CUSA00001 THE PLAYROOM.
These rows are marked with *; icons already hidden by the console are shown as visible = 0. Without a terminal,
the default set is used; --titles NPXS20102,NPXS20104 skips the menu, and --yes auto-confirms before downloading.

Which user to edit
Warning! It is advisable to modify only one user. This way, if there are jailbreak issues, you can select another user and run the WebKit exploit under it.

Each console user has their own tbl_appbrowse_<suffix> table. The program prints the suffixes at startup and, if --profile is not specified, asks which user to modify:
for which user should the icons be changed?
  1    0123456789   (default)
  2    0123456790
numbers (1 3), range (1-2), suffix tail, 'all' = all users
Enter = 1, meaning only the first profile (0123456789)

There are no usernames in app.db, so the profile is identified as follows:
hide one icon, log out of the profile, and check which user lost it.

MIT, Copyright (c) 2026 Alex Goodwin


# hide_icons 
Главный экран PS4 показывает плитку для каждой строки таблицы `tbl_appbrowse_<пользователь>` с
`visible = 1`. `hide_icons` скачивает `/system_data/priv/mms/app.db` с консоли по FTP-серверу GoldHEN
и ставит `visible = 0` для выбранных иконок — а `--show` возвращает их обратно. Сама консоль скрывает
Music Unlimited, PlayStation Video и подобное точно так же.

Прошивки 5.05 – 13.02, вероятно будет работать на прошивках до 13.52. включительно.

## Быстрый старт
1. Распакуйте архив в одну папку — `exe` и `.bat` должны лежать рядом.
2. Запустите GoldHEN на PS4 вместе с его FTP-сервером (порт 2121, логин `username` / `password`).
3. Запустите `.bat` и введите IP консоли:

run_list.bat   список иконок для просмотра, на консоль ничего не пишется
run_hide.bat   список + выбор иконок для скрытия (visible = 0)
run_show.bat   список + выбор иконок для возврата (visible = 1)

После записи **выйдите из профиля на PS4 или перезагрузите консоль**, иначе PS4 продолжит держать
в памяти старую app.db. Копия оригинала остаётся в `tmp\backup\`.

## Как выбирать иконки
`--pick` (его используют `run_hide.bat` и `run_show.bat`) печатает все иконки рабочего стола с
номерами и спрашивает, что менять:

  1    NPXS20979  1   PlayStation Store  *
  2    NPXS20102  1   Интернет-браузер
  3    NPXS20106  0   Music Unlimited
what to hide?  номера (1 3 5), диапазон (3-6), title id, 'all', 'default'
             Enter = отмена

`default` — обычный набор прошивки: `NPXS20979` Store, `NPXS20108` Что нового, `NPXS20105` ТВ и
видео, `NPXS20104` Галерея, `CUSA00001` THE PLAYROOM. Эти строки помечены `*`; иконки, которые
консоль уже скрыла, показаны как `visible = 0`. Без терминала используется набор по умолчанию,
`--titles NPXS20102,NPXS20104` пропускает меню, `--yes` — подтверждение перед загрузкой.

## Какого пользователя править
Внимание! Желательно менять только у одного пользователя.
Тогда при проблемах с jailbreak можно будет выбрать другого пользователя и запустить webkeet под ним.

У каждого пользователя консоли своя таблица `tbl_appbrowse_<суффикс>`. Программа печатает суффиксы
при запуске и, если не указан `--profile`, спрашивает, какого пользователя менять:

for which user should the icons be changed?
  1    0123456789   (default)
  2    0123456790
  номера (1 3), диапазон (1-2), хвост суффикса, 'all' = все пользователи
  Enter = 1, то есть только первый профиль (0123456789)

Имён пользователей в app.db нет, поэтому профиль ищут так:
скрыть одну иконку, выйти из профиля и посмотреть, у кого она пропала.

MIT, Copyright (c) 2026 Alex Goodwin
