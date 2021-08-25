"""Test login.

pytest --log-cli-level=20 tests -k login

https://miyakogi.github.io/pyppeteer/_modules/pyppeteer/launcher.html

"""
# pylint:

import os
import asyncio
import atexit
import dotenv
import pytest
from logzero import logger

from extend_noip.login_noip import login_noip
from extend_noip.get_ppbrowser import LOOP, BROWSER

_ = dotenv.find_dotenv()
if _:
    logger.info("Loading .env from %s", _)
    dotenv.load_dotenv()

#  All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


# async def _cleanup():
def _cleanup():
    import sys

    try:
        # LOOP.run_until_complete(BROWSER.close())
        ...
    except Exception as exc:
        logger.debug(" BROWSER.close exc: %s", exc)
    finally:
        # sys.exit(0)
        ...


# atexit.register(_cleanup)


async def test_login():
    """Test login."""
    # assert os.environ.get("NOIP_USERNAME"), 'You need to set NOIP_USERNAME, e.g. set NOIP_USERNAME="your noip_username or email address or set it up in .env (refer to .env.sample)'
    # assert os.environ.get("NOIP_PASSWORD"), 'You need to set NOIP_USERNAME, e.g. set NOIP_USERNAME="your noip_username or email address or set it up in .env  (refer to .env.sample)'

    try:
        page = await login_noip()
        assert "DASHBOARD" in (await page.content())
        # await page.close()
        # await BROWSER.close()
        # await BROWSER.killChrome()
        await page.browser.close()
        await asyncio.sleep(0.4)
    except Exception as exc:
        logger.error(exc)


async def test_failed_login():
    """Test login."""
    try:
        page = await login_noip(username="abc")
        assert "DASHBOARD" in (await page.content())
        # await page.close()
        # await BROWSER.close()
        # await BROWSER.killChrome()
        await page.browser.close()
        await asyncio.sleep(0.4)
    except Exception as exc:
        logger.error(exc)
