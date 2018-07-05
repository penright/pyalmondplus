# -*- coding: utf-8 -*-

"""Console script for pyalmondplus."""
import sys
import asyncio
import time
import threading
import click
import pyalmondplus.api

loop = None
@click.command()
@click.option('--url', default='')

def main(url):
    """Console script for pyalmondplus."""
    click.echo("Connecting to " + url)
    almond_devices = pyalmondplus.api.PyAlmondPlus(url, loop)
    almond_devices.start()
    print("Connected to Almond+")
    while True:
        value = click.prompt("What next: ")
        print("command is: " + value)
        if value == "stop":
            break
    almond_devices.stop()
    return 0

def LoopStart():
    global loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

if __name__ == "__main__":
    t = threading.Thread(target=LoopStart())
    t.start()
    sys.exit(main())  # pragma: no cover
