
   const { Worker } = require('worker_threads');
   const playwright = require('playwright');

   class WorkerPlaywright {
     constructor() {
       this.browser = null;
       this.context = null;
       this.page = null;
     }

     async init() {
       this.browser = await playwright.chromium.launch({ headless: true });
       this.context = await this.browser.newContext();
       this.page = await this.context.newPage();
     }

     async execute(script) {
       try {
         return await this.page.evaluate(script);
       } catch (error) {
         console.error('Erro ao executar script:', error);
         throw error;
       }
     }

     async close() {
       if (this.page) await this.page.close();
       if (this.context) await this.context.close();
       if (this.browser) await this.browser.close();
     }
   }

   module.exports = WorkerPlaywright;
   