import click
import os
import re
import requests
import time

from lxml import html
from pprint import pprint
from urllib.parse import unquote, urljoin


class Scraper:

    def __init__(self, save_location, base_url):
        self.save_location = save_location

        self.s = requests.session()
        self.base_url = base_url

        self.tree = None
        self.path = None

        self.exclude = ["mini_", "normal_", "thumb_"]
        self.seen = {}

        self.count = 1
        self.total = 0

    def build_url(self, link):
        return urljoin(self.base_url, link)

    def set_html_tree(self, url):
        r = self.s.get(url)
        self.tree = html.fromstring(r.text)

    def set_page_path(self, title=None, subtitle=None):
        temp = self.tree.xpath('//td[@class="tableh1"]//a/text()')

        if title is not None:
            temp[-1] = title

        if subtitle is not None:
            temp[-1] += " - " + subtitle

        self.path = [x
                     .replace("/", " & ")
                     .replace(":", " -")
                     .replace("?", "")
                     .replace("\"", "")
                     .replace("|", "-")
                     .replace("’", "'")
                     .replace("  ", " ")
                     .replace("\t", "")
                     .strip(".")
                     .strip() for x in temp]

    def get_album_size(self):
        info = self.tree.xpath('//td[@class="tableh1" and @valign="middle"]//text()')
        if info:
            items = len(info[0].split()[0])
            if items < 3:
                items = 3

            return items

    def get_page_count(self):
        info = self.tree.xpath('//td[@class="tableh1" and @valign="middle"]//text()')
        if info:
            pages = int(info[0].split()[3])
            return pages
        else:
            return False

    def get_image_links(self):
        links = self.tree.xpath('//a/img[@class="image thumbnail"]/@src')
        for i in range(len(links)):
            for j in self.exclude:
                links[i] = links[i].replace(j, "")

        return links

    def album_page_saved(self, links):
        path = os.path.join(self.save_location, *self.path)
        if os.path.isdir(path):
            os.chdir(path)
            saved = os.listdir(os.getcwd())

            for i in range(len(links)):
                if str(self.count + i).zfill(self.get_album_size()) + "." + links[i].rpartition('.')[2] not in saved:
                    return False

            self.count += len(links)
            return True

        return False

    def get_album_page(self, url, page):
        if page > 1:
            self.set_html_tree(url)

        links = self.get_image_links()
        if self.album_page_saved(links):
            print("|   |-- PAGE " + str(page) + " - SKIPPED")
            return

        print("|   |-- PAGE " + str(page))

        images = [x.rpartition('/')[2] for x in links]
        for i in range(len(links)):
            image_url = self.build_url(links[i])
            r = self.s.get(image_url)

            filename = str(self.count).zfill(self.get_album_size()) + "." + links[i].rpartition('.')[2]
            location = os.path.join(self.save_location, *self.path, filename)

            print("|   |   |-- saving " + images[i] + " as " + filename)
            os.makedirs(os.path.dirname(location), exist_ok=True)
            with open(location, 'wb') as f:
                f.write(r.content)

            self.count += 1
            self.total += 1

    def get_album(self, url, title=None, subtitle=None):
        self.count = 1

        self.set_html_tree(url)
        self.set_page_path(title, subtitle)

        print("SAVING\n"
              + "|-- " + unquote(url) + "\n"
              + "|-- " + "/".join(self.path))

        pages = self.get_page_count()
        for i in range(1, pages + 1):
            if i == 1:
                self.get_album_page(url, i)
            else:
                page_url = url + "&page=" + str(i)
                self.get_album_page(page_url, i)

    def get_album_url(self, stat):
        url = stat.xpath('../../..//span[@class="alblink"]/a/@href')[0]
        album_url = self.build_url(url)

        return album_url

    def get_album_title(self, stat):
        title = stat.xpath('../../..//span[@class="alblink"]/a/text()')[0]
        album_title = title.strip()

        if album_title in self.seen:
            self.seen[album_title] += 1
            album_title += " (" + str(self.seen[album_title]) + ")"
        else:
            self.seen[album_title] = 1

        return album_title

    def get_album_subtitle(self, stat):
        album_subtitle = None

        strong = stat.xpath('../p[not(@class)]/strong/text()')
        if strong:
            for j in range(len(strong)):
                strong[j] = strong[j].replace(":", "").lower().strip()

        details = stat.xpath('../p[not(@class)]/text()')
        if details:
            details = [x.replace("\r\n", "").strip() for x in details if x.strip(" ") != "\r\n"][:2]
            if not strong:
                strong = ["", ""]
                for j in range(len(details)):
                    if details[j].lower().strip().startswith("from"):
                        pattern = re.compile(r"^from*\s*:*\s", re.IGNORECASE)
                        details[j] = pattern.sub("", details[j])
                        strong[0] = "from"
                    if details[j].lower().strip().startswith("by"):
                        pattern = re.compile(r"^by*\s*:*\s", re.IGNORECASE)
                        details[j] = pattern.sub("", details[j])
                        strong[1] = "by"

            subtitle = strong[0] + " " + details[0] + " " + strong[1] + " " + details[1]
            album_subtitle = subtitle.strip()

        return album_subtitle

    def scrape(self, start_url, ps=False):
        queue = [start_url]

        while queue:
            url = queue.pop()
            self.set_html_tree(url)
            self.set_page_path()

            print("SCRAPING\n"
                  + "|-- " + unquote(url) + "\n"
                  + "|-- " + "/".join(self.path))

            pages = self.get_page_count()
            if pages:
                if "&page=" not in url:
                    self.seen = {}
                    if pages > 1:
                        for i in range(pages, 1, -1):
                            page_url = url + "&page=" + str(i)
                            queue.append(page_url)

            cats = self.tree.xpath('//span[@class="catlink"]/a/@href')
            if cats:
                for i in range(len(cats) - 1, -1, -1):
                    cat_url = self.build_url(str(cats[i]))
                    queue.append(cat_url)

            albums = self.tree.xpath('//p[@class="album_stat"]')
            for i in albums:
                if i.text.lower().strip() != "0 files":
                    album_url = self.get_album_url(i)
                    album_title = self.get_album_title(i)

                    if ps:
                        album_subtitle = self.get_album_subtitle(i)
                    else:
                        album_subtitle = None

                    self.get_album(album_url, album_title, album_subtitle)

    def start(self, start_url, ps=False):
        if "album" in start_url:
            self.get_album(start_url)
        else:
            self.scrape(start_url, ps)


def main():
    # for f in os.listdir("."):
    #     os.remove(f)

    current = os.path.abspath(os.path.dirname(__file__))
    save_location = click.prompt("save_location", default=current)

    base_url = click.prompt("base_url")
    start_url = click.prompt("start_url")
    ps = click.confirm("ps")

    scraper = Scraper(save_location, base_url)

    start = time.time()
    scraper.start(start_url, ps=ps)
    end = time.time() - start

    print(round(end), "seconds")
    print(scraper.total, "images")


if __name__ == '__main__':
    main()
