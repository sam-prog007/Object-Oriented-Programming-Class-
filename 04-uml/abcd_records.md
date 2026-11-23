# Exo 2: ABCD Records

ABCD Records is a mail-order company selling CDs and tapes at discount prices to record club members.

- Only members can place orders; non-members receive a membership application form.
- Two member classes: **Royal** (discounts + priority) and **Regular**.
- Royal members can order unavailable items.
- Payment methods: cash, check, bank draft.
- The Order Processing Clerk handles verification and processing; the Collection Department Clerk handles payments.
- All orders are saved to a daily records file.

> GitHub's Mermaid has no native use case diagram, so use cases are drawn as a flowchart: rounded boxes = use cases, circles = actors, the frame = the system boundary, dashed arrows = «include» / «extend». On paper, use stick figures and ellipses.

---

## Level 1

### Task 1.1: simple use case diagram

```mermaid
flowchart LR
    M((Member))
    C((Order Processing Clerk))
    subgraph ABCD["ABCD Records ordering system"]
        PO([Place Order])
        VM([Verify Membership])
        PR([Process Order])
        MP([Make Payment])
    end
    M --- PO
    M --- MP
    C --- PR
    C --- VM
    PO -. "«include»" .-> VM
```

`Place Order` **includes** `Verify Membership`: "only members can place orders", so the check happens every time. The arrow goes **from the base to the included** use case.

### Task 1.2: basic class diagram

```mermaid
classDiagram
    direction LR
    class Member {
        -member_id: int
        -name: str
        -address: str
        +place_order(items: list) Order
        +pay(order: Order, method: str) None
    }
    class Order {
        -order_id: int
        -date: date
        -status: str
        +add_item(item, quantity: int) None
        +total() float
    }
    class OrderProcessingClerk {
        -employee_id: int
        -name: str
        +verify_membership(member: Member) bool
        +process_order(order: Order) None
    }
    Member "1" --> "*" Order : places
    OrderProcessingClerk "1" --> "*" Order : processes
```

---

## Level 2

### Task 2.1: complete use case diagram

```mermaid
flowchart LR
    M((Member))
    RM((Royal Member))
    RG((Regular Member))
    NM((Non-Member))
    OC((Order Processing Clerk))
    CC((Collection Dept Clerk))

    RM -- "is a ▷" --> M
    RG -- "is a ▷" --> M

    subgraph ABCD["ABCD Records ordering system"]
        PO([Place Order])
        VM([Verify Membership])
        VA([Verify Item Availability])
        AD([Apply Discount])
        OU([Order Unavailable Items])
        SA([Send Membership Application])
        PR([Process Order])
        PI([Print Invoice])
        PS([Print Shipping List])
        MP([Make Payment])
    end

    M --- PO
    M --- MP
    RM --- OU
    NM --- SA
    OC --- PR
    OC --- VM
    CC --- MP

    PO -. "«include»" .-> VM
    PO -. "«include»" .-> VA
    PR -. "«include»" .-> PI
    PR -. "«include»" .-> PS
    AD -. "«extend»" .-> PO
    OU -. "«extend»" .-> PO
    SA -. "«extend»" .-> VM
```

| Relationship | Why |
| --- | --- |
| Place Order «include» Verify Membership | every order needs a membership check |
| Place Order «include» Verify Item Availability | every order needs a stock check |
| Process Order «include» Print Invoice / Print Shipping List | always done when processing |
| Apply Discount «extend» Place Order | optional: only Royal members get discounts |
| Order Unavailable Items «extend» Place Order | optional: only Royal members, only when an item is out of stock |
| Send Membership Application «extend» Verify Membership | only happens when the check fails (non-member) |
| Royal / Regular ▷ Member | generalization: both are members and do everything a member does |

### Task 2.2: complete class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        #member_id: int
        #name: str
        #address: str
        +place_order(lines: list) Order
        +discount_rate()* float
    }
    class RoyalMember {
        -priority: bool
        +discount_rate() float
        +order_unavailable(item: Item) None
    }
    class RegularMember {
        +discount_rate() float
    }
    class Order {
        -order_id: int
        -date: date
        -status: OrderStatus
        +total() float
    }
    class OrderStatus {
        <<enumeration>>
        PENDING
        BACKORDERED
        PROCESSED
        PAID
    }
    class OrderLine {
        -quantity: int
        +subtotal() float
    }
    class Item {
        <<abstract>>
        #item_id: int
        #title: str
        #artist: str
        #price: float
        #stock: int
        +is_available(quantity: int) bool
    }
    class CD {
        -nb_tracks: int
    }
    class Tape {
        -duration_min: int
    }
    class Invoice {
        -invoice_id: int
        -amount: float
        +print() None
    }
    class ShippingList {
        -address: str
        +print() None
    }
    class Payment {
        <<abstract>>
        #amount: float
        #date: date
        +process()* bool
    }
    class Cash {
        +process() bool
    }
    class Check {
        -check_number: str
        +process() bool
    }
    class BankDraft {
        -draft_number: str
        +process() bool
    }
    class MembershipApplication {
        -applicant_name: str
        -sent_on: date
        +send() None
    }
    class OrderProcessingClerk {
        +verify_membership(name: str) bool
        +process_order(order: Order) None
    }
    class CollectionDeptClerk {
        +collect_payment(payment: Payment) bool
    }
    class DailyRecordsFile {
        -date: date
        +save(order: Order) None
    }

    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft
    OrderStatus <-- Order

    Member "1" --> "*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "*" --> "1" Item : refers to
    Order "1" -- "1" Invoice : billed by
    Order "1" -- "1" ShippingList : shipped with
    Order "1" -- "0..*" Payment : paid by
    OrderProcessingClerk "1" --> "*" Order : processes
    OrderProcessingClerk ..> MembershipApplication : sends
    CollectionDeptClerk "1" --> "*" Payment : collects
    DailyRecordsFile "1" o-- "*" Order : records
```

**Choices**
- `Order ◆— OrderLine`: **composition**, an order line has no meaning without its order.
- `DailyRecordsFile ◇— Order`: **aggregation**, the file lists orders but does not own them.
- `OrderLine → Item`: a plain association, the item exists in the catalogue independently.
- Inheritance for members, items and payments, as the exercise asks.

### Scenario: a Royal member orders 2 CDs (one unavailable) and pays by check

```mermaid
sequenceDiagram
    actor R as RoyalMember
    participant O as Order
    participant C as OrderProcessingClerk
    participant CD1 as cd1: CD
    participant CD2 as cd2: CD
    participant K as Check
    participant CC as CollectionDeptClerk
    participant F as DailyRecordsFile

    R->>+O: place_order([cd1, cd2])
    O->>+C: verify_membership(R)
    C-->>-O: True
    O->>+CD1: is_available(1)
    CD1-->>-O: True
    O->>+CD2: is_available(1)
    CD2-->>-O: False
    O->>R: cd2 unavailable
    R->>O: order_unavailable(cd2)
    O->>O: status = BACKORDERED for cd2
    O->>O: apply Royal discount
    O-->>-R: total
    R->>+K: create Check(total)
    K-->>-R: check
    R->>+CC: collect_payment(check)
    CC->>K: process()
    CC-->>-R: payment confirmed
    C->>C: process_order(order)
    C->>F: save(order)
```

---

## Level 3: advanced sequence diagrams

### 1. Complete order processing flow

```mermaid
sequenceDiagram
    actor M as Member
    participant S as System
    actor C as OrderProcessingClerk
    participant F as DailyRecordsFile
    M->>+S: place_order(lines)
    S->>C: new order to process
    C->>+S: verify_membership(M)
    S-->>-C: valid
    loop for each order line
        C->>S: is_available(item, quantity)
        S-->>C: True / False
    end
    C->>S: apply_discount(member)
    C->>S: print_invoice(order)
    C->>S: print_shipping_list(order)
    C->>F: save(order)
    S-->>-M: confirmation + invoice
```

### 2. Membership verification (success and failure)

```mermaid
sequenceDiagram
    actor P as Person
    participant S as System
    actor C as OrderProcessingClerk
    P->>+S: place_order(lines)
    S->>+C: verify_membership(P)
    alt is a member
        C-->>S: valid
        S-->>P: order accepted
    else not a member
        C-->>-S: invalid
        S->>S: create MembershipApplication
        S-->>-P: order refused + membership application form
    end
```

### 3. Payment processing (all types)

```mermaid
sequenceDiagram
    actor M as Member
    actor CC as CollectionDeptClerk
    participant P as Payment
    participant O as Order
    M->>+CC: pay(order, method)
    alt cash
        CC->>P: Cash(amount).process()
    else check
        CC->>P: Check(amount, number).process()
    else bank draft
        CC->>P: BankDraft(amount, number).process()
    end
    P-->>CC: True / False
    opt payment accepted
        CC->>O: status = PAID
    end
    CC-->>-M: receipt or refusal
```

### 4. Item reordering for Royal members

```mermaid
sequenceDiagram
    actor R as RoyalMember
    participant S as System
    actor C as OrderProcessingClerk
    participant Sup as Supplier
    R->>+S: order_unavailable(item)
    S->>S: check member is Royal
    alt Royal member
        S->>C: create back-order (priority)
        C->>Sup: reorder(item)
        Sup-->>C: delivery date
        C-->>S: back-order confirmed
        S-->>R: item reserved, expected delivery date
    else Regular member
        S-->>-R: refused: only Royal members can order unavailable items
    end
```
