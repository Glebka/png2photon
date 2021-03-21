# -*- mode: python ; coding: utf-8 -*-

import os
from os import path
from shutil import copyfile

block_cipher = None


a = Analysis(['src/main.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='png2photon',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

copyfile(path.join(os.getcwd(), 'src/config.ini'), path.join(os.getcwd(), 'dist/config.ini'))