# Exercise 4 (slide 68): UML practice

**Statement:** [gist: uml_exo.md](https://gist.github.com/bdallard/2d2407c4de4c182afca6d3ec7235e9eb)

- [`hospital.md`](hospital.md): Exo 1, Hospital Management System (tasks 1 to 3: class diagrams, sequence diagrams, questions)
- [`abcd_records.md`](abcd_records.md): Exo 2, ABCD Records (levels 1 to 3: use case, class and sequence diagrams)

Diagrams are written in Mermaid so GitHub draws them. The exercises were also done by hand on paper, since the exam is handwritten.

## Class diagram relationships

| Relationship | Symbol | Meaning | Example |
| --- | --- | --- | --- |
| Association | plain line / arrow | uses or knows another object | Doctor → Prescription |
| Dependency | dashed arrow | temporary use (parameter) | Clerk ┄> MembershipApplication |
| Aggregation | hollow diamond ◇ | has-a, the part survives the whole | DailyRecordsFile ◇— Order |
| Composition | filled diamond ◆ | made-of, the part dies with the whole | Order ◆— OrderLine |
| Inheritance | solid line + hollow triangle ▷ | is-a | RoyalMember ▷ Member |
| Realization | dashed line + hollow triangle | implements an interface | CheckPayment ┄▷ PaymentMethod |

Visibility: `+` public, `-` private, `#` protected. Multiplicities: `1`, `0..1`, `*`, `1..*`.

## Use case diagram rules

- Actors **outside** the system boundary, use cases (ellipses, verb + object) **inside**.
- Actor — use case: **plain solid line**.
- **«include»** = mandatory, dashed arrow **from the base to the included** use case.
- **«extend»** = optional, dashed arrow **from the extension to the base**.
- Actor generalization: hollow triangle pointing to the **more general** actor (Royal Member ▷ Member).

## Sequence diagram rules

- Participants at the top, time goes **down**.
- Solid arrow = call, dashed arrow = return.
- `alt` = if / else, `opt` = optional, `loop` = repetition.
