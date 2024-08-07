.DEFAULT: commands

DB=cip.db

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## serve: serve the application in debug mode
.PHONY: serve
serve:
	flask --app cip --debug run

## testdb: make a test database
.PHONY: testdb
testdb:
	rm -rf ${DB}
	sqlite3 ${DB} < sql/makedb.sql
	sqlite3 ${DB} < sql/testdb.sql
