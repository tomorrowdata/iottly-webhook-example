# iottly-webhook-example
A simple example application that forward **iottly** webhooks over web socket.

The application is composed of 2 component:

1. an HTTP server exposing a webhook to the iottly platform
1. a sample Js application showing the messages forwarded to the webhook.

## Obtaining the example application source

You can download the example application source code from [here](https://github.com/tomorrowdata/iottly-webhook-example/archive/master.zip).

Alternatively you can use `git` to clone the GitHub repository to your local
machine

```sh
git clone https://github.com/tomorrowdata/iottly-webhook-example.git
```

## Running the example application

Before running the application make sure to:

- have a linux machine running python3
- be able to reach this machine over the public Internet (required to expose the webhook to **iottly**)

In the `iottly-webhook-example` directory execute:

```sh
pip3 install -r requirements.txt
```
to install the required python dependencies and then

```sh
python3 server/main.py
```
to start the server (**NOTE**: the server will listen by default on port 9000).

The server will log informational messages on `stdout`.

Use `Ctrl + C` to halt the server.


### Running using Docker

If you have Docker installed on your machine you can run the example application
using the provided Dockerfile.

In the `iottly-webhook-example` directory execute
```sh
docker build -t iottly-example .
```
and then run the container with:
```sh
docker run -it -p0.0.0.0:<public port>:9000 iottly-example
```
(**NOTE**: change `<public port>` with a port exposed to the Internet)


## Configure a webhook in iottly

Once the example application is up-and-running you should configure a **webhook** in your **iottly project**.
The webhook URL should be set to the public domain/IP were the example application server is running followed by `/webhook/user`.
 (**NOTE:** Use http or https protocol accordingly to your set-up).

For this example application you should **uncheck** the "Send only payload?" option. In this configuration each message is
forwarded to the webhook as received from the agent.

![Setup the webhook](/docs/webhookconf.png)

If you have never configured a webhook in **iottly** before, check out our simple tutorial [here](https://iottly.github.io/dev/webhooks).

## Access the client

The web client of the example application is served on the same domain. So you should simply point your browser (possibly a modern one) to the public url you have chosen.

For your convenience each message received from web-socket
is logged in your browser console.
