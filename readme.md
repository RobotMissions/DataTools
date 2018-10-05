In this repository, you will find all of the tools related to parsing, editing, visualising, and generally doing things with the data!

The robot's data includes its on-board log that gets saved to the sd card, as well as the imagery data. As we're working on getting the data sorted from this summer, we'll be looking in to what will be useful data to share with the community.

This repository is a work in progress, with a big thanks to @bjb for her work on making the tools for the data!

----

## Bowie Run Times

**LogHandling/runs.py**

This script will calculate how long the Bowie runs have been. This is useful to double check for any times when Bowie might have experienced difficulty by turning off or something. It can serve as a way to highlight the time. The log files do not have to start at 0, but they do have to be sequential.

1. Locate the folder of your logs

2. ```python3 runs.py <<input directory>>```

3. Output that you will see is:

	```
	-----------------
	run durations
	10:36:14 13:05:47 8973 /.../LOG_0.csv /.../LOG_8.csv
	```

	* start timestamp (hour:min:sec)

	* stop timestamp (hour:min:sec)

	* run duration (seconds)

	* filename of the start of the run

	* filename of the stop of the run

4. From here, you can see how long each of the Bowie runs were


**LogHandling/convert_data.py**





