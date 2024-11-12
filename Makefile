.PHONY: run1 test1

# Comando para iniciar la aplicación de la parte1
run1:
	cd parte1/src && fastapi dev app/main.py

# Comando para testear la aplicación de la parte1
test1:
	cd parte1/src && pytest tests -vv --cov=app --cov-report=term-missing --cov-branch

run2:
	cd parte2/src && PYTHONPATH=. python3 app/main.py

test2:
	cd parte2/src && pytest tests -vv --cov=app --cov-report=term-missing --cov-branch