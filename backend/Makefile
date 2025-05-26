# Makefile para automatizar testing
.PHONY: test test-unit test-integration test-cov install-test clean

# Instalar dependencias de testing
install-test:
	pip install -r requirements-test.txt

# Ejecutar todas las pruebas
test:
	pytest

# Ejecutar solo pruebas unitarias
test-unit:
	pytest -m unit

# Ejecutar solo pruebas de integración
test-integration:
	pytest -m integration

# Ejecutar con cobertura de código
test-cov:
	pytest --cov=routes --cov-report=html --cov-report=term

# Ejecutar pruebas específicas
test-auth:
	pytest tests/test_auth.py -v

test-dates:
	pytest tests/test_dates.py -v

test-users:
	pytest tests/test_users.py -v

# Ejecutar pruebas en modo watch (requiere pytest-watch)
test-watch:
	ptw

# Limpiar archivos de cobertura
clean:
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

# Ejecutar pruebas con diferentes niveles de verbosidad
test-verbose:
	pytest -vvv

test-quiet:
	pytest -q