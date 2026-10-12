# PA 5 — Retrospective

## 1. Plan Mode Value

In Session 1, Plan Mode helped me catch a problem before Claude started changing my code. Claude originally wanted to put priority validation directly in `repositories/tasks.py`, but my project is supposed to keep validation in the service layer. I asked Claude to change the plan so the repository would only handle storing task data, while validation would be added to `services/tasks.py` in the next session. This saved me from having to move the validation code later. After making the change to the plan, the implementation worked, and all 10 tests passed.

## 2. Plan Mode Limits

One thing I learned from Plan Mode is that reviewing a plan doesn't mean Claude will always follow it perfectly. However, in my four sessions, I didn't find a case where Claude's final code went against an approved plan. In Session 3, Claude changed where `DEFAULT_PRIORITY` was imported from so the route would only depend on the service layer. At first, I thought this might count as a difference, but after reviewing it, the change actually followed my amendment. By the end of Session 4, all 61 tests passed. This showed me that even when Plan Mode works, I still need to check the actual code instead of just trusting the plan or the test results.

## 3. Subagent Value

I think the most important boundary was keeping the service layer separate from the route layer. In SA-2, Claude added notification preference validation to `services/users.py`, while SA-3 only created the route functions in `routes/users.py`. This kept the code organized because the routes didn't need to handle validation themselves. If I had done everything in one session, Claude might have mixed these responsibilities together, making the code harder to review. Breaking the work into separate sessions also made it easier to identify problems, like the incorrect `notification_preference` field name and the missing user-list function that SA-4 found.

## 4. Gap Analysis

The rule I would most want to enforce automatically is that route files should never contain business logic or access repository functions directly. Even though Claude followed this rule during my subagent sessions, I don't want to depend on it always remembering the instruction. A hook could check changes made to files inside `routes/` and reject edits that import directly from `repositories/`. This would make the boundary easier to enforce without having to catch every mistake manually.