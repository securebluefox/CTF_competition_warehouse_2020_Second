const crawl = async (url) => {
    console.log(`[*] started: ${url}`)
    
    let browser = await puppeteer.launch(browser_option);
    const page = await browser.newPage();
    try {
        await page.authenticate({username: 'seccon', password: 't0nk02'});

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

        await page.goto(url, {
            waitUntil: 'networkidle0',
            timeout: 5000,
        });
    } catch (err){
        console.log(err);
    }
    await page.close();
    await browser.close();
    console.log(`[*] finished: ${url}`)
};