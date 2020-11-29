import discord, youtube_dl, subprocess, calendar, datetime, asyncio, json

sys_token = 'NzYxOTI5NDgxNDIxOTc5NjY5.X3hwIA.ItlW0Q2Fej-OyNdbfUKO2czZQvk'
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
		self.np = 0
		self.queue = []
		self.voice = None
		self.volume = 0.1

	def add(self, value):
		self.queue.append(value)
	def remove(self, value):
		try:
			del self.queue[int(value)]
			return 'Done'
		except:
			return 'Failed'
	def start(self):
		self.start = now_date('off', 9)
		self.start2 = now_date('on', 9)
		self.play()
	def set(self, value):
		self.voice = value
	def next(self):
		if len(self.queue) == 1:
			self.stop()
			self.start = now_date('off', 9)
			self.start2 = now_date('on', 9)
			self.play()
		self.played = self.queue[0]
		self.queue = self.queue[1:]
		self.queue.append(self.played)
		self.stop()
		self.start = now_date('off', 9)
		self.start2 = now_date('on', 9)
		self.play()
	def np1(self):
		return self.queue
	def np2(self):
	    return self.start
	def np3(self):
		return self.start2
	def skip(self, value):
		if len(self.queue) == 1:
			self.stop()
			self.start = now_date('off', 9)
			self.start2 = now_date('on', 9)
			self.play()
		if value == 1:
			self.played = self.queue[0]
			self.queue = self.queue[1:]
			self.queue.append(self.played)
			self.stop()
			self.start = now_date('off', 9)
			self.start2 = now_date('on', 9)
			self.play()
		else:
			for n in range(value):
				self.played = self.queue[0]
				self.queue = self.queue[1:]
				self.queue.append(self.played)
			self.stop()
			self.start = now_date('off', 9)
			self.start2 = now_date('on', 9)
			self.play()
	def stop(self):
		self.voice.stop()
	def play(self):
		self.voice.play(discord.FFmpegPCMAudio('{0}.mp3'.format(self.queue[0]['id'])))

q = Queue()

async def save():
    messages = await client.get_channel(774525604116037662).history(limit=1).flatten()
    queues = []
    for n in range(len(q.np1())):
    	queues.append('https://youtu.be/{}'.format(q.np1()[n]['id']))
    for message in messages:
    	await message.edit(content='\n'.join(queues))

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
		sendms.add_field(name='Codec', value='mp3 / {}kbps(CBR) / {}kHz / {}'.format(str(int(info['format']['bit_rate'])/1000), str(int(int(info['streams'][0]['sample_rate'])/1000)), info['streams'][0]['channel_layout']), inline=False)
		sendms.set_thumbnail(url=str(info['thumbnails'][len(info['thumbnails']) - 1]['url']))
		sendms.set_footer(text='Started at {}'.format(start2.split('.')[0]))
		await message.channel.send(embed=sendms)
	elif command == 'play':
		await message.channel.send(':arrows_counterclockwise: **Your request processing...**')
		info = search(' '.join(arg))
		if info == 'Failed':
			await message.channel.send(':x: **No result**')
		else:
			sendms = discord.Embed(title='Downloading...')
			link = 'https://youtu.be/' + info['id']
			sendms.add_field(name='Title', value='[{}]({})'.format(info['title'], link), inline=False)
			sendms.add_field(name='Uploader',value='[{}]({})'.format(info['uploader'],info['uploader_url']),inline=False)
			sendms.add_field(name='Duration', value=reverse(info['duration']))
			sendms.set_thumbnail(url=str(info['thumbnails'][len(info['thumbnails']) - 1]['url']))
			sendms.set_footer(text='Extracted from {}'.format(info['extractor']))
			await message.channel.send(embed=sendms)
			await save()
			conver('https://youtu.be/{}'.format(info['id']))
	elif command == 'skip':
		arg = message.content.split(' ')
		if len(arg) == 1:
			q.skip(1)
			await message.channel.send(':fast_forward: **Skipped**')
		else:
			if int(arg[1]) > 1000000:
				await message.channel.send('**Sorry. I can\'t skip over 1000000 songs. Please use 1-999999**')
			if arg[1] == '1':
				q.skip(1)
				await message.channel.send(':fast_forward: **Skipped**')
			else:
				q.skip(int(arg[1]))
				await message.channel.send(':fast_forward: **{} songs skipped**'.format(arg[1]))
	elif command == 'remove':
		arg = message.content.split(' ')
		q.remove(int(arg[1]))
		await message.channel.send(':white_check_mark: **Removed**')
		await save(l)
	elif command == 'join':
	    await client.get_channel(vcch).connect()
	    await message.channel.send(':white_check_mark: **Joined**')
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
		await message.channel.send('white_check_mark: **Disconnected**')

async def create_queue(channelid):
	messages = await client.get_channel(channelid).history(limit=1).flatten()
	for message in messages:
		return message.content

def search(url):
	for n in range(1, 10):
		try:
			if url.startswith('https://'):
				info_dict = youtube_dl.YoutubeDL().extract_info(info, download=False, process=False)
				return info_dict
			else:
				info_dict = youtube_dl.YoutubeDL().extract_info("ytsearch:{}".format(info), download=False, process=False)
				return info_dict['entries'][0]
		except:
			print('Retrying... ({})'.format(n))
	return 'Failed'

def conver(info):
	ydl = youtube_dl.YoutubeDL(ydl_opts)
	for n in range(1, 10):
		try:
			info_dict = youtube_dl.YoutubeDL().extract_info(info, download=False, process=False)
			title = info_dict['id'] + '.mp3'
			url = 'https://www.320youtube.com/watch?v={}'.format(info_dict['id'])
			result = requests.get(url)
			soup = bs4.BeautifulSoup(result.text, 'html.parser')
			dllink = str(str(soup).split('href=')[8])[1:].split('" rel')[0]
			urllib.request.urlretrieve(dllink, title)
		    #convert = subprocess.run("ffmpeg -i {0}.webm -af bass=g=1:f=200:w=10 -b:a 320000 -c:a libmp3lame -n {0}.mp3".format(info_dict['id']), shell=True)
			data = json.loads(subprocess.run("ffprobe -print_format json -show_streams  -show_format {}.mp3".format(info_dict['id']), stdout=subprocess.PIPE, shell=True).stdout)
			info_dict['format'] = data['format']
			info_dict['streams'] = data['streams']
			q.add(info_dict)
			return info_dict
			break
		except:
			print('Retrying... ({})'.format(n))
	return 'Failed'

first = ['Not Converted']

@client.event
async def on_ready():
	print('Bot Started')
	if len(first) == 1:
		print('Loading queue...')
		links = str(await create_queue(774525604116037662)).split('\n')
		for n in range(len(links)):
		    conver(links[n])
		print('Loaded queue')
		first.append('Converted')
	voice = client.get_channel(vcch).guild.voice_client
	if not voice:
		await client.get_channel(vcch).connect(reconnect=20)
	voice = client.get_channel(vcch).guild.voice_client
	q.set(voice)
	q.start()
	while sys_loop == 1:
		if not voice.is_playing():
			q.next()
		await asyncio.sleep(0.1)

@client.event
async def on_message(message):
	if message.content.startswith(command_prefix):
		prefix = message.content[len(command_prefix):]
		start = prefix.split(' ')[0]
		print(start)
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
