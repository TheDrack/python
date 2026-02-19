
# Extension Manager para Automações Complexas

class ExtensionManager:
    def __init__(self):
        self.extensions = {}

    def register_extension(self, name, extension):
        self.extensions[name] = extension

    def get_extension(self, name):
        return self.extensions.get(name)

    def list_extensions(self):
        return list(self.extensions.keys())

class AutomationExtension:
    def __init__(self, name):
        self.name = name

    def execute(self):
        pass

class ExampleExtension(AutomationExtension):
    def __init__(self):
        super().__init__('example')

    def execute(self):
        print('Executando extensão de exemplo')

# Criando o gerenciador de extensões
manager = ExtensionManager()

# Registrando uma extensão
extension = ExampleExtension()
manager.register_extension(extension.name, extension)

# Listando extensões registradas
print('Extensões registradas:')
for extension_name in manager.list_extensions():
    print(extension_name)

# Executando uma extensão
extension_to_execute = manager.get_extension('example')
if extension_to_execute:
    extension_to_execute.execute()
