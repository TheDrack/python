# -*- coding: utf-8 -*-
import argparse
import os
import sys
import json
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
        "Você é o Arquiteto Senior do JARVIS. Responda APENAS JSON.\n"
        "Determine o arquivo alvo: {'target_file': 'path/file.py', 'reason': 'motivo'}"
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

        # --- PASSO 2: ENGENHARIA ---
        system_eng = (
            "Você é o Engenheiro Senior do JARVIS.\n"
            "Retorne APENAS um JSON válido. O campo 'code' deve conter o código completo.\n"
            "Use \\n para quebras de linha e \\\" para aspas internas."
        )
        user_eng = f"OBJETIVO: {issue_body}\nARQUIVO: {target_file}\nCÓDIGO ATUAL:\n{current_code}"

        print(f"🧬 Gerando mutação de DNA em: {target_file}")
        mutation = core.ask_jarvis(system_eng, user_eng)

        new_code = mutation.get('code', '')
        summary = mutation.get('summary', 'Evolução aplicada.')

        if len(new_code.strip()) > 20:
            path.write_text(new_code, encoding='utf-8')
            Path("mutation_summary.txt").write_text(str(summary), encoding='utf-8')
            print(f"✅ Evolução Concluída: {target_file}")
        else:
            print("❌ Erro: Código gerado insuficiente.")
            sys.exit(1)

    except Exception as e:
        # CORREÇÃO: Bloco preenchido para evitar IndentationError
        print(f"❌ Falha Crítica no Ciclo de Evolução: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    evolve()
