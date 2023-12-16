test:
  cargo test --all --lib
  maturin develop
  poetry run pytest tests

build:
  maturin develop --release --strip
