# Wrapper → Canonical Schema Mapping

## Current live wrapper output fields
- system
- active_forms
- source
- sink
- gradient
- path
- barrier
- loss
- maintenance
- control
- fragility

## Canonical schema fields
- system
- flow_objects.source
- flow_objects.sink
- flow_objects.gradient
- flow_objects.path
- constraint_objects.barrier
- constraint_objects.loss
- constraint_objects.maintenance
- constraint_objects.control
- constraint_objects.fragility
- structural_commitments.asymmetry
- structural_commitments.pressure_point
- structural_commitments.tradeoff
- structural_commitments.actors
- structural_commitments.cost_bearer
- structural_commitments.fracture_condition

## Mapping table
| Live wrapper field | Canonical field | Status | Notes |
|---|---|---|---|
| system | system | direct | |
| source | flow_objects.source | direct | |
| sink | flow_objects.sink | direct | |
| gradient | flow_objects.gradient | direct | |
| path | flow_objects.path | direct | |
| barrier | constraint_objects.barrier | direct | |
| loss | constraint_objects.loss | direct | |
| maintenance | constraint_objects.maintenance | direct | |
| control | constraint_objects.control | direct | |
| fragility | constraint_objects.fragility | direct | |
| active_forms | unmapped | provisional | decide whether canonical or runtime-only |
| asymmetry | structural_commitments.asymmetry | missing in emitted structure | |
| pressure_point | structural_commitments.pressure_point | missing | |
| tradeoff | structural_commitments.tradeoff | missing | |
| actors | structural_commitments.actors | missing | |
| cost_bearer | structural_commitments.cost_bearer | missing | |
| fracture_condition | structural_commitments.fracture_condition | missing | |
