# -*- mode: python ; coding: utf-8 -*-
import sys

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('tools', 'tools'),
        ('pages', 'pages'),
        ('styles', 'styles'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

if sys.platform.startswith('win'):
    # Windows 配置
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,        # 打包成单文件
        a.datas,
        [],
        name='PDF工具箱',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='icon.ico' if sys.platform.startswith('win') else None,
    )
else:
    # macOS 配置
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='PDF工具箱',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='PDF工具箱',
    )
    
    # macOS 特定配置
    app = BUNDLE(
        coll,
        name='PDF工具箱.app',
        icon=None,
        bundle_identifier='com.pdftools.app',
        version='1.0.0',
        info_plist={
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': 'True',
        },
    ) 