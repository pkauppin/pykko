#!/bin/sh

cat $1 |
python3 -m tools.tokenizer |
python3 -m tools.parse |
python3 -m tools.normalize