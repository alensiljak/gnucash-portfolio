""" runs lint from Python """

import subprocess

args = ['pylint', 'app', '--output-format=colorized']
subprocess.run(args, check=True)

args = ['pylint', 'gnucash_portfolio', '--output-format=colorized']
subprocess.run(args, check=True)

#output = subprocess.check_output(['pylint', 'app --output-format=colorized'])
#print(output)
