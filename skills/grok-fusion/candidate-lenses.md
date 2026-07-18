# Candidate Lenses

Eight isolated proposer lenses. Each call uses `gf-worker` with a distinct objective, stance, and forbidden solution family.

Select which lenses to launch from [task-packs.md](task-packs.md):

- Quick: optional one verifier lens
- Standard: exactly three preferred pack lenses
- Heavy architecture: all eight unless the router narrows them
- MVP waves: pack-selected lenses for the current wave

## Shared requirements

Every lens must:

- follow [candidate-card.md](candidate-card.md)
- stay under 900 words
- include `FACTS / ASSUMPTIONS / UNKNOWNS`
- include at least one falsifiable prediction
- for architecture tasks: provide two designs or explicitly critique two designs from the brief
- never see other candidates

## Lenses

### 1. Minimal-change

- Objective: smallest reversible change that satisfies constraints
- Stance: conservative
- Forbidden: greenfield rewrite, new service layer as the first answer

### 2. Evolution-and-scale

- Objective: growth path, boundaries, and change amplification over time
- Stance: exploratory
- Forbidden: one-off local patch that cannot evolve

### 3. First-principles

- Objective: clean-slate constraint reasoning, then migration reality
- Stance: exploratory
- Forbidden: incremental patch to current code as the only answer

### 4. Implementation-realist

- Objective: concrete integration into the current stack and ownership model
- Stance: conservative
- Forbidden: greenfield rewrite or abstract architecture with no file-level path

### 5. Failure-and-security

- Objective: abuse cases, threat model, failure containment
- Stance: exploratory
- Forbidden: happy-path-only design

### 6. Operability-data-performance

- Objective: observability, data ownership, capacity, recovery, and performance risks
- Stance: conservative
- Forbidden: generic advice outside operability, data, or performance

### 7. Product-and-requirements

- Objective: outcome fit, scope cuts, build-versus-buy, wrong-problem detection
- Stance: exploratory
- Forbidden: accepting the user's framing as given without challenge

### 8. Persona-free wildcard

- Objective: alternate solution without professional role priming
- Stance: exploratory
- Forbidden: copying any standard enterprise pattern as the default

## Prompt construction

Each worker prompt must begin with:

1. required candidate card schema
2. Five Iron Rules
3. lens objective, stance, and forbidden family
4. original query
5. canonical brief
6. evidence pack
