#!/bin/bash
################################################################################
# Title:    runtests.sh
# Version:  0.2
# Date:     2011-07-28
# Author:   Tim Flink <tflink@redhat.com>
# License:  GPLv2
#
# This is a quick script used to run the autoqa tests inside a virtualenv
# You will need the following packages already installed:
#   - python-virtualenv
#   - python-pip
#
# Usage:
#  runtests [-f]
################################################################################

# used for the name of the virtualenv
ENV_NAME='env_flask'

# pip-python's requirements
REQ_FILE='dependencies.txt'

# by default, only run unit tests
RUN_FUNCTIONAL='TRUE'

# name of library under test
LIB_NAME='mock_fedorainfra'

# directory containing library to test, relative to this dir
LIB_LOC='mock_fedorainfra'

# directory containing tests
TESTS_LOC='testing'

# this is to make sure that pip-python isn't going to touch anything but the
# virtualenv
PIP_REQUIRE_VIRTUALENV=1

# this keeps track of the python version since virtualenv will use the system
# python version by default
PYTHON_VERSION=`python --version 2>&1 | egrep -o "2.[0-9]"`

usage()
{
    cat << EOF
    usage: $0
    This script prepares a virtualenv for running the tests (if it doesn't
    already exist) and runs unit tests in that virtualenv.

    OPTIONS:
      -h    Show this message
      -f    Run functional tests

EOF
}

# Creates and prepares a virtualenv
create_env()
{
    echo "Virtualenv ($ENV_NAME) Does not already exist."
    echo "Creating virtualenv"
    echo ""
    virtualenv $ENV_NAME

    echo "Installing packages (into $ENV_NAME) required for tests"
    echo ""
    pip-python -E $ENV_NAME install -r $REQ_FILE

    echo "Adding autoqa to virtualenv site-packages"
    pushd "$ENV_NAME/lib/python$PYTHON_VERSION/site-packages"
    ln -s "../../../../$LIB_LOC" "$LIB_NAME"
    popd

    echo "Virtualenv created and prepared."
    echo ""
}

while getopts “hf” OPTION
do
    case $OPTION  in
        h)
            usage
            exit 0
            ;;
        f)
            RUN_FUNCTIONAL='TRUE'
            ;;
    esac
done

# check for virtualenv
if [ ! -e $ENV_NAME ]
    then
        create_env
    else
        echo "Virtualenv ($ENV_NAME) detected."
fi

# activate the virtualenv
source "$ENV_NAME/bin/activate"

# run the tests
if [ $RUN_FUNCTIONAL = 'TRUE' ]
then
    py.test "$TESTS_LOC" --functional
else
    py.test "$TESTS_LOC"
fi

TEST_RESULT=$?

#deactivate the virtualenv
deactivate

if [ $TEST_RESULT -ne 0 ]
then
    exit 1
else
    exit 0
fi
