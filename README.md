# Depallettizer
 SMR1 Depalletizer project

 Special Thanks to
    - Guus Zwart for guiding us through the project, and being a great client.
    - Thijs Brilleman for helping us with project related difficulties.
    - Mathijs van der Vegt for helping us with technical difficulties.

 This is the main code used for the project.
 The most important files are:
 [main.py](main.py)
 [Labels.py](labeldetectie/labels.py)
 [RealSense.py](IntelRealsence/RealSense.py)

 main.py is the main program which sets up the TCP/IP connection, and handles the communication commands with the robot.
 labels.py can be run on it's own, to test label detection algorithm.
 RealSense.py can als be run on it's own, to test box detection algorithm.