.DEFAULT_GOAL := help
PYTHON ?= python3

.PHONY: help validate structure yaml links hierarchy schema guide tree phase

help: ## Show available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

validate: ## Run every specification check (structure, YAML, links, hierarchy, schema)
	@$(PYTHON) scripts/validate_repository.py

structure: ## Verify the repository layout only
	@$(PYTHON) scripts/validate_repository.py --only structure

yaml: ## Verify YAML specification syntax only
	@$(PYTHON) scripts/validate_repository.py --only yaml

links: ## Verify internal documentation links only
	@$(PYTHON) scripts/validate_repository.py --only links

hierarchy: ## Verify the workspace page tree and navigation constraints
	@$(PYTHON) scripts/validate_repository.py --only hierarchy

schema: ## Verify entity field contracts, taxonomy references, and ownership
	@$(PYTHON) scripts/validate_repository.py --only schema

guide: ## Re-render the Notion user guide PDF from its HTML source
	@CHROME=$$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1); \
	 [ -z "$$CHROME" ] && CHROME=$$(command -v chromium || command -v google-chrome); \
	 "$$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
	   --print-to-pdf=docs/03-user-guide/2nd-Brain-Notion-Guide.pdf \
	   docs/03-user-guide/notion-guide.html 2>/dev/null; \
	 echo "rendered docs/03-user-guide/2nd-Brain-Notion-Guide.pdf"

tree: ## Print the repository map
	@git ls-files \
		| awk -F/ '{ if (NF>2) print $$1"/"$$2"/"; else if (NF>1) print $$1"/"; else print $$1 }' \
		| sort -u

phase: ## Show current build phase status
	@sed -n '/^| # | Phase | Status |/,/^$$/p' README.md
