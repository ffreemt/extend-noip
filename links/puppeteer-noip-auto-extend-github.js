const puppeteer = require('puppeteer');

(async () => {
    try {
    const browser = await puppeteer.launch({
        "headless": true // to debug and see action set to false !
    });
    const page = await browser.newPage();

    await page.goto("https://www.noip.com/login");
    {
        const targetPage = page;
        const frame = targetPage.mainFrame();
        const element = await frame.waitForSelector("aria/Username");
        await element.click();
    }
    {
        const targetPage = page;
        const frame = targetPage.mainFrame();
        const element = await frame.waitForSelector("aria/Username");
        await element.type("SetyourUsername");
    }
    {
        const targetPage = page;
        const frame = targetPage.mainFrame();
        const element = await frame.waitForSelector("aria/Password");
        await element.click();
    }
    {
        const targetPage = page;
        const frame = targetPage.mainFrame();
        const element = await frame.waitForSelector("aria/Password");
        await element.type("SetyourPassword");
    }
    {
        const targetPage = page;
        const frame = targetPage.mainFrame();
        const element = await frame.waitForSelector("form#clogs");
        await element.evaluate(form => form.submit());
    }
    await page.waitForNavigation();
    await page.screenshot({ path: 'screenLogin.png' });
    await page.goto("https://my.noip.com/");
    {
        const targetPage = page;
        const frame = targetPage.mainFrame();
        const element = await frame.waitForSelector("aria/DNS Dinamico");
        await element.click();
    }

    const [el] = await page.$x('//a[text()="myadress.torenew.com"]');
    if (el) { await el.click(); }
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'screenPreUpdate.png' });
   
    await page.waitForTimeout(2000);
    const [button] = await page.$x("//button[contains(., 'Update Hostname')]");
    if (button) {
    await button.click();
    }

    await page.waitForTimeout(3000);
    await page.screenshot({ path: 'screenUpdate.png' });
    await browser.close();
    } catch(e) {console.log('main program error:' + e.stack);
    }
})();

