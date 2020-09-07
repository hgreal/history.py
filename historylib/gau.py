
from historylib.core import *
from historylib.providers.common import Common
from historylib.providers.otx import OTX
from historylib.providers.wayback import Wayback
from historylib.providers.provider import *


class Gau(Wrapper):
	def __init__(self, session, input, output=False, subdomains=True, retries=2, provider="all"):
		super().__init__(session, input, output)
		self.subs = False
		self.providers = []
		self.retries = retries
		self.provider = provider
		self.subdomains = subdomains

		if self.provider.upper() == "ALL":
			self.providers = [Common(self.subdomains), Wayback(self.subdomains), OTX(self.subdomains)]

		elif self.provider.upper() == "COMMON":
			self.providers = [Common(self.subdomains)]

		elif self.provider.upper() == "WAYBACK":
			self.providers = [Wayback(self.subdomains)]

		elif self.provider.upper() == "OTX":
			self.providers = [OTX(self.subdomains)]

	def dump(self, given_results=False):
		results = list(set([url for provider in [task for task in self.tasks] for url in provider]))

		return super().dump(results)

	async def process(self):
		targets = self.get_targets()
		chunks = create_chunks(targets)
		for chunk in chunks:
			target = chunk[0].split('//')
			if 1 < len(target):
				target = target[1]
			else:
				target = target[0]
			tasks = []
			for provider in self.providers:
				await provider.setup(self.session)
				task = asyncio.ensure_future(provider.fetch(self.session, target))
				tasks.append(task)
			await asyncio.gather(*tasks, return_exceptions=True)
			for task in tasks:
				self.tasks.append(task.result())
