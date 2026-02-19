# -*- coding: utf-8 -*-
import os, sys, json, re, argparse, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Mutator")

class MetabolismMutator:
    def __init__(self, repo_path=None):
        self.repo_path = Path(repo_path) if repo_path else Path(os.getcwd())
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def apply_mutation(self, strategy, intent, impact, roadmap_context):
        issue_body = os.getenv('ISSUE_BODY', 'Evolução')
        api_key = os.getenv('GROQ_API_KEY')
        
        try: import requests
        except: 
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import requests

        target_file = "app/application/services/task_runner.py"
        path = self.repo_path / target_file
        current_code = path.read_text(encoding='utf-8')
        
        # Pedimos o código E o resumo das alterações
        prompt = f"Missão: {issue_body}\nRoadmap: {roadmap_context}\nRetorne um JSON com: 'code' (código completo) e 'summary' (lista em markdown das mudanças em PT-BR).\nCÓDIGO ATUAL:\n{current_code}"
        
        try:
            resp = requests.post(self.groq_url, headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "Você é um Engenheiro de Software Senior. Responda APENAS com JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.1
                }, timeout=60)
            
            data = resp.json()
            content = json.loads(data['choices'][0]['message']['content'])
            new_code = content['code']
            summary = content.get('summary', "Evolução do DNA aplicada.")

            if "class TaskRunner" in new_code:
                path.write_text(new_code, encoding='utf-8')
                # Salvamos o resumo em um arquivo temporário para o Workflow ler
                (self.repo_path / "mutation_summary.txt").write_text(summary, encoding='utf-8')
                return {'success': True, 'mutation_applied': True}
        except Exception as e:
            logger.error(f"Erro: {e}")
        return {'success': False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', required=True); parser.add_argument('--intent', required=True)
    parser.add_argument('--impact', required=True); parser.add_argument('--roadmap-context', default="")
    args = parser.parse_args()
    res = MetabolismMutator().apply_mutation(args.strategy, args.intent, args.impact, args.roadmap_context)
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
            f.write(f"mutation_applied={str(res.get('mutation_applied', False)).lower()}\n")
