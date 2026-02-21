---
name: agentic-progressive-disclosure-architecture
description: Build codebases for agentic coding with progressive disclosure using module trees, API-first top layers, and implementation split by depth (best fit for Rust and Go).
---

# Agentic Progressive Disclosure Architecture

Use this skill when you want code structure that reveals intent first and implementation details only when deeper files are loaded.

## What it is

Progressive disclosure for code architecture mirrors how skills are read:

1. Top layer: short explanation + module map + API signatures.
2. Middle layer: domain-focused modules that re-export or wire submodules.
3. Leaf layer: detailed implementations.

This pattern is strongest in **Rust** and **Go** where module/package boundaries are explicit.

## When to use it

- Agent-heavy coding workflows where small context windows must stay focused.
- Large systems where API shape should be visible without loading full implementations.
- Teams comfortable with IDE/LSP navigation for jump-to-definition and symbol search.

## Architecture rules

- Keep top-level files mostly declarative (exports, signatures, short docs).
- Place heavy logic in deeper modules/files.
- Re-export from higher layers to preserve ergonomic public APIs.
- Keep this orthogonal to existing clean-code practices (naming, testing, error handling, etc.).

## Rust pattern

Top-level crate API in `src/lib.rs`:

```rust
//! Public API and architecture map.
pub mod domain;
pub mod util;

pub use domain::{Plan, Planner}; // progressive API surface
```

Split declarations from implementations:

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

## Go pattern

Top-level package file:

```go
// package architecture exposes intent-first APIs.
package architecture

type Plan struct{}
type Planner interface {
	Create(Plan) error
}
```

Deeper implementation package:

```go
package plannerimpl

import "your/module/architecture"

type Planner struct{}
func (p Planner) Create(plan architecture.Plan) error { return nil }
```

## Proof strategy: tests and benchmarks

Use tests and benchmarks to verify the architecture is practical, not only stylistic.

- **Tests**: ensure re-exports and API contracts behave as expected.
  - Rust: integration tests against top-level crate exports (`tests/`).
  - Go: package tests that import only top-level package APIs.
- **Benchmarks**: compare baseline vs progressive-disclosure layout to detect runtime or compile-time regressions.
  - Rust: `cargo bench`
  - Go: `go test -bench . ./...`

Success criteria:

- Callers can use top-level APIs without importing leaf implementation modules.
- Benchmarks show no unacceptable regression for critical paths.
- Navigation remains fast via IDE/LSP symbols and definitions.
