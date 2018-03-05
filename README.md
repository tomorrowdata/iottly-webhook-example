# iottly-webhook-example
A simple example application that forward **iottly** webhooks over WS

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
- be able to reach this machine over the public Internet

In the `iottly-webhook-example` directory execute:

```sh
pip3 install -r requirements.txt
```
to install the required python dependencies and then

```sh
python3 server/main.py
```
to start the server (**NOTE**: the server will listen by default on port 9000).


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



More detailed docs on how to configure webhook in **iottly** can be found [here](https://iottly.github.io/dev/webhooks).
