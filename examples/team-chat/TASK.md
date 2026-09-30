# Task

Implement the storage core for a 30-user local team-chat prototype: durable message history, room-scoped ordered reads, nonempty room/sender/body, body limit 2000 characters and read limit 100. This is not an exposed chat server or Discord clone.

Constraints: Python stdlib; one process/local database; 30-user product context.

Non-goals: HTTP/UI; authentication; federation; push delivery.

Acceptance: Reopen persistence, room isolation/order, Unicode/SQL-like text, empty/oversized input, bounded history.
