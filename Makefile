.DEFAULT_GOAL := help
PYTHON ?= python3

.PHONY: help validate structure yaml links hierarchy schema tree phase

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

tree: ## Print the repository map
	@git ls-files \
		| awk -F/ '{ if (NF>2) print $$1"/"$$2"/"; else if (NF>1) print $$1"/"; else print $$1 }' \
		| sort -u

phase: ## Show current build phase status
	@sed -n '/^| # | Phase | Status |/,/^$$/p' README.md
