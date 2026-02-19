# -*- coding: utf-8 -*-
import os, sys, json, re, datetime, argparse, logging, subprocess
from pathlib import Path
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetabolismMutator:
    def __init__(self, repo_path: str = None):
        self.repo_path = Path(repo_path) if repo_path else Path(os.getcwd())
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def _engineering_brainstorm(self, issue_body: str, roadmap_context: str) -> Dict[str, Any]:
        logger.info("🧠 Brainstorming de Evolução...")
        api_key = os.getenv('GROQ_API_KEY')
        prompt = f"CONTEXTO: {roadmap_context}\nMISSÃO: {issue_body}\nRetorne JSON: mission_type, target_files[], required_actions[], can_auto_implement: true"
        try:
            import requests
            resp = requests.post(self.groq_url, headers={"Authorization": f"Bearer {api_key}"},
                               json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}],
                                     "temperature": 0.2, "response_format": {"type": "json_object"}}, timeout=30)
            data = resp.json()
            content = json.loads(data['choices'][0]['message']['content'])
            usage = data.get('usage', {})
            content['usage'] = {'total_tokens': usage.get('total_tokens', 0), 'cost': (usage.get('total_tokens', 0)/1e6)*0.7}
            return content
        except: return {'can_auto_implement': False}

    def _validate_integrity(self, old_code: str, new_code: str) -> bool:
        old_methods = set(re.findall(r'def\s+(\w+)\s*\(', old_code))
        new_methods = set(re.findall(r'def\s+(\w+)\s*\(', new_code))
        return old_methods.issubset(new_methods)

    def _reactive_mutation(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("⚡ Mutando DNA...")
        files_changed = []
        api_key = os.getenv('GROQ_API_KEY')
        for file_path_str in analysis.get('target_files', []):
            path = self.repo_path / file_path_str
            if not path.exists(): continue
            current = path.read_text(encoding='utf-8')
            prompt = f"Retorne o código COMPLETO. Use exit_code 124 para TimeoutExpired. CÓDIGO:\n{current}"
            try:
                import requests
                resp = requests.post(self.groq_url, headers={"Authorization": f"Bearer {api_key}"},
                                   json={"model": "llama-3.3-70b-versatile", "messages": [
                                       {"role": "system", "content": "Saída: APENAS código Python. SEM markdown."},
                                       {"role": "user", "content": prompt}], "temperature": 0.1}, timeout=60)
                new_code = resp.json()['choices'][0]['message']['content']
                new_code = re.sub(r'```(?:python)?', '', new_code).strip()
                compile(new_code, file_path_str, 'exec')
                if self._validate_integrity(current, new_code):
                    path.write_text(new_code, encoding='utf-8')
                    files_changed.append(file_path_str)
            except: pass
        return {'success': len(files_changed) > 0, 'mutation_applied': len(files_changed) > 0, 'files_changed': files_changed}

    def apply_mutation(self, strategy: str, intent: str, impact: str, roadmap_context: str = None) -> Dict[str, Any]:
        issue_body = os.getenv('ISSUE_BODY', 'Evolução')
        analysis = self._engineering_brainstorm(issue_body, roadmap_context or "")
        result = self._reactive_mutation(analysis) if analysis.get('can_auto_implement') else {'success': False}
        
        # Salva Log
        log_dir = self.repo_path / ".github" / "metabolism_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_dir / f"mut_{datetime.datetime.now().strftime('%H%M%S')}.json", 'w') as f:
            json.dump(result, f)
        
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                f.write(f"mutation_applied={str(result.get('mutation_applied', False)).lower()}\n")
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy', required=True); parser.add_argument('--intent', required=True)
    parser.add_argument('--impact', required=True); parser.add_argument('--roadmap-context', default="")
    args = parser.parse_args()
    res = MetabolismMutator().apply_mutation(args.strategy, args.intent, args.impact, args.roadmap_context)
    sys.exit(0 if res.get('success') else 1)
