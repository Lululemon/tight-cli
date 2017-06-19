#!/bin/bash -e
declare -r CONF="setup.cfg"
declare -r ARGS=(ignore select max-line-length)
declare -r HELP="usage: $0 [fix]

Run autopep8 on all staged and unstaged *.py files in the git index

If you specified \"fix\" as an argument, it will run autopep8 on all *.py files
in the repository, regardless of staging.
"


# Parse a value out of the CONF file and return it with a '--' in front
get_arg() {
    set +e
    local _value=$(grep $1 $CONF)
    set -e
    if [ "$_value" ]; then
        echo "--$_value"
    fi
}

main() {
    local _tests="tests"
    local _autopep="autopep8 -j 0 -i -r"
    local _autopep_diff="autopep8 -d"
    local _package="tight_cli"
    for _arg in ${ARGS[@]}; do
        _autopep="$_autopep $(get_arg $_arg)"
    done
    if [ "$1" == "-h" ]; then
        echo "$HELP"
    elif [ "$1" == "fix" ]; then
        find $_package -name '*.py' | xargs $_autopep
        find $_tests -name '*.py' | xargs $_autopep
    elif [ "$1" == "check" ]; then
        local _package_result=$(find $_package -name '*.py' | xargs $_autopep_diff)
        local _tests_result=$(find $_tests -name '*.py' | xargs $_autopep_diff)

        local _exit="0"

        if [[ !  -z $_package_result ]]; then
            _exit="1"
            which colordiff > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo -- "$_package_result" | colordiff
            else
                echo -- "$_package_result"
            fi
        fi

        if [[ !  -z $_tests_result ]]; then
            which colordiff > /dev/null 2>&1
            _exit=1
            if [ $? -eq 0 ]; then
                echo -- "$_tests_result" | colordiff
            else
                echo -- "$_tests_result"
            fi
        fi

        exit "$_exit"
    else
        local _diff=$(git diff --name-only --diff-filter=ACMRT | grep '.py$')
        if [ "$_diff" ]; then
            echo "$_diff" | xargs $_autopep
        fi
        local _diff_cached=$(git diff --cached --name-only --diff-filter=ACMRT | grep '.py$')
        if [ "$_diff_cached" ]; then
            echo "$_diff_cached" | xargs $_autopep
        fi
    fi
}

main "$@"