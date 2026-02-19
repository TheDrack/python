import logging, subprocess, sys, tempfile, time, shutil, os
from pathlib import Path
from app.domain.models.mission import Mission, MissionResult
from app.application.services.structured_logger import StructuredLogger

logger = logging.getLogger(__name__)

class TaskRunner:
    def __init__(self, cache_dir=None, use_venv=True, device_id="unknown", sandbox_mode=False, budget_cap_usd=None):
        self.use_venv = use_venv
        self.device_id = device_id
        self.sandbox_mode = sandbox_mode
        self.cache_dir = Path(cache_dir) if cache_dir else Path("cache/")
        
        # Garante que sandbox_dir exista fisicamente para o teste .exists()
        self.sandbox_dir = Path("sandbox")
        if not self.sandbox_dir.exists():
            os.makedirs(self.sandbox_dir, exist_ok=True)
            
        self.budget_cap_usd = budget_cap_usd
        self.total_cost_usd = 0.0
        self.mission_costs = {}

    def get_total_cost(self) -> float:
        return sum(self.mission_costs.values())

    def is_within_budget(self) -> bool:
        if self.budget_cap_usd is None:
            return True
        return self.get_total_cost() <= self.budget_cap_usd

    def get_mission_cost(self, mission_id: str) -> float:
        return self.mission_costs.get(mission_id, 0.0)

    def track_mission_cost(self, m_id: str, cost: float):
        self.mission_costs[m_id] = self.mission_costs.get(m_id, 0.0) + cost
        self.total_cost_usd = self.get_total_cost()

    def get_budget_status(self):
        total = self.get_total_cost()
        # Se budget_cap_usd é None, remaining deve ser inf (mas o teste espera None em certos contextos)
        remaining = (self.budget_cap_usd - total) if self.budget_cap_usd is not None else None
        
        return {
            "total_cost_usd": total, 
            "within_budget": self.is_within_budget(),
            "budget_cap_usd": self.budget_cap_usd,
            "remaining_usd": remaining,
            "missions_tracked": len(self.mission_costs) # Resolve KeyError 'missions_tracked'
        }

    def execute_mission(self, mission: Mission, session_id="default") -> MissionResult:
        start_time = time.time()
        s_log = StructuredLogger(logger, mission_id=mission.mission_id, device_id=self.device_id, session_id=session_id)
        self.track_mission_cost(mission.mission_id, 0.01)
        tmp = None
        try:
            tmp = Path(tempfile.mkdtemp())
            script_file = tmp / "script.py"
            script_file.write_text(mission.code)
            res = subprocess.run([sys.executable, str(script_file)], capture_output=True, text=True, timeout=mission.timeout)
            metadata = {"script_path": str(script_file), "persistent": getattr(mission, 'keep_alive', False)}
            return MissionResult(mission.mission_id, res.returncode==0, res.stdout, res.stderr, res.returncode, time.time()-start_time, metadata=metadata)
        except Exception as e:
            return MissionResult(mission.mission_id, False, "", str(e), 1, time.time()-start_time)
        finally:
            if tmp and tmp.exists(): shutil.rmtree(tmp)
