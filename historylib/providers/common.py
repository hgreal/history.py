import asyncio
import json

from historylib.providers.provider import make_request


class Common(object):
	def __init__(self, include_subdomains=True):
		self.include_subdomains = include_subdomains

	async def setup(self, session):
		if type(self.provider) is not str:
			self.provider = await self.provider(session)

	async def provider(self, session, api="cdx-api"):
		response = await make_request(
			session, "http://index.commoncrawl.org/collinfo.json", retries=2
		)

		if response:
			try:
				result = json.loads(response)
				return result[0][api]
			except:
				pass
		else:
			return False

	def format_url(self, domain, page):
		if self.include_subdomains:
			domain = "*." + domain

		return "%s?url=%s/*&output=json&fl=url&page=%d" % (
			self.provider, domain, page
		)

	async def get_pages(self, session, domain):
		try:
			return json.loads(await make_request(
				session, self.format_url(domain, 0) + "&showNumPages=true"
			))["pages"]
		except:
			return 1

	async def fetch(self, session, domain):
		results = []
		if self.provider is None:
			return results
		pages = await self.get_pages(session, domain)
		for page in range(pages):
			response = await make_request(session, self.format_url(domain, page))
			for line in response.split('\n')[:-1]:
				try:
					results.append(json.loads(line)["url"])
				except:
					pass

		return results






























