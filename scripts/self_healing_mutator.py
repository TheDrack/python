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
    if not report_path.exists(): return

    try:
        report = json.loads(report_path.read_text(encoding='utf-8'))
        
        # 1. Tenta pegar falhas em testes executados
        failed_tests = [t for t in report.get('tests', []) if t.get('outcome') in ['failed', 'error']]
        
        # 2. Se não houver, tenta pegar falhas na COLETA (ImportErrors)
        if not failed_tests:
            failed_tests = [c for c in report.get('collectors', []) if c.get('result') == 'error']
            if not failed_tests: return
            
            # Trata erro de coleta
            error_msg = failed_tests[0].get('longrepr', 'Erro de importação')
            nodeid = failed_tests[0].get('nodeid', 'desconhecido')
        else:
            error_msg = failed_tests[0].get('call', {}).get('longrepr', 'Erro de teste')
            nodeid = failed_tests[0].get('nodeid', '')

        file_to_fix = nodeid.split('::')[0] if '::' in nodeid else nodeid
        path = Path(file_to_fix)
        if not path.exists(): return

        current_code = path.read_text(encoding='utf-8')
        system_p = "Você é o Engenheiro de Auto-Cura do JARVIS. Corrija o arquivo para que ele pare de dar erro. Responda APENAS JSON: {'code': str, 'explanation': str}"
        user_p = f"ARQUIVO: {file_to_fix}\nERRO:\n{error_msg}\nCÓDIGO ATUAL:\n{current_code}"

        solution = core.ask_jarvis(system_p, user_p)
        new_code = solution.get('code', '')
        
        if len(new_code.strip()) > 10:
            path.write_text(new_code, encoding='utf-8')
            print(f"✅ Corrigido: {file_to_fix}")

    except Exception as e:
        print(f"❌ Erro Mutator: {e}")

if __name__ == "__main__":
    heal()
