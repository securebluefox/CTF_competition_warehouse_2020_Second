const crawl = async (url) => {
    console.log(`[*] started: ${url}`)
    
    let browser = await puppeteer.launch(browser_option);
    try {
        {
            const page = await browser.newPage();

            await page.goto(`https://${process.env.DOMAIN}`, {
                waitUntil: 'networkidle0',
                timeout: 5000,
            });

            await page.type('.column:nth-child(2) [name=username]', process.env.ADMIN_USER);
            await page.type('.column:nth-child(2) [name=password]', process.env.ADMIN_PASS);
            await Promise.all([
                page.waitForNavigation({
                    waitUntil: 'networkidle0',
                    timeout: 5000,
                }),
                page.click('.column:nth-child(2) [type=submit]'),
            ]);
            await page.close();
        }

        {
            const page = await browser.newPage();
            await page.goto(url, {
                waitUntil: 'networkidle0',
                timeout: 5000,
            });
            await page.close();
        }
    } catch (err){
        console.log(err);
    }
    await browser.close();
    console.log(`[*] finished: ${url}`)
};