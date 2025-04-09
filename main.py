import io

from js import (
    console,
    document,
    File,
    Uint8Array,
    URL
)


class UserError(Exception):
    def __init__(self, msg):
        self.msg = msg


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


async def run_superimpose(event):
    try:
        set_names = document.querySelector('input[name="setNames"][value="yes"]').checked

        base_file = await get_base_file()
        other_files = await get_other_files()

        out_file = io.BytesIO()
        for other_file in other_files:
            out_file.write(other_file.read())

        download_file(out_file, 'out.dem')
    except UserError as e:
        document.getElementById("message").innerHTML = f"ERROR: {e.msg}"
