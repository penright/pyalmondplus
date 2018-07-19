# -*- coding: utf-8 -*-

"""Console script for pyalmondplus."""
import sys
import json
import time
import click
import pyalmondplus.almond_plus
import threading
import ruamel.yaml as yaml


def do_commands(url, my_api):
    click.echo("Connecting to " + url)
    while True:
        value = click.prompt("What next: ")
        print("command is: " + value)
        if value == "stop":
            break
        elif value == "dl":
            tmp_list = my_api.get_device_list()
            for tmp_entity in tmp_list:
                print(str(tmp_entity))
        elif value == "set":
            tmp_list = my_api.get_device_list()
            for tmp_entity in tmp_list:
                print(tmp_entity)
            id = input("Enter ID: ")
            device_id = input("Enter Device ID: ")
            if tmp_list.exist(id, device_id) is False:
                print("Device does not exist")
            else:
                value = input("Enter value: ")
                print(my_api.set_device(id, device_id, value))
    print("Do command is stopped")
    my_api.stop()
    my_api = None
    time.sleep(3)


def api_start(url, my_api):
    print("Do commands 1")
    my_api.start()
    print("Connected to Almond+")


@click.command()
@click.option('--url', default='')
def main(url):
    main_run(url)


def receive_callback(resp):
    print("resp: "+resp)


def main_run(url):
    my_api = pyalmondplus.almond_plus.PyAlmondPlus(url, receive_callback)
    do_command = threading.Thread(target=do_commands, args=(url, my_api))
    do_command.start()
    start_api = threading.Thread(target=api_start, args=(url, my_api))
    start_api.start()


def read_yaml():
    with open('../secrets.yaml') as fp:
        my_configuration_dict = yaml.safe_load(fp)
        fp.close()
        return my_configuration_dict


if __name__ == "__main__":
    my_configuration_dict = read_yaml()
    print("My URL: "+my_configuration_dict['almond_plus_url'])
    main_run(my_configuration_dict['almond_plus_url'])
