.PHONY: clean format lint loc size build publish

clean:
	@find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -rf
	@rm -rf dist
format:
	@isort mul
	@black mul
lint: format
	@flake8 mul
loc:
	@find . -path mul -prune -o -print | egrep '\.py$$' | xargs cat | sed '/^\s*$$/d' | wc -l | awk '{print $$1}'
size:
	@find . -path mul -prune -o -print | egrep '\.py$$' | xargs cat | sed '/^\s*$$/d' | wc -c | awk '{print $$1/1000"K"}'
build: clean lint
	@poetry build
publish:
	@poetry publish --skip-existing
