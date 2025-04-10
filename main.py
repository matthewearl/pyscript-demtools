import io
import logging

import demsuperimpose
import showros
from js import (
    document,
    File,
    Uint8Array,
    URL
)


logger = logging.getLogger(__name__)


class HTMLTextAreaHandler(logging.Handler):
    def __init__(self, element_id):
        super().__init__()
        self._element_id = element_id

    def emit(self, record):
        msg = self.format(record)
        textarea = document.getElementById(self._element_id)
        textarea.value += msg + '\n'
        textarea.scrollTop = textarea.scrollHeight


class UserError(Exception):
    def __init__(self, msg):
        self.msg = msg


async def upload_files(id_):
    input_ = document.getElementById(id_)

    out = []
    for file in input_.files:
        bytes_ = (await file.arrayBuffer()).to_bytes()
        out.append(io.BytesIO(bytes_))
    return out


async def get_base_file():
    files = await upload_files("baseDemInput")

    if len(files) == 0:
        raise UserError("Please select a base demo file")

    if len(files) > 1:
        raise UserError("Please select only one base DEM file")

    return files[0]


async def get_other_files():
    files = await upload_files("otherDemsInput")

    if len(files) == 0:
        raise UserError("Please select at least one non-base DEM file")

    return files


def download_file(f, fname):
    js_array = Uint8Array.new(f.seek(0, 2))
    js_array.assign(f.getbuffer())

    file = File.new([js_array], "", {type: "binary/octet-stream"})
    url = URL.createObjectURL(file)

    hidden_link = document.createElement("a")
    hidden_link.setAttribute("download", fname)
    hidden_link.setAttribute("href", url)
    hidden_link.click()


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    html_handler = HTMLTextAreaHandler("log-box")
    html_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s: %(message)s'
        )
    )
    logger.addHandler(html_handler)

    document.getElementById("log-box").value = ""


async def run_superimpose(event):
    try:
        set_names = document.querySelector(
            'input[name="setNames"][value="yes"]'
        ).checked

        base_dem_file = await get_base_file()
        other_dem_files = await get_other_files()

        out_dem_file = io.BytesIO()
        demsuperimpose.superimpose(
            base_dem_file, other_dem_files, out_dem_file, set_names
        )

        download_file(out_dem_file, 'out.dem')
    except UserError as e:
        logger.error("user error: %s", e.msg)


async def run_showros(event):
    try:
        files = await upload_files("demInput")
        if len(files) == 0:
            raise UserError("Please select a base demo file")
        if len(files) > 1:
            raise UserError("Please select only one base DEM file")
        in_dem_file = files[0]

        out_dem_file = io.BytesIO()
        showros.show_ros(in_dem_file, out_dem_file, None)

        download_file(out_dem_file, 'out.dem')
    except UserError as e:
        logger.error("user error: %s", e.msg)


setup_logging()
logger.info('ready!')
