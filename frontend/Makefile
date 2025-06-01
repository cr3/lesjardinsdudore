NODE_MODULES := node_modules

NODE := npm exec -- node
TOUCH := $(NODE) -e 'fs.utimesSync(process.argv[1], new Date(), new Date())'

# Build node_modules with deps.
$(NODE_MODULES):
	@echo Installing Node environment
	@npm install
	@$(TOUCH) $@

# Convenience target to build node_modules
.PHONY: setup
setup: $(NODE_MODULES)

.PHONY: check
check: $(NODE_MODULES)

.PHONY: test
test: $(NODE_MODULES)

.PHONY: coverage
coverage: $(NODE_MODULES)

.DEFAULT_GOAL := test
