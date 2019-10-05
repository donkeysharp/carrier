Carrier
===

Tool that provision cloud instances and can attack multiple web servers that use Apache Http using the Slow Loris DOS technique.


## Usage

### Installing dependencies
Before using Carrier you will need to download and install its dependencies.

```
$ git clone https://github.com/donkeysharp/carrier.git
$ virtualenv env
$ source env/bin/active
$ pip install -r requirements.txt
```

### Provisioning and Attack
Carrier is a simple tool that will let you provision cloud servers and attack multiple vulnerable servers with the provisioned ones.

Just specify the target domains and their protocol scheme before starting the attack.

You need to create a directory called `/home/{your_user}/.carrier` and inside of it a file called `targets` with the following format:

```
site1.com,http
www.site2.com,https
site3.com,https
api.site4.com,https
...
```

And you can start provisioning the servers by running:

```
$ python carrier.py provision --nodes <number of attack servers> --containers-per-node <docker containers on each node that will do the attack> --api-key <DigitalOcean API key>
```

The command above will create a number of servers that will distribute the attack to the hosts specificed in the `/home/your-user/.carrier/targets` file.

To start the Slow Loris attack to the specified hosts run:

```
$ python carrier.py start
```

To stop the attack run:

```
$ python carrier.py stop
```

And finally to delete the attack servers to avoid having them idle run:

```
$ python carrier.py delete
```

The idea of deleting the servers is to reduce costs and pay only for the time that servers will run the attack. DigitalOcean pricing model is per hour which means that if you run the attack for 5 hours in 2 servers, you will charged only for those 10 computing hours.

## Disclaimer
Carrier was created for educational purposes, its author and contributors are not responsible for misuse or for any damage that you may cause!
You agree that you use this software at your own risk.
