import os
import asyncio
import json
import socket
import aiohttp

try:
	import uvloop
	uvloop.install()
	if uvloop:
		asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
	connector = None
except:
	connector = aiohttp.TCPConnector(
		family=socket.AF_INET,
		use_dns_cache=False,
		ssl=False
	)


class Wrapper(object):
	def __init__(self, session, input, output=False):
		self.tasks = []
		self.input = input
		self.output = output
		self.session = session
		self.results = input

	def dump(self, given_results=False):
		if not given_results and self.tasks == type(list):
			results = list(set([task for task in self.tasks if task]))

		elif given_results:
			results = given_results

		else:
			results = self.tasks

		try:
			results.sort()
		except:
			pass

		while "" in results:
			results.remove("")

		if self.output:
			json.dump(results, open(self.output, 'w'), indent=2, sort_keys=True)

		return results

	async def run(self):
		await self.process()
		return self.dump()

	def get_targets(self):
		targets = self.results
		if not type(targets) == list:
			if os.path.exists(self.input):
				targets = open(self.input, "r").read().strip().split('\n')
			else:
				targets = self.input.split(',')

		return targets

	async def process(self):
		pass
