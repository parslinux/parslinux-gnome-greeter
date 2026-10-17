#!/bin/bash

langs=("tr" "pt" "es")

if ! command -v xgettext &> /dev/null
then
	echo "xgettext could not be found."
	echo "you can install the package with 'apt install gettext' command on debian."
	exit
fi

echo "Updating pot file..."

# Define source files for different parsers
PY_FILES=$(grep '\.py$' data/po/POTFILES | tr '\n' ' ')
UI_FILES=$(grep '\.ui$' data/po/POTFILES | tr '\n' ' ')
DESKTOP_FILES=$(grep '\.desktop\.in$' data/po/POTFILES | tr '\n' ' ')

# Extract from Python files
xgettext -o data/po/py.pot -L Python $PY_FILES

# Extract from UI files
xgettext -o data/po/ui.pot -L Glade --keyword=_ $UI_FILES

# Extract from desktop files and merge
if [ -n "$DESKTOP_FILES" ]; then
    xgettext -o data/po/desktop.pot -L Desktop --keyword=Name --keyword=Comment --keyword=Keywords $DESKTOP_FILES
    msgcat --sort-output data/po/py.pot data/po/ui.pot data/po/desktop.pot > data/po/parslinux-gnome-greeter.pot
    rm -f data/po/desktop.pot
else
    msgcat --sort-output data/po/py.pot data/po/ui.pot > data/po/parslinux-gnome-greeter.pot
fi

# Clean up temporary files
rm -f data/po/py.pot data/po/ui.pot

for lang in ${langs[@]}; do
	if [[ -f data/po/$lang.po ]]; then
		echo "Updating $lang.po"
		msgmerge -U data/po/$lang.po data/po/parslinux-gnome-greeter.pot
	else
		echo "Creating $lang.po"
		cp data/po/parslinux-gnome-greeter.pot data/po/$lang.po
	fi
done 