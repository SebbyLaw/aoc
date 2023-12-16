use pyo3::prelude::*;

mod orange;
mod point;

use crate::orange::Orange;
use crate::point::Point;

#[pymodule]
fn aoclib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Orange>().unwrap();
    m.add_class::<Point>().unwrap();

    Ok(())
}
