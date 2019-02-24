# long-live

> will you take a moment, promise me this /
> that you'll stand by me forever /
> but if god forbid fate should step in /
> and force us into a goodbye /
> if you have children someday /
> when they point to the pictures /
> please tell them my name /
> tell them how the crowds went wild /
> tell them how i hope they shine

long-live is a small web scraping script that recursively downloads albums from Coppermine photo galleries. It should work for most websites, but the XPaths may need some modification to handle different gallery themes.

## Installation

For an all-in-one package, [download the latest release](https://github.com/kivaar/long-live/releases).

Alternatively, you can git clone this repository and build the executable yourself:

```bash
git clone https://github.com/kivaar/long-live.git

cd long-live/

pyinstaller build.spec
```

## Usage

There are a few options here as I was playing around with a couple of Python packages. You can use the exe to run the script in a GUI or execute either `scraper.py` or `tkinter.py` from the command line. `tkinter.py` presents a small window for the user to enter all of the required arguments before running the script. `scraper.py` is the script itself.

`save_location` - the path to save the images to

`base_url` - the URL for the home page of the gallery

`start_url` - the URL to start downloading from. If this points to a category, ALL albums nested under this category will be downloaded. This can also be the URL of a single photo album

`ps (experimental)` - some galleries have a category for photoshoots where each album is tagged with the photographer's name and the publication the photos were for. If your `start_url` falls under a category such as this, you can enable this option to have these fields appended to folder names in the following manner: \<album name> - for \<publication> by \<photographer>