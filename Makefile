.PHONY: init tests help

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init:  ## Initialize repository: install pre-commit
	${INFO} "Initializing..."
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py loaddata fixtures.json
	${INFO} "Initialization complete. Now It's time to run project."

run: ## Run project
	${INFO} "Running project"
	celery -A enigma_recruitment_task worker -l info
	celery -A enigma_recruitment_task beat -l info
	python manage.py runserver

# Colors
YELLOW := "\e[1;33m"
BLUE := "\e[1;34m"
NC := "\e[0m"

# Logs
INFO := @bash -c '\
	printf $(YELLOW); \
	echo "=> $$1"; \
	printf $(NC)' VALUE
