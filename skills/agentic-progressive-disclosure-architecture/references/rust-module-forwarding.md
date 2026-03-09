# Rust module forwarding example

```rust
// src/lib.rs
//! Public API and architecture map.
pub mod domain;
pub mod util;

pub use domain::{Plan, Planner};
```

```rust
// src/domain/mod.rs
mod planner_impl;
pub struct Plan;
pub struct Planner;
impl Planner {
    pub fn create(plan: Plan) -> Result<(), String> {
        planner_impl::create(plan)
    }
}
```

```rust
// src/domain/planner_impl.rs
use super::Plan;
pub(super) fn create(_plan: Plan) -> Result<(), String> { Ok(()) }
```
