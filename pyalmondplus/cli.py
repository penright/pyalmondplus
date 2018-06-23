# -*- coding: utf-8 -*-

"""Console script for pyalmondplus."""
import sys
import click
import pyalmondplus.api


@click.command()
@click.option('--url', default='')
def main(url):
    """Console script for pyalmondplus."""
    click.echo("Connecting to " + url)
    almond_devices = pyalmondplus.api.PyAlmondPlus(url)
    click.echo("Email Name: " + almond_devices.email_id)


    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
