import json
import os
import re
import logging
from datetime import datetime

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("Crystallizer")

class CrystallizerEngine:
    def __init__(self, cap_path="data/capabilities.json", crystal_path="data/master_crystal.json", container_path="app/container.py"):
        self.cap_path = cap_path
        self.crystal_path = crystal_path
        self.container_path = container_path
        
        # Carregar dados
        with open(self.cap_path, 'r', encoding='utf-8') as f:
            self.capabilities = json.load(f).get('capabilities', [])
            
        with open(self.crystal_path, 'r', encoding='utf-8') as f:
            self.master_crystal = json.load(f)

    def _check_container_connection(self, keyword):
        """Verifica se uma palavra-chave (classe ou serviço) está no container.py"""
        if not os.path.exists(self.container_path):
            return False
        with open(self.container_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return keyword.lower() in content.lower()

    def audit_and_map(self):
        """Varre as capacidades e popula o Master Crystal"""
        logger.info(f"Iniciando auditoria de {len(self.capabilities)} capacidades...")
        
        registry = []
        stats = {"total": len(self.capabilities), "crystallized": 0, "legacy": 0, "orphan": 0}

        for cap in self.capabilities:
            cap_id = cap.get('id')
            notes = cap.get('notes', '')
            status = cap.get('status')

            # Tenta extrair o rastro do arquivo original nas notas
            # Ex: "Implementado em scripts/metabolism_mutator.py"
            file_match = re.search(r'([\w/]+\.py)', notes)
            source_file = file_match.group(1) if file_match else "unknown"
            
            # Checar se está conectado ao sistema nervoso (Container)
            # Usamos o título ou palavras-chave da descrição para a busca
            is_connected = self._check_container_connection(cap.get('title').split()[0]) or \
                           (source_file != "unknown" and self._check_container_connection(source_file.split('/')[-1]))

            # Lógica de Classificação (Sabedoria do JARVIS)
            integration_type = "orphan"
            if is_connected:
                integration_type = "connected_core"
                stats["crystallized"] += 1
            elif source_file != "unknown":
                integration_type = "connected_legacy"
                stats["legacy"] += 1
            else:
                stats["orphan"] += 1

            # Definir Destino Sugerido (Arquitetura Hexagonal)
            target = "app/domain/capabilities/"
            if "LLM" in cap.get('title') or "Gear" in notes:
                target = "app/domain/gears/"
            elif any(x in notes.lower() for x in ["pyautogui", "webdriver", "os", "db"]):
                target = "app/adapters/"

            # Criar entrada no registro
            entry = {
                "capability_id": cap_id,
                "title": cap.get('title'),
                "genealogy": {
                    "source": source_file,
                    "target_suggested": target
                },
                "integration": {
                    "type": integration_type,
                    "connected_to_container": is_connected,
                    "needs_gear": "LLM" in cap.get('title')
                },
                "last_update": datetime.now().isoformat()
            }
            registry.append(entry)

        # Atualizar Master Crystal
        self.master_crystal['last_scan'] = datetime.now().isoformat()
        self.master_crystal['registry'] = registry
        self.master_crystal['crystallization_summary'] = {
            "total_capabilities": stats["total"],
            "crystallized": stats["crystallized"],
            "connected_legacy": stats["legacy"],
            "orphan": stats["orphan"]
        }

        self.save_crystal()
        logger.info("Auditoria completa. Master Crystal atualizado.")

    def save_crystal(self):
        with open(self.crystal_path, 'w', encoding='utf-8') as f:
            json.dump(self.master_crystal, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    engine = CrystallizerEngine()
    engine.audit_and_map()
