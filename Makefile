# ---------- Configuration ----------
PACKAGE = xytb           # project import-/wheel name

.ONESHELL:
# Use bash for all recipes, enable strict mode
SHELL        := bash
.SHELLFLAGS  := -euo pipefail -c

.PHONY: bump build release

# 1) Bump version & create changelog / tag (does NOT push)
bump:
	@echo "🔖  semantic-release: bumping version …"
	uvx --from python-semantic-release semantic-release version --no-push

# 2) Build the sdist & wheel with Hatch
build: bump
	@echo "📦  Building $(PACKAGE) …"
	uv build

# 3) Convenience target: bump + build
release: build
	@echo "✅  Release artefacts ready in dist/"
	uv publish
