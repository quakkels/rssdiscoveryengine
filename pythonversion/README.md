> ## Planned JavaScript Port
> RSS Discovery Engine is facing problems related to bots taking advantage of it and spaming websites with requests. The result is some sites are forced to block the server's IP address.

>Since the engine keeps no cache nor persists any spidered data to disk, the engine would work on the client. So the plan is to port the engine from Python to client side JavaScript. Once it's running in the client, blocking a spammer means the spammer's own IP gets blocked. Therefore, the many legitimate users of RSS Discovery Engine would not be affected.

# RSS Discovery Engine

The [RSS Discovery Engine](https://rdengine.quakkels.com/) exists to encourage people to use RSS for finding and consuming their news and current events.

![RSS Discovery Engine Screenshot](http://quakkels.com/images/rde_dark.png)

Check it out here: [rdengine.quakkels.com](https://rdengine.quakkels.com/)

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

## Resources
- [RSS is Wonderful](https://quakkels.com/posts/rss-is-wonderful/)

## License

RSS Discovery Engine is licensed under the [MIT](LICENSE) license.
