set export

default: build

test:
  cargo test --all --lib
  poetry run maturin develop --features extension-module
  poetry run pytest tests

build:
  poetry run maturin develop --release --strip --features extension-module

new YEAR DAY:
  mkdir -p sols/$YEAR
  cp -i template.py sols/$YEAR/$(printf "%02d" $DAY).py
  code sols/$YEAR/$(printf "%02d" $DAY).py
