# pyalmondplus

This is an API for the Home Assistant home automation.
It is a wrapper for the Almond+ websocket interface.
The Almond+ is a discontinued product from Securifi. It main goal was a wifi router, but they added zwave and zigbee radios and has some decent automation. But Home Assistant is better, so now with this API you can use the Almond+ as a zwave and zigbee hub.

See both https://www.home-assistant.io/ and https://forum.securifi.com/ for more information.
This is to test an update(3).

## Getting Started

Not sure what I need here yet.

### Prerequisites

The assumption is Home Assistant is up and running. The API uses python's websockets 5.0.

### Installing

Not Sure what I need  here either?

## Running the tests

There is a testapi entry point console script for testing. It takes a --url parameter and it is the URL that connects to the Almond+.
For example testapi --url ws://192.168.1.20:8671/root/password

## Deployment

Need to: Add additional notes about how to deploy this on a live system

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/?fromMenu)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Paul Enright** - *Started project*

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Hat tip to @kvldr for his jump start.
* Also @rytilahti for helping me to learn how to setup the dev environment.
* Hat tip to anyone whose code was used
