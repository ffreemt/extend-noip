"""Login to https://www.noip.com/members/dns/."""
# pylint:

from typing import Optional

import os
import asyncio
import dotenv
import pyppeteer
from logzero import logger
from extend_noip.get_ppbrowser import get_ppbrowser, BROWSER

# load .env to os.environ
dotenv.load_dotenv()
URL = "https://www.noip.com/members/dns/"


# fmt: off
async def login_noip(
        username: Optional[str] = "",
        password: Optional[str] = "",
        browser = BROWSER,
) -> pyppeteer.page.Page:
    # fmt: on
    """Login to https://www.noip.com/members/dns/.

    return a pyppeteer.page.Page for subsequent processin.
    """
    try:
        _ = await browser.newPage()
    except Exception as exc:
        logger.error(exc)
        logger.info("Getting a new ppbrowser...")
        browser = await get_ppbrowser()

    page = await browser.newPage()

    try:
        logger.debug("Going to %s", URL)
        # await page.goto(URL, {"timeout": 20000})
        await asyncio.wait([
            page.goto(URL),
            page.waitForNavigation(),
        ])
    except Exception as exc:
        logger.error(exc)
        await asyncio.sleep(.2)

    # We give it another try
    try:
        _ = await page.waitForXPath('//*[contains(text(),"Dashboard")]', {"timeout": 20000})

        # already logged in
        if "Dashboard" in (await page.content()):
            logger.info("Already logged in.")
            # raise SystemExit(" Change this to return page ")
            return page
    except Exception as exc:
        logger.error("Not logged in yet, exc: %s, proceed", exc)

    # proceed
    # wait for form/submit
    logger.debug("Trying logging in...")
    try:
        handle = await page.waitForSelector("#clogs", {"timeout": 20000})
    except TimeoutError:
        logger.error(TimeoutError)
        raise
    except Exception as exc:
        logger.error("Unable to fetch the page, network problem or noip has changed page layout, %s, existing", exc)
        raise SystemExit(1) from exc

    if not username:  # or email
        username = os.environ.get("NOIP_USERNAME")
    if not password:
        password = os.environ.get("NOIP_PASSWORD")

    if username is None:
        logger.error('Supply username or email address login_noip(username="...") or set it in .env or as ENVIRONMENT (set/export NOIP_USERNAME="...")')
        raise SystemExit(1)

    if not password:
        logger.error('Supply password, e.g., login_noip(password="...") or set it in .env or as ENVIRONMENT (set/export NOIP_USERNAME="...")')
        raise SystemExit(1)

    logger.info("\nusername: %s \npassword: %s", "*" * 6 + username[6:], "*" * len(password))

    logger.debug("Logging in with username/email and password")
    try:
        await page.type('input[name="username"]', username, {"delay": 20})
        await page.type('input[name="password"]', password, {"delay": 20})
        # await handle.type('input[name="username"]', username, {"delay": 20})
        # await handle.type('input[name="password"]', password, {"delay": 20})

        bhandle = await page.xpath('//*[@id="clogs"]/button')
        await bhandle[0].click()
    except Exception as exc:
        logger.error("Oh no, exc: %s, exiting", exc)
        raise SystemExit(1)

    # wait for page to load
    logger.info("Waiting for Dashboard to load...")
    try:
        _ = await page.waitForXPath('//*[contains(text(),"Dashboard")]', {"timeout": 45000})
    except Exception as exc:
        logger.error("No go, exc: %s, exiting", exc)
        if "incorrect" in (await page.content()):
            logger.info("""Username / Password combination is incorrect. Please try again.""")
        # raise Exception(str(exc))
        logger.warning("Bad news: we are _not_ in, closing the page")
        await page.close()
        return page  # use page.isClosed() to check

    logger.info("Good news: we are in.")

    return page
