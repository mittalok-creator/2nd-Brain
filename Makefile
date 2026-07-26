.DEFAULT_GOAL := help
PYTHON ?= python3

.PHONY: help validate structure yaml links tree phase

help: ## Show available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

validate: ## Run every specification check (structure, YAML, internal links)
	@$(PYTHON) scripts/validate_repository.py

structure: ## Verify the repository layout only
	@$(PYTHON) scripts/validate_repository.py --only structure

yaml: ## Verify YAML specification syntax only
	@$(PYTHON) scripts/validate_repository.py --only yaml

links: ## Verify internal documentation links only
	@$(PYTHON) scripts/validate_repository.py --only links

tree: ## Print the repository map
	@git ls-files \
		| awk -F/ '{ if (NF>2) print $$1"/"$$2"/"; else if (NF>1) print $$1"/"; else print $$1 }' \
		| sort -u

phase: ## Show current build phase status
	@sed -n '/^| # | Phase | Status |/,/^$$/p' README.md
