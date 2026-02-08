# -*- coding: utf-8 -*-
"""Agent Service - LLM-based agent logic using Function Calling"""

from typing import Any, Dict, List

from app.domain.models import CommandType


class AgentService:
    """
    Service that defines the agent's capabilities using Function Calling.
    Maps ActionProvider methods to function definitions for LLM.
    """

    @staticmethod
    def get_function_declarations() -> List[Dict[str, Any]]:
        """
        Get function declarations for the LLM to use.
        These represent the ActionProvider capabilities.

        Returns:
            List of function declarations in Gemini function calling format
        """
        return [
            {
                "name": "type_text",
                "description": "Digita texto usando o teclado. Use esta função quando o usuário pedir para escrever ou digitar algo.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "O texto a ser digitado",
                        }
                    },
                    "required": ["text"],
                },
            },
            {
                "name": "press_key",
                "description": "Pressiona uma tecla do teclado. Use para comandos como 'aperte enter', 'pressione tab', etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "Nome da tecla a ser pressionada (ex: 'enter', 'tab', 'escape', 'space')",
                        }
                    },
                    "required": ["key"],
                },
            },
            {
                "name": "open_browser",
                "description": "Abre o navegador web usando um atalho de teclado. Use quando o usuário pedir para abrir o navegador ou internet.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
            {
                "name": "open_url",
                "description": "Abre uma URL específica no navegador. Use quando o usuário mencionar um site ou endereço web.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "A URL a ser aberta (será adicionado https:// se necessário)",
                        }
                    },
                    "required": ["url"],
                },
            },
            {
                "name": "search_on_page",
                "description": "Procura texto em uma página web aberta. Use quando o usuário pedir para procurar ou clicar em algo na página.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_text": {
                            "type": "string",
                            "description": "O texto a ser procurado na página",
                        }
                    },
                    "required": ["search_text"],
                },
            },
        ]

    @staticmethod
    def map_function_to_command_type(function_name: str) -> CommandType:
        """
        Map a function name to a CommandType.

        Args:
            function_name: Name of the function called by the LLM

        Returns:
            Corresponding CommandType
        """
        function_to_command = {
            "type_text": CommandType.TYPE_TEXT,
            "press_key": CommandType.PRESS_KEY,
            "open_browser": CommandType.OPEN_BROWSER,
            "open_url": CommandType.OPEN_URL,
            "search_on_page": CommandType.SEARCH_ON_PAGE,
        }
        return function_to_command.get(function_name, CommandType.UNKNOWN)

    @staticmethod
    def get_system_instruction() -> str:
        """
        Get the system instruction for the LLM.
        Defines the personality and behavior of the "Xerife" assistant as an orchestrator.

        Returns:
            System instruction text
        """
        return """Xerife - Orquestrador de Ambiente. Resposta técnica direta, sem saudações. Máximo 3 tópicos.

Ações:
- Coordenar dispositivos (celular, PC, IoT) baseado em capacidades e localização GPS
- Solicitar comandos a Pontes Locais
- Gerenciar recursos físicos (câmera, sensores, TVs)

Diretrizes:
- Respostas objetivas e diretas
- Foco em ação e resultado
- Sem redundância ou formalidades
- Considerar localização GPS para priorizar dispositivos próximos (<1km)
- Pedir confirmação se dispositivo alvo >50km de distância

Exemplos:
- "tire uma selfie" -> câmera do dispositivo atual
- "ligue a TV" -> dispositivo IoT da mesma rede/local
- "escreva olá" -> use type_text"""
