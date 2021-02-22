"""Fetch myservices info and update links."""
# pylint:

from typing import List, Optional, Tuple

import asyncio
import re
import more_itertools as mit
from pyquery import PyQuery as pq
import pyppeteer
from logzero import logger


# fmt: off
async def fetch_myservices(
        page: pyppeteer.page.Page,
) -> Tuple[List[Optional[str]], List[Optional[str]]]:
    # fmt: on
    """Fetch my_services info and their update links if any.

    return info, links
    """
    if page.isClosed():
        logger.warning("Invalid page handle provided, return ([], [])...")
        return [], []

    # make sure we are on the right page
    if page.url != "https://www.noip.com/members/dns/":
        try:
            await asyncio.wait([
                page.goto("https://www.noip.com/members/dns/"),
                page.waitForNavigation()
            ])
        except Exception as exc:
            logger.error("%s, exiting", exc)
            return [str(exc)], [""]

    # retrieve Current Hostnames number
    content = await page.content()
    hostname_numb = re.findall(r"Current\s+Hostnames.*\d+", content)

    if not hostname_numb:
        _ = "Not logged in or noip has changed page layout"
        logger.warning("%s, return  ([], [])...", _)
        return [_], []
    # retrieve str inside the list
    (hostname_numb,) = hostname_numb
    logger.info(hostname_numb)  # 'Current Hostnames: 2'

    try:
        numb = int(hostname_numb.split(":")[1])
    except Exception as exc:
        logger.error("%s, setting numb=0", exc)
        numb = 0

    if numb in [0]:  # no hostname configured
        return [hostname_numb], []

    # links
    # pq(content)('a.btn.btn-labeled.btn-configure').outerHtml()

    # [pq(elm).attr('href') for elm in pq(content)('a.btn.btn-labeled.btn-configure')]
    # ['host.php?host_id=77151845', 'host.php?host_id=77151476']

    links = re.findall(r"host.php\?host_id=\d+", content)
    # ['host.php?host_id=77151845', 'host.php?host_id=77151476']

    logger.debug("update links: %s", links)
    _ = "https://www.noip.com/members/dns/"
    full_links = [f"{_}{elm}" for elm in links]
    logger.info("update links (full): %s", full_links)

    # existing services
    _ = pq(content)(".my-services").text()
    logger.debug("existing services: \n%s", _)

    try:
        my_services = [*mit.chunked(_.splitlines()[3:], 4)]
        # my_services = [*mit.chunked(_[3:], 4)]
        my_services = [", ".join(elm[1:3]) for elm in my_services]
    except Exception as exc:
        logger.error(exc)
        my_services = [_.replace("Modify", "").replace("Action", "")]
        logger.info("my servies text: \n%s", my_services)

    return my_services, full_links
    # return [], []
