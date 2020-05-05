import os
import subprocess
import glob 
import os

def scan_for_files_recursivly(path=None):	
	if not path:
		path = os.getcwd()		
		files = []
		for root, d, f in os.walk(path):		
			for basename in f:
				filename = os.path.join(root, basename)
				files.append(filename)
		return {'files': files}

def scan_for_files(path=None):
	if not path:
		path = os.getcwd()
		folders = []
		files = []
		for item in os.listdir(path):
			if os.path.isdir(item):
				folders.append(item)
			else:
				files.append(item)
		return {'folders': folders, 'files': files}

def get_duration(path):
	from pymediainfo import MediaInfo
	media_info = MediaInfo.parse(path)
	#duration in milliseconds
	duration_in_ms = media_info.tracks[0].duration
	print(duration_in_ms)
	return duration_in_ms

def convert_milliseconds(ms=1000, to='minutes'):
	''' Convert milliseconds to seconds/minutes/hours '''
	conversion_dict = {'minutes': 1000 * 60,
		'seconds': 1000,
		'hours': 1000 * 3600
	}	
	try:
		converted = ms / conversion_dict.get(to)
		print(f'{ms} milliseconds is equal to {round(converted, 5)} {to}')
		return converted
	except TypeError:
		return -1

def scan_videos_durations(path=None, display=False, time_unit='minutes', export=False, export_name='video_durations.html'):
	durations = {}
	for filename in scan_for_files_recursivly(path).get('files'):
		if not filename:
			return
		durations[filename] = get_duration(filename)
	if display:
		[print(f'{filename} => {convert_milliseconds(duration, time_unit)}') for filename,duration in durations.items()]
	if export:
		html = '''<!DOCTYPE html>
<html>
<head>
	<link href="https://fonts.googleapis.com/css2?family=Jost&display=swap" rel="stylesheet">
	<style>	
		html {
			font-family: 'Jost', sans-serif;
		}
		.file-table {
			border: 2px solid rgb(99, 55, 127, .3);
			width: 100%;
			border-collapse: collapse;
		}
		th,td {
			padding: 0.5rem 1rem;
			font-size: 1.4rem;
		}
		th {
			height: 4rem;
			font-weight: bold;
			background: rgb(195, 199, 235);
		}
		.table__total {
			font-weight: 700; font-size: 2rem;
			color: rgb(141, 54, 107);
		}
		td:hover {
			background: rgb(195, 34, 163, .2);
		}
		td {
			height: 4rem;
			border: 2px solid rgb(99, 55, 127, .3);
		}
	</style>
</head>
	<body>
		<table class="file-table">
			<tr>
				<th>File</th>
				<th>Duration</th>
			</tr>
'''
		for filename,duration in durations.items():
			try:
				if duration < 0:
					continue
			except TypeError:
				continue
			formatted_duration = round(convert_milliseconds(duration, time_unit), 4)
			html += f'''
				<tr>
					<td>{filename}</td>
					<td>{formatted_duration} {time_unit}</td>
				</tr>'''
		sum_durations = round(
			convert_milliseconds(
				sum([x for x in durations.values() if x]),
				time_unit
			), 4
		)
		if time_unit == 'minutes':
			total = round(sum_durations / 60)
		else:
			total = round(sum_durations * 60)
		html += f'''
			<tr>
				<td class="table__total">Total</td>
				<td class="table__total">{sum_durations} {time_unit} | {total}</td>
			</tr>'''
		html += '</table></body></html>'
		with open(export_name, 'w') as f:
			f.write(html)
	return durations

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

if __name__ == '__main__':	
	dur = scan_videos_durations(display=True, time_unit='minutes', export=True)
	