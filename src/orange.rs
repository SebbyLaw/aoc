use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::ops::{BitAnd, Sub};

#[derive(Debug, PartialEq, Copy, Clone)]
#[pyclass(module = "aoclib", name = "orange", frozen, get_all)]
pub struct Orange {
    start: i128,
    stop: i128,
}

impl BitAnd for Orange {
    type Output = Option<Orange>;

    fn bitand(self, rhs: Self) -> Self::Output {
        if self.start >= rhs.stop || self.stop <= rhs.start {
            None
        } else {
            let start = std::cmp::max(self.start, rhs.start);
            let stop = std::cmp::min(self.stop, rhs.stop);
            Some(Orange { start, stop })
        }
    }
}

impl Sub for Orange {
    type Output = Vec<Orange>;

    fn sub(self, rhs: Self) -> Self::Output {
        if self.start >= rhs.stop || self.stop <= rhs.start {
            vec![self]
        } else if self.start < rhs.start {
            if self.stop > rhs.stop {
                vec![
                    Orange {
                        start: self.start,
                        stop: rhs.start,
                    },
                    Orange {
                        start: rhs.stop,
                        stop: self.stop,
                    },
                ]
            } else {
                vec![Orange {
                    start: self.start,
                    stop: rhs.start,
                }]
            }
        } else if self.stop > rhs.stop {
            vec![Orange {
                start: rhs.stop,
                stop: self.stop,
            }]
        } else {
            vec![]
        }
    }
}

#[pyclass]
struct OrangeIterator {
    iter: Box<dyn Iterator<Item = i128> + Send>,
}

#[pymethods]
impl OrangeIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>) -> Option<i128> {
        slf.iter.next()
    }
}

#[pymethods]
impl Orange {
    #[new]
    fn py_new(start: i128, stop: i128) -> PyResult<Self> {
        if stop < start {
            Err(PyValueError::new_err("stop must not be less than start"))
        } else {
            Ok(Orange { start, stop })
        }
    }

    fn __contains__(&self, item: i128) -> bool {
        self.start <= item && item < self.stop
    }

    fn __eq__(&self, other: &Self) -> bool {
        self == other
    }

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.start.hash(&mut hasher);
        self.stop.hash(&mut hasher);
        hasher.finish()
    }

    fn __bool__(&self) -> bool {
        self.start < self.stop
    }

    fn __and__(&self, other: Self) -> Option<Orange> {
        self.bitand(other)
    }

    fn __sub__(&self, other: Self) -> Vec<Orange> {
        self.sub(other)
    }

    fn __repr__(&self) -> String {
        format!("orange({}, {})", self.start, self.stop)
    }

    fn __len__(&self) -> usize {
        (self.stop - self.start) as usize
    }

    fn __iter__(&self) -> OrangeIterator {
        OrangeIterator {
            iter: Box::new(self.start..self.stop),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_orange() {
        let orange = Orange::py_new(1, 2).unwrap();
        assert_eq!(orange.start, 1);
        assert_eq!(orange.stop, 2);
    }

    #[test]
    fn test_orange_eq() {
        let orange1 = Orange::py_new(1, 2).unwrap();
        let orange2 = Orange::py_new(1, 2).unwrap();
        assert_eq!(orange1, orange2);
    }

    #[test]
    fn test_orange_intersection() {
        let orange1 = Orange::py_new(1, 3).unwrap();
        let orange2 = Orange::py_new(2, 4).unwrap();

        assert_eq!(orange1 & orange2, Some(Orange::py_new(2, 3).unwrap()));
    }

    #[test]
    fn test_orange_intersection_none() {
        let orange1 = Orange::py_new(1, 2).unwrap();
        let orange2 = Orange::py_new(3, 4).unwrap();

        assert_eq!(orange1 & orange2, None);
    }

    #[test]
    fn test_orange_sub() {
        let orange1 = Orange::py_new(0, 10).unwrap();
        let orange2 = Orange::py_new(5, 15).unwrap();

        assert_eq!(orange1 - orange2, vec![Orange::py_new(0, 5).unwrap()]);
    }

    #[test]
    fn test_orange_sub_none() {
        let orange1 = Orange::py_new(0, 10).unwrap();
        let orange2 = Orange::py_new(0, 10).unwrap();

        assert_eq!(orange1 - orange2, vec![]);
    }
}
