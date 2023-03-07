from cx_Freeze import setup, Executable

includefiles = ['similarity_model']
includes = []
excludes = []
packages = []

setup(
    name = 'app',
    version = '0.1',
    options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable('app.py')],
    base="Win32GUI"
)
