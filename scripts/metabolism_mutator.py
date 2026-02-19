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
        
        try:
            import requests
        except ImportError:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import requests

        target_file = "app/application/services/task_runner.py"
        path = self.repo_path / target_file
        
        if not path.exists():
            logger.error(f"Arquivo não encontrado: {target_file}")
            return {'success': False}

        current_code = path.read_text(encoding='utf-8')
        
        prompt = f"Missão: {issue_body}\nRoadmap: {roadmap_context}\nRetorne um JSON com: 'code' (string com código completo) e 'summary' (string markdown das mudanças).\nCÓDIGO ATUAL:\n{current_code}"
        
        try:
            resp = requests.post(self.groq_url, headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "Você é um Engenheiro Senior. Responda APENAS com JSON puro. O campo 'summary' deve ser uma string única."},
                        {"role": "user", "content": prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.1
                }, timeout=60)
            
            data = resp.json()
            content_raw = data['choices'][0]['message']['content']
            
            # Converte o conteúdo para dicionário de forma segura
            content = json.loads(content_raw)
            
            new_code = content.get('code', "")
            summary = content.get('summary', "")

            # Se a IA enviou o sumário como lista, converte para string markdown
            if isinstance(summary, list):
                summary = "\n".join([f"- {item}" for item in summary])

            if "class TaskRunner" in new_code:
                path.write_text(new_code, encoding='utf-8')
                # Garante que o sumário seja salvo como string
                (self.repo_path / "mutation_summary.txt").write_text(str(summary), encoding='utf-8')
                logger.info(f"DNA mutado com sucesso.")
                return {'success': True}
        except Exception as e:
            logger.error(f"Falha na mutação: {e}")
        return {'success': False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', required=True)
    parser.add_argument('--intent', required=True)
    parser.add_argument('--impact', required=True)
    parser.add_argument('--roadmap-context', default="")
    args = parser.parse_args()
    
    mutator = MetabolismMutator()
    res = mutator.apply_mutation(args.strategy, args.intent, args.impact, args.roadmap_context)
    # Se falhar, forçamos o exit code 0 para o workflow não travar, 
    # mas o git status vazio impedirá a PR se nada mudar.
    sys.exit(0)
