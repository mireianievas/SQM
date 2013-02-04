#!/bin/env python
# Tested in Python 2.7 .

try:
	import sys
except:
	print('Error importing essential modules')

__author__ = "Miguel Nievas"
__copyright__ = ""
__license__ = "GPL"
__version__ = "0.01"
__maintainer__ = "Miguel Nievas"
__email__ = "miguelnr89[at]gmail[dot]com"
__status__ = "Prototype" # "Prototype", "Development", or "Production"


# Some constants
HeaderLength = 35
NumberDataColumns = 6
VersionStandard = '0.1.5' # If file format follows a different version of the standard, print a Warning.



class PrintHelp():
	def print_help(self):
		HelpMessage = \
			'-----------------------------------------------------------\n'+\
			'Simple script to validate SQM data file according to v'+str(VersionStandard)+'\n'+\
			'Light Pollution Monitoring Data Format 0.1.5 standard.     \n'+\
			'-----------------------------------------------------------\n'+\
			'Example: '+str(sys.argv[0])+' sqmle_obs_2013-01-01.dat\n\n'+\
			'Returns:\n'+\
			'  [OK] File is standard compliant \n'+\
			'  or \n'+\
			'  [ERR] Invalid File.\n'+\
			'    {List of detected errors}\n'
		print(HelpMessage)

class PrintError():
	def print_error(self):
		ErrorMessage = \
			'[ERR] Invalid File.\n'
		for error in self.ErrorList:
			ErrorMessage +='  '+str(error)+'\n'
		print(ErrorMessage)


class SqmDataFile(PrintHelp,PrintError):
	def validate_file(self):
		self.ErrorList = []
		self.test_file = ''
		try:
			self.test_file = sys.argv[1]
			self.file_content = open(self.test_file,'r').readlines()
		except:
			self.ErrorList.append('Cannot open file: '+str(self.test_file))
		else:
			self.extract_header()
			self.extract_data()
		
		if len(self.ErrorList)>0:
			self.print_error()
			self.print_help()
			exit(0)
	
	def extract_header(self):
		self.header = [line for num,line in enumerate(self.file_content) if line[0]=='#' and num<HeaderLength]
		if len(self.header)!=HeaderLength:
			self.ErrorList.append('Header length is not '+str(HeaderLength)+' but '+str(len(self.header)))
			self.print_error()
	
	def extract_data(self):
		self.data = [line for num,line in enumerate(self.file_content) if line[0]!='#' and num>=HeaderLength]
		if len(self.data)==0:
			self.ErrorList.append('No data found in file')
			self.print_error()


class SqmAnalysis(SqmDataFile):
	def __init__(self):
		self.validate_file()
		self.test_header()
		self.test_data()
	
	def test_header(self):
		# Test if header follows the standard format.
		# Note that python starts to count from 0, so line 23 is actually line 24
		try:
			header_device_type = [self.header[0][2:40],self.header[0][41:]]
			assert header_device_type[0] == 'Light Pollution Monitoring Data Format'
			assert header_device_type[1] != '\n' and header_device_type[1] != '\r\n'
			assert header_device_type[1][0:len(VersionStandard)] == VersionStandard
		except:
			print('Warning: file uses a different standard version')
		
		try:
			header_device_type = [self.header[4][2:13],self.header[4][15:]]
			assert header_device_type[0] == 'Device type'
			assert header_device_type[1] != '\n' and header_device_type[1] != '\r\n'
		except:
			self.ErrorList.append('No device type found in line 5')
		
		try:
			header_instrument_id = [self.header[5][2:15],self.header[5][17:]]
			assert header_instrument_id[0] == 'Instrument ID'
			assert header_instrument_id[1] != '\n' and header_instrument_id[1] != '\r\n'
		except:
			self.ErrorList.append('No Instrument ID found in line 6')
		
		try:
			header_data_supplier = [self.header[6][2:15],self.header[6][17:]]
			assert header_data_supplier[0] == 'Data supplier'
			assert header_data_supplier[1] != '\n' and header_data_supplier[1] != '\r\n'
		except:
			self.ErrorList.append('No Data supplier found in line 7')
		
		try:
			header_location_name = [self.header[7][2:15],self.header[7][17:]]
			assert header_location_name[0] == 'Location name'
			assert header_location_name[1] != '\n' and header_location_name[1] != '\r\n'
		except:
			self.ErrorList.append('No Location name found in line 8')
		
		try:
			header_position = [self.header[8][2:10],self.header[8][12:]]
			assert header_position[0] == 'Position'
			assert header_position[1] != '\n' and header_position[1] != '\r\n'
			try:
				latitude = float(header_position[1].split(",")[0])
				longitude = float(header_position[1].split(",")[1])
				altitude = float(header_position[1].split(",")[2])
			except:
				self.ErrorList.append('No latitude/longitude/altitude defined in line 9')
		except:
			self.ErrorList.append('No Position found in line 9')
		
		try:
			header_timezone = [self.header[9][2:16],self.header[9][18:]]
			assert header_timezone[0] == 'Local timezone'
			assert header_timezone[1] != '\n' and header_timezone[1] != '\r\n'
			try:
				assert 'UTC' in header_timezone[1]
			except:
				self.ErrorList.append('Local timezone must be especified as UTC+# or UTC-# in line 10')
		except:
			self.ErrorList.append('No Local timezone found in line 10')
		
		try:
			header_timesync = [self.header[10][2:22],self.header[10][24:]]
			assert header_timesync[0] == 'Time Synchronization'
			assert header_timesync[1] != '\n' and header_timesync[1] != '\r\n'
		except:
			self.ErrorList.append('No Time Synchronization found in line 11')
		
		try:
			header_movstationary = [self.header[11][2:30],self.header[11][32:]]
			assert header_movstationary[0] == 'Moving / Stationary position'
			assert header_movstationary[1] != '\n' and header_movstationary[1] != '\r\n'
			try:
				assert 'STATIONARY' in header_movstationary[1] or 'MOVING' in header_movstationary[1]
			except:
				self.ErrorList.append('no STATIONARY or MOVING especified in line 12')
		except:
			self.ErrorList.append('No Moving / Stationary position found in line 12')
		
		try:
			header_movfixeddir = [self.header[12][2:31],self.header[12][33:]]
			assert header_movfixeddir[0] == 'Moving / Fixed look direction'
			assert header_movfixeddir[1] != '\n' and header_movfixeddir[1] != '\r\n'
			try:
				assert 'FIXED' in header_movfixeddir[1] or 'MOVING' in header_movfixeddir[1]
			except:
				self.ErrorList.append('no FIXED or MOVING especified in line 13')
		except:
			self.ErrorList.append('No Moving / Fixed look direction found in line 13')
		
		try:
			header_number_channels = [self.header[13][2:20],self.header[13][22:]]
			assert header_number_channels[0] == 'Number of channels'
			assert header_number_channels[1] != '\n' and header_number_channels[1] != '\r\n'
			try:
				number_channels = int(header_number_channels[1])
			except:
				self.ErrorList.append('Number of channels should be an integer, line 14')
		except:
			self.ErrorList.append('No Number of channels found in line 14')
		
		try:
			header_filters_per_channel = [self.header[14][2:21],self.header[14][23:]]
			assert header_filters_per_channel[0] == 'Filters per channel'
			assert header_filters_per_channel[1] != '\n' and header_filters_per_channel[1] != '\r\n'
			try:
				filters_per_channel = header_filters_per_channel[1].split(",")
				assert len(filters_per_channel)>=1
			except:
				self.ErrorList.append('No filters especified in line 15')
		except:
			self.ErrorList.append('No Filters per channel found in line 15')
		
		try:
			header_dir_per_channel = [self.header[15][2:35],self.header[15][37:]]
			assert header_dir_per_channel[0] == 'Measurement direction per channel'
			assert header_dir_per_channel[1] != '\n' and header_dir_per_channel[1] != '\r\n'
			try:
				direction_per_channel = [float(direction) for direction in header_dir_per_channel[1].split(",")]
				assert len(direction_per_channel)>=1
			except:
				self.ErrorList.append('No directions especified in line 16')
		except:
			self.ErrorList.append('No Measurement direction per channel found in line 16')
		
		try:
			header_fov = [self.header[16][2:15],self.header[16][17:]]
			assert header_fov[0] == 'Field of view'
			assert header_fov[1] != '\n' and header_fov[1] != '\r\n'
			try:
				fov = float(header_fov[1])
			except:
				self.ErrorList.append('No field of view especified in line 17')
		except:
			self.ErrorList.append('No Field of view found in line 17')
		
		try:
			header_fields = [self.header[17][2:27],self.header[17][29:]]
			assert header_fields[0] == 'Number of fields per line'
			assert header_fields[1] != '\n' and header_fields[1] != '\r\n'
			try:
				fields = int(header_fields[1])
			except:
				self.ErrorList.append('No number of fields especified in line 18, should be an integer')
		except:
			self.ErrorList.append('No Number of fields per line found in line 18')
		
		try:
			header_serialnumber = [self.header[18][2:19],self.header[18][21:]]
			assert header_serialnumber[0] == 'SQM serial number'
			assert header_serialnumber[1] != '\n' and header_serialnumber[1] != '\r\n'
		except:
			self.ErrorList.append('No SQM serial number found in line 19')
		
		try:
			header_firmware = [self.header[19][2:22],self.header[19][24:]]
			assert header_firmware[0] == 'SQM firmware version'
			assert header_firmware[1] != '\n' and header_firmware[1] != '\r\n'
		except:
			self.ErrorList.append('No SQM firmware version found in line 20')
		
		try:
			header_offset = [self.header[20][2:24],self.header[20][26:]]
			assert header_offset[0] == 'SQM cover offset value'
			assert header_offset[1] != '\n' and header_offset[1] != '\r\n'
			try:
				offset = float(header_offset[1])
			except:
				self.ErrorList.append('No offset especified in line 21, should be a float number')
		except:
			self.ErrorList.append('No SQM cover offset value found in line 21')
		
	
	def test_data(self):
		# Test if data follows the standard format.
		for line in xrange(len(self.data)):
			try:
				first_line_parts = self.data[line].split(";")
				assert len(first_line_parts) == NumberDataColumns
			except:
				self.ErrorList.append('Number of columns is not '+str(NumberDataColumns)+' as in the standard format | Line:'+str(line))
			else:
				try:
					for k in [0,1]:
						datetime = first_line_parts[k]
						date = datetime.split('T')[0].split("-")
						year = int(date[0])
						month = int(date[1])
						day = int(date[2])
						assert 1990<=year<=2100 and 1<=month<=12 and 1<=day<=31
						time = datetime.split('T')[1].split(":")
						hour = int(time[0])
						minute = int(time[1])
						second = float(time[2])
						assert 0<=hour<24 and 0<=minute<60 and 0.0<=second<60.0
				except:
					self.ErrorList.append('Wrong UTC date/time or Local date/time format, should be YYYY-MM-DDTHH:mm:ss.fff | Line:'+str(line))
			
				try:
					temperature = float(first_line_parts[2])
				except:
					self.ErrorList.append('Temperature doesnt follow the standard format, should be float | Line:'+str(line))
				
				try:
					fluxcounts = float(first_line_parts[3])
				except:
					self.ErrorList.append('Flux (counts) doesnt follow the standard format, should be float | Line:'+str(line))
				
				try:
					fluxfreq = float(first_line_parts[4])
				except:
					self.ErrorList.append('Flux (frequency) doesnt follow the standard format, should be float | Line:'+str(line))
				
				try:
					msas = float(first_line_parts[4])
				except:
					self.ErrorList.append('MSAS (mag/arcsec2) doesnt follow the standard format, should be float | Line:'+str(line))
			
	
	
if __name__ == '__main__':
	SqmFile = SqmAnalysis()
	if len(SqmFile.ErrorList)>0:
		SqmFile.print_error()
	else:
		print('Standard compliant file.')
