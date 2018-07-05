# -*- coding: utf-8 -*-

"""Console script for pyalmondplus."""
import sys
import time
import click
import pyalmondplus.api
import threading
import asyncio

def do_commands(url, my_api):
    click.echo("Connecting to " + url)
    while True:
        value = click.prompt("What next: ")
        print("command is: " + value)
        if value == "stop":
            break
        elif value == "dl":
            my_api.get_device_list()

    print("Do command is stopped")
    my_api.stop()
    time.sleep(3)


def api_start(url, my_api):
    print("Do commands 1")
    my_api.start()
    print("Connected to Almond+")


@click.command()
@click.option('--url', default='')
def main(url):
    my_api = pyalmondplus.api.PyAlmondPlus(url)
    do_command = threading.Thread(target=do_commands, args=(url, my_api))
    do_command.start()
    start_api = threading.Thread(target=api_start, args=(url, my_api))
    start_api.start()
