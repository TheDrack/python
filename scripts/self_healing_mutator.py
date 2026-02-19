# -*- coding: utf-8 -*-
import argparse, json, sys, os
from pathlib import Path
from app.application.services.metabolism_core import MetabolismCore

def heal():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', required=True)
    args = parser.parse_args()

    core = MetabolismCore()
    report_path = Path(args.report)
    
    if not report_path.exists():
        print(f"Erro: Relatório {args.report} não encontrado.")
        sys.exit(1)

    try:
        report = json.loads(report_path.read_text(encoding='utf-8'))
        failed_tests = [t for t in report.get('tests', []) if t.get('outcome') == 'failed']
        
        if not failed_tests:
            print("Nenhum erro detectado no relatório JSON.")
            return

        # Foco no primeiro erro crítico detectado
        error_detail = failed_tests[0]
        nodeid = error_detail.get('nodeid', '')
        file_to_fix = nodeid.split('::')[0] if '::' in nodeid else nodeid
        
        error_msg = error_detail.get('call', {}).get('longrepr', 'Detalhes do erro ausentes.')
        
        path = Path(file_to_fix)
        if not path.exists():
            print(f"Arquivo alvo {file_to_fix} não existe fisicamente.")
            sys.exit(1)

        current_code = path.read_text(encoding='utf-8')

        system_p = (
            "Você é o Engenheiro de Auto-Cura do JARVIS. Sua missão é analisar o erro do Pytest "
            "e corrigir o código fonte para que os testes passem. Mantenha a lógica original, "
            "corrigindo apenas o bug. Responda APENAS um JSON com os campos 'code' (string com o "
            "arquivo completo atualizado) e 'explanation' (breve descrição da correção)."
        )
        
        user_p = f"ARQUIVO: {file_to_fix}\n\nERRO DO PYTEST:\n{error_msg}\n\nCÓDIGO ATUAL:\n{current_code}"

        print(f"🛠️ Solicitando correção para: {file_to_fix}")
        solution = core.ask_jarvis(system_p, user_p)
        
        new_code = solution.get('code', '')
        if len(new_code.strip()) > 10:
            path.write_text(new_code, encoding='utf-8')
            print(f"✅ Sucesso: {file_to_fix} foi reescrito com a tentativa de correção.")
            print(f"📝 Explicação: {solution.get('explanation', 'Sem explicação.')}")
        else:
            print("❌ Falha: O código retornado pela IA é inválido ou curto demais.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Falha crítica no Self-Healing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    heal()
