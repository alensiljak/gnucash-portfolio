"""
Show how to read Windows registry.
On Windows, this is used to read the GnuCash preferences, like default currency.

References:
- [winReg](https://docs.python.org/3.1/library/winreg.html)
- [GnuCash Currency settings](https://github.com/Gnucash/gnucash/blob/723530a9bc212a618bf6adf69d88fb9f8789ca17/gnucash/gnome/gschemas/org.gnucash.gschema.xml.in.in#L128)
- [Settings Migration](https://www.gnucash.org/docs/v2.6/C/gnucash-guide/basics-migrate-settings.html) shows where the settings are stored on different OS's.
"""
import winreg

def display_key(key):
    root= winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\GSettings\org\gnucash\general', 0, winreg.KEY_READ)
    [Pathname,regtype]=(winreg.QueryValueEx(root, key))
    print(key, [Pathname, regtype])
    winreg.CloseKey(root)

key = "currency-choice-locale"
display_key(key)

key = "currency-choice-other"
display_key(key)

key = "currency-other"
display_key(key)
