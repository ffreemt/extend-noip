"""Fetch info on Last Update."""
# pylint:

from typing import Optional

import asyncio
import re
import pyppeteer
from pyquery import PyQuery as pq
from logzero import logger

# fmt: off
async def fetch_lastupdate(
        link: Optional[str],
        page: pyppeteer.page.Page,
        ip_info: bool = False,
) -> str:
    # fmt: on
    """Fetch info on Last Update."""
    if page.isClosed():
        return "Invalid page: page.isClosed() is True"

    logger.debug("link: %s", link)
    logger.debug("page.url: %s", page.url)

    # if link is None, use page.url
    if link is None:
        link = page.url

    if link != page.url:  # already there at link
        try:
            # await page.goto(link)
            await asyncio.wait([
                page.goto(link),
                page.waitForNavigation()
            ])
        except TimeoutError:
            logger.error("Timed out.")
            return "Timed out."
        except Exception as exc:
            logger.error(exc)
            return str(exc)

    content = await page.content()
    doc = pq(content)

    ip_address = pq(content)("#ip").attr("value")
    if ip_address is None:
        ip_address = ""

    last_update = [pq(elm).text() for elm in doc(".form-group") if 'Last Update' in pq(elm).text()]
    # ['IP Address\nLast Update 2021-02-20 10:16:18 PST']

    logger.debug("last update: %s", last_update)
    if last_update:
        last_update = str(last_update[0])

    # keep the last part
    #    'IP Address\nLast Update 2021-02-20 10:16:18 PST'
    # -> 'Last Update 2021-02-20 10:16:18 PST'

    temp = re.search(r"Last Update.*", str(last_update))
    if temp:
        last_update = temp.group()

    if ip_info:
        return f"{ip_address} {str(last_update)}"

    return str(last_update)
