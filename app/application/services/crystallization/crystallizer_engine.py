# -*- coding: utf-8 -*-
import json
import os
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Crystallizer")

class CrystallizerEngine:
    def __init__(self, 
                 cap_path="data/capabilities.json", 
                 crystal_path="data/master_crystal.json", 
                 container_path="app/container.py"):
        
        self.paths = {
            "caps": Path(cap_path),
            "crystal": Path(crystal_path),
            "container": Path(container_path)
        }
        
        # Garante que a pasta data existe
        self.paths["caps"].parent.mkdir(parents=True, exist_ok=True)
        
        # Carrega ou Inicializa o Master Crystal
        self.master_crystal = self._load_json(self.paths["crystal"]) or self._init_crystal()
        
        # Carrega as Capabilities (Fonte da Verdade)
        caps_data = self._load_json(self.paths["caps"])
        self.capabilities = caps_data.get('capabilities', []) if caps_data else []

    def _load_json(self, path: Path):
        try:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao ler JSON em {path}: {str(e)}")
        return None

    def _init_crystal(self):
        return {
            "system_id": "JARVIS_CORE",
            "version": "1.0.0",
            "last_scan": None,
            "crystallization_summary": {
                "total_capabilities": 0,
                "crystallized": 0,
                "connected_legacy": 0,
                "orphan": 0
            },
            "registry": []
        }

    def _map_target(self, cap: Dict[str, Any]) -> str:
        """Mapeia o destino hexagonal baseado no título e descrição"""
        title = cap.get('title', '').lower()
        desc = cap.get('description', '').lower()
        
        # Prioridade para Gears (Cognição/LLM)
        if any(x in title or x in desc for x in ["llm", "ai", "reasoning", "gear", "cognition", "gpt", "claude", "groq"]):
            return "app/domain/gears/"
        # Domínio/Modelos
        if any(x in title or x in desc for x in ["model", "state", "entity", "schema", "database"]):
            return "app/domain/models/"
        # Adapters (Interface/Sistemas externos)
        if any(x in title or x in desc for x in ["adapter", "web", "db", "keyboard", "pyautogui", "os"]):
            return "app/adapters/"
        
        return "app/domain/capabilities/"

    def audit(self):
        """Varre o sistema e identifica a conectividade das capacidades"""
        logger.info("⚡ Iniciando Auditoria do Sistema...")
        
        container_content = ""
        if self.paths["container"].exists():
            container_content = self.paths["container"].read_text(encoding='utf-8')

        new_registry = []
        stats = {"total": len(self.capabilities), "crystallized": 0, "legacy": 0, "orphan": 0}

        for cap in self.capabilities:
            cap_id = cap['id']
            notes = cap.get('notes', '')
            
            # Localiza rastro em scripts/
            file_match = re.search(r'(scripts/[\w\.]+\.py)', notes)
            source_file = file_match.group(1) if file_match else "unknown"
            
            # Define alvos
            target_dir = self._map_target(cap)
            target_file_name = f"{cap_id.lower().replace('-', '_')}_core.py"
            target_path = os.path.join(target_dir, target_file_name)
            
            is_in_container = cap_id in container_content
            is_physically_present = Path(target_path).exists()

            if is_in_container and is_physically_present:
                status = "crystallized"
                stats["crystallized"] += 1
            elif source_file != "unknown" and not is_physically_present:
                status = "legacy_connected"
                stats["legacy"] += 1
            else:
                status = "orphan"
                stats["orphan"] += 1

            entry = {
                "id": cap_id,
                "title": cap['title'],
                "status": status,
                "genealogy": {
                    "source": source_file,
                    "target_suggested": target_dir,
                    "target_file": target_path
                },
                "integration": {
                    "in_container": is_in_container,
                    "physically_present": is_physically_present
                },
                "last_check": datetime.now().isoformat()
            }
            new_registry.append(entry)

        self.master_crystal["registry"] = new_registry
        self.master_crystal["last_scan"] = datetime.now().isoformat()
        self.master_crystal["crystallization_summary"] = {
            "total_capabilities": stats["total"],
            "crystallized": stats["crystallized"],
            "connected_legacy": stats["legacy"],
            "orphan": stats["orphan"]
        }
        
        self._save_crystal()
        logger.info(f"✅ Auditoria completa. Órfãos/Legados: {stats['orphan'] + stats['legacy']}")

    def transmute(self):
        """Cria fisicamente a estrutura hexagonal e arquivos core"""
        logger.info("🛠️ Iniciando Transmutação Física (Criação de Estrutura)...")
        
        for entry in self.master_crystal["registry"]:
            # Só transmuta o que não está cristalizado
            if entry["status"] in ["orphan", "legacy_connected"]:
                t_path = Path(entry["genealogy"]["target_file"])
                t_dir = Path(entry["genealogy"]["target_suggested"])
                
                # 1. Cria diretórios e __init__.py
                t_dir.mkdir(parents=True, exist_ok=True)
                init_file = t_dir / "__init__.py"
                if not init_file.exists():
                    init_file.touch()

                # 2. Cria o arquivo de capacidade se não existir
                if not t_path.exists():
                    try:
                        with open(t_path, 'w', encoding='utf-8') as f:
                            f.write('# -*- coding: utf-8 -*-\n')
                            f.write(f'"""\nCAPABILITY: {entry["title"]}\nID: {entry["id"]}\nSTATUS: Cristalizado\n"""\n\n')
                            f.write('from typing import Dict, Any\n\n')
                            f.write('def execute(context: Dict[str, Any] = None) -> Dict[str, Any]:\n')
                            f.write('    """Lógica central da capacidade gerada pelo Arquiteto"""\n')
                            f.write('    return {"status": "ready", "id": "' + entry["id"] + '"}\n')
                        
                        logger.info(f"  [💎] Arquivo criado: {t_path}")
                        entry["integration"]["physically_present"] = True
                        entry["status"] = "crystallized" # Atualiza status para o próximo ciclo
                    except Exception as e:
                        logger.error(f"  [!] Erro ao criar {t_path}: {e}")

        # Salva o estado final após as criações
        self._save_crystal()

    def _save_crystal(self):
        with open(self.paths["crystal"], 'w', encoding='utf-8') as f:
            json.dump(self.master_crystal, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    engine = CrystallizerEngine()
    engine.audit()      # Fase 1: Mapear o que falta
    engine.transmute()  # Fase 2: Criar as pastas e arquivos físicos
    logger.info("✨ Sistema cristalizado e organizado.")
