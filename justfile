test:
  cargo test --all --lib
  poetry run maturin develop --features extension-module
  poetry run pytest tests

build:
  poetry run maturin develop --release --strip --features extension-module
