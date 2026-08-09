const puppeteer = require('puppeteer');
(async () => {
    try {
        const browser = await puppeteer.launch();
        await browser.close();
        console.log("Puppeteer OK");
    } catch(e) {
        console.log("Puppeteer Error:", e.message);
    }
})();
