.PHONY: runparte1 testparte1

# Comando para iniciar la aplicación de la parte1
run1:
	cd parte1/src && fastapi dev app/main.py

# Comando para testear la aplicación de la parte1
test1:
	cd parte1/src && pytest tests -vv --cov=app --cov-report=term-missing --cov-branch
