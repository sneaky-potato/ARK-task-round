# Task 3: Path Planning and Computer Vision puzzle

## Format

All the files present in the main directory have been named according to the levels. The **Input** directory is to contain the raw files which were given in problem statement (refer to task3.pdf for more information about problem statement and approach followed). The **output** directory is to contain every processed result which was created either in between some level *OR* after some level

## Sequence followed

* `lvl1_read_ascii.py` is to solve the first level and outputs `lvl1_message.txt` inside the **output** directory
* `lvl2_template_match.py` first transforms the searchable template matrix, outputs `lvl2_transformed.png`, then searches this template in `zucky_elon.png` (**Input**) and then outputs `lvl2_zucky_elon_search.png`. It should also print the value used for next level.
* `lvl3_password_crack.py` first removes the noise from `maze_lv3.png` (**Input**), outputs the denoised form `lvl2_denoised.png`, it then asks the user to click at two places- starting point and finish point. A mouse callback function has been attached and it should prompt in the terminal also. After clicking first at starting point and then at ending point, the python script then employs Dijkstra's algorithm to solve the maze. Solved maze contains the password to `treasure.zip` (**Input**)
* After extraction, place the `treasure_mp3.png` (should be the zipped file) in **output** directory and then run the `lvl4_rgb_to_mp3.py` to extract ASCII bits and output `lvl4_binary_file.dat`
* Change the file's extension from .dat to .mp3 and enjoy the tunes :-)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install opencv.

```bash
pip install opencv-contrib-python
```

## Treasure
Although you can easily find the output results in **output** directory, however I must mention that the end result or the final treasure for the whole puzzle is `lvl4_binary_file.mp3`.
