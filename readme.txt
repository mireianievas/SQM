# Sky Quality Meter file validator
# Writen by Miguel Nievas (UCM) miguelnr89[at]gmail[dot]com


This simple program has been designed to validate SQM data files according to the Community Standard defined by Christopher Kyba et al. in July 2012 (http://unihedron.com/pipermail/sqm/2012-July/000136.html).

Latest supported version of the standard is 0.1.5. 



The validator consists on a single script written with Python 2.7 in mind. It has not been tested in other Python versions.

You can get Python 2.7 here: http://python.org/download/

To launch the program, open a terminal/console session and type,

Windows:
	>> C:\Path\to\Python\Python.exe sqm_data_validator_s%%%_v###.py mysqmdatafile
	
Linux:
	>> /path/to/python sqm_data_validator_s%%%_v###.py mysqmdatafile

	
You will need to replace
	%% with the standard version (p.e. 015, thats it 0.1.5), 
	## with the validator version (p.e. 010, thats it, 0.1.0) 
	mysqmdatafile with the complete or relative path to the SQM data file you want to analize.

The program will show on screen a list of detected errors (some errors are considered critical and the program halts).




Summary of detectable errors:
	- File existence.
	- File is openable.
	- Header length.
	- File contains data.
	- Version of the standard (if it is not the same as in the analizer, print a warning message).
	- Header keywords: device type, instrument ID, Data supplier, Location name, Latitude/Longitude/Altitude, Local timezone, Time synchronization method, position (moving/stationary), direction (moving/fixed), number of channels, number of filters per channel, number of measurement directions per channel, field of view, number of data fields, SQM serial number, SQM firmware version, cover/enclosure offset.
	- Data fields:
		* if the day/month are correct (althought it doesnt check if the year is bisiest).
		* If date&time format is correct.
		* If temperature, flux and MSAS is a float number.
