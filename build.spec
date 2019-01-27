import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

a = Analysis(['scraper_gui.py'],
             pathex=['C:\\Users\\kivaar\\projects\\long-live'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             )
pyz = PYZ(a.pure)

options = [('u', None, 'OPTION')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('.\\images', prefix='images\\'),
          options,
          gooey_languages, # Add them in to collected files
          gooey_images, # Same here.
          name='scraper_gui',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='.\\images\\program_icon.ico')