from setuptools import setup, find_packages

setup(
    name='evdev-joystick-calibration',
    version='0.1',
    description='Run, pick up the gamepad and turn sticks with triggers around',
    url='https://github.com/Virusmater/evdev-joystick-calibration',
    author='Dima Kompot',
    author_email='virusmater@gmail.com',
    license='MIT',
    install_requires=['evdev'],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['evdev-joystick-calibration=src.__main__:main']
    )
)
