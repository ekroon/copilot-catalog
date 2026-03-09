# Go package forwarding example

```go
// architecture/api.go
package architecture

import "your/module/architecture/plannerimpl"

type Plan struct{}

type Planner struct {
	plannerImpl plannerimpl.Planner
}

func NewPlanner() Planner {
	return Planner{plannerImpl: plannerimpl.New()}
}

func (p Planner) Create(plan Plan) error {
	return p.plannerImpl.Create(plan)
}
```

```go
// architecture/plannerimpl/planner.go
package plannerimpl

import "your/module/architecture"

type Planner struct{}

func New() Planner { return Planner{} }

func (p Planner) Create(plan architecture.Plan) error {
	return nil
}
```
