# First run: every decision escalated

Before the escalation fix, the first full run covered TC-01 to TC-08. **All 17 decisions said "a person must check this".**
The raw outputs are `runs/TC-01_run2.json` to `runs/TC-08_run2.json`. They were committed before the fix
(repository commits `716694c` to `b1d09a6`, fix in `2d5a10d`). The cause and the fix are in `RESULTS.md`.

| Case | Country | Hours given | Sent to a person | First reason given |
|---|---|---|---|---|
| TC-01 | UK | On the service described in the observations (free-to-air satellite,... | yes | The operative unsuitability finding rests on judgment_based rules: UK-SCH-001, UK-VIO-001, UK-DEF-002,... |
| TC-02 | UK | Not before 21:00 (and not after 05:30). No specific slot is cleared,... | yes | The decision rests on judgment_based rules: UK-SCH-001, UK-VIO-001, UK-VIO-002, UK-DEF-002, UK-DEF-003,... |
| TC-02 | FR | On the provisional category III (-12) classification: not before... | yes | The classification is not settled and I decline to pick one. Category III (-12) is the floor on the... |
| TC-03 | UK | Any time of day, INCLUDING the recorded 14:30 Wednesday slot - but... | yes | The entire daytime permission rests on the access control, and two of the four MDP conditions are... |
| TC-03 | FR | CANNOT BE DETERMINED FROM THIS RULE SLICE, and I will not supply a... | yes | The rows carrying the category III and category IV broadcast windows are absent from this rule slice for... |
| TC-04 | UK | 22:15 is permitted on the hours axis - it falls inside the... | yes | UK-SCH-008 is engaged on the facts: the strongest material (the werewolf transformation in sustained... |
| TC-04 | UK | Not before 21:00 as currently cut, absent mandatory daytime... | yes | The surrounding programme at 15:00 and the age profile of its audience are not_stated, and UK-TRL-003 turns... |
| TC-04 | FR | 22:15 is permitted on every branch considered, on either candidate... | yes | FR-CLS-003 is judgment_based and carries human_review_required = yes in the table. Whether the work is... |
| TC-04 | FR | No French rule in the provided slice bars this trailer from 15:00 on... | yes | The decisive question - whether the decayed faces (o9) and the faster-cut pursuit (o10) are 'scenes likely to... |
| TC-05 | UK | Cannot be resolved as described. Branch (A) free-to-air / general... | yes | The description contradicts itself and the conflict is unresolved: the distributor summary states 'suitable... |
| TC-05 | FR | Cannot be resolved as described, and the obstacle is twofold: the... | yes | FR-PRO-001 (offence to human dignity) is a live question, not a cleared one. o2 is the body of a real... |
| TC-06 | UK | Not before 21:00 on this free-to-air transmission. | yes | The extractor states it cannot tell whether the single listed event is the complete event list for the asset... |
| TC-06 | FR | Cannot be stated as a single time, because the category is unresolved... | yes | The classification is unresolved between III (-12) and IV (-16), and in France the hour follows the category.... |
| TC-07 | UK | Not fully resolved, and the honest shape of the answer is asymmetric.... | yes | The pre-watershed question is genuinely open and finely balanced, and it is the question the broadcaster will... |
| TC-07 | FR | Depends on the category, and on the provisional category the answer... | yes | The classification is unresolved between I (tous publics) and II (-10), and that step is the whole decision:... |
| TC-08 | UK | Provisionally permitted at 14:30, on the view that a post-coital... | yes | The decision turns on a fact the record does not contain: whether the dialogue in the 00:11:40 scene refers... |
| TC-08 | UK | Provisionally permitted at 15:30, on the same provisional view of... | yes | The 15:30 start time is DERIVED from the '+1' label and is not stated in the source. The whole transmission... |

**17 of 17 sent to a person.**

The reviewer's finding that the cookery show (TC-09) was also escalated comes from a run that was not saved,
so it is not in this table. The saved `runs/TC-09_run2.json` is from after the fix and comes back clear.
