# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import datetime
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetabolismMutator:
    def __init__(self, repo_path: str = None):
        self.repo_path = Path(repo_path) if repo_path else Path(os.getcwd())
        self.mutation_log = []
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

    def _engineering_brainstorm(self, issue_body: str, roadmap_context: str) -> Dict[str, Any]:
        import time
        logger.info("🧠 Brainstorming de Evolução (Llama-3.3-70b)...")
        api_key = os.getenv('GROQ_API_KEY')
        prompt = f"CONTEXTO: {roadmap_context}\nMISSÃO: {issue_body}\nRetorne um JSON com 'mission_type', 'target_files' (lista), 'required_actions' (lista) e 'can_auto_implement' (bool)."
        
        try:
            import requests
            resp = requests.post(self.groq_url, headers={"Authorization": f"Bearer {api_key}"},
                               json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}],
                                     "temperature": 0.2, "response_format": {"type": "json_object"}}, timeout=30)
            data = resp.json()
            content = json.loads(data['choices'][0]['message']['content'])
            usage = data.get('usage', {})
            content['usage'] = {'total_tokens': usage.get('total_tokens', 0), 'cost': (usage.get('total_tokens', 0) / 1_000_000) * 0.70}
            return content
        except Exception as e:
            logger.error(f"❌ Erro no Brainstorm: {e}")
            return {'can_auto_implement': False}

    def _update_evolution_dashboard(self, mission_name: str, tokens: int, cost: float):
        """Reintegrado: Atualiza o status no README.md"""
        logger.info("🏆 Atualizando Dashboard...")
        readme_path = self.repo_path / "README.md"
        if not readme_path.exists(): return
        try:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            entry = f"| {date_str} | {mission_name} | {tokens} | ${cost:.6f} | ✅ |\n"
            content = readme_path.read_text(encoding='utf-8')
            if "## 🧬 Painel de Evolução" in content:
                parts = content.split("## 🧬 Painel de Evolução JARVIS")
                readme_path.write_text(parts[0] + "## 🧬 Painel de Evolução JARVIS\n" + entry + parts[1], encoding='utf-8')
        except Exception as e: logger.warning(f"⚠️ Erro dashboard: {e}")

    def _validate_integrity(self, old_code: str, new_code: str) -> bool:
        """Verifica se não houve amputação de métodos"""
        old_methods = set(re.findall(r'def\s+(\w+)\s*\(', old_code))
        new_methods = set(re.findall(r'def\s+(\w+)\s*\(', new_code))
        missing = old_methods - new_methods
        if missing:
            logger.warning(f"⚠️ Integridade violada. Métodos ausentes: {missing}")
            return False
        return True

    def _reactive_mutation(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("⚡ Executando Mutação...")
        files_changed = []
        api_key = os.getenv('GROQ_API_KEY')
        for file_path_str in analysis.get('target_files', []):
            path = self.repo_path / file_path_str
            if not path.exists(): continue
            current = path.read_text(encoding='utf-8')
            prompt = f"Mantenha todos os métodos. Corrija o Timeout para retornar exit_code 124. CÓDIGO:\n{current}"
            try:
                import requests
                resp = requests.post(self.groq_url, headers={"Authorization": f"Bearer {api_key}"},
                                   json={"model": "llama-3.3-70b-versatile", "messages": [
                                       {"role": "system", "content": "Saída: código Python completo. Use exit_code 124 para TimeoutExpired."},
                                       {"role": "user", "content": prompt}], "temperature": 0.1}, timeout=60)
                new_code = resp.json()['choices'][0]['message']['content']
                new_code = re.sub(r'```(?:python)?', '', new_code).strip()
                
                compile(new_code, file_path_str, 'exec')
                if self._validate_integrity(current, new_code):
                    path.write_text(new_code, encoding='utf-8')
                    files_changed.append(file_path_str)
            except Exception as e: logger.error(f"❌ Falha no arquivo {file_path_str}: {e}")
        return {'success': len(files_changed) > 0, 'mutation_applied': len(files_changed) > 0, '
