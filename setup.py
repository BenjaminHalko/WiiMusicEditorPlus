import site
import sys
from pathlib import Path

from pyshortcuts import make_shortcut
from setuptools import setup, Distribution
from setuptools.command.install import install


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        install_site = site.getsitepackages()[1]
        if not (Path(install_site) / "wii_music_editor").is_dir():
            install_site = self.install_usersite
        make_shortcut(
            f"{install_site}/wii_music_editor/__main__.py",
            name="Wii Music Editor",
            description="Wii Music Editor",
            icon=f"{install_site}/wii_music_editor/include/all/icon/icon.ico",
            terminal=True,
            desktop=False,
            startmenu=True,
        )


if "sdist" in sys.argv:
    data = ["include/**/**/*"]
else:
    plat = "windows"
    if sys.platform == "linux":
        plat = "linux"
    elif sys.platform == "darwin":
        plat = "mac"
    data = ["include/all/**/*", f"include/{plat}/**/*"]


setup(
    distclass=BinaryDistribution,
    package_data={"wii_music_editor": data},
    cmdclass={
        'install': PostInstallCommand,
    },
)
