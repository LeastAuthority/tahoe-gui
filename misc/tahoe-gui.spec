# -*- mode: python -*-

block_cipher = None


a = Analysis(['../tahoe_gui/cli.py'],
             pathex=[],
             binaries=None,
             datas=[('../tahoe_gui/resources/*', 'resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Tahoe-GUI',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='images/icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Tahoe-GUI')
app = BUNDLE(coll,
             name='Tahoe-GUI.app',
             icon='images/icon.icns',
             bundle_identifier=None)
