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


async def make_request(session, url, retries=1):
	for retry in range(retries, 0, -1):
		await asyncio.sleep(0.41337)
		try:
			async with session.get(url) as response:
				try:
					return await response.text()
				except:
					pass
		except:
			pass

	return ""
