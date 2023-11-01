#!/usr/bin/env bash

mode="$1"
codesubdir="$2"
shift 2

codedir="/code/$codesubdir"

function upfind() {
  currentdir="$codedir"
  while [ "$currentdir" != "/" ]; do
    path=$(find "$currentdir" -maxdepth 1 -name $1)
    if [ ! -z $path ]; then
      echo "$path"
      return
    fi
    currentdir=$(dirname "$currentdir")
  done
}

FLAKE8_CONFIG="$(upfind .flake8)"
BLACK_CONFIG="$(upfind .black)"

if [[ "$mode" = "check" ]]
then
  echo "check $codedir"
  flake8 --config "$FLAKE8_CONFIG" --black-config "$BLACK_CONFIG" -v "$codedir" $@

elif [[ "$mode" = "format" ]]
then
  echo "format --config $BLACK_CONFIG $codedir"
  black --config "$BLACK_CONFIG" "$codedir"

else
  echo "unsupported mode"
  exit 1
fi
