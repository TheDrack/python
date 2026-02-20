
   import { chromium } from 'playwright';
   import { Worker } from 'worker_threads';

   class WorkerPlaywright {
       private browser: any;

       constructor() {
           this.init();
       }

       async init() {
           try {
               this.browser = await chromium.launch({
                   headless: true,
                   args: ['--no-sandbox', '--disable-setuid-sandbox']
               });
           } catch (error) {
               console.error('Erro ao inicializar o navegador:', error);
           }
       }

       async execute(script: string) {
           if (!this.browser) {
               console.error('Navegador não inicializado');
               return;
           }

           const context = await this.browser.newContext();
           const page = await context.newPage();
           try {
               await page.evaluate(script);
           } catch (error) {
               console.error('Erro ao executar script:', error);
           } finally {
               await page.close();
               await context.close();
           }
       }

       async close() {
           if (this.browser) {
               try {
                   await this.browser.close();
               } catch (error) {
                   console.error('Erro ao fechar o navegador:', error);
               }
           }
       }
   }

   const worker = new WorkerPlaywright();

   worker.execute(`
       // script a ser executado
       console.log('Executando script...');
   `);

   process.on('exit', () => {
       worker.close();
   });
   