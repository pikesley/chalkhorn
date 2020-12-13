all: style test clean

style: format
	python -m pylama

test:
	python -m pytest \
		--random-order \
		--cov \
		--verbose \
		--capture no \
		--exitfirst \
		--last-failed

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

clean:
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .pytest_cache -exec rm -fr {} \;
	@find . -depth -name .coverage -exec rm -fr {} \;
	@find . -name .DS_Store -delete

format: isort black

isort:
	python -m isort .

black:
	python -m black .
