# Rexctl: CLI application to control Rex
`Rexctl` is a CLI application to bootstrap and control [Rex](https://github.com/nicrusso7/rexctl/wiki). The purpose of this 
repository is to provide an application to implement the `knowledge tranfer` of the `control policies` pre-trained with 
[rex-gym](https://github.com/nicrusso7/rex-gym).  

# Prerequisites
This code is designed to run on UNIX machines and was tested on the Nvidia Jetson Nano. Check out the 
[Wiki](https://github.com/nicrusso7/rexctl/wiki) for more information on the hardware setup.

`Rexctl` starts a web server using `uwsgi` and `Flask`. In order to allow operations on the board, you need to give 
permissions to the `www-data` user:

```
sudo usermod -a -G gpio www-data
sudo usermod -a -G i2c www-data
```

# Installation
Install this package system-wide.

From the root of the project:
```
sudo -H pip3 install .
```
# Commands
The entry point command is `rexctl`. 

| Command | Description |
| ------- | ----------- |
| init    | Start the web server and initialise the hardware. |
|         | This is the first command you need to run in order to bootstrap the robot. | 
| status  | Get the status of all the daemons. |
| exec | Start a `task`. Check the `/exec` endpoint for more info. |
| log | Get the execution logs. |
| stop-all | Kill all the active `tasks`. |
| debug-pose | Set the debug pose. This is used to check the servos alignment. |
| calibration | Get the BNO055 calibration status. |
| store-calibration | Persist the current BNO055 calibration. |

# API
Rexctl uses `nginx` to create a local DNS entry to map the device name you have setup during the bootstrap to `localhost`.

E.g. using `rex` you will able to access the APIs as follows:
```
http://rex/
```

## Endpoints
### Start a Task

Start a new Task. Currently, the following `tasks` are available:

| Task | Parameters | Description |
| ---- | ---------- | ----------- |
| set_position | * pose_id: (str) The pose name. Check the available poses [here](https://github.com/nicrusso7/rex-gym/blob/aa31345f4d41081deabe11f3d06689220b0d8cb7/rex_gym/model/rex.py#L56). | Set a position setting the servos angles. |
| set_gait | * action_id: (str) The gait name. Check the available poses [here](https://github.com/nicrusso7/rex-gym/blob/1bf66f41e76a699c66949a0d771b79fa67df0160/rex_gym/util/action_mapper.py#L1) | Start a gait running a pre-trained `control policy`. |

**URL** : `/exec`

**Method** : `POST`

**Body**

Provide the `task` name and the required arguments.

```json
{ 
  "daemon_id": "str",
  "command_id": "str",
  "command_args": {
    "arg_0": "value0",
    ...
  }
} 
```

**Examples**

Set a standard position.

```json
{
	"daemon_id": "motion",
	"command_id": "set_position",
	"command_args": {
		"pose_id": "stand_low"
	}
}
```

Start a pre-trained gait.
```json
{
	"daemon_id": "motion",
	"command_id": "set_gait",
	"command_args": {
		"action_id": "walk",
		"simulation": true
	}
}
```

#### Response
**Code** : `200 OK`

### Get the robot status

Get the current status.

**URL** : `/status`

**Method** : `GET`

#### Response
**Code** : `200 OK`

```json
{
	"motion": "active",
	"perception": "active"
}
```

### Stop all the tasks.

Kill all the running tasks.

**URL** : `/stop_all`

**Method** : `GET`

#### Response
**Code** : `200 OK`

```json
{
	"200": "command sent."
}
```

### Get the BNO055 calibration.

Retrieve the current calibration status.

**URL** : `/get_calibration`

**Method** : `GET`

#### Response
**Code** : `200 OK`

```json
{
  "system": "int",
  "gyroscope": "int", 
  "accelerometer": "int", 
  "magnetometer": "int", 
  "mode": "int"
}
```

### Store BNO055 calibration.

Persist the current BNO055 calibration data.
This data will be loaded at every startup.

**URL** : `/store_calibration`

**Method** : `GET`

#### Response
**Code** : `200 OK`

```json
{
	"200": "command sent."
}
```