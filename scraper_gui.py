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

import codecs

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def runner(save_location, start_url, ps):
    if '\n' in start_url:
        url_list = start_url.split('\n')
    else:
        url_list = [start_url]

    for url in url_list:
        base_url = ''.join(url.rpartition('/')[:-1])
        scraper = Scraper(save_location, base_url)

        start = time.time()
        scraper.start(url, ps=ps)
        end = time.time() - start

        print(round(end), "seconds")
        print(scraper.total, "images")


@Gooey(
    program_name='long-live',
    program_description='Download gallery images',
    default_size=(800, 600),
    monospace_display=True,
    image_dir=os.path.join(current, 'images'),
    navigation='TABBED',
    requires_shell=False    # https://github.com/chriskiehl/Gooey/issues/499
)
def main():
    parser = GooeyParser()
    subparser = parser.add_subparsers()

    single = subparser.add_parser('Single')

    single_scrape_group = single.add_argument_group('Scrape Options', gooey_options={'columns': 1})
    single_scrape_group.add_argument('URL')
    single_scrape_group.add_argument('--ps', action='store_true', help=' Contains photoshoots')

    single_save_group = single.add_argument_group('Save Options', gooey_options={'columns': 1})
    single_save_group.add_argument('Destination Folder', widget='DirChooser')

    bulk = subparser.add_parser('Bulk')

    bulk_scrape_group = bulk.add_argument_group('Scrape Options', gooey_options={'columns': 1})
    bulk_scrape_group.add_argument('URL', widget='Textarea')
    bulk_scrape_group.add_argument('--ps', action='store_true', help=' All of the URLs above contain photoshoots')

    bulk_save_group = bulk.add_argument_group('Save Options', gooey_options={'columns': 1})
    bulk_save_group.add_argument('Destination Folder', widget='DirChooser')

    args = parser.parse_args()

    dest = vars(args)['Destination Folder']
    if dest.endswith('"'):
        dest = dest[:-1] + "\\"

    runner(dest, args.URL, args.ps)


if __name__ == '__main__':
    main()
