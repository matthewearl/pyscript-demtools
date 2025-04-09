import io

from js import console, document
from pydem.messages import ProtocolVersion


async def get_base_file():
    base_input = document.getElementById("baseDemInput")
    if not base_input.files or len(base_input.files) == 0:
        document.getElementById("downloadLink").innerHTML = "Please select a base DEM file."
        return
    base_file = base_input.files.item(0)
    base_bytes = (await base_file.arrayBuffer()).to_bytes()
    return io.BytesIO(base_bytes)


async def run_superimpose(event):
    base_file = await get_base_file()
    console.log(str(base_file.getvalue()))
