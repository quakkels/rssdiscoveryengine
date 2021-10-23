# RSS Discovery Engine

The RSS Discovery Engine exists to encourage people to use RSS for finding and consuming their news and current events.

![RSS Discovery Engine Screenshot](http://quakkels.com/images/rde_dark.png)

## Running RSS Discovery Engine locally

These instructions assume a Unix-like system.

First, run the bootstrap script, which will create a virtual environment in `.venv` and install the Python requirements within it. You only need to do this once.

```shell
./bootstrap.sh
```

And then run the development server, which will make a development server accessible on `http://localhost:5000/`:

```shell
./run.sh
```
