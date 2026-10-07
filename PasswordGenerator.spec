# -*- mode: python ; coding: utf-8 -*-
#
# PasswordGenerator.spec
# Arquivo de configuração do PyInstaller para empacotamento profissional.

from pathlib import Path

ROOT = Path(SPECPATH)

# ── Análise de dependências ──────────────────────────────────────────────────
a = Analysis(
    [str(ROOT / 'main.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # Inclui o ícone no bundle
        (str(ROOT / 'icon.ico'), '.'),
    ],
    hiddenimports=[
        'mvc.model',
        'mvc.view',
        'mvc.controller',
        'pyperclip',
        'PIL',
        'PIL.Image',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'unittest', 'email', 'html', 'http', 'urllib',
        'xmlrpc', 'pydoc', 'doctest', 'argparse', 'difflib',
        'pickle', 'calendar', 'ftplib', 'getpass', 'imaplib',
        'mailbox', 'mimetypes', 'poplib', 'smtplib',
    ],
    noarchive=False,
    optimize=2,
)

# ── Compactação dos arquivos Python ─────────────────────────────────────────
pyz = PYZ(a.pure)

# ── Executável único (onefile) ───────────────────────────────────────────────
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PasswordGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # <<< Sem janela de console (modo GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ROOT / 'icon.ico'),
    version_file=None,
)
