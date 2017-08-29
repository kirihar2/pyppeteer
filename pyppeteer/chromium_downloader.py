#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import BytesIO
import logging
from pathlib import Path
import sys
from urllib import request
from zipfile import ZipFile

from pyppeteer import __chromimum_revision__ as REVISION

logger = logging.getLogger(__name__)
DOWNLOADS_FOLDER = Path.home() / '.pyppeteer' / 'local-chromium'
BASE_URL = 'https://storage.googleapis.com/chromium-browser-snapshots'

downloadURLs = {
  'linux': f'{BASE_URL}/Linux_x64/{REVISION}/chrome-linux.zip',
  'mac': f'{BASE_URL}/Mac/{REVISION}/chrome-mac.zip',
  'win32': f'{BASE_URL}/Win/{REVISION}/chrome-win32.zip',
  'win64': f'{BASE_URL}/Win_x64/{REVISION}/chrome-win32.zip',
}

chromiumExecutable = {
    'linux': DOWNLOADS_FOLDER / REVISION / 'chrome-linux' / 'chrome',
    'mac': (DOWNLOADS_FOLDER / REVISION / 'chrome-mac' / 'Chromium.app' /
            'Contents' / 'MacOS' / 'Chromium'),
    'win32': DOWNLOADS_FOLDER / REVISION / 'chrome-win32' / 'chrome.exe',
    'win64': DOWNLOADS_FOLDER / REVISION / 'chrome-win32' / 'chrome.exe',
}


def curret_platform() -> str:
    """Get current platform name by short string."""
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    elif sys.platform.startswith('win'):
        if sys.maxsize > 2 ** 31 - 1:
            return 'win64'
        return 'win32'
    raise Exception('Unsupported platform: ' + sys.platform)


def get_url() -> str:
    """Get chromium download url."""
    return downloadURLs[curret_platform()]


def download_zip(url: str) -> bytes:
    """Download data from url."""
    logger.warn('start chromium download.\nDownload may take a few minutes.')
    with request.urlopen(url) as f:
        data = f.read()
    logger.warn('chromium download done.')
    return data


def extract_zip(data: bytes, path: Path) -> None:
    """Extract zipped data to path."""
    with ZipFile(BytesIO(data)) as f:
        f.extractall(str(path))
    logger.warn(f'chromium extracted to: {path}')


def download_chromium() -> None:
    """Downlaod and extract chrmoium."""
    extract_zip(download_zip(get_url()), DOWNLOADS_FOLDER / REVISION)


def chromium_excutable() -> Path:
    """Get path of the chromium executable."""
    return chromiumExecutable[curret_platform()]


def check_chromium() -> bool:
    """Check if chromium is placed at correct path."""
    return chromium_excutable().exists()
