# Task 2: Face Detection Game

## Format

There are two files namely `gamePrototype.py` which is as the name suggests a prototype game environment of final game (Refer to task2.pdf for more information about the task) and `T2.py` which is the solution file for this task.  

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install opencv.

```bash
pip install opencv-contrib-python
```

### Run the game

```bash
python T2.py
```

## General Instruction for smooth gameplay
* The program is to be run on a machine with webcam
* There should be a single face detected in the feed
* Maintain atleast 50 cm gap between your face and screen (Reason for this has been well documented in task2.pdf)
* Refrain from taking your face outside the frame

#### Endnote
The program employs face detection which is computationally heavy and the data in program changes every instance. It is natural for the program to halt when an anomly is found (face not detected or taken out of feed). However the game is playable is all the general instructions are followed.
