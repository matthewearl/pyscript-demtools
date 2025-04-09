import io

from js import (
    console,
    document,
    File,
    Uint8Array,
    URL
)
from pydem.messages import ProtocolVersion


def set_error(msg):
    document.getElementById("message").innerHTML = f"ERROR: {msg}"


async def upload_files(id_):
    input_ = document.getElementById(id_)
    console.log(str(input_.files))

    out = []
    for file in input_.files:
        bytes_ = (await file.arrayBuffer()).to_bytes()
        out.append(io.BytesIO(bytes_))
    return out


async def get_base_file():
    files = await upload_files("baseDemInput")
    if len(files) == 0:
        set_error("Please select a base DEM file")
    elif len(files) > 1:
        set_error("Please select only one base DEM file")
    else:
        return files[0]


def download_file(f, fname):
    js_array = Uint8Array.new(f.seek(0, 2))
    js_array.assign(f.getbuffer())

    file = File.new([js_array], "", {type: "binary/octet-stream"})
    url = URL.createObjectURL(file)

    hidden_link = document.createElement("a")
    hidden_link.setAttribute("download", fname)
    hidden_link.setAttribute("href", url)
    hidden_link.click()


async def run_superimpose(event):
    base_file = await get_base_file()

    out_f = io.BytesIO(b'!!!' + base_file.read() + b'!!!')

    download_file(out_f, 'out.dem')
