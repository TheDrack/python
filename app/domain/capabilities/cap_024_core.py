
      def execute(context=None):
         import time
         import logging
         from app.domain.capabilities import metrics

         # Inicializar o logger
         logger = logging.getLogger(__name__)

         # Definir o intervalo de tempo para monitorar o desempenho
         interval = 60  # 1 minuto

         # Definir o limite de desempenho aceitável
         threshold = 0.5  # 50% de desempenho em relação ao baseline

         # Carregar o baseline de desempenho
         baseline = metrics.load_baseline()

         # Loop infinito para monitorar o desempenho
         while True:
            # Medir o tempo de execução do sistema
            start_time = time.time()
            # Executar uma tarefa de exemplo (substituir por uma tarefa real)
            example_task()
            end_time = time.time()

            # Calcular o tempo de execução
            execution_time = end_time - start_time

            # Calcular a taxa de desempenho
            performance_ratio = execution_time / baseline

            # Verificar se o desempenho está abaixo do limite aceitável
            if performance_ratio > threshold:
               logger.warning(f'Desempenho degradado: {performance_ratio:.2f}')

            # Aguardar o intervalo de tempo para a próxima medição
            time.sleep(interval)
   