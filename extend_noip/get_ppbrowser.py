"""Extracted from deepl_tr_pp."""
# pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements

from typing import (
    # List,
    Optional,
    # Tuple,
    Union,
)

from pathlib import Path
import asyncio
import platform
import tempfile

from pyppeteer import launch

import logzero
from logzero import logger

from extend_noip.config import Settings

LOOP = asyncio.get_event_loop()

CONFIG = Settings()  # CONFIG = Settings(env=dotenv.find_dotenv())
HEADFUL = CONFIG.headful
DEBUG = CONFIG.debug
PROXY = "" if CONFIG.proxy is None else CONFIG.proxy

logger.info(" HEADFUL: %s", HEADFUL)
logger.info(" DEBUG: %s", DEBUG)
logger.info(" PROXY: %s", PROXY)
if DEBUG:
    logzero.loglevel(10)


# fmt: off
async def get_ppbrowser(
        headless: bool = not HEADFUL,
        proxy: Optional[str] = PROXY,
        executable_path: Optional[Union[str, Path]] = None,
):
    # fmt: on
    """Get a puppeeter browser.

    headless=not HEADFUL; proxy: str = PROXY
    """
    # half-hearted attempt to use an existing chrome
    if Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe").exists():
        executable_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    elif Path(r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe").exists():
        executable_path = r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    # devtools = False
    if not headless:  # if headless is False
        devtools = True  # pop devtools, auto headless=False

    # tempdir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
    # mkdir a random dir for each session

    # tfile = tempfile.NamedTemporaryFile()
    # tfile.close()

    tname = tempfile.NamedTemporaryFile().name
    tempdir = Path("/tmp" if platform.system() == "Darwin" else tname)
    tempdir.mkdir(exist_ok=True)

    try:
        browser = await launch(
            args=[
                "--disable-infobars",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "--window-size=1440x900",
                # "--autoClose=False",
                # f"--proxy-server={PROXY}",
                f"--proxy-server={proxy}",
                "--disable-popup-blocking",  #
            ],
            executablePath=executable_path,  # use chrome
            # autoClose=False,
            headless=headless,
            # devtools=devtools,  # replace headless
            dumpio=True,
            # userDataDir=".",
            userDataDir=tempdir,
        )
    except Exception as exc:
        logger.error("get_ppbrowser exc: %s", exc)
        raise
    # page = await browser.newPage()
    # await page.goto(url)
    # logger.debug("page.goto deepl time: %.2f s", default_timer() - then)
    return browser


try:
    BROWSER = LOOP.run_until_complete(get_ppbrowser(not HEADFUL))
except Exception as exc:
    logger.error(" Unable to pyppeteer.launch exc: %s", exc)
    logger.info(
        "\n\t%s",
        r"Possible cause: abnormal exit from a previous session. Try `taskkill /f /im chrome.exe`",
    )
    logger.warning(" %s", "Note that this will also kill your chrome browser.")
    raise SystemExit(1)
