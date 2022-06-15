from setuptools import setup, find_packages
from distutils.errors import CompileError
from subprocess import call
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
import os


class build_go_ext(build_ext):
    """Customized build command to build go module as shared library"""
    def build_extension(self, ext):
        ext_path = os.path.join(os.getcwd(), self.get_ext_fullpath(ext.name))
        od = os.getcwd()
        td = os.path.join(os.getcwd(), "bbolt-ffi")
        os.chdir(td)
        cmd = ['go', 'build', '-buildmode=c-shared', '-o', ext_path, "./ffi"]
        out = call(cmd)
        os.chdir(od)
        if out != 0:
            raise CompileError('Go build failed')


setup(
    name='py-bbolt',
    version='0.0.1',
    description='',
    license='MIT',
    packages=find_packages(),
    author='Amin Rezaei',
    author_email='AminRezaei0x443@gmail.com',
    keywords=[],
    url='https://github.com/AminRezaei0x443/py-bbolt',
    install_requires=[],
    extras_require={},
    ext_modules=[
         Extension('_bbolt_go', [])
    ],
    cmdclass={'build_ext': build_go_ext},
    zip_safe=False,
)
