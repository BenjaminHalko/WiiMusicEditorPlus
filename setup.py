import sys

from setuptools import setup, Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


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
    package_data={"wii_music_editor": data}
)
