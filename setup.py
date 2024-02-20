import sys

from setuptools import setup, Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


plat = "windows"
if sys.platform == "linux":
    plat = "linux"
elif sys.platform == "darwin":
    plat = "mac"

setup(
    distclass=BinaryDistribution,
    package_data={"wii_music_editor": ["include/all/**/*", f"include/{plat}/**/*"]}
)
