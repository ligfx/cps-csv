#!/bin/bash

textutil -convert html "$1" -stdout | sed "s:<span class=\"Apple-tab-span\">[[:space:]]*</span>:$(printf "\t"):g" | sed "s:<span class=\"Apple-converted-space\">[[:space:]]*</span>: :g" | sed "s:<[^>]*>::g" | sed -E "s:[[:space:]]+: :g"
