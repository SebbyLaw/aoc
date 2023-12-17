use pyo3::prelude::*;

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::ops::{Add, Mul, Sub};

#[derive(Clone, Copy, Debug, PartialEq, PartialOrd)]
#[pyclass(module = "aoclib", frozen, get_all)]
pub struct Point {
    row: i64,
    col: i64,
}

impl Add for Point {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Point {
            row: self.row + other.row,
            col: self.col + other.col,
        }
    }
}

impl Sub for Point {
    type Output = Self;

    fn sub(self, other: Self) -> Self {
        Point {
            row: self.row - other.row,
            col: self.col - other.col,
        }
    }
}

impl Mul<i64> for Point {
    type Output = Self;

    fn mul(self, scalar: i64) -> Self {
        Point {
            row: self.row * scalar,
            col: self.col * scalar,
        }
    }
}

#[pymethods]
impl Point {
    #[new]
    fn new(row: i64, col: i64) -> Self {
        Point { row, col }
    }

    fn __eq__(&self, other: &Self) -> bool {
        self == other
    }

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.row.hash(&mut hasher);
        self.col.hash(&mut hasher);
        hasher.finish()
    }

    fn __bool__(&self) -> bool {
        true
    }

    fn __repr__(&self) -> String {
        format!("Point({}, {})", self.row, self.col)
    }

    fn __add__(&self, other: &Self) -> Self {
        self.add(*other)
    }

    fn __sub__(&self, other: &Self) -> Self {
        self.sub(*other)
    }

    fn __mul__(&self, scalar: i64) -> Self {
        *self * scalar
    }

    fn __lt__(&self, other: &Self) -> bool {
        self < other
    }

    fn __le__(&self, other: &Self) -> bool {
        self <= other
    }

    #[getter]
    fn up(&self) -> Self {
        Point {
            row: self.row - 1,
            col: self.col,
        }
    }

    #[getter]
    fn down(&self) -> Self {
        Point {
            row: self.row + 1,
            col: self.col,
        }
    }

    #[getter]
    fn left(&self) -> Self {
        Point {
            row: self.row,
            col: self.col - 1,
        }
    }

    #[getter]
    fn right(&self) -> Self {
        Point {
            row: self.row,
            col: self.col + 1,
        }
    }

    #[getter]
    fn north(&self) -> Self {
        Point {
            row: self.row - 1,
            col: self.col,
        }
    }

    #[getter]
    fn south(&self) -> Self {
        Point {
            row: self.row + 1,
            col: self.col,
        }
    }

    #[getter]
    fn west(&self) -> Self {
        Point {
            row: self.row,
            col: self.col - 1,
        }
    }

    #[getter]
    fn east(&self) -> Self {
        Point {
            row: self.row,
            col: self.col + 1,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_point_eq() {
        let p1 = Point::new(1, 2);
        let p2 = Point::new(1, 2);
        assert_eq!(p1, p2);
    }

    #[test]
    fn test_point_add() {
        let p1 = Point::new(1, 2);
        let p2 = Point::new(3, 4);
        let p3 = p1 + p2;
        assert_eq!(p3, Point::new(4, 6));
    }

    #[test]
    fn test_point_sub() {
        let p1 = Point::new(1, 2);
        let p2 = Point::new(3, 4);
        let p3 = p1 - p2;
        assert_eq!(p3, Point::new(-2, -2));
    }

    #[test]
    fn test_point_mul() {
        let p1 = Point::new(1, 2);
        let p3 = p1 * 3;
        assert_eq!(p3, Point::new(3, 6));
        assert_eq!(p1, Point::new(1, 2));
    }
}
