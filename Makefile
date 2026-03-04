.PHONY: install run test clean

# Instalar dependências
install:
	pip install -r requirements.txt

# Rodar o servidor local
run:
	uvicorn app.main:app --reload

# Rodar testes
test:
	pytest tests/ -v

# Limpar cache Python
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cache cleaned."
