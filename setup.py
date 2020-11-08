import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name = 'Subliminal-Study',
    options = {'build_exe': {'packages': ['pygame', 'smtplib', 'ssl', 'email.mime.text'],
                             'include_files': ['circle.png', 'circle-small.png', 'fixation2.png']}},
    executables = executables
)
