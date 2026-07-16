# 🎯 GUIA PASSO A PASSO COMPLETO — COMECE AQUI!

## 👋 Bem-vindo!

Você está prestes a construir algo incrível! 🚀

Este é o guia completo para aprender como **integrar Azure AI Language com Python**. Vamos criar um **analisador inteligente de textos** que usa IA para detectar sentimento, extrair frases-chave, reconhecer entidades, identificar dados pessoais (PII) e detectar idiomas!

Perfeito para aprender, experimentar e criar algo legal pro seu portfólio. 💻

---

## 📋 O Que Você Vai Fazer

1. ✅ Instalar Python e dependências
2. ✅ Criar recurso Azure AI Language
3. ✅ Rodar o projeto localmente
4. ✅ Testar com textos de exemplo

**Tempo total estimado:** ~1 hora (incluindo leitura)

---

## 🚀 ETAPA 1: Preparar o Ambiente (15 minutos)

### 1.1 — Instalar Python

1. Acesse: `https://www.python.org/downloads/`
2. ⚠️ **CRÍTICO:** Baixe **Python 3.11.x ou superior**
3. Execute o instalador
4. ⚠️ **Marque "Add Python to PATH"** na primeira tela
5. Clique em **"Install Now"**

**Validar:**

```powershell
python --version
# Deve mostrar: Python 3.11.x ou superior
```

---

### 1.2 — Instalar Git (opcional, para clonar)

1. Acesse: `https://git-scm.com/download/win`
2. Baixe e instale com opções padrão

---

## 💻 ETAPA 2: Baixar e Configurar o Projeto (10 minutos)

### 2.1 — Obter o projeto

```powershell
# Se tem Git:
git clone https://github.com/ofabricio-oliveira/lab-azure-ai-language.git
cd lab-azure-ai-language

# OU: baixe o ZIP e extraia
```

### 2.2 — Criar ambiente virtual

```powershell
# Windows
python -m venv venv
venv\Scripts\activate
```

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.3 — Instalar dependências

```bash
pip install -r requirements.txt
```

Aguarde ~2 minutos.

---

## 🔑 ETAPA 3: Criar o Recurso no Azure (20 minutos)

### 3.1 — Acessar Azure Portal

1. Abra: `https://portal.azure.com`
2. Faça login com sua conta Microsoft

### 3.2 — Criar recurso Language

1. Na barra de busca, digite: **"Language"**
2. Clique em **"Language service"** (ou use este link direto: [Criar recurso Language](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics))
3. Na tela "Select additional features", clique em **"Continue to create your resource"**
4. Preencha:
   - **Subscription:** Selecione sua assinatura
   - **Resource group:** Clique "Create new" → `language-lab-rg`
   - **Region:** `East US` (boa disponibilidade)
   - **Name:** `meu-language-lab-2026` (nome único)
   - **Pricing tier:** `Free F0` (para lab — 5.000 chamadas/mês grátis)
5. Marque o checkbox de **Responsible AI Notice**
6. Clique **"Review + create"** → **"Create"**
7. Aguarde ~1 minuto → **"Go to resource"**

### 3.3 — Obter Endpoint e Key

1. No recurso, menu esquerdo: **"Keys and Endpoint"**
2. Copie:
   - **Endpoint:** `https://meu-language-lab-2026.cognitiveservices.azure.com/`
   - **KEY 1:** Clique no ícone de copiar

### 3.4 — Configurar .env

Aqui precisaremos ter um arquivo chamado `.env`, então copie o arquivo `.env.example` e renomeie para `.env`.

```powershell
copy .env.example .env
```

```bash
# macOS/Linux
cp .env.example .env
```

Edite o `.env`:

```env
AZURE_LANGUAGE_ENDPOINT=https://meu-language-lab-2026.cognitiveservices.azure.com
AZURE_LANGUAGE_KEY=sua-chave-copiada-aqui
```
Após editar o arquivo, salve-o.

⚠️ **O endpoint NÃO deve terminar com `/`**

---

## 🎮 ETAPA 4: Rodar o Projeto (5 minutos)

```bash
uvicorn app.main:app --reload
```

Saída esperada:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

✅ O servidor está rodando!

---

## 🧪 ETAPA 5: Testar (10 minutos)

### 5.1 — Abrir no navegador

1. Abra: `http://localhost:8000`
2. Você verá o formulário com:
   - Um campo de texto grande (textarea)
   - 5 checkboxes para as análises
   - Um botão "Analisar"

### 5.2 — Testar com texto de exemplo

Cole o seguinte texto no campo:

```
Adorei o atendimento da equipe Microsoft em São Paulo! O suporte foi excelente
e resolveu meu problema rapidamente. Meu nome é João Silva, meu e-mail é
joao.silva@email.com e meu telefone é (11) 99999-0000. Recomendo fortemente
para todos que precisam de ajuda técnica.
```

### 5.3 — Selecionar análises

Deixe **todos os 5 checkboxes marcados** (já vêm marcados por padrão).

### 5.4 — Clicar "Analisar"

Aguarde alguns segundos. Você verá a página de resultado com:

1. **🌍 Idioma** → Portuguese (pt) com alta confiança
2. **🎭 Sentimento** → Positivo, com barras mostrando o score
3. **🔑 Frases-Chave** → Tags como "atendimento", "equipe Microsoft", "São Paulo"
4. **🏷️ Entidades (NER)** → Tabela: "Microsoft" (Organization), "São Paulo" (Location), "João Silva" (Person)
5. **🔒 PII** → Texto mascarado + tabela mostrando e-mail e telefone detectados

### 5.5 — Baixar resultado

Clique em **"Baixar JSON"** para obter o resultado completo em formato JSON.

✅ **Funcionou? Parabéns!**

---

## ✅ CHECKLIST FINAL

- [ ] Python instalado e funcionando
- [ ] Recurso Azure AI Language criado
- [ ] Endpoint e key configurados no `.env`
- [ ] Servidor rodando (`http://localhost:8000`)
- [ ] Teste com texto funcionou (todas as 5 análises)
- [ ] Download do JSON funcionou

---

## 🎉 PARABÉNS!

Você completou o lab com sucesso:

✅ Integrou com Azure AI Language (Text Analytics)
✅ Analisou sentimento, frases-chave, entidades, PII e idioma
✅ Gerou export em JSON
✅ Criou um projeto de portfólio!

---

## 📚 Próximos Passos

1. **Experimente:** Teste com textos em diferentes idiomas (inglês, espanhol, etc.)
2. **Compare:** Ative/desative features individuais e veja a diferença
3. **PII:** Teste com textos contendo CPF, e-mail, cartão de crédito, etc.
4. **Sentimento:** Teste com avaliações positivas e negativas
5. **Explore:** Veja os textos de exemplo em `sample_texts/README.md`
6. **Compartilhe:** Adicione ao seu GitHub e portfólio

---

## 🆘 Precisa de Ajuda?

- **Documentação completa:** [README.md](README.md)
- **Resumo rápido:** [QUICKSTART.md](QUICKSTART.md)
- **Mais conteúdo:** [fabricio.tech](https://fabricio.tech)

---

**Desenvolvido com ❤️ para aprendizado — 2026**

📌 Mais conteúdo em [fabricio.tech](https://fabricio.tech)
