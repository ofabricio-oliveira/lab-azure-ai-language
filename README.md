# 🔤 Analisador de Textos com Azure AI Language

[![License: MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11-3.12](https://img.shields.io/badge/python-3.11--3.12-blue.svg)](https://www.python.org/downloads/)

**Lab prático:** Aprenda a integrar as features de **Text Analytics** do **Azure AI Language** com FastAPI — incluindo **Análise de Sentimento**, **Extração de Frases-Chave**, **Reconhecimento de Entidades (NER)**, **Detecção de PII** e **Detecção de Idioma**.

---

## 📋 O que você vai fazer

1. ✅ Colar ou digitar um texto no navegador
2. ✅ Escolher quais análises executar (uma, várias ou todas)
3. ✅ **Sentimento** → ver se o texto é positivo, negativo, neutro ou misto
4. ✅ **Frases-Chave** → extrair os termos mais relevantes
5. ✅ **Entidades (NER)** → identificar pessoas, locais, organizações, datas
6. ✅ **PII** → detectar dados pessoais e gerar versão mascarada do texto
7. ✅ **Idioma** → detectar o idioma predominante do texto
8. ✅ Baixar resultado completo em JSON

---

## 🤖 O que é o Azure AI Language?

O [Azure AI Language](https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview) é um serviço de IA do Azure que fornece recursos de **Processamento de Linguagem Natural (NLP)** para compreender e analisar textos. Ele oferece features **preconfigured** (pré-treinadas) prontas para uso, sem necessidade de treinar modelos.

Neste lab utilizamos cinco features:

| Feature | O que faz | Exemplo de saída |
|---------|-----------|------------------|
| **Sentiment Analysis** | Identifica sentimento positivo, negativo, neutro ou misto | "positivo (95%)" |
| **Key Phrase Extraction** | Extrai os termos e conceitos mais relevantes | ["Azure", "inteligência artificial"] |
| **Named Entity Recognition (NER)** | Detecta e categoriza entidades no texto | "Microsoft" → Organization |
| **PII Detection** | Identifica dados pessoais e gera texto mascarado | "joao@email.com" → "***@***.com" |
| **Language Detection** | Detecta o idioma predominante entre 100+ idiomas | "Portuguese (pt) — 100%" |

> **Referências oficiais:**
> - [Sentiment Analysis](https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview)
> - [Key Phrase Extraction](https://learn.microsoft.com/en-us/azure/ai-services/language-service/key-phrase-extraction/overview)
> - [Named Entity Recognition](https://learn.microsoft.com/en-us/azure/ai-services/language-service/named-entity-recognition/overview)
> - [PII Detection](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview)
> - [Language Detection](https://learn.microsoft.com/en-us/azure/ai-services/language-service/language-detection/overview)

### Este app vs. Language Studio

O Azure também oferece o [Language Studio](https://language.cognitive.azure.com/), que é uma interface web do próprio Azure para testar as features diretamente no navegador, sem escrever código.

**A diferença é que este lab é um app Python próprio** que consome a mesma API por trás do Studio — via SDK — mostrando como integrar o Azure AI Language em uma aplicação real. No Studio você testa; aqui você aprende a construir.

---

## 💡 Exemplo de Caso de Uso

Imagine que sua empresa recebe **centenas de avaliações de clientes por dia** — em e-mails, formulários, redes sociais. O time de Customer Experience precisa entender rapidamente:

- **O sentimento geral é positivo ou negativo?** → Análise de Sentimento
- **Quais são os temas mais mencionados?** → Frases-Chave
- **Quais produtos, pessoas e locais aparecem?** → NER
- **Alguma avaliação contém dados pessoais (e-mail, CPF, telefone)?** → PII
- **Em que idioma a mensagem foi escrita?** → Detecção de Idioma

Com este lab, basta colar o texto, selecionar as análises, clicar em "Analisar" e ter as respostas em segundos. É isso que você vai aprender: **análise inteligente de textos com IA do Azure**.

---

## 🛠️ Requisitos

- **Seu computador:** Windows 10/11 ou macOS
- **Python:** 3.11 ou 3.12 (⚠️ NÃO validado com 3.13+ ou 3.14+)
- **Conta Azure:** Com recurso Azure AI Language criado
- **VS Code:** Recomendado (opcional)
- **Internet:** Conexão estável

---

## 📖 Como Começar

| Guia | Tempo | Indicado para |
|------|-------|---------------|
| [COMECE AQUI (START_HERE.md)](START_HERE.md) | ~1h | Primeira vez? Comece aqui! |
| [RESUMO RÁPIDO (QUICKSTART.md)](QUICKSTART.md) | ~5 min | Já tem tudo configurado? Rode rápido |

---

## 🎯 Caso esteja começando do zero, vá por aqui:

👉 Leia **[COMECE AQUI (START_HERE.md)](START_HERE.md)** para o guia passo a passo completo!

---

## 🚀 Caso Já Tenha Noções do Funcionamento, Veja o Resumo

Para quem já tem tudo configurado, em resumo será:

```bash
# Clonar o repositório
git clone https://github.com/SEU_USUARIO/lab-azure-ai-language.git
cd lab-azure-ai-language

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
# ⚠️ Edite .env e adicione suas credenciais do Azure

# Rodar o servidor
uvicorn app.main:app --reload

# Abra no navegador
# http://localhost:8000
```

---

## 📐 Arquitetura

```
Usuário
  │
  │  1. Cola texto no formulário
  ▼
┌──────────────────────────┐
│  Frontend (HTML/CSS)     │
│  - Textarea para texto   │
│  - Checkboxes: escolher  │
│    Sentimento, NER,      │
│    PII, Key Phrases,     │
│    Idioma                │
└──────────┬───────────────┘
           │ 2. POST /analyze
           ▼
┌──────────────────────────┐
│  FastAPI Backend         │
│  ├─ Validação            │  3. Valida texto
│  ├─ Language Service     │  4. Chama Azure (1x por feature)
│  ├─ Normalizer           │  5. Normaliza resultados
│  └─ Exporter             │  6. Gera JSON (download)
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Azure AI Language       │
│  (Text Analytics API)    │
│  - analyze_sentiment     │
│  - extract_key_phrases   │
│  - recognize_entities    │
│  - recognize_pii_entities│
│  - detect_language       │
└──────────────────────────┘
```

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` baseado em `.env.example`:

```env
AZURE_LANGUAGE_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com
AZURE_LANGUAGE_KEY=sua-chave-aqui
```

| Variável | Obrigatória | Descrição | Default |
|----------|-------------|-----------|---------|
| `AZURE_LANGUAGE_ENDPOINT` | ✅ | URL do recurso Azure AI Language | — |
| `AZURE_LANGUAGE_KEY` | ✅ | Chave de acesso (KEY 1 ou KEY 2) | — |
| `MAX_TEXT_LENGTH` | ❌ | Limite de caracteres por análise | `5000` |

⚠️ **Pontos críticos:**
- ✅ `AZURE_LANGUAGE_ENDPOINT` **NÃO** deve terminar com `/`
- ✅ A key deve ser copiada exatamente do portal Azure
- ✅ **Não commite o `.env`!** Ele já está no `.gitignore`

---

## 🏗️ Estrutura do Código

```
lab-azure-ai-language/
├── app/
│   ├── main.py                      # FastAPI — rotas e app principal
│   ├── config.py                    # Configuração via .env
│   ├── models.py                    # Pydantic models (SentimentResult, PiiResult, etc.)
│   ├── services/
│   │   └── language_service.py      # Integração com Azure AI Language SDK (5 features)
│   ├── utils/
│   │   ├── normalizer.py            # Normalização dos resultados do SDK
│   │   └── exporter.py              # Geração de JSON para download
│   ├── templates/
│   │   ├── index.html               # Formulário de entrada (texto + checkboxes)
│   │   └── result.html              # Resultado de todas as análises
│   └── static/
│       └── styles.css               # Estilos
├── sample_texts/                    # Textos de exemplo para testar
│   └── README.md                    # Guia dos textos de exemplo
├── tests/
│   ├── test_normalizer.py           # Testes do normalizer (todas as features)
│   ├── test_exporter.py             # Testes do exporter JSON
│   └── test_main.py                 # Testes das rotas e validações
├── .env.example                     # Exemplo de variáveis de ambiente
├── .gitignore
├── Makefile                         # Atalhos: make run, make test, make clean
├── requirements.txt
├── QUICKSTART.md                    # Resumo rápido (~5 min)
├── START_HERE.md                    # Guia passo a passo completo (~1h)
├── LICENSE                          # MIT
└── README.md                        # Este arquivo
```

**Fluxo de dados:**

1. Usuário cola texto no `index.html` e seleciona as análises (checkboxes)
2. `main.py` recebe e valida (texto não vazio, tamanho máximo, pelo menos 1 feature)
3. `language_service.py` chama cada feature selecionada no Azure AI Language
4. `normalizer.py` converte os objetos do SDK em Pydantic models
5. `result.html` exibe tudo: sentimento com barras, frases-chave como tags, entidades e PII em tabelas, idioma detectado
6. Download: JSON com o resultado completo

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest tests/ -v

# Ou via Makefile
make test
```

São **55 testes** cobrindo:
- Normalização de sentimento (positivo, negativo, neutro, misto, múltiplas frases)
- Extração de frases-chave (com e sem dados)
- Reconhecimento de entidades (categorias, subcategorias, confiança)
- Detecção de PII (e-mail, CPF, telefone, texto mascarado)
- Detecção de idioma (português, inglês, espanhol)
- Build do resultado combinado (todas features, parcial, sem dados)
- Geração de JSON (valid JSON, Unicode, exclude_none)
- Rotas HTTP (index, validação de texto, validação de features, 404)

---

## 📚 Conceitos Aprendidos

✅ Integração com Azure AI Language (Text Analytics)
✅ 5 features preconfigured: Sentiment, Key Phrases, NER, PII, Language Detection
✅ SDK `azure-ai-textanalytics` com `TextAnalyticsClient`
✅ Processamento de Linguagem Natural (NLP) com serviços de IA na nuvem
✅ Normalização de dados retornados por APIs de IA
✅ API com FastAPI
✅ Validação de entrada e tratamento de erros
✅ Variáveis de ambiente e configuração segura

---

## ❌ Troubleshooting

### Erro: "Azure AI Language not configured"

**Verificar:**
- ✅ Arquivo `.env` existe na raiz do projeto
- ✅ `AZURE_LANGUAGE_ENDPOINT` e `AZURE_LANGUAGE_KEY` estão preenchidos
- ✅ Sem espaços extras ou aspas nos valores

### Erro: "403 Forbidden" ou "401 Unauthorized"

**Verificar:**
- ✅ A key está correta (copie novamente do portal)
- ✅ O endpoint corresponde ao recurso correto

### Erro: "Text is empty" ou "Text too long"

**Verificar:**
- ✅ O campo de texto não está vazio
- ✅ O texto não excede 5.000 caracteres (configurável via `MAX_TEXT_LENGTH`)

### Nenhuma análise selecionada

**Verificar:**
- ✅ Marque pelo menos um checkbox de análise antes de clicar "Analisar"

---

## ⚠️ Aviso Importante sobre Segurança

Este projeto **NÃO possui** as seguintes proteções necessárias para produção:

- 🔓 **Sem autenticação/autorização** — qualquer pessoa com acesso à URL pode usar
- 🔑 **Chave da API em .env** — em produção, use Azure Key Vault ou Managed Identity
- 💾 **Dados em memória** — reiniciar o servidor perde todos os resultados
- 🌐 **Sem HTTPS** — em produção, sempre use HTTPS com certificado válido
- 🛡️ **Sem rate limiting** — sem proteção contra uso excessivo

**Para uso em produção**, considere: autenticação (Azure AD / OAuth), HTTPS, banco de dados, Azure Key Vault para secrets, rate limiting, logging centralizado e monitoramento.

---

## ⚠️ Disclaimer

> **Esta solução foi desenvolvida com finalidade exclusivamente laboratorial e educacional.**
>
> O objetivo deste projeto é demonstrar as capacidades do **Azure AI Language** — especificamente as features Text Analytics (Sentiment, Key Phrases, NER, PII e Language Detection) — e não ensinar boas práticas de desenvolvimento Python ou engenharia de software.
>
> O uso em ambientes de produção deve considerar critérios adicionais de segurança, desempenho, conformidade e manutenção, que **não estão contemplados** neste projeto.

---

## 📄 Licença

MIT. Veja [LICENSE](LICENSE).

---

**Desenvolvido com ❤️ para aprendizado — 2026**
