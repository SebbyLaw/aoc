test:
  cargo test --all --lib
  maturin develop --features extension-module
  poetry run pytest tests

build:
  maturin develop --release --strip --features extension-module
