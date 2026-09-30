# Research: team-chat

## Project definition

Implement the storage core for a 30-user local team-chat prototype: durable message history, room-scoped ordered reads, nonempty room/sender/body, body limit 2000 characters and read limit 100. This is not an exposed chat server or Discord clone.

## Assumptions and research questions

This is a small educational subsystem with Python 3.11+ available. It is not a production-ready clone.
Question: What is the smallest mechanism that meets this bounded task?

## References

<!-- rfb:references:start -->
| ID | Reference | Why relevant | Mismatch | License / reuse |
| --- | --- | --- | --- | --- |
| REF-001 | [https://github.com/zulip/zulip](https://github.com/zulip/zulip) | Durable team-chat history and recipient locality | Much broader real-time product | INSPECTED · Apache-2.0 · PATTERN_ONLY |
| REF-002 | [https://github.com/tinode/chat](https://github.com/tinode/chat) | Chat product boundary comparison | Federation/mobile platform | INSPECTED · GPL-3.0-only · PATTERN_ONLY |
| REF-003 | [https://github.com/hack-chat/main](https://github.com/hack-chat/main) | Small chat counterexample | Ephemeral retention conflicts with our goal | DECLARED_ONLY · MIT · PATTERN_ONLY |
<!-- rfb:references:end -->

## Source index

<!-- rfb:sources:start -->
| ID / note | Primary source | Locator | Inspection |
| --- | --- | --- | --- |
| [SRC-001](sources/SRC-001.md) | [original](https://github.com/zulip/zulip/blob/9778ffc23c3e83e321152a48ab32c1426e1bd941/docs/overview/architecture-overview.md) | 9778ffc23c3e83e321152a48ab32c1426e1bd941 · docs/overview/architecture-overview.md · Components: PostgreSQL; Django and Tornado; RabbitMQ | INSPECTED |
| [SRC-002](sources/SRC-002.md) | [original](https://github.com/zulip/zulip/blob/9778ffc23c3e83e321152a48ab32c1426e1bd941/zerver/models/messages.py) | 9778ffc23c3e83e321152a48ab32c1426e1bd941 · zerver/models/messages.py · AbstractMessage.recipient and Message.Meta indexes (lines 25-38, 190-208) | INSPECTED |
| [SRC-003](sources/SRC-003.md) | [original](https://github.com/tinode/chat/blob/eb90ef83acae6542f52719377ee5a76d267a5618/README.md) | eb90ef83acae6542f52719377ee5a76d267a5618 · README.md · Why? | INSPECTED |
| [SRC-004](sources/SRC-004.md) | [original](https://github.com/hack-chat/main/blob/e5a50c83bb043bedea1455e26c3baf33370686ea/README.md) | e5a50c83bb043bedea1455e26c3baf33370686ea · README.md · Opening product description | INSPECTED |
<!-- rfb:sources:end -->

## Evidence

<!-- rfb:evidence:start -->
| ID | Claim | Class | Sources / premises | Scope |
| --- | --- | --- | --- | --- |
| EV-001 | Zulip documents PostgreSQL for persistent data. | VERIFIED · documented | [SRC-001](sources/SRC-001.md) | Documented Zulip storage, not a prescription for our MVP. |
| EV-002 | Zulip's Message model has a recipient field and recipient-related indexes. | VERIFIED · implementation | [SRC-002](sources/SRC-002.md) | This model/file only; not the whole authorization pipeline. |
| EV-003 | Tinode describes federation as a project goal. | VERIFIED · documented | [SRC-003](sources/SRC-003.md) | Documented product goal, not verified interoperability. |
| EV-004 | hack.chat describes itself as logless and disappearing chat. | VERIFIED · documented | [SRC-004](sources/SRC-004.md) | Documented behavior, not personally observed retention. |
| EV-005 | A single local SQLite store fits this educational durable-history scope. | INFERENCE | EV-001, EV-002, EV-004 | Our constrained design; no assertion that the references use SQLite. |
| EV-006 | Zulip documents long-lived delivery and expensive background work as distinct roles. | VERIFIED · documented | [SRC-001](sources/SRC-001.md) | These roles exist in the documented Zulip deployment; our task excludes them. |
<!-- rfb:evidence:end -->

## Cross-project comparison

| Area | Zulip | Tinode | hack.chat | Our choice |
| --- | --- | --- | --- | --- |
| Retention | Durable data (EV-001) | Broader messaging platform | Logless (EV-004) | Local SQLite, inferred and tested |
| Scope | Push/jobs (EV-006) | Federation goal (EV-003) | Minimal chat | Storage core only |

## Adopted, rejected and deferred patterns

<!-- rfb:decisions:start -->
| ID | Choice | Outcome | Evidence | Reason / complexity | Revisit |
| --- | --- | --- | --- | --- | --- |
| DEC-001 | One SQLite durable message table | ADOPT | EV-005 | Durability is required; one process/file is enough. Complexity: One embedded database, no service | Sustained concurrent writer demand |
| DEC-002 | Room-scoped ordered query with bounded input | ADOPT | EV-002, EV-005 | Recipient locality informs our simpler room boundary. Complexity: One composite index and validation | Search/product requirements expand |
| DEC-003 | Logless ephemeral retention | REJECT | EV-004 | Conflicts with explicit durable history. Complexity: Simple but loses required history | User explicitly requests ephemeral chat |
| DEC-004 | Federation protocol | REJECT | EV-003 | No cross-server communication is requested. Complexity: Protocol/identity/operations complexity | Federated product requirement |
| DEC-005 | Separate delivery/background infrastructure | DEFER | EV-006 | This slice implements storage, not push or notification jobs. Complexity: Extra processes, queues and monitoring | Measured push/job workload |
<!-- rfb:decisions:end -->

### Rejected patterns

The REJECT/DEFER records above describe actual candidates considered, with concrete scope mismatches.

## Risks, licenses and unknowns

Repository licenses were inspected at the recorded revisions where fetched. Documentation-only rights may remain
unknown; all interactions are PATTERN_ONLY, with no code/text transfer. Source notes paraphrase narrow findings.
No repository runtime, security certification or commercial-success causal claim was tested.
