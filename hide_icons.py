from __future__ import print_function

import argparse
import io
import os
import re
import sqlite3
import sys
import traceback

import fix_db

REPORT_FILE = os.path.join(fix_db.TMP_DIR, "hide_icons_report.txt")
DEFAULT_TITLES = "NPXS20979,NPXS20108,NPXS20105,NPXS20104,CUSA00001"
DEFAULT_IDS = tuple(DEFAULT_TITLES.split(","))
TITLE_ID_RE = re.compile(r"^[A-Z]{4}[0-9]{5}$")

_report = []


def log(message=""):
	_report.append(u"%s" % (message,))
	print(message)


fix_db.log = log


def save_report():
	try:
		if not os.path.isdir(fix_db.TMP_DIR):
			os.makedirs(fix_db.TMP_DIR)
		with io.open(REPORT_FILE, "w", encoding="utf-8", newline="\n") as handle:
			handle.write(u"\n".join(_report) + u"\n")
	except Exception as error:
		print("could not write %s: %s" % (REPORT_FILE, error))


def table_rows(cursor, tables, title_id):
	per_table = {}
	for table in tables:
		row = cursor.execute("SELECT titleName, visible FROM [%s] WHERE titleId=?;"
			% table, (title_id,)).fetchone()
		if row is not None:
			per_table[table] = (row[0], row[1])
	return per_table


def all_ids(cursor, tables):
	found = set()
	for table in tables:
		for (title_id,) in cursor.execute("SELECT titleId FROM [%s];" % table):
			found.add(u"%s" % (title_id,))
	return sorted(found)


def icon_table(cursor, tables):
	log("desktop icons -- visible is shown per table (%s):" %
		", ".join(table.rsplit("_", 1)[-1] for table in tables))
	log("  %-4s %-10s %-14s %s" % ("#", "titleId", "visible", "titleName"))
	title_ids = all_ids(cursor, tables)
	for index, title_id in enumerate(title_ids):
		per_table = table_rows(cursor, tables, title_id)
		values = list(per_table.values())[0]
		flags = " ".join(("%s" % per_table[table][1]) if table in per_table else "-"
			for table in tables)
		log("  %-4d %-10s %-14s %s%s" % (index + 1, title_id, flags, values[0],
			"  *" if title_id in DEFAULT_IDS else ""))
	log("")
	log("  * = part of the default list %s" % DEFAULT_TITLES)
	return title_ids


def set_visible(cursor, tables, title_ids, value, dry_run=True):
	changes = []
	for title_id in title_ids:
		for table in tables:
			row = cursor.execute("SELECT titleName, visible FROM [%s] WHERE titleId=?;"
				% table, (title_id,)).fetchone()
			if row is None or row[1] == value:
				continue
			changes.append((table, title_id, row[0], row[1]))
			if not dry_run:
				cursor.execute("UPDATE [%s] SET visible=? WHERE titleId=?;" % table,
					(value, title_id))
	return changes


def profile_tables(tables, wanted):
	suffixes = dict((table.rsplit("_", 1)[-1], table) for table in tables)
	chosen = []
	for part in re.split(r"[,\s]+", wanted or ""):
		if not part:
			continue
		if part.lower() in ("all", "*"):
			return list(tables)
		if part in tables:
			table = part
		elif part in suffixes:
			table = suffixes[part]
		else:
			matches = [table for suffix, table in suffixes.items()
				if suffix.endswith(part)]
			if not matches:
				raise SystemExit("no tbl_appbrowse table matches %r, found: %s"
					% (part, ", ".join(sorted(suffixes))))
			if len(matches) > 1:
				raise SystemExit("%r is ambiguous (%s), use the full suffix"
					% (part, ", ".join(sorted(matches))))
			table = matches[0]
		if table not in chosen:
			chosen.append(table)
	if not chosen:
		raise SystemExit("--profile is empty")
	return [table for table in tables if table in chosen]


def profile_list(tables):
	return ", ".join(table.rsplit("_", 1)[-1] for table in tables)


def select_profiles(text, tables):
	tails = [table.rsplit("_", 1)[-1] for table in tables]
	text = (text or "").strip()
	if not text:
		return tables[:1]
	chosen = []
	for part in re.split(r"[,\s;]+", text):
		if not part:
			continue
		if part.lower() in ("all", "*"):
			return list(tables)
		if part.isdigit() and 1 <= int(part) <= len(tables):
			candidates = [tables[int(part) - 1]]
		elif re.match(r"^\d+-\d+$", part):
			first, last = (int(value) for value in part.split("-"))
			if first > last:
				first, last = last, first
			if first < 1 or last > len(tables):
				return None
			candidates = tables[first - 1:last]
		else:
			candidates = [table for table, tail in zip(tables, tails)
				if table == part or tail == part or tail.endswith(part)]
			if not candidates or len(candidates) > 1:
				return None
		for table in candidates:
			if table not in chosen:
				chosen.append(table)
	return chosen


def profile_prompt(tables):
	tails = [table.rsplit("_", 1)[-1] for table in tables]
	log("for which user should the icons be changed?")
	for index, tail in enumerate(tails):
		log("  %-4d %s%s" % (index + 1, tail, "   (default)" if index == 0 else ""))
	log("  numbers (1 3), a range (1-2), profile tails, 'all' = every user")
	log("  Enter = 1, i.e. only the first profile (%s)" % tails[0])
	while True:
		line = read_selection()
		chosen = select_profiles(line, tables)
		if chosen is None:
			log("could not understand %r: numbers 1-%d, a range, profile tails "
				"or 'all'" % (line.strip(), len(tables)))
			continue
		if not chosen:
			log("nothing was selected, cancelled")
			return []
		return chosen


def choose_profile_tables(args, tables):
	if args.profile:
		chosen = profile_tables(tables, args.profile)
		log("editing profile(s): %s" % profile_list(chosen))
		return chosen
	if args.list:
		return tables
	if interactive():
		chosen = profile_prompt(tables)
		if chosen:
			log("editing profile(s): %s" % profile_list(chosen))
		return chosen
	chosen = tables[:1]
	log("editing profile(s): %s   (only the first one: use --profile <suffix>, "
		"'all' = every user)" % profile_list(chosen))
	return chosen


def split_titles(option):
	title_ids = []
	for part in re.split(r"[,\s]+", option or ""):
		if not part:
			continue
		title_id = part.strip().upper()
		if not TITLE_ID_RE.match(title_id):
			raise SystemExit("not a title id: %r" % (part,))
		if title_id not in title_ids:
			title_ids.append(title_id)
	if not title_ids:
		raise SystemExit("no title id given, --titles is empty")
	return title_ids


def interactive():
	if sys.stdin is None:
		return False
	try:
		return bool(sys.stdin.isatty())
	except Exception:
		return False


def read_selection():
	sys.stdout.write("> ")
	try:
		sys.stdout.flush()
	except Exception:
		pass
	if sys.stdin is None:
		return ""
	try:
		line = sys.stdin.readline()
	except Exception:
		line = ""
	if not line:
		log("")
	return line.replace(u"\ufeff", "")


def select_ids(text, title_ids, fallback):
	chosen = []
	if text.strip().lower() in ("all", "*"):
		return list(title_ids)
	if text.strip().lower() == "default":
		return [title_id for title_id in fallback if title_id in title_ids]
	for part in re.split(r"[,\s;]+", text.strip()):
		if not part:
			continue
		if part == "*":
			candidates = list(title_ids)
		elif part.isdigit():
			index = int(part)
			if index < 1 or index > len(title_ids):
				return None
			candidates = [title_ids[index - 1]]
		elif re.match(r"^\d+-\d+$", part):
			first, last = (int(value) for value in part.split("-"))
			if first > last:
				first, last = last, first
			if first < 1 or last > len(title_ids):
				return None
			candidates = title_ids[first - 1:last]
		else:
			title_id = part.upper()
			if not TITLE_ID_RE.match(title_id):
				return None
			candidates = [title_id]
		for title_id in candidates:
			if title_id not in chosen:
				chosen.append(title_id)
	return chosen


def pick_title_ids(args, cursor, tables):
	verb = "show" if args.show else "hide"
	title_ids = icon_table(cursor, tables)
	if not title_ids:
		log("no icon row was found in tbl_appbrowse_*, nothing to pick")
		return []
	log("what to %s?  numbers (1 3 5), a range (3-6), title ids, 'all', 'default'"
		% verb)
	log("             Enter = cancel")
	while True:
		line = read_selection()
		if not line.strip():
			log("nothing was selected, cancelled")
			return []
		chosen = select_ids(line, title_ids, DEFAULT_IDS)
		if chosen is None:
			log("could not understand %r: numbers 1-%d, a range, title ids, "
				"'all' or 'default'" % (line.strip(), len(title_ids)))
			continue
		if not chosen:
			log("nothing was selected, cancelled")
			return []
		return chosen


def choose_title_ids(args, cursor, tables):
	if args.pick or (args.titles is None and interactive()):
		return pick_title_ids(args, cursor, tables)
	return split_titles(args.titles or DEFAULT_TITLES)


def run(args):
	ftp = None
	try:
		if not args.offline:
			ftp = fix_db.ftp_connect(args)
		local_db = fix_db.prepare_db(ftp, args)
		conn = sqlite3.connect(local_db)
		try:
			cursor = conn.cursor()
			if cursor.execute("PRAGMA integrity_check;").fetchone()[0] != "ok":
				log("local app.db is damaged, stop")
				return 1
			tables = fix_db.appbrowse_tables(cursor)
			if not tables:
				log("warning: no tbl_appbrowse_* table found, the DB layout is unknown")
				return 1
			log("tbl_appbrowse tables: %s" % ", ".join(tables))
			log("profiles: %s   (--profile <suffix>, 'all' = every user)" %
				" ".join(table.rsplit("_", 1)[-1] for table in tables))
			tables = choose_profile_tables(args, tables)
			if not tables:
				return 0
			for table in tables:
				if "visible" not in fix_db.table_columns(cursor, table):
					log("table %s has no visible column, stop" % table)
					return 1

			if args.list:
				log("")
				icon_table(cursor, tables)
				return 0

			value = 1 if args.show else 0
			word = "shown" if args.show else "hidden"
			title_ids = choose_title_ids(args, cursor, tables)
			if not title_ids:
				return 0
			log("")
			log("icons to be %s (visible -> %d): %s" % (word, value, ", ".join(title_ids)))
			missing = [title_id for title_id in title_ids
				if not table_rows(cursor, tables, title_id)]
			changes = set_visible(cursor, tables, title_ids, value, dry_run=not args.apply)
			log("")
			for table, title_id, name, old_value in changes:
				log("  %-26s %-10s visible %s -> %s   %r" % (
					table, title_id, old_value, value, name))
			if not changes:
				log("  every row already has visible=%d" % value)
			if missing:
				log("  warning: no tbl_appbrowse row for %s" % ", ".join(missing))

			if not args.apply:
				log("")
				log("dry run finished, nothing was written to the PS4")
				log("  local copy of app.db : %s" % local_db)
				log("  original app.db      : %s" % fix_db.APP_DB_ORIG)
				log("  write it with        : hide_icons.exe %s --apply --yes" %
					(args.PS4_IP or "PS4_IP"))
				return 0

			left = set_visible(cursor, tables, title_ids, value, dry_run=True)
			if left or missing:
				log("local app.db still has %d wrong row(s), upload skipped" % len(left))
				return 1
			conn.commit()
			check = cursor.execute("PRAGMA integrity_check;").fetchone()[0]
			log("")
			log("verification: %d row(s) changed, %d icon(s) %s, integrity_check=%s" % (
				len(changes), len(title_ids), word, check))
			if check != "ok":
				log("upload skipped")
				return 1

			if ftp is None:
				log("")
				log("offline mode, nothing was uploaded")
				log("  changed DB      : %s" % local_db)
				log("  original app.db : %s" % fix_db.APP_DB_ORIG)
				log("  upload it with  : fix_db.exe PS4_IP --db %s --apply" % local_db)
				return 0

			if not fix_db.confirm(args):
				log("upload cancelled, the changed DB stays in %s" % local_db)
				return 1
			log("")
			fix_db.upload_db(ftp, local_db)
			log("")
			log("done. Log the PS4 user out (or reboot) so PS4 reads app.db again.")
			return 0
		finally:
			conn.close()
	finally:
		if ftp is not None:
			try:
				ftp.quit()
			except Exception:
				try:
					ftp.close()
				except Exception:
					pass


def parse_args(argv=None):
	parser = argparse.ArgumentParser(
		description="hide the desktop icons of a PS4 (tbl_appbrowse_*.visible = 0), "
			"--show brings them back")
	parser.add_argument("PS4_IP", nargs="?", default=None, help="PS4 address, e.g. 192.0.2.10")
	parser.add_argument("--port", type=int, default=2121, help="FTP port (GoldHEN uses 2121)")
	parser.add_argument("--user", default="username", help="FTP user")
	parser.add_argument("--password", default="password", help="FTP password")
	parser.add_argument("--titles", default=None, metavar="ID,ID",
		help="title ids to hide; without it the script asks which icons to hide "
			"when it runs in a terminal, otherwise it hides the default list %s"
			% DEFAULT_TITLES)
	parser.add_argument("--pick", action="store_true",
		help="always ask: print every icon of app.db with its visible value and "
			"take the numbers/title ids you type (works with --offline too)")
	parser.add_argument("--show", action="store_true",
		help="set visible=1 instead, i.e. bring the icons back")
	parser.add_argument("--list", action="store_true",
		help="only list every icon with its visible value and exit")
	parser.add_argument("--apply", action="store_true",
		help="upload the changed app.db back to the PS4 (without it nothing is written)")
	parser.add_argument("--yes", action="store_true", help="do not ask before uploading")
	parser.add_argument("--db", default=None, metavar="FILE",
		help="use this local app.db instead of downloading one")
	parser.add_argument("--offline", action="store_true", help="no FTP at all (needs --db)")
	parser.add_argument("--no-backup", action="store_true",
		help="do not copy app.db to tmp/backup")
	parser.add_argument("--profile", default=None, metavar="ID",
		help="which users to change: ID is the suffix of tbl_appbrowse_<ID> as "
			"printed by --list (e.g. 0473217505), a unique tail works too "
			"(e.g. 512), several ids may be separated by commas, all = every "
			"user of the console. Without --profile the script asks which user "
			"in a terminal (Enter = the first profile) and uses the first "
			"profile when there is no terminal")
	return parser.parse_args(argv)


def main(argv=None):
	args = parse_args(argv)
	fix_db.ensure_dirs()
	if args.PS4_IP is None and not args.offline:
		raise SystemExit("usage: hide_icons.exe PS4_IP [--list] [--pick] [--apply]    "
			"(offline: --offline --db tmp/app.db)")
	code = 1
	try:
		code = run(args)
	except SystemExit:
		raise
	except Exception:
		log("ERROR:")
		log(traceback.format_exc())
	finally:
		save_report()
	return code


if __name__ == "__main__":
	try:
		sys.stdout.reconfigure(errors="replace")
	except Exception:
		pass
	try:
		sys.stdin.reconfigure(encoding="utf-8", errors="replace")
	except Exception:
		pass
	sys.exit(main())
