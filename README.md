# python-itertools-label-grouping-lab

Tiny deterministic correctness lab for `itertools.groupby` label grouping.

Hacker News thread: https://news.ycombinator.com/item?id=41450824 — "Lesser known parts of Python standard library"

## Cases

Four deterministic cases on a fixed six-record dataset (`c1/cat, c2/cat, d1/dog, c3/cat, d2/dog, d3/dog`):

1. **`contiguous_label_runs_marker`** — Labels `cat, cat, dog, cat`. `groupby` produces keys `cat, dog, cat` with sizes `2, 1, 1`. The two `cat` runs are not merged.

2. **`unsorted_repeated_labels_marker`** — Both `cat` and `dog` appear in multiple runs. Raw `groupby` produces multiple groups per label — not global aggregation.

3. **`sorted_global_grouping_marker`** — Stably sort by label, then `groupby`. Each label appears exactly once, and original relative order within each label is preserved (`c1,c2,c3` / `d1,d2,d3`).

4. **`shared_group_iterator_marker`** — Delayed consumption of the first group after advancing the outer iterator no longer yields the original records. Early materialization with `list(group)` preserves them.

## Methods

All three methods run for every case (12 rows total):

- `inspect_inputs` — required fields, label sequence, record count, run structure, stable sort verification
- `execute_groupby` — group count, keys, sizes, collected names
- `verify_relation` — check observed behavior matches documented `itertools.groupby` semantics

## Results

| case | method | passed |
|------|--------|--------|
| contiguous_label_runs_marker | inspect_inputs | true |
| contiguous_label_runs_marker | execute_groupby | true |
| contiguous_label_runs_marker | verify_relation | true |
| unsorted_repeated_labels_marker | inspect_inputs | true |
| unsorted_repeated_labels_marker | execute_groupby | true |
| unsorted_repeated_labels_marker | verify_relation | true |
| sorted_global_grouping_marker | inspect_inputs | true |
| sorted_global_grouping_marker | execute_groupby | true |
| sorted_global_grouping_marker | verify_relation | true |
| shared_group_iterator_marker | inspect_inputs | true |
| shared_group_iterator_marker | execute_groupby | true |
| shared_group_iterator_marker | verify_relation | true |

12 / 12 passed.

## Running

```bash
python3 run_lab.py          # generates observations.json and RESULTS.md
python3 -m unittest test_lab -v
```

## Files

- `run_lab.py` — lab runner, 4 cases × 3 methods
- `test_lab.py` — unittest verification
- `observations.json` — twelve-row result table
- `RESULTS.md` — human-readable results
- `hn_evidence.md` / `hn_evidence.jsonl` — HN thread evidence
- `hn_story_41450824.json` — raw HN story JSON

## Limitations

- `itertools.groupby` does not perform global label aggregation — it groups consecutive runs only.
- Sorting before `groupby` is not always appropriate for ML pipelines.
- This lab does not prove batching correctness or measure performance.
- Materializing every group is not always memory-efficient.
