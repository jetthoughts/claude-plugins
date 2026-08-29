# unFIX pattern reference

Detail behind `SKILL.md`. Read when a design decision turns on the difference between two patterns of the same kind.

## Contents

- [Base types](#base-types) — how tightly Crews couple
- [Crew types in full](#crew-types-in-full)
- [Forum types](#forum-types)
- [Role attributes in full](#role-attributes-in-full)
- [Relation to other models](#relation-to-other-models)
- [What Appelo says is unproven](#what-appelo-says-is-unproven)

## Base types

The Base is the home unit — a handful to a few hundred people, ideally covering a **customer domain, not a technical domain**, containing every skill needed to design, develop and deliver. Four variants, by how tightly its Crews couple:

| Base type | Crews are | Cadence | Fits when |
|---|---|---|---|
| **Fully Integrated** | tightly coupled, one product, shared everything | usually synchronised | one product, heavy interdependence |
| **Strongly Aligned** | coupled but distinguishable value streams | often synchronised | related products with real shared surface |
| **Loosely Aligned** | mostly independent, occasional coordination | asynchronous is fine | streams that rarely touch |
| **Fully Segregated** | independent, near-separate businesses | asynchronous | distinct customers with almost nothing shared |

**Cadence and synchronisation are optional in every case.** Appelo is explicit that neither the Spotify model nor unFIX prescribes them, and that asynchronous work is often correct — particularly for Loosely Aligned and Fully Segregated Bases.

## Crew types in full

| Crew | Purpose | Signal it is missing |
|---|---|---|
| **Value Stream Crew** | end-to-end responsibility for delivering value to a customer | work crosses many teams and nobody owns the outcome |
| **Facilitation Crew** | temporarily helps other Crews get up to speed, then withdraws | the same problem is solved badly and separately in several Crews |
| **Capability Crew** | wraps rare or unique skills; members work *on* the Value Stream Crews | one specialist is a bottleneck across everything |
| **Platform Crew** | infrastructure or architecture offered as if by a supplier | every Crew rebuilds the same plumbing |
| **Governance Crew** | the Chiefs; conflicts and trade-offs land here | decisions escalate more than one level, or stall |
| **Experience Crew** | one representative per customer-touching Value Stream Crew; owns the journey across streams | each stream optimises its slice, the whole journey belongs to nobody |
| **Partnership Crew** | outside relationships: suppliers, partners, channels | partner relationships are held personally and are invisible |

A Crew has **final say over how it gets its work done**, on the condition that it takes full responsibility for the value it provides. All actual value-stream work happens on the Crews — Capability and Facilitation Crew members do their work *on* the Value Stream Crews, not in an ivory tower.

## Forum types

A Forum groups people from several Crews along a functional line, to agree how work is done. **No line management, ever** — no recruitment, compensation, career development or performance review.

| Forum | Groups by |
|---|---|
| **Functional** | discipline — DevOps, UX, product management |
| **Product** | a product or product line |
| **Market** | a served market |
| **Channel** | a sales or delivery channel |
| **Business Model** | a way of making money |
| **Customer Journey** | a stage or whole journey |
| **Regional** | geography |
| **Technological** | a technology or platform |
| **Seasonal** | a recurring time-bound concern |

Chiefs decide which Forums the Base needs, and may delegate standardisation, templates, toolsets, infrastructure, personal development and cross-team coordination to them. Each worker is expected to belong to at least one.

Scaled up beyond one Base, a Forum becomes a **Super-Forum** — which is what guilds and communities of interest are. Appelo's observation: *"when you remove line management out of a chapter, the chapter is just a small version of a guild"*, so no new element type is needed and the model stays fractal.

## Role attributes in full

Sixteen ingredients for composing context-specific roles, rather than a fixed role set. Appelo gives the list and the composition principle; the groupings below are a reading aid, not his taxonomy.

**Leading and coordinating** — Chief · Captain · Chair · Envoy · Agent
**Enabling and teaching** — Enabler · Guide · Guru · Maven
**Making and performing** — Creator · Performer · Producer · Director
**Recording and checking** — Scribe · Custodian · Inspector

Worked examples Appelo gives:

- a rotating informal team lead → **Captain + Producer**
- someone leading quality improvement → **Custodian** or **Inspector**
- managing dependencies between teams without everyone talking to everyone → **Agent** and **Envoy**

The constraint that matters is restraint: *"An Italian chef won't unload half the kitchen onto people's plates, and neither should you."* Roles trade flexibility for clarity, and balancing that is a continuing process rather than a design output.

## Relation to other models

**Team Topologies** supplies four of the seven Crew types; unFIX adds Governance, Experience and Partnership. Appelo credits it for giving practical language to an idea he had only stated vaguely — that every team must offer defined value to its clients, whether customers or other teams.

**Dynamic Reteaming** (Helfand) supplies the assumption that **static teams are not agile**. Crews are stable but not static.

**The Spotify model** is what unFIX is most often positioned against. Appelo's own list of differences: value streams drawn horizontally rather than vertically; remote allowed rather than co-located; dynamic reteaming rather than long-lived squads; Experience Crew added for PO collaboration; Facilitation Crew added for agile coaches; Governance Crew instead of one tribe lead; Platform Crew instead of an operations team; Capability Crew instead of system owners; four Forum types instead of only functional chapters; Chairs who are explicitly not managers; not a matrix; fractal rather than one company's snapshot.

**Holacracy and sociocracy** are among the models unFIX offers an alternative to. The structural difference worth knowing: consent-based governance distributes decision rights through argued objection among people with independent judgement, while unFIX keeps a named owner per Crew (Captain) and a single management team (Chiefs) and does not require independent judgement to function.

**Management 3.0** supplies the Governance Crew, and is now merged with unFIX into M3K.

## What Appelo says is unproven

Quote this rather than paraphrasing it, because it is the honest boundary of the model:

> *"To be honest, most of this upward scaling with unFIX is still hypothetical. We know the patterns work at a small scale; we believe they can work at a large scale too."*

He also flags the fractal claim itself as hypothesis: *"I'm sure that design purists will appreciate that this could make the unFIX model fractal and scale-invariant. (To be honest, I am just hypothesizing here. I have no personal experience with this.)"*

So: **Base-level patterns are the evidenced part. League, Crowd, Cluster, Coalition, Assembly and Congress are proposals.**
