# 📝 Textos de Exemplo

Use estes textos para testar as diferentes features do **Azure AI Language**.

---

## 🎭 Teste de Sentimento — Texto Positivo

```
Adorei o atendimento da equipe de suporte! O problema foi resolvido em menos de
10 minutos. A interface do produto é intuitiva e fácil de usar. Recomendo
fortemente para todos que buscam qualidade e eficiência.
```

---

## 😞 Teste de Sentimento — Texto Negativo

```
Péssima experiência com o serviço. Fiquei mais de 2 horas esperando e ninguém
me atendeu. O produto veio com defeito e a política de troca é absurda.
Não recomendo de forma alguma. Pior compra que já fiz.
```

---

## 😐 Teste de Sentimento — Texto Misto

```
A comida do restaurante estava maravilhosa, especialmente o prato principal.
Porém, o atendimento deixou muito a desejar. O garçom foi grosseiro e demorou
quase 40 minutos para trazer o pedido. Voltaria pela comida, mas não pelo serviço.
```

---

## 🔒 Teste de PII — Dados Pessoais

```
Meu nome é Maria Oliveira e moro na Rua das Flores, 123 - São Paulo, SP.
Meu e-mail é maria.oliveira@email.com, meu telefone é (11) 0000-1234 e
meu CPF é 123.456.789-00. Preciso atualizar meu cadastro no sistema.
O número do meu cartão de crédito é 1111-1111-1111-1111.
```

---

## 🏷️ Teste de Entidades (NER)

```
A Empresa de Tecnologia anunciou em janeiro de 2026 que vai investir US$ 80 bilhões em
data centers para inteligência artificial. O CEO Satya Nadella disse em Seattle
que o Azure é a plataforma de nuvem que mais cresce no mundo. Outras empresas de tecnologia
também anunciaram investimentos similares na Europa e na Ásia.
```

---

## 🌍 Teste de Detecção de Idioma — Português

```
O Brasil é um país de dimensões continentais, com uma rica diversidade cultural
e natural. De norte a sul, encontramos paisagens únicas: a floresta amazônica,
o cerrado, a caatinga, a mata atlântica e os pampas gaúchos.
```

---

## 🌍 Teste de Detecção de Idioma — Inglês

```
The quick brown fox jumps over the lazy dog. Machine learning and artificial
intelligence are transforming how we interact with technology every day.
Cloud computing enables businesses to scale their operations globally.
```

---

## 🌍 Teste de Detecção de Idioma — Espanhol

```
La inteligencia artificial está revolucionando la forma en que las empresas
operan en todo el mundo. Los servicios en la nube permiten a las organizaciones
procesar grandes volúmenes de datos de manera eficiente y segura.
```

---

## 🔑 Teste Completo — Todas as Features

Este texto é ideal para testar **todas as 5 análises** de uma vez:

```
Ontem participei de um workshop incrível da Empresa XYZ em São Paulo sobre
Azure AI e inteligência artificial. O palestrante Joãozinho explicou como usar
os serviços de linguagem natural para processar textos automaticamente.

O evento foi excelente, mas a internet do local era muito lenta, o que
dificultou as demos ao vivo. No geral, saí muito satisfeito.

Para inscrição nos próximos eventos, envie um e-mail para
eventos@empresaxyz.com ou ligue para (11) 1111-2222. Meu contato pessoal
é fulano@email.com.
```

**O que esperar:**
- **Sentimento:** Misto (positivo sobre o evento, negativo sobre a internet)
- **Frases-Chave:** "workshop", "Empresa", "Azure AI", "inteligência artificial", "serviços de linguagem natural"
- **Entidades:** "Empresa" (Organization), "São Paulo" (Location), "João Mendes" (Person), "Azure AI" (Product)
- **PII:** E-mails e telefone detectados e mascarados
- **Idioma:** Português (pt)
