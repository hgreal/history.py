import time
import json
import asyncio
import urllib.parse


def create_chunks(targets):
	chunk_sets = {}
	if type(targets) == str:
		if '//' not in targets:
			targets = "https://" + targets
		return [[targets]]

	for target in targets:
		netloc = urllib.parse.urlparse(target).netloc
		parts = netloc.split('.')
		if 2 < len(parts) and target.endswith("co.uk"):
			netloc = '.'.join(parts[-3:])
		else:
			netloc = '.'.join(parts[-2:])

		if netloc not in chunk_sets:
			chunk_sets[netloc] = []

		chunk_sets[netloc].append(target)

	largest_chunk_set = max([len(chunk_sets[chunk_set]) for chunk_set in chunk_sets])
	chunks = [[] for _ in range(largest_chunk_set)]
	for chunk_set in chunk_sets:
		for idx, target in enumerate(chunk_sets[chunk_set][::]):
			chunks[idx].append(chunk_sets[chunk_set].pop())

	while [] in chunks:
		chunks.remove([])

	return chunks


async def get_response(session, url, retries=2):
	for retry in range(retries, 0, -1):
		await asyncio.sleep(1.1337)
		async with session.get(url) as response:
			try:
				html = await response.text()
				return response.url, html, response.headers
			except Exception as e:
				pass

	return


async def get_json(session, url, retries=2):
	for retry in range(retries, 0, -1):
		await asyncio.sleep(0.5)
		async with session.get(url) as response:
			try:
				return await response.json()
			except Exception as e:
				pass

	return None


async def make_request(session, url, retries=1):
	for retry in range(retries, 0, -1):
		await asyncio.sleep(0.1337)
		try:
			async with session.get(url) as response:
				try:
					return await response.text()
				except:
					pass
		except:
			pass

	return ""
