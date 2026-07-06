Instructions
Your task is to implement a simplified version of a task management system. It consists of four progressive levels, with each level introducing new features or constraints.

Solving this task consists of several levels. Subsequent levels are opened when the current level is correctly solved. You always have access to the data for the current and all previous levels.

You are not required to provide the most efficient implementation. Any code that passes the unit tests is sufficient.

You can execute a single test case by running the following command in the terminal: bash run_single_test.sh "<test_case_name>".

Requirements
Plan your design according to the level specifications below:

Level 1: Implement basic operations to add, update, and retrieve tasks.
Level 2: Add functionality to search and sort tasks based on priority and creation order.
Level 3: Introduce users, time-based task assignment with TTL expiration, and dynamic quota management.
Level 4: Add task completion tracking and historical analysis to identify overdue assignments that expired without completion.
Note

All priority (introduced in Level 1) and quota (introduced in Level 3) values provided in the tests will be non-negative integers (>= 0).
All timestamp (introduced in Level 3) and finish_time (introduced in Level 3) values will be positive integers representing seconds since the system started.
Time always flows forward, so timestamps are guaranteed to strictly increase as operations are executed.
Level 1
Implement basic task management operations.

add_task(self, timestamp: int, name: str, priority: int) -> str — Adds a new task with the given name and priority. Returns the unique task ID in the format "task_id_N" where N is a sequential number. Task IDs are sequentially generated, starting from "task_id_1". Adding a task with the same name and priority as an existing task is allowed; each task is differentiated by a unique ID. The priority parameter is a non-negative integer (>= 0). The timestamp parameter is unused in Level 1 logic but included for API consistency.

update_task(self, timestamp: int, task_id: str, name: str, priority: int) -> bool — Updates the name and priority of the task identified by task_id. Returns True if the update is successful, or False if task_id does not exist.

get_task(self, timestamp: int, task_id: str) -> str | None — Retrieves a task by task_id. Returns a string representing the task details (name and priority) in JSON format if the task exists, or None if the task does not exist. The JSON string must be compact. No whitespace should be added between keys and values, but whitespace within string values (e.g., in name) must be preserved. Keys must be ordered: first name, then priority. Tip: You do not need a JSON library. You can manually construct the string.

Examples
The following table demonstrates how these operations should work:

Queries:
add_task(1, "Task 1", 5)
add_task(2, "Task 1", 5)
update_task(3, "task_id_1", "Updated Task 1", 4)
get_task(4, "task_id_1")
get_task(5, "task_id_3")
update_task(6, "task_id_3", "Non-existing Task", 1)

Explanations
returns "task_id_1"
returns "task_id_2"; successfully adds another task with the same name and priority
returns True; "task_id_1" is updated
returns '{"name":"Updated Task 1","priority":4}'; note: no spaces
returns None; "task_id_3" does not exist
returns False; "task_id_3" does not exist