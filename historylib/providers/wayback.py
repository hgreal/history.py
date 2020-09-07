import asyncio
import json

from historylib.providers.provider import make_request


class Wayback(object):
	def __init__(self, include_subdomains=True):
		self.include_subdomains = include_subdomains

	async def setup(self, session=None):
		self.provider = "http://web.archive.org/cdx/search/cdx"

	def format_url(self, domain, page):
		if self.include_subdomains:
			domain = "*." + domain

		return "%s?url=%s/*&output=json&collapse=urlkey&fl=original&page=%d" % (
			self.provider, domain, page
		)

	async def get_pages(self, session, domain):
		return int(await make_request(
			session, self.format_url(domain, 0) + "&showNumPages=true"
		))

	async def fetch(self, session, domain):
		results = []
		pages = await self.get_pages(session, domain)
		for page in range(pages):
			response = await make_request(session, self.format_url(domain, page))
			for url in json.loads(response)[1:]:
				results.append(url[0])

		return results






























