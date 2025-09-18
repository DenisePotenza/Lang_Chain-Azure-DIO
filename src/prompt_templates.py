def build_prompt(module_import_path: str, module_source: str, functions: list) -> str:
    """
    Constrói o prompt que será enviado ao modelo de linguagem,
    já incluindo a linha de import com todas as funções extraídas.
    """
    # Lista das funções encontradas no módulo
    function_names = [f["name"] for f in functions]
    imports_line = f"from {module_import_path} import {', '.join(function_names)}"

    # Montagem do prompt
    parts = [
        f"Módulo: {module_import_path}",
        f"\nCódigo do módulo:\n```py\n{module_source}\n```\n",
        f"Import necessário para os testes:\n{imports_line}\n"
    ]

    for f in functions:
        parts.append(
            f"Função: {f['name']}\n"
            f"Assinatura: ({', '.join(f['args'])})\n"
            f"Docstring: {f['docstring'] or ''}\n"
            f"Fonte:\n```py\n{f['source']}\n```\n"
        )

    parts.append("Gere agora o arquivo de testes completo, atendendo às regras do sistema. "
                 "Retorne apenas o código Python do arquivo de testes.")

    return "\n".join(parts)