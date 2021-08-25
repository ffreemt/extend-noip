"""Save to tempfile.NamedTemporaryFile.

with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    # url = 'file://' + f.name
    f.write(html)
webbrowser.open('file://' + f.name)

https://stackoverflow.com/questions/21437386/launch-html-code-in-browser-that-is-generated-by-beautifulsoup-straight-from-p

savetofile(text, filename='out.txt', encoding='utf-8', start=False)

Open file in firefox if set

based on savetofile
"""
import os
import pathlib
from pathlib import Path
import tempfile

import subprocess
import platform

import webbrowser
import chardet

# from nose.tools import (eq_, with_setup)

# from loguru import logger as LOGGER
from logzero import logger


# def savetofile(text, filename='out.html', encoding='utf-8', start=False):
# def save_tempfile(text, filename=None, encoding='ascii', start=True):
# fmt: off
def save_tempfile(
        text,
        filename=None,
        encoding='utf-8',
        start=True,
        browser=False,
):  # pylint: disable=too-many-branches, too-many-return-statements
    # fmt: on
    """Save text (str) to file (default to tmp.txt) or filepath (Path(str)).

    if brwoser set to True/1, attempt to use system default open method usin webbrowser package.
    """
    if filename is None:
        filename = tempfile.NamedTemporaryFile('w', delete=False, suffix='.html').name

    if text is None:
        logger.warning('Input is None, exiting...')
        return ''

    if isinstance(text, bytes):
        # _ = cchardet.detect(text)
        _ = chardet.detect(text)
        enc = _['encoding'][:5]  # takes only the first 5
        if enc is None:
            enc = 'UTF-8'

        text = text.decode(enc)

    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            logger.warning(" Not a str, cant convert to a str, exiting")
            return ''

    if isinstance(filename, pathlib.Path):
        fpath = filename.absolute()
    else:
        try:
            fpath = Path(filename).absolute()
        except Exception as exc:
            logger.error(" fpath = Path(filename).absolute() Exception: %s, exiting", exc)
            return ''

    if encoding.lower() in ['utf8', 'utf-8']:
        encoding = 'utf-8'

    #  if encoding == 'ascii': ncr xmlcharrefreplace
    if encoding not in ['utf-8']:
        text = text.encode(encoding, errors='xmlcharrefreplace').decode(encoding)

    with open(str(fpath), 'w', encoding=encoding) as fhandle:
        fhandle.write(text)
        # logger.info("\n\tSaved to %s (encoding: %s)", str(fpath), encoding)
        logger.info("\n\tSaved to %s", str(fpath))

    if browser:
        try:
            webbrowser.open(str(fpath))
            return fpath.__str__()
        except Exception as exc:
            logger.warning("Unable to start webbrowser.open: %s", exc)

    if start:
        # modi

        # 'start' only valid in Windows
        platform_ = platform.system()
        if not platform_ == 'Windows':
            logger.info('Platform is %s, exiting...', platform_)
            return fpath.__str__()

        _ = """
            if sys.platform == "win32":
                os.startfile(filename)
            else:
                opener ="open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filename])
        # """

        try:
            os.startfile(str(fpath))  # type: ignore
            return fpath.__str__()
        except Exception as exc:
            logger.debug('startfile didnt work ...: %s', exc)
            logger.info("Trying firefox in C:...")

        proc = subprocess.Popen([r"C:\Program Files\Mozilla Firefox\firefox.exe", str(fpath)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Opening file in Firefox...")
        err, out = proc.communicate()
        if err:
            logger.error("Start file in firefox errors: %s, out: %s", err, out)

        return fpath.__str__()

    return str(fpath)


def main():
    """Main."""


if __name__ == "__main__":
    main()
