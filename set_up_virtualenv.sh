#!/bin/bash

# Set up virtualenv for our setup (uses 'requirements/*')

if ! [ -x "$(command -v python3)" ]; then
    echo "Error: cannot find executable 'python3'. Install it first. Exiting..."
    exit 0
fi

if ! [ -x "$(command -v pip3)" ]; then
    echo "Error: cannot find executable 'pip3'. Install it first. Exiting..."
    exit 0
fi

MY_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# cd "$MY_DIR/.."

if [ -d "env" ]; then
    # echo "set_up_virtualenv: env/ exists, doing nothing..." 1>&2
    exit 0
else
    python3 -m virtualenv env
    . env/bin/activate
    if [ -e requirements.txt ]; then
        pip3 install -r requirements.txt
    fi
fi
