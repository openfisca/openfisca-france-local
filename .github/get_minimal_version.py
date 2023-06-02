import re


with open('./setup.py') as file:
    for line in file:
        version = re.search(r'(Core|France)\s*>=\s*([\d\.]*)', line)
        if version:
            # if/else to be removed when Custom requirement removed from setup.py
            if 'Core' in version.string:
                print(
                    'git+http://github.com/openfisca/openfisca-core.git@35.12.0_fix_testrunner_reforme_clone')
            else:
                print(f'Openfisca-{version[1]}=={version[2]}')
