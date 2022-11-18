clean:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
format:
	isort mul
	black mul
lint: format
	flake8 mul
