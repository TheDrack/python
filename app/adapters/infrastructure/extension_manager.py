
# Arquivo de gerenciamento de extensões para automações complexas
from abc import ABC, abstractmethod
from typing import List

class Extension(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class ExtensionManager:
    def __init__(self):
        self.extensions = []

    def register_extension(self, extension: Extension):
        self.extensions.append(extension)

    def execute_extensions(self, *args, **kwargs):
        for extension in self.extensions:
            extension.execute(*args, **kwargs)

class AutomationExtension(Extension):
    def execute(self, *args, **kwargs):
        # Lógica de automação
        print('Executando automação...')

class NotificationExtension(Extension):
    def execute(self, *args, **kwargs):
        # Lógica de notificação
        print('Enviando notificação...')

# Exemplo de uso
if __name__ == '__main__':
    manager = ExtensionManager()

    automation_extension = AutomationExtension()
    notification_extension = NotificationExtension()

    manager.register_extension(automation_extension)
    manager.register_extension(notification_extension)

    manager.execute_extensions()
