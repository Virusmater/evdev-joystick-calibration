# evdev-joystick-calibration
Run, pick up the gamepad and turn sticks with triggers around. 
```bash
evdev-joystick-calibration -h
usage: evdev-joystick-calibration [-h] [-l] [-c]

Pick up the gamepad and turn sticks with triggers around

optional arguments:
  -h, --help       show this help message and exit
  -l, --load       load configuration
  -c, --calibrate  calibrate and save configuration
```
# install
```bash
kompot@pc:~$ sudo apt install python3-pip git -y
kompot@pc:~$ sudo pip3 install git+https://github.com/Virusmater/evdev-joystick-calibration
```
# example
## calibrate
```bash
kompot@pc:~$ evdev-joystick-calibration -c
Available devices:
0 Nintendo Wii Remote Classic Controller
2 Nintendo Wii Remote IR
3 Nintendo Wii Remote Accelerometer
4 Wii U GameCube Adapter Port 1
Pick one device for the calibration: 0
Move sticks and triggers of Nintendo Wii Remote Classic Controller to max and min positions.
Press any button to apply.
Configuration for Nintendo Wii Remote Classic Controller
analog: ABS_HAT1Y  min:-28 max:25
analog: ABS_HAT1X  min:-26 max:26
analog: ABS_HAT2X  min:-28 max:24
analog: ABS_HAT2Y  min:-28 max:24
analog: ABS_HAT3X  min:6 max:46
analog: ABS_HAT3Y  min:2 max:40
Configuration for Nintendo Wii Remote Classic Controller saved at /home/kompot/.config/evdev-joystick-calibration/NintendoWiiRemoteClassicController.json
```
## load
```bash
kompot@pc:~$ evdev-joystick-calibration -l
Configuration for Nintendo Wii Remote Classic Controller loaded from /home/kompot/.config/evdev-joystick-calibration/NintendoWiiRemoteClassicController.json
Configuration for Nintendo Wii Remote Classic Controller
analog: ABS_HAT1Y  min:-28 max:25
analog: ABS_HAT1X  min:-26 max:26
analog: ABS_HAT2X  min:-28 max:24
analog: ABS_HAT2Y  min:-28 max:24
analog: ABS_HAT3X  min:6 max:46
analog: ABS_HAT3Y  min:2 max:40
Skip Nintendo Wii Remote IR
Skip Nintendo Wii Remote Accelerometer
Skip Wii U GameCube Adapter Port 1
```
# requirements
https://github.com/gvalkov/python-evdev

The user should be able to write to the evdev device. Example of udev rule for Nintendo Wii Remote Classic Controller
```bash
kompot@pc:~$ sudo nano /etc/udev/rules.d/99-wiimote.rules 
SUBSYSTEM=="input", ATTRS{name}=="Nintendo Wii Remote Classic Controller", MODE="0666", ENV{ID_INPUT_JOYSTICK}="1", ENV{ID_INPUT_KEY}="0"
```
# auto load configuration on connect
1. Run calibration **as root** (unfortunatelly all udev rules are executed under root and there is no way to get current user. if you know how to avoid it - please let me know):
`kompot@pc:~$ sudo evdev-joystick-calibration -c`
2. Make new udev rule for add action:
```bash
kompot@pc:~$ sudo nano /etc/udev/rules.d/99-wiimote.rules 
SUBSYSTEM=="input", ATTRS{name}=="Nintendo Wii Remote Classic Controller", MODE="0666", ENV{ID_INPUT_JOYSTICK}="1", ENV{ID_INPUT_KEY}="0"
SUBSYSTEM=="input", KERNEL=="event*", ACTION=="add", ATTRS{name}=="Nintendo Wii Remote Classic Controller", RUN+="/bin/sh -c 'evdev-joystick-calibration -l'"
```
3. Reload rules:
`sudo udevadm control --reload-rules`
