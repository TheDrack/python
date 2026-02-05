#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Example usage of the CommandProcessor class.

This script demonstrates how to use the new CommandProcessor class
to execute commands instead of the old TuplaDeComandos approach.
"""

from app.core.processor import CommandProcessor


def main():
    """Demonstrate CommandProcessor usage."""
    
    # Create a CommandProcessor instance
    processor = CommandProcessor()
    
    print("=== CommandProcessor Demo ===\n")
    
    # Show registered commands
    print(f"Registered commands ({len(processor.comandos)}):")
    for cmd in sorted(processor.comandos.keys()):
        print(f"  - {cmd}")
    
    print("\n=== Example Command Executions ===\n")
    
    # Example commands (these would normally come from voice recognition)
    example_commands = [
        "falar olá mundo",
        "escreva teste",
        "internet",
        "sulfite",
        "planilha financeira",
    ]
    
    for comando in example_commands:
        print(f"Executing: '{comando}'")
        try:
            result = processor.execute(comando)
            print(f"  → Result: {result}\n")
        except Exception as e:
            print(f"  → Error: {e}\n")
    
    print("=== Comparison with old approach ===\n")
    print("Old approach (from assistente.pyw):")
    print("  TuplaDeComandos = {")
    print("      ('sulfite', FazerRequisicaoSulfite),")
    print("      ('planilha', AbrirPlanilha),")
    print("      ...")
    print("  }")
    print("  for comandos, acao in TuplaDeComandos:")
    print("      if comandos in comando:")
    print("          acao(comando)")
    print()
    print("New approach:")
    print("  processor = CommandProcessor()")
    print("  processor.execute(comando)")


if __name__ == '__main__':
    main()
