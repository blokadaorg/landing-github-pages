.PHONY: test gen-whitelist sync gates

# Run whitelist filter tests
test:
	python3 whitelist_filter.py
	@echo "Tests passed."

# Generate master whitelist from manual entries and external sources
gen-whitelist:
	python3 gen-whitelist.py
	@echo "Master whitelist generated."

# Sync mirrors (depends on tests passing and updated whitelist)
sync: test gen-whitelist
	./sync-mirrors.sh

# Run safety gates against the working tree vs HEAD. Used by CI before
# auto-merging a sync PR; safe to run locally too (e.g. after
# `SKIP_COMMIT=1 make sync` to inspect what would land).
gates: test
	./gates/check_paths.sh
	./gates/check_new_files.sh
	python3 ./gates/check_size_deltas.py
	python3 ./gates/check_format.py
	@echo "All gates passed."
