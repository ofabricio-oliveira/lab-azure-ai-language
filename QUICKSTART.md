# ⚡ RESUMO RÁPIDO (5 minutos)

Para quem **já tem tudo pronto** (Python, Azure AI Language configurado).

---

## 📋 Requisitos

- Python 3.11 ou superior
- Recurso Azure AI Language criado (endpoint + key)
- VS Code (opcional)

---

## 🚀 Passos

### 1. Abra a pasta do projeto

```powershell
cd C:\seu\caminho\project-03-text-analytics
```

### 2. Crie ambiente virtual e instale dependências

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure .env

```powershell
copy .env.example .env
```

```bash
# macOS/Linux
cp .env.example .env
```

Abra `.env` e preencha:

```env
AZURE_LANGUAGE_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com
AZURE_LANGUAGE_KEY=sua-chave-aqui
```

### 4. Rode o servidor

```bash
uvicorn app.main:app --reload
```

Saída esperada:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 5. Teste no navegador

1. Abra: `http://localhost:8000`
2. Cole um texto no campo
3. Marque as análises desejadas: **Sentimento**, **Frases-Chave**, **Entidades (NER)**, **PII**, **Idioma**
4. Clique em **"Analisar"**
5. Veja os resultados: sentimento com barras, frases-chave como tags, entidades e PII em tabelas
6. Clique em **"Baixar JSON"** para exportar

✅ **Pronto!**

---

## 🆘 Precisa de ajuda?

- **Guia completo:** [COMECE AQUI (START_HERE.md)](START_HERE.md)
- **Documentação:** [README.md](README.md)
