# -*- coding: utf-8 -*-
import argparse
import os
import sys
import json
import re
from pathlib import Path
from app.application.services.metabolism_core import MetabolismCore

def evolve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', required=True)
    parser.add_argument('--intent', required=True)
    parser.add_argument('--impact', required=True)
    parser.add_argument('--roadmap-context', default="")
    args = parser.parse_args()

    core = MetabolismCore()
    issue_body = os.getenv('ISSUE_BODY', 'Nova funcionalidade')

    # --- PASSO 1: ARQUITETURA ---
    system_arch = (
        "Você é o Arquiteto Senior do ecossistema JARVIS.\n"
        "Responda EXCLUSIVAMENTE em formato JSON.\n"
        "Determine o arquivo alvo para a implementação da capacidade.\n"
        "Estrutura: {\"target_file\": \"caminho/do/arquivo.py\", \"reason\": \"motivo\"}"
    )

    user_arch = f"MISSÃO: {issue_body}\nCONTEXTO: {args.roadmap_context}"

    try:
        print(f"🧠 JARVIS analisando arquitetura para: {issue_body}...")
        arch_decision = core.ask_jarvis(system_arch, user_arch)
        target_file = arch_decision.get('target_file')

        if not target_file:
            raise ValueError("O Arquiteto não definiu um 'target_file'.")

        path = Path(target_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        current_code = path.read_text(encoding='utf-8') if path.exists() else "# Novo componente JARVIS"

        # --- PASSO 2: ENGENHARIA (Com proteção de JSON) ---
        system_eng = (
            "Você é o Engenheiro Senior do JARVIS.\n"
            "Sua resposta deve ser um JSON puro e válido.\n"
            "O campo 'code' deve conter o código completo. "
            "IMPORTANTE: Use escapes de string adequados (\\n para quebras de linha, \\\" para aspas) para garantir que o JSON não quebre."
        )

        user_eng = f"""
        OBJETIVO: {issue_body}
        ARQUIVO: {target_file}
        CÓDIGO ATUAL:
        {current_code}

        Retorne EXCLUSIVAMENTE este JSON:
        {{
          "code": "string_do_codigo_completo",
          "summary": "resumo_das_mudancas"
        }}
        """

        print(f"🧬 Gerando mutação de DNA em: {target_file}")
        mutation = core.ask_jarvis(system_eng, user_eng)

        # Extração segura do código para evitar erros de parser
        new_code = mutation.get('code', '')
        summary = mutation.get('summary', 'Evolução aplicada.')

        if len(new_code.strip()) > 20:
            # Garantimos que quebras de linha literais (se houver) sejam tratadas
            path.write_text(new_code, encoding='utf-8')
            Path("mutation_summary.txt").write_text(str(summary), encoding='utf-8')
            print(f"✅ Evolução Concluída: {target_file}")
        else:
            print("❌ Erro: Código gerado muito curto ou inválido.")
            sys.exit(1)

    except Exception as e:
        # Tenta capturar se o erro foi de parser JSON para dar um feedback melhor
