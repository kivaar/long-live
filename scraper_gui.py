# import argparse
import builtins
import functools
import os
import sys
import time

from gooey import Gooey, GooeyParser
from scraper import Scraper

builtins.print = functools.partial(print, flush=True)
current = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


def runner(save_location, start_url, ps):
	base_url = ''.join(start_url.rpartition('/')[:-1])
	scraper = Scraper(save_location, base_url)

	start = time.time()
	scraper.start(start_url, ps=ps)
	end = time.time() - start

	print(round(end), "seconds")
	print(scraper.total, "images")


@Gooey(
	program_name='long-live',
	program_description='Download gallery images',
	monospace_display=True,
	image_dir=os.path.join(current, 'images')
)
def main():
	parser = GooeyParser()

	scrape_group = parser.add_argument_group('Scrape Options', gooey_options={'columns': 1})
	scrape_group.add_argument('URL')
	scrape_group.add_argument('--ps',
		action='store_true',
		help='Contains photoshoots')

	save_group = parser.add_argument_group('Save Options', gooey_options={'columns': 1})
	save_group.add_argument('Destination Folder', widget='DirChooser')
	
	args = parser.parse_args()

	dest = vars(args)['Destination Folder']
	if dest.endswith('"'):
		dest = dest[:-1] + "\\"

	runner(dest, args.URL, args.ps)


if __name__ == '__main__':
	main()
