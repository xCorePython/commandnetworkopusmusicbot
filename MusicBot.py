import discord, youtube_dl, subprocess, calendar, datetime, asyncio, json, os

sys_token = 'NzYxOTI5NDgxNDIxOTc5NjY5.X3hwIA.ItlW0Q2Fej-OyNdbfUKO2czZQvk'
sys_token2 = 'NzYwNDkwNjYwNDQzODQ4NzM0.X3M0Hg.lTDx_AvmNNr1spqwUo1wqetaVlM'
sys_token3 = 'NzIzMjE4MDQ1NjY4OTUwMTE2.XuubSg.1zFOpD-ywOcWj0J2twss7IlhiPE'
sys_loop = 1
command_prefix = 'c.'
client = discord.Client()
vcch = 734217960222228490
#vcch = 584262828807028746
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': "%(id)s" + '.%(ext)s',
    'ignoreerrors': True,
    'noplaylist': True,
    'quiet': True,
#	'postprocessors': [{
#    	'key': 'FFmpegExtractAudio',
#        'preferredcodec': 'mp3',
#        'preferredquality': '320'},
#    {'key': 'FFmpegMetadata'},],
}

def now_month(mode):
	if mode == 'total':
		now = datetime.datetime.utcnow()
		if now.month == 1:
			a01 = 0
			for n in range(1):
				nowcalendar = str(
				    calendar.month(
				        int('{}'.format(now.year)), int('{}'.format(n))))
				a01 = a01 + int(nowcalendar[int(len(nowcalendar) -
				                                3):int(len(nowcalendar) - 1)])
			a01 = a01 + now.day
			return a01
		if now.month > 2:
			a01 = 0
			for n in range(1, now.month):
				nowcalendar = str(
				    calendar.month(
				        int('{}'.format(now.year)), int('{}'.format(n))))
				a01 = a01 + int(nowcalendar[int(len(nowcalendar) -
				                                3):int(len(nowcalendar) - 1)])
			a01 = a01 + now.day
			return a01
	if mode == 'month':
		now = datetime.datetime.utcnow()
		nowcalendar = str(
		    calendar.month(
		        int('{}'.format(now.year)), int('{}'.format(now.month))))
		a01 = int(
		    nowcalendar[int(len(nowcalendar) - 3):int(len(nowcalendar) - 1)])
		return a01


def now_date(mode, location):
	if mode == 'off':
		now = datetime.datetime.utcnow()
		return float(now.strftime("0.%f")) + int(now.second) + int(
		    int(int(now.month * 365) + int(now_month('month'))) * 86400) + int(
		        int(now.day) * 86400) + int(int(now.hour) * 3600) + int(
		            int(now.minute) * 60)
	if mode == 'on':
		now = datetime.datetime.utcnow()
		locationtime = location
		year = now.year
		hour = now.hour + locationtime
		day = now.day
		month = now.month
		if hour > 24:
			hour2 = hour / 24
			hour = hour - int(hour2 * 24)
			day = day + 1
			if day > now_month('month'):
				month = month + 1
				if month > 12:
					month = month - 12
					year = year + 1
		a01 = datetime.datetime(year, month, day, hour, now.minute, now.second, int(now.strftime("%f")))
		return a01.strftime("%Y/%m/%d %H:%M:%S.%f")

def reverse(data):
	time = int(float(data))
	if time < 10:
		second = int(time)
		uptime = '0:0' + str(second)
		return uptime
	if time >= 60:
		if time < 3600:
			minute = int(time / 60)
			second = int(time - minute * 60)
			if second < 10:
				uptime = str(minute) + ':0' + str(second)
				return uptime
			else:
				uptime = str(minute) + ':' + str(second)
				return uptime
		else:
			hour = int(time / 3600)
			minute = int(int(time - hour * 3600) / 60)
			second = int(time - hour * 3600 - minute * 60)
			if minute < 10:
				if second < 10:
					uptime = str(hour) + ':0' + str(minute) + ':0' + str(
					    second)
					return uptime
				else:
					uptime = str(hour) + ':0' + str(minute) + ':' + str(second)
					return uptime
			else:
				if second < 10:
					uptime = str(hour) + ':' + str(minute) + ':0' + str(second)
					return uptime
				else:
					uptime = str(hour) + ':' + str(minute) + ':' + str(second)
					return uptime
	else:
		uptime = '0:' + str(time)
		return uptime

class Queue:
	def __init__(self):
		self.queue = []
		self._volume = 0.01

	def add(self, value):
		self.queue.append(value)
	def remove(self, value):
		try:
			del self.queue[int(value)]
			return 'Done'
		except:
			return 'Failed'
	def start(self):
		self._start = now_date('off', 9)
		self._start2 = now_date('on', 9)
		self.play()
	def set(self, value):
		self._voice = value
	def next(self):
		if len(self.queue) == 1:
			self.stop()
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.play()
		self.played = self.queue[0]
		self.queue = self.queue[1:]
		self.queue.append(self.played)
		self.stop()
		self._start = now_date('off', 9)
		self._start2 = now_date('on', 9)
		self.play()
	def np1(self):
		return self.queue
	def np2(self):
	    return self._start
	def np3(self):
		return self._start2
	def nvol(self):
		return self._volume
	def skip(self, value):
		if len(self.queue) == 1:
			self.stop()
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.play()
		if value == 1:
			self.played = self.queue[0]
			self.queue = self.queue[1:]
			self.queue.append(self.played)
			self.stop()
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.play()
		else:
			for n in range(value):
				self.played = self.queue[0]
				self.queue = self.queue[1:]
				self.queue.append(self.played)
			self.stop()
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.play()
	def stop(self):
		self._voice.stop()
	def setvolume(self, value):
		self._volume = value
	def play(self):
		self._voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('{0}.mp3'.format(self.queue[0]['id'])), volume=self._volume))
		

q = Queue()

async def save():
    messages = await client.get_channel(774525604116037662).history(limit=1).flatten()
    queues = []
    for n in range(len(q.np1())):
    	queues.append('https://youtu.be/{}'.format(q.np1()[n]['id']))
    for message in messages:
    	try:
    		await message.edit(content='\n'.join(queues))
    	except:
    		await message.channel.send(content='\n'.join(queues))

async def commands(command, message):
	arg = message.content.split(' ')[1:]
	if command == 'nowplaying':
		info = q.np1()[0]
		start = q.np2()
		start2 = q.np3()
		link = 'https://youtu.be/' + info['id']
		sendms = discord.Embed(title='Now Playing')
		sendms.add_field(name='Title', value='[{}]({})'.format(info['title'], link), inline=False)
		sendms.add_field(name='Uploader',value='[{}]({})'.format(info['uploader'],info['uploader_url']),inline=False)
		nowti = now_date('off', 9)
		nowpl = int(float(nowti - start))
		duration = info['duration']
		if nowpl > duration:
			nowpl = duration
		sendms.add_field(name='Time', value='{} / {}'.format(reverse(nowpl),reverse(info['duration'])),inline=False)
		sendms.add_field(name='Codec', value=info['streams'][0]['codec_long_name'], inline=False)
		sendms.add_field(name='Bitrate', value='{}kbps / {}'.format(str(int(info['format']['bit_rate'])/1000),  info['streams'][0]['channel_layout']), inline=False)
		sendms.add_field(name='Volume', value='{}%'.format(str(int(float(client.get_channel(vcch).guild.voice_client.source.volume)*100))), inline=False)
		sendms.add_field(name='Equalizer', value='Bass: x5.0 Truble: x9.0')
		sendms.set_thumbnail(url=str(info['thumbnails'][len(info['thumbnails']) - 1]['url']))
		sendms.set_footer(text='Started at {} | High Quality Technology from FFmpeg | FireEqualizer from FFmpeg'.format(start2))
		await message.channel.send(embed=sendms)
	elif command == 'play':
		await message.channel.send(':arrows_counterclockwise: **Searching...**')
		info = search(' '.join(arg))
		if info == 'Failed':
			await message.channel.send(':x: **No result**')
		else:
			sendms = discord.Embed(title='Converting...')
			link = 'https://youtu.be/' + info['id']
			sendms.add_field(name='Title', value='[{}]({})'.format(info['title'], link), inline=False)
			sendms.add_field(name='Uploader',value='[{}]({})'.format(info['uploader'],info['uploader_url']),inline=False)
			sendms.add_field(name='Duration', value=reverse(info['duration']))
			sendms.set_thumbnail(url=str(info['thumbnails'][len(info['thumbnails']) - 1]['url']))
			sendms.set_footer(text='Extracted from {}'.format(info['extractor']))
			await message.channel.send(embed=sendms)
			conver(info)
			await save()
	elif command == 'skip':
		arg = message.content.split(' ')
		if len(arg) == 1:
			q.skip(1)
			await message.channel.send(':fast_forward: **Skipped**')
		else:
			if arg[1] == '1':
				q.skip(1)
				await message.channel.send(':fast_forward: **Skipped**')
			if int(arg[1]) > 1000000:
				await message.channel.send('**Sorry. I can\'t skip over 1000000 songs. Please use 1-999999**')
			else:
				q.skip(int(arg[1]))
				await message.channel.send(':fast_forward: **{} songs skipped**'.format(arg[1]))
	
	elif command == 'remove':
		arg = message.content.split(' ')
		q.remove(int(arg[1]))
		await message.channel.send(':white_check_mark: **Removed**')
		await save()
	elif command == 'join':
	    await client.get_channel(vcch).connect()
	    await message.channel.send(':white_check_mark: **Joined**')
	elif command == 'volume':
		if 0 <= int(arg[0]) <= 100:
			client.get_channel(vcch).guild.voice_client.source.volume = float(int(arg[0])/100)
			q.setvolume(float(arg[0])/100)
			await message.channel.send(':white_check_mark: **Successfully changed volume {}%**'.format(arg[0]))
		else:
			await message.channel.send(':x: **Please input between 0-100**')
	elif command == 'queue':
		queue = q.np1()
		queues = []
		for n in range(1, len(queue)):
			queues.append('{}: {}'.format(n, queue[n]['title']))
		sendms = discord.Embed(title='Queue', description='\n'.join(queues))
		sendms.add_field(name='Now Playing', value=queue[0]['title'])
		await message.channel.send(embed=sendms)
	elif command == 'leave':
		await client.get_channel(vcch).guild.voice_client.disconnect()
		await message.channel.send(':white_check_mark: **Disconnected**')
	elif command == 'start':
		await client.get_channel(vcch).connect()
		q.set(client.get_channel(vcch).guild.voice_client)
		q.start()
		await np()

async def create_queue(channelid):
	messages = await client.get_channel(channelid).history(limit=1).flatten()
	for message in messages:
		return message.content

def search(value):
	for n in range(1, 3):
		try:
			if value.startswith('https://'):
				info_dict = youtube_dl.YoutubeDL(ydl_opts).extract_info(value, download=True, process=True)
				if info_dict:
					return info_dict
				else:
					error = raiseerror
			else:
				info_dict = youtube_dl.YoutubeDL(ydl_opts).extract_info("ytsearch:{}".format(value), download=True, process=True)
				if not info_dict:
					error = raiseerror
				else:
					return info_dict['entries'][0]
		except:
			print('Retrying... ({})'.format(n))
	return 'Failed'

async def np():
	data = q.np1()[0]
	duration = float(data['format']['duration'])
	await client.get_channel(782863961153339403).edit(topic='Title: {}\nUploader : {}\nDuration : {}\nCodec : {}\nBitrate : {}kbps / {}'.format(data['title'], data['uploader'], str(reverse(duration)), data['streams'][0]['codec_long_name'], str(int(data['format']['bit_rate'])/1000), data['streams'][0]['channel_layout']))

def conv(info_dict):
	title = info_dict['id'] + '.mp3'
	url = 'https://www.320youtube.com/watch?v={}'.format(info_dict['id'])
	result = requests.get(url)
	soup = bs4.BeautifulSoup(result.text, 'html.parser')
	dllink = str(str(soup).split('href=')[8])[1:].split('" rel')[0]
	urllib.request.urlretrieve(dllink, title)

def conver(info_dict):
	if os.path.isfile('{}.m4a'.format(info_dict['id'])):
		convert = subprocess.run("ffmpeg -i {0}.m4a -af \"firequalizer=gain_entry=\'entry(0,4);entry(100,0.5);entry(250,0);entry(7000,0);entry(9000,1.5);entry(16000,9);entry(40000,9)\'\" -vn -b:a 320000 -c:a libmp3lame -n {0}.mp3".format(info_dict['id']), shell=True)
		data = json.loads(subprocess.run("ffprobe -print_format json -show_streams  -show_format {}.m4a".format(info_dict['id']), stdout=subprocess.PIPE, shell=True).stdout)
		info_dict['format'] = data['format']
		info_dict['streams'] = data['streams']
		q.add(info_dict)
		return info_dict
	try:
			#ffmpeg -y -i original.mp3 -af "firequalizer=gain_entry='entry(0,-23);entry(250,-11.5);entry(1000,0);entry(4000,8);entry(16000,16)'" test1.mp3
		convert = subprocess.run("ffmpeg -i {0}.webm -af \"firequalizer=gain_entry=\'entry(0,4);entry(100,0.5);entry(250,0);entry(7000,0);entry(9000,1.5);entry(16000,9);entry(40000,9)\'\" -vn -b:a 320000 -c:a libmp3lame -n {0}.mp3".format(info_dict['id']), shell=True)
		data = json.loads(subprocess.run("ffprobe -print_format json -show_streams  -show_format {}.webm".format(info_dict['id']), stdout=subprocess.PIPE, shell=True).stdout)
		info_dict['format'] = data['format']
		info_dict['streams'] = data['streams']
		q.add(info_dict)
		return info_dict
	except:
		return 'Failed'

first = ['Not Converted']

@client.event
async def on_ready():
	print('Bot Started')
	if len(first) == 1:
		print('Loading queue...')
		links = str(await create_queue(774525604116037662)).split('\n')
		for n in range(len(links)):
		    info = search(links[n])
		    conver(info)
		print('Loaded queue')
		first.append('Converted')
	await client.get_channel(773053692629876757).send('[endless-play] started')
	while sys_loop == 1:
		if not client.get_channel(vcch).guild.voice_client.is_playing():
			try:
				q.next()
				await np()
			except:
				await asyncio.sleep(1)
		q.set(client.get_channel(vcch).guild.voice_client)
		await asyncio.sleep(0.1)

@client.event
async def on_message(message):
	if message.channel.id == 773053692629876757:
		if message.content == '[endless-play] started':
			await commands('start', message)
			await np()
	if message.content.startswith(command_prefix):
		prefix = message.content[len(command_prefix):]
		start = prefix.split(' ')[0]
		print(start)
		if start == 'start':
			await commands('start', message)
		if start == 'volume':
			await commands('volume', message)
			return
		if start == 'vol':
			await commands('volume', message)
			return
		if start == 'v':
			await commands('volume', message)
			return
		if start == 'q':
		    await commands('queue', message)
		    return
		if start == 'n':
		    await commands('nowplaying', message)
		    return
		if start == 'd':
		    await commands('remove', message)
		    return
		if start == 'del':
		    await commands('remove', message)
		    return
		if start == 'dc':
		    await commands('leave', message)
		    return
		if start == 'l':
		    await commands('leave', message)
		    return
		if start == 'p':
			await commands('play', message)
			return
		if start == 'join':
		    await commands('join', message)
		    return
		if start == 'r':
		    await commands('remove', message)
		    return
		if start == 's':
			await commands('skip', message)
			return
		if start == 'np':
			await commands('nowplaying', message)
			return
		if start == 'play':
			await commands('play', message)
			return
		if start == 's':
			await commands('skip', message)
			return
		if start == 'skip':
			await commands('skip', message)
			return
		if start == 'now':
			await commands('nowplaying', message)
			return
		if start == 'nowplaying':
			await commands('nowplaying', message)
			return
		if start == 'remove':
			await commands('remove', message)
			return
		if start == 'delete':
			await commands('remove', message)
			return
		if start == 'j':
			await commands('join', message)
			return
		if start == 'leave':
			await commands('leave', message)
			return
		if start == 'queue':
			await commands('queue', message)
			return

client.run(sys_token)
