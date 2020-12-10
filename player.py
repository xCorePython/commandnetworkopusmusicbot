import youtube_dl, requests, discord, json, advancedtime

class Queue:
	def __init__(self):
		self.queue = []
		self._volume = 0.1
		self.skipped = False
		now_date = advancedtime.checktime
		self.options = {
			'options': '-vn -af \"firequalizer=gain_entry=\'entry(0,6);entry(30,3);entry(50,-4);entry(7000,-4);entry(9000,9);entry(21000,9)\'\"',
		}
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
	def next(self, error):
		try:
			self.stop()
		except:
			print('Stop Failed : Not Playing')
		if self.skipped == True:
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.skipped = False
			self.play()
			return
		if len(self.queue) == 1:
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.play()
			return
		self.played = self.queue[0]
		self.queue = self.queue[1:]
		self.queue.append(self.played)
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
		self.skipped = True
		if len(self.queue) == 1:
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.stop()
		if value == 1:
			self.played = self.queue[0]
			self.queue = self.queue[1:]
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.queue.append(self.played)
			self.stop()
		else:
			for n in range(value):
				self.played = self.queue[0]
				self.queue = self.queue[1:]
				self.queue.append(self.played)
			self._start = now_date('off', 9)
			self._start2 = now_date('on', 9)
			self.stop()
	def stop(self):
		self._voice.stop()
	def setvolume(self, value):
		self._volume = value
	def play(self):
		self._voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.queue[0]['path'], **self.options), volume=self._volume), after=self.next)
