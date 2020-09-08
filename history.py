import requests
import shutil

from historylib.linkfinder import *
from historylib.core import *
from historylib.gau import Gau
import argparse

parser = argparse.ArgumentParser(description='Dump the History of a Bug Bounty Target')
parser.add_argument('--target',
                    type=str,
                    help='bug bounty target: domain.tld or filename.txt containing your targets',
                    required=True)
arguments = parser.parse_args()
target = arguments.target


async def main():
    async with aiohttp.ClientSession(connector=connector) as session:
        if target.endswith(".txt"):
            targets = open(target, 'r').read().split('\n')
        else:
            targets = [target]
        results = await Gau(session, targets).run()
        results = list(set([
            element.split('?')[0] if '?' in element else element for element in results
        ]))
        results.sort()
        data = {"folder": []}
        for element in results:
            if '//' in element:
                path = '/'.join(element.split('//')[-1].split('/')[1:])
                if '.' in path and not path.endswith('/'):
                    ext = path.split('.')[-1]
                    if ext in ["jpeg", "png", "svg", "jpg", "woff", "woff2", "otf", "ttf", "ico", "gif", "eot", "css"]:
                        continue
                    if ext not in data:
                        data[ext] = []
                    data[ext].append('http://' + element.split('//')[-1])
                else:
                    data["folder"].append('http://' + element.split('//')[-1])

        if not os.path.exists("history-dumps/"):
            os.makedirs("history-dumps/")

        if not os.path.exists("tmp/"):
            os.makedirs("tmp/")
        else:
            shutil.rmtree("tmp")
            os.makedirs("tmp/")

        if not os.path.exists("linkfinder-dumps/"):
            os.makedirs("linkfinder-dumps/")

        print(json.dumps(data, indent=4, sort_keys=True))
        json.dump(data, open("history-dumps/" + target + "-history.json", 'w'), indent=4, sort_keys=True)

        for javascript_file in data["js"]:
            try:
                fname = javascript_file.split('://')[-1].replace('/', '_')
                with open("tmp/" + fname, 'w') as f:
                    f.write(requests.get(javascript_file, timeout=1.337).text)
            except:
                pass


        linkfinder(targets[0])


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
