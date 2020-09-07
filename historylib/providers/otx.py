import asyncio
import json

from historylib.providers.provider import make_request

otx_reults_limit = 200


class OTX(object):
	def __init__(self, include_subdomains=True):
		self.include_subdomains = include_subdomains

	async def setup(self, session=None):
		self.provider = "https://otx.alienvault.com/api/v1/indicators/hostname/"

	def format_url(self, domain, page):
		return self.provider + "%s/url_list?limit=%d&page=%d" % (
			domain, otx_reults_limit, page
		)

	async def fetch(self, session, domain):
		page = 0
		results = []
		while True:
			response = json.loads(await make_request(session, self.format_url(domain, page)))
			for url in response["url_list"]:
				results.append(url["url"])

			if not response["has_next"]:
				break

			page += 1

		return results
