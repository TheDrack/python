# -*- coding: utf-8 -*-
"""Dependency Injection Container - Wires together all components"""

import logging
import os
import sys
from typing import Optional

from app.adapters.edge import AutomationAdapter, CombinedVoiceProvider, WebAdapter
from app.domain.capabilities.cap_102_core import execute as cap_102_exec
from app.domain.gears.cap_101_core import execute as cap_101_exec
from app.domain.models.cap_100_core import execute as cap_100_exec
from app.domain.gears.cap_099_core import execute as cap_099_exec
from app.domain.capabilities.cap_098_core import execute as cap_098_exec
from app.domain.capabilities.cap_097_core import execute as cap_097_exec
from app.domain.gears.cap_096_core import execute as cap_096_exec
from app.adapters.cap_095_core import execute as cap_095_exec
from app.domain.capabilities.cap_094_core import execute as cap_094_exec
from app.domain.gears.cap_093_core import execute as cap_093_exec
from app.domain.gears.cap_092_core import execute as cap_092_exec
from app.domain.capabilities.cap_091_core import execute as cap_091_exec
from app.domain.capabilities.cap_090_core import execute as cap_090_exec
from app.domain.capabilities.cap_089_core import execute as cap_089_exec
from app.domain.capabilities.cap_088_core import execute as cap_088_exec
from app.domain.gears.cap_087_core import execute as cap_087_exec
from app.domain.capabilities.cap_086_core import execute as cap_086_exec
from app.domain.capabilities.cap_085_core import execute as cap_085_exec
from app.domain.capabilities.cap_084_core import execute as cap_084_exec
from app.domain.capabilities.cap_083_core import execute as cap_083_exec
from app.domain.capabilities.cap_082_core import execute as cap_082_exec
from app.domain.capabilities.cap_081_core import execute as cap_081_exec
from app.domain.gears.cap_080_core import execute as cap_080_exec
from app.domain.capabilities.cap_079_core import execute as cap_079_exec
from app.domain.capabilities.cap_078_core import execute as cap_078_exec
from app.adapters.cap_077_core import execute as cap_077_exec
from app.domain.capabilities.cap_076_core import execute as cap_076_exec
from app.domain.capabilities.cap_075_core import execute as cap_075_exec
from app.domain.capabilities.cap_074_core import execute as cap_074_exec
from app.domain.capabilities.cap_073_core import execute as cap_073_exec
from app.adapters.cap_072_core import execute as cap_072_exec
from app.domain.capabilities.cap_071_core import execute as cap_071_exec
from app.domain.capabilities.cap_070_core import execute as cap_070_exec
from app.domain.capabilities.cap_069_core import execute as cap_069_exec
from app.domain.capabilities.cap_068_core import execute as cap_068_exec
from app.adapters.cap_067_core import execute as cap_067_exec
from app.domain.capabilities.cap_066_core import execute as cap_066_exec
from app.domain.gears.cap_065_core import execute as cap_065_exec
from app.domain.gears.cap_064_core import execute as cap_064_exec
from app.domain.capabilities.cap_063_core import execute as cap_063_exec
from app.adapters.cap_062_core import execute as cap_062_exec
from app.domain.gears.cap_061_core import execute as cap_061_exec
from app.domain.capabilities.cap_060_core import execute as cap_060_exec
from app.adapters.cap_059_core import execute as cap_059_exec
from app.domain.capabilities.cap_058_core import execute as cap_058_exec
from app.domain.gears.cap_057_core import execute as cap_057_exec
from app.domain.capabilities.cap_056_core import execute as cap_056_exec
from app.domain.capabilities.cap_055_core import execute as cap_055_exec
from app.domain.models.cap_054_core import execute as cap_054_exec
from app.domain.capabilities.cap_053_core import execute as cap_053_exec
from app.domain.capabilities.cap_052_core import execute as cap_052_exec
from app.domain.capabilities.cap_051_core import execute as cap_051_exec
from app.domain.gears.cap_050_core import execute as cap_050_exec
from app.domain.capabilities.cap_049_core import execute as cap_049_exec
from app.domain.capabilities.cap_048_core import execute as cap_048_exec
from app.adapters.cap_047_core import execute as cap_047_exec
from app.domain.capabilities.cap_046_core import execute as cap_046_exec
from app.domain.gears.cap_045_core import execute as cap_045_exec
from app.adapters.cap_044_core import execute as cap_044_exec
from app.domain.gears.cap_043_core import execute as cap_043_exec
from app.domain.models.cap_042_core import execute as cap_042_exec
from app.domain.capabilities.cap_041_core import execute as cap_041_exec
from app.adapters.cap_040_core import execute as cap_040_exec
from app.adapters.cap_039_core import execute as cap_039_exec
from app.domain.capabilities.cap_038_core import execute as cap_038_exec
from app.domain.capabilities.cap_037_core import execute as cap_037_exec
from app.domain.capabilities.cap_036_core import execute as cap_036_exec
from app.domain.capabilities.cap_035_core import execute as cap_035_exec
from app.domain.models.cap_034_core import execute as cap_034_exec
from app.domain.models.cap_033_core import execute as cap_033_exec
from app.domain.gears.cap_032_core import execute as cap_032_exec
from app.domain.capabilities.cap_031_core import execute as cap_031_exec
from app.domain.capabilities.cap_030_core import execute as cap_030_exec
from app.domain.gears.cap_029_core import execute as cap_029_exec
from app.domain.gears.cap_028_core import execute as cap_028_exec
from app.domain.gears.cap_027_core import execute as cap_027_exec
from app.domain.capabilities.cap_026_core import execute as cap_026_exec
from app.domain.capabilities.cap_025_core import execute as cap_025_exec
from app.domain.capabilities.cap_024_core import execute as cap_024_exec
from app.domain.gears.cap_023_core import execute as cap_023_exec
from app.domain.capabilities.cap_022_core import execute as cap_022_exec
from app.domain.capabilities.cap_021_core import execute as cap_021_exec
from app.domain.capabilities.cap_020_core import execute as cap_020_exec
from app.domain.capabilities.cap_019_core import execute as cap_019_exec
from app.domain.capabilities.cap_018_core import execute as cap_018_exec
from app.domain.capabilities.cap_017_core import execute as cap_017_exec
from app.domain.capabilities.cap_016_core import execute as cap_016_exec
from app.domain.capabilities.cap_015_core import execute as cap_015_exec
from app.domain.capabilities.cap_014_core import execute as cap_014_exec
from app.domain.capabilities.cap_013_core import execute as cap_013_exec
from app.domain.capabilities.cap_012_core import execute as cap_012_exec
from app.domain.capabilities.cap_011_core import execute as cap_011_exec
from app.domain.gears.cap_010_core import execute as cap_010_exec
from app.domain.gears.cap_009_core import execute as cap_009_exec
from app.domain.gears.cap_008_core import execute as cap_008_exec
from app.domain.capabilities.cap_007_core import execute as cap_007_exec
from app.domain.gears.cap_006_core import execute as cap_006_exec
from app.domain.capabilities.cap_005_core import execute as cap_005_exec
from app.domain.capabilities.cap_004_core import execute as cap_004_exec
from app.domain.capabilities.cap_003_core import execute as cap_003_exec
from app.domain.models.cap_002_core import execute as cap_002_exec
from app.domain.gears.cap_001_core import execute as cap_001_exec
from app.adapters.infrastructure import DummyVoiceProvider, LLMCommandAdapter, SQLiteHistoryAdapter
from app.adapters.infrastructure.github_adapter import GitHubAdapter
from app.adapters.infrastructure.reward_adapter import RewardAdapter
try:
    from app.adapters.infrastructure import GatewayLLMCommandAdapter
except ImportError:
    GatewayLLMCommandAdapter = None
from app.application.ports import ActionProvider, HistoryProvider, VoiceProvider, WebProvider
from app.application.services import AssistantService, DependencyManager, ExtensionManager
from app.application.services.evolution_loop import EvolutionLoopService
from app.core.config import settings
from app.domain.services import CommandInterpreter, IntentProcessor

logger = logging.getLogger(__name__)

# Direct OS environment variable reading for Gemini API Key
render_key = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
print(f"DEBUG SISTEMA: Chave encontrada no OS? {'Sim' if render_key else 'Não'}")


def _is_headless_environment() -> bool:
    """
    Detect if we're running in a headless environment (tests, CI/CD, cloud).
    
    Returns:
        True if running in headless environment, False otherwise
    """
    # Check if running in pytest
    if "pytest" in sys.modules:
        return True
    
    # Check if running in CI/CD (common CI environment variables)
    ci_vars = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "TRAVIS", "CIRCLECI"]
    if any(os.getenv(var) for var in ci_vars):
        return True
    
    # Check if running on cloud platform (Render, Heroku, etc.)
    # Render sets both PORT and RENDER environment variables
    # Heroku sets both PORT and DYNO environment variables
    if os.getenv("PORT") and (os.getenv("RENDER") or os.getenv("DYNO") or os.getenv("RENDER_SERVICE_NAME")):
        return True
    
    return False


class Container:
    """
    Dependency Injection Container for the application.
    Manages creation and lifecycle of all components.
    """

    def __init__(
        self,
        voice_provider: Optional[VoiceProvider] = None,
        action_provider: Optional[ActionProvider] = None,
        web_provider: Optional[WebProvider] = None,
        history_provider: Optional[HistoryProvider] = None,
        wake_word: str = "xerife",
        language: str = "pt-BR",
        use_llm: bool = False,
        gemini_api_key: Optional[str] = None,
        gemini_model: str = "gemini-flash-latest",
        groq_api_key: Optional[str] = None,
        groq_model: str = "llama-3.3-70b-versatile",
        use_ai_gateway: bool = True,
        db_path: str = "jarvis.db",
    ):
        """
        Initialize the container

        Args:
            voice_provider: Optional pre-configured voice provider
            action_provider: Optional pre-configured action provider
            web_provider: Optional pre-configured web provider
            history_provider: Optional pre-configured history provider
            wake_word: Wake word for the assistant
            language: Language for voice recognition
            use_llm: Whether to use LLM-based command interpretation (default: False)
            gemini_api_key: Optional Gemini API key (defaults to GEMINI_API_KEY env var)
            gemini_model: Gemini model name to use (default: gemini-flash-latest)
            groq_api_key: Optional Groq API key (defaults to GROQ_API_KEY env var)
            groq_model: Groq model name to use (default: llama-3.3-70b-versatile)
            use_ai_gateway: Whether to use AI Gateway for intelligent provider routing (default: True)
            db_path: Path to SQLite database file (default: jarvis.db)
        """
        self.wake_word = wake_word
        self.language = language
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        # Force the value from direct OS reading
        self.gemini_api_key = self.gemini_api_key or render_key
        self.gemini_model = gemini_model or os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.groq_model = groq_model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.use_ai_gateway = use_ai_gateway and GatewayLLMCommandAdapter is not None
        self.db_path = db_path
        
        # Debug logging for API keys (only show presence, not content)
        if self.gemini_api_key:
            logger.debug("Gemini API key configured")
        if self.groq_api_key:
            logger.debug("Groq API key configured")
        
        # Log API key detection during boot
        if self.gemini_api_key:
            logger.info("✓ Chave de API do Gemini detectada pelo sistema de configurações")
        else:
            logger.warning("⚠ Chave de API do Gemini NÃO detectada")
        
        if self.groq_api_key:
            logger.info("✓ Chave de API do Groq detectada pelo sistema de configurações")
        else:
            logger.warning("⚠ Chave de API do Groq NÃO detectada")
        
        # Use LLM if any API key is available (unless explicitly disabled)
        # This ensures the adapter is created when an API key exists
        self.use_llm = use_llm or bool(self.gemini_api_key or self.groq_api_key)

        # Create or use provided adapters
        self._voice_provider = voice_provider
        self._action_provider = action_provider
        self._web_provider = web_provider
        self._history_provider = history_provider

        # Domain services (always created fresh)
        self._command_interpreter: Optional[CommandInterpreter] = None
        self._llm_command_adapter: Optional[LLMCommandAdapter] = None
        self._intent_processor: Optional[IntentProcessor] = None
        self._dependency_manager: Optional[DependencyManager] = None
        self._extension_manager: Optional[ExtensionManager] = None
        self._github_adapter: Optional[GitHubAdapter] = None
        
        # Evolution RL services
        self._reward_adapter: Optional[RewardAdapter] = None
        self._evolution_loop_service: Optional[EvolutionLoopService] = None

        # Application service
        self._assistant_service: Optional[AssistantService] = None

    @property
    def voice_provider(self) -> VoiceProvider:
        """Get or create voice provider"""
        if self._voice_provider is None:
            # Use DummyVoiceProvider in headless environments
            if _is_headless_environment():
                logger.info("Detected headless environment, using DummyVoiceProvider")
                self._voice_provider = DummyVoiceProvider()
            else:
                logger.info("Creating default CombinedVoiceProvider")
                self._voice_provider = CombinedVoiceProvider(
                    language=self.language,
                    ambient_noise_adjustment=True,
                )
        return self._voice_provider

    @property
    def action_provider(self) -> ActionProvider:
        """Get or create action provider"""
        if self._action_provider is None:
            logger.info("Creating default AutomationAdapter")
            self._action_provider = AutomationAdapter(
                pause=0.4,
                search_timeout=7.5,
            )
        return self._action_provider

    @property
    def web_provider(self) -> WebProvider:
        """Get or create web provider"""
        if self._web_provider is None:
            logger.info("Creating default WebAdapter")
            self._web_provider = WebAdapter(self.action_provider)
        return self._web_provider

    @property
    def history_provider(self) -> HistoryProvider:
        """Get or create history provider"""
        if self._history_provider is None:
            logger.info(f"Creating SQLiteHistoryAdapter with database configuration")
            # Use DATABASE_URL from settings if it's not the default SQLite
            # Only use SQLite fallback (db_path) if the URL is the exact default
            database_url = None
            if settings.database_url and settings.database_url != "sqlite:///jarvis.db":
                # Custom database URL (could be PostgreSQL, another SQLite path, etc.)
                database_url = settings.database_url
            
            self._history_provider = SQLiteHistoryAdapter(
                db_path=self.db_path,
                database_url=database_url
            )
        return self._history_provider

    @property
    def command_interpreter(self) -> CommandInterpreter:
        """Get or create command interpreter"""
        if self._command_interpreter is None:
            # Try to create AI Gateway adapter first if enabled and we have API keys
            if self.use_ai_gateway and (self.gemini_api_key or self.groq_api_key):
                logger.info("Tentando criar GatewayLLMCommandAdapter com AI Gateway")
                try:
                    self._llm_command_adapter = GatewayLLMCommandAdapter(
                        groq_api_key=self.groq_api_key,
                        gemini_api_key=self.gemini_api_key,
                        groq_model=self.groq_model,
                        gemini_model=self.gemini_model,
                        voice_provider=self.voice_provider,
                        wake_word=self.wake_word,
                        history_provider=self.history_provider,
                        use_llm=self.use_llm,
                    )
                    logger.info("✓ GatewayLLMCommandAdapter criado com sucesso")
                    return self._llm_command_adapter
                except Exception as e:
                    logger.error(f"✗ ERRO ao criar GatewayLLMCommandAdapter: {type(e).__name__}: {str(e)}")
                    print(f"ERRO DETALHADO ao criar GatewayLLMCommandAdapter: {type(e).__name__}: {str(e)}")
                    # Fall through to try basic LLM adapter
            
            # Fallback to basic LLM adapter if we have Gemini API key
            if self.gemini_api_key:
                logger.info("Tentando criar LLMCommandAdapter para interpretação de comandos")
                try:
                    self._llm_command_adapter = LLMCommandAdapter(
                        api_key=self.gemini_api_key,
                        model_name=self.gemini_model,
                        voice_provider=self.voice_provider,
                        wake_word=self.wake_word,
                        history_provider=self.history_provider,
                    )
                    logger.info("✓ LLMCommandAdapter criado com sucesso")
                    return self._llm_command_adapter
                except Exception as e:
                    logger.error(f"✗ ERRO ao criar LLMCommandAdapter: {type(e).__name__}: {str(e)}")
                    print(f"ERRO DETALHADO ao criar LLMCommandAdapter: {type(e).__name__}: {str(e)}")
                    # Fall through to create rule-based interpreter
            
            # Use rule-based interpreter as fallback
            logger.info("Using rule-based CommandInterpreter")
            self._command_interpreter = CommandInterpreter(wake_word=self.wake_word)
        return self._command_interpreter

    @property
    def intent_processor(self) -> IntentProcessor:
        """Get or create intent processor"""
        if self._intent_processor is None:
            self._intent_processor = IntentProcessor()
        return self._intent_processor

    @property
    def dependency_manager(self) -> DependencyManager:
        """Get or create dependency manager"""
        if self._dependency_manager is None:
            logger.info("Creating DependencyManager")
            self._dependency_manager = DependencyManager()
        return self._dependency_manager

    @property
    def extension_manager(self) -> ExtensionManager:
        """Get or create extension manager"""
        if self._extension_manager is None:
            logger.info("Creating ExtensionManager")
            self._extension_manager = ExtensionManager()
        return self._extension_manager

    @property
    def github_adapter(self) -> Optional[GitHubAdapter]:
        """Get or create GitHub adapter"""
        if self._github_adapter is None:
            # Only create if GITHUB_TOKEN is available
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                logger.info("Creating GitHubAdapter")
                self._github_adapter = GitHubAdapter()
            else:
                logger.debug("GitHubAdapter not created - GITHUB_TOKEN not available")
        return self._github_adapter
    
    @property
    def reward_adapter(self) -> RewardAdapter:
        """Get or create reward adapter for RL evolution tracking"""
        if self._reward_adapter is None:
            logger.info("Creating RewardAdapter for Evolution RL")
            self._reward_adapter = RewardAdapter(engine=self.history_provider.engine)
        return self._reward_adapter
    
    @property
    def evolution_loop_service(self) -> EvolutionLoopService:
        """Get or create evolution loop service"""
        if self._evolution_loop_service is None:
            logger.info("Creating EvolutionLoopService")
            # Try to get AI Gateway if available
            ai_gateway = None
            if self._llm_command_adapter is not None and hasattr(self._llm_command_adapter, 'ai_gateway'):
                ai_gateway = self._llm_command_adapter.ai_gateway
            
            self._evolution_loop_service = EvolutionLoopService(
                reward_provider=self.reward_adapter,
                ai_gateway=ai_gateway
            )
        return self._evolution_loop_service

    @property
    def assistant_service(self) -> AssistantService:
        """Get or create assistant service with all dependencies injected"""
        if self._assistant_service is None:
            logger.info("Creating AssistantService with injected dependencies")
            
            # Determine if we have a gemini_adapter - force creation if we have API keys
            gemini_adapter = None
            if self.gemini_api_key or self.groq_api_key:
                # If we have any API key, force creation of LLM adapter
                if self._llm_command_adapter is not None:
                    gemini_adapter = self._llm_command_adapter
                    logger.info("✓ Adaptador de IA será injetado no AssistantService")
                else:
                    # Trigger creation of LLM adapter by accessing command_interpreter
                    _ = self.command_interpreter
                    gemini_adapter = self._llm_command_adapter
                    if gemini_adapter:
                        logger.info("✓ Adaptador de IA criado e será injetado no AssistantService")
                    else:
                        logger.error("✗ Falha ao criar adaptador de IA")
            else:
                logger.warning("⚠ AssistantService será criado SEM adaptador de IA (API keys não disponíveis)")
            
            self._assistant_service = AssistantService(
                voice_provider=self.voice_provider,
                action_provider=self.action_provider,
                web_provider=self.web_provider,
                command_interpreter=self.command_interpreter,
                intent_processor=self.intent_processor,
                history_provider=self.history_provider,
                dependency_manager=self.dependency_manager,
                wake_word=self.wake_word,
                gemini_adapter=gemini_adapter,
                github_adapter=self.github_adapter,
            )
        return self._assistant_service


def create_edge_container(
    wake_word: str = "xerife",
    language: str = "pt-BR",
    use_llm: bool = False,
    use_ai_gateway: bool = True,
) -> Container:
    """
    Factory function to create a container with edge adapters

    Args:
        wake_word: Wake word for the assistant
        language: Language for voice recognition
        use_llm: Whether to use LLM-based command interpretation (default: False)
                 Note: LLM will be auto-enabled if API key is available in settings,
                 regardless of this parameter value
        use_ai_gateway: Whether to use AI Gateway for intelligent provider routing (default: True)

    Returns:
        Configured container with edge adapters
    """
    return Container(
        wake_word=wake_word,
        language=language,
        use_llm=use_llm,
        gemini_api_key=settings.gemini_api_key,
        gemini_model=settings.gemini_model,
        groq_api_key=settings.groq_api_key,
        groq_model=settings.groq_model,
        use_ai_gateway=use_ai_gateway,
    )
