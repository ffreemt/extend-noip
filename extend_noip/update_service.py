"""Update a given service."""
# pylint:

from typing import List, Optional, Tuple

import asyncio
import re
import pyppeteer
from pyquery import PyQuery as pq
from logzero import logger
from extend_noip.fetch_lastupdate import fetch_lastupdate


# fmt: off
async def update_service(
        link: str,
        page: pyppeteer.page.Page,
) -> Tuple[Optional[str], Optional[str]]:
    # fmt: on
    """Update a given service given link and page handle.

    return last update info, new update info.
    """
    if page.isClosed():
        logger.warning("page handle closed, exiting")
        return "Invalid page: page.isClosed() is True", ""

    if 'login?ref_url' in page.url:
        _ = "no longer logged in, probably timed out, exiting"
        logger.warning(_)
        return _, ""

    try:
        last_update = await fetch_lastupdate(link, page, ip_info=True)
    except Exception as exc:
        logger.error(exc)
        last_update = str(exc)

    logger.debug("Before update: %s", last_update)
    res = str(last_update), ""

    logger.debug("Accessing %s...", link)
    if page.url != link:
        try:
            await asyncio.wait([
                page.goto(link),
                page.waitForNaviation()
            ])
        except Exception as exc:
            logger.error("problem: %s, probably makes no sense to continue, exiting", exc)
            return last_update, str(exc)

    # locate, click the button and update
    # button selector = .form-footer.text-right > input.btn.btn-success
    logger.debug("Updating %s...", last_update)
    try:
        selector = ".form-footer.text-right > input.btn.btn-success"
        handle = await page.waitForSelector(selector, {"timeout": 20000})
    except TimeoutError:
        logger.error(TimeoutError)
        raise
    except Exception as exc:
        logger.error("%s", exc)
        raise SystemExit(1) from exc

    try:
        coros = [handle.click(), page.waitForNaviation()]
        await asyncio.wait(coros)
    except Exception as exc:
        logger.error("%s", exc)
        # raise SystemExit(1) from exc
        res = res[0], str(exc)

    # update info after update
    try:
        last_update = await fetch_lastupdate(link, page, ip_info=True)
    except Exception as exc:
        logger.error(exc)
        last_update = str(exc)

    logger.debug("After update: %s", last_update)

    res = res[0], str(last_update)

    return res
    # return res[0], ""
