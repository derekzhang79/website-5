#!/bin/sh

# Coffeescript settings
CS_INPUT='src/cs/'
CS_OUT='js/'

# SASS
SASS_INPUT='src/sass'
SASS_OUT='css'

# main conf
PID_DIR='PID/'
PID_CS='cs.pid'
PID_SASS='sass.pid'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -f $DIR/$PID_DIR$PID_CS ];
then
	echo 'killing'
	PID="$(cat $DIR/$PID_DIR$PID_CS)"
	kill -9 $PID
	rm $DIR/$PID_DIR$PID_CS
fi

COFFEE='coffee -o '$DIR'/'$CS_OUT' -cw '$DIR'/'$CS_INPUT
SASS='sass --watch '$DIR'/'$SASS_INPUT':'$DIR'/'$SASS_OUT

$COFFEE &
echo $! > $DIR/$PID_DIR$PID_CS
#$SASS &