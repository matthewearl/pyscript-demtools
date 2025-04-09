from js import console, document
from pydem.messages import ProtocolVersion


async def run_superimpose(event):
    base_input = document.getElementById("baseDemInput")
    if not base_input.files or len(base_input.files) == 0:
        document.getElementById("downloadLink").innerHTML = "Please select a base DEM file."
        return
    base_file = base_input.files.item(0)

    array_buf = await base_file.arrayBuffer()
    console.log(str(array_buf.to_bytes()))
