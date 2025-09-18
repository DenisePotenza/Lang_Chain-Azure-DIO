# 🤖 Agente Gerador de Testes Unitários (LangChain + Azure OpenAI)

Este projeto implementa um **agente de IA** que, a partir de um arquivo Python contendo funções, gera automaticamente testes unitários no formato **pytest**.  

O objetivo é praticar o uso do **LangChain** integrado ao **Azure OpenAI**, mostrando como LLMs podem auxiliar em tarefas de automação no desenvolvimento de software.

---

## 📂 Estrutura do Projeto

langchain-pytest-agent/  
├─ examples/  
│ ├─ init.py # para reconhecer a pasta como pacote  
│ └─ add.py # funções de exemplo (soma, subtração, divisão)  
├─ outputs/ # onde os testes gerados serão salvos  
├─ src/  
│ ├─ agent.py # script principal do agente  
│ ├─ prompt_templates.py # templates de prompt usados pelo LLM  
│ └─ utils.py # funções auxiliares (ex.: parsing de AST)  
├─ .env.example # modelo de variáveis de ambiente  
├─ README.md # este arquivo  
└─ requirements.txt # dependências do projeto  



## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/langchain-pytest-agent.git
cd langchain-pytest-agent
```

2. Crie e ative um ambiente virtual
```bash

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

4. Instale as dependências
```bash

pip install -r requirements.txt
```

5. Configure as variáveis de ambiente
Copie o arquivo .env.example para .env e preencha com suas credenciais do Azure OpenAI:
```ini

AZURE_OPENAI_API_KEY=coloque_sua_chave_aqui
AZURE_OPENAI_ENDPOINT=https://SEU-ENDPOINT.openai.azure.com/
AZURE_DEPLOYMENT_NAME=nome_da_implantacao
AZURE_OPENAI_API_VERSION=2023-12-01-preview
```

▶️ Uso do Agente
Gerar testes para o arquivo examples/add.py
```bash

python src/agent.py examples/add.py -o outputs
```

Se tudo estiver correto, será criado um arquivo de saída:
```bash

outputs/test_add.py
```

✅ Executando os Testes
Após gerar os testes, basta rodar o pytest normalmente:
```bash

pytest
```

Exemplo de saída esperada:
```bash

============================= test session starts =============================
collected 4 items

outputs/test_add.py ....                                               [100%]

============================== 4 passed in 0.02s ==============================
```

🧩 Exemplo de Funções (examples/add.py)
```python

def add(a, b):
    """Retorna a soma de dois números."""
    return a + b

def subtract(a, b):
    """Retorna a subtração (a - b)."""
    return a - b

def divide(a, b):
    """Retorna a divisão (a / b)."""
    return a / b
```

📌 Observações
* O agente usa LangChain + Azure OpenAI para gerar os testes.
* Atualmente, o projeto cobre funções simples (ex.: soma, subtração, divisão).
* O prompt foi desenhado para gerar testes determinísticos e prontos para rodar.
* É possível expandir para suportar:
    * pytest.mark.parametrize
    * Mocks (unittest.mock)
    * Cobertura de funções mais complexas

🚀 Próximos Passos
+ [ ] Integrar com GitHub Actions para rodar os testes automaticamente no CI/CD.
+ [ ] Permitir a geração de testes para classes, não apenas funções.
+ [ ] Adicionar exemplos de casos mais complexos.

👩‍💻 Autor
Projeto desenvolvido como parte de um desafio de curso, por Denise Potenza.
