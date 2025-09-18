import os
import argparse
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

from prompt_templates import BASE_SYSTEM_PROMPT, build_prompt
from utils import extract_functions, file_path_to_module


def generate_tests_for_file(input_path: str, output_dir: str = 'outputs') -> str:
    # carrega .env
    load_dotenv()

    with open(input_path, 'r', encoding='utf-8') as f:
        src = f.read()

    functions = extract_functions(src)
    module_import = file_path_to_module(input_path)

    prompt = build_prompt(module_import, src, functions)

    # Configure ambiente para Azure OpenAI compatível com LangChain
    # (aceitamos variáveis via .env - se preferir, configure nas variáveis do sistema)
    # As variáveis esperadas são: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME

    # Algumas bibliotecas usam OPENAI_* env vars quando OPENAI_API_TYPE=azure; aqui fazemos set por garantia
    if os.getenv('AZURE_OPENAI_ENDPOINT'):
        os.environ.setdefault('OPENAI_API_BASE', os.getenv('AZURE_OPENAI_ENDPOINT'))
    if os.getenv('AZURE_OPENAI_API_KEY'):
        os.environ.setdefault('OPENAI_API_KEY', os.getenv('AZURE_OPENAI_API_KEY'))
    if os.getenv('AZURE_OPENAI_API_VERSION'):
        os.environ.setdefault('OPENAI_API_VERSION', os.getenv('AZURE_OPENAI_API_VERSION'))

    deployment = os.getenv('AZURE_DEPLOYMENT_NAME') or os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    if not deployment:
        raise ValueError('Defina AZURE_DEPLOYMENT_NAME (nome da sua implantação no Azure OpenAI) no .env')

    # Inicializa o modelo com temperatura baixa para gerar saídas mais determinísticas
    llm = AzureChatOpenAI(azure_deployment=deployment, temperature=0)

    system_message = SystemMessage(content=BASE_SYSTEM_PROMPT)
    human_message = HumanMessage(content=prompt)

    resp = llm([system_message, human_message])
    test_code = resp.content

    # salva o arquivo de testes
    os.makedirs(output_dir, exist_ok=True)
    module_basename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"test_{module_basename}.py")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(test_code)

    return output_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gerador automático de testes com LangChain + Azure OpenAI')
    parser.add_argument('input', help='Caminho para o arquivo .py de entrada')
    parser.add_argument('-o', '--output', default='outputs', help='Diretório de saída para o arquivo de testes')
    args = parser.parse_args()

    out = generate_tests_for_file(args.input, args.output)
    print(f'Testes gerados em: {out}')