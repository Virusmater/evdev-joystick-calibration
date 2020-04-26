# evdev-joystick-calibration
Run, pick up the gamepad and turn sticks with triggers around
# example
```bash
kompot@pc:~/evdev-joystick-calibration$ python3 __main__.py 
Available devices:
0 Wii U GameCube Adapter Port 1
1 Nintendo Wii Remote Classic Controller
3 Nintendo Wii Remote IR
4 Nintendo Wii Remote Accelerometer
Pick one device for the calibration: 1
Move sticks and triggers of Nintendo Wii Remote Classic Controller to max and min positions.
Press any button to apply.
New configuration:                    
analog: ABS_HAT2X  min:-28 max:24
analog: ABS_HAT2Y  min:-28 max:24
analog: ABS_HAT1Y  min:-28 max:25
analog: ABS_HAT1X  min:-26 max:24
analog: ABS_HAT3X  min:6 max:44
analog: ABS_HAT3Y  min:2 max:42
```
# requirements
https://github.com/gvalkov/python-evdev
The user should be able to write to the evdev device. Example of udev rule for Nintendo Wii Remote Classic Controller
```bash
kompot@pc:~$ cat /etc/udev/rules.d/99-wiimote.rules 
SUBSYSTEM=="input", ATTRS{name}=="Nintendo Wii Remote Classic Controller", MODE="0666", ENV{ID_INPUT_JOYSTICK}="1", ENV{ID_INPUT_KEY}="0"

```
