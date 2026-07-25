#!/usr/bin/env python3
"""python-itertools-label-grouping-lab

Four deterministic correctness cases for itertools.groupby label grouping.
"""
import itertools
import json

# Fixed six-record dataset: c1/cat, c2/cat, d1/dog, c3/cat, d2/dog, d3/dog
DATASET_ALL = [
    {"name": "c1", "label": "cat"},
    {"name": "c2", "label": "cat"},
    {"name": "d1", "label": "dog"},
    {"name": "c3", "label": "cat"},
    {"name": "d2", "label": "dog"},
    {"name": "d3", "label": "dog"},
]
DATASET_CONTIGUOUS = DATASET_ALL[:4]  # c1/cat, c2/cat, d1/dog, c3/cat


# ---------------------------------------------------------------------------
# Case 1: contiguous_label_runs_marker
# ---------------------------------------------------------------------------

def case1_contiguous_inspect(records=None):
    records = records if records is not None else DATASET_CONTIGUOUS
    # Invariant checks
    has_required_fields = all("name" in r and "label" in r for r in records)
    expected_labels = ["cat", "cat", "dog", "cat"]
    actual_labels = [r.get("label") for r in records] if has_required_fields else []
    label_sequence_ok = has_required_fields and actual_labels == expected_labels
    record_count_ok = len(records) == 4
    # Repeated labels occur in separate contiguous runs
    if has_required_fields:
        runs = [(k, len(list(g))) for k, g in itertools.groupby(actual_labels)]
        run_keys = [k for k, _ in runs]
    else:
        runs = []
        run_keys = []
    repeated_in_separate_runs = run_keys == ["cat", "dog", "cat"]
    passed = all([has_required_fields, label_sequence_ok, record_count_ok, repeated_in_separate_runs])
    return {
        "passed": passed,
        "detail": {
            "has_required_fields": has_required_fields,
            "label_sequence": actual_labels,
            "label_sequence_ok": label_sequence_ok,
            "record_count": len(records),
            "record_count_ok": record_count_ok,
            "run_keys": run_keys,
            "repeated_in_separate_runs": repeated_in_separate_runs,
        }
    }


def case1_contiguous_execute(records=None):
    records = records if records is not None else DATASET_CONTIGUOUS
    grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
    keys = [k for k, _ in grouped]
    sizes = [len(g) for _, g in grouped]
    names = [[r["name"] for r in g] for _, g in grouped]
    expected_keys = ["cat", "dog", "cat"]
    expected_sizes = [2, 1, 1]
    passed = (keys == expected_keys and sizes == expected_sizes and len(grouped) == 3)
    return {
        "passed": passed,
        "detail": {
            "group_count": len(grouped),
            "keys": keys,
            "sizes": sizes,
            "names": names,
            "keys_match": keys == expected_keys,
            "sizes_match": sizes == expected_sizes,
        }
    }


def case1_contiguous_verify(records=None):
    records = records if records is not None else DATASET_CONTIGUOUS
    grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
    keys = [k for k, _ in grouped]
    sizes = [len(g) for _, g in grouped]
    # Relation: contiguous keys cat, dog, cat with sizes 2, 1, 1; do NOT merge the two cat runs
    keys_ok = keys == ["cat", "dog", "cat"]
    sizes_ok = sizes == [2, 1, 1]
    cat_runs_not_merged = keys.count("cat") == 2
    passed = keys_ok and sizes_ok and cat_runs_not_merged
    return {
        "passed": passed,
        "detail": {
            "keys": keys,
            "sizes": sizes,
            "keys_ok": keys_ok,
            "sizes_ok": sizes_ok,
            "cat_runs_not_merged": cat_runs_not_merged,
        }
    }


# ---------------------------------------------------------------------------
# Case 2: unsorted_repeated_labels_marker
# ---------------------------------------------------------------------------

def case2_unsorted_inspect(records=None):
    records = records if records is not None else DATASET_ALL
    has_required_fields = all("name" in r and "label" in r for r in records)
    expected_labels = ["cat", "cat", "dog", "cat", "dog", "dog"]
    actual_labels = [r.get("label") for r in records] if has_required_fields else []
    label_sequence_ok = has_required_fields and actual_labels == expected_labels
    record_count_ok = len(records) == 6
    # Both cat and dog appear in more than one run
    if has_required_fields:
        runs = [(k, len(list(g))) for k, g in itertools.groupby(actual_labels)]
        run_keys = [k for k, _ in runs]
    else:
        runs = []
        run_keys = []
    cat_runs = run_keys.count("cat")
    dog_runs = run_keys.count("dog")
    repeated_labels_separate_runs = cat_runs >= 2 and dog_runs >= 2
    passed = all([has_required_fields, label_sequence_ok, record_count_ok, repeated_labels_separate_runs])
    return {
        "passed": passed,
        "detail": {
            "has_required_fields": has_required_fields,
            "label_sequence": actual_labels,
            "label_sequence_ok": label_sequence_ok,
            "record_count": len(records),
            "record_count_ok": record_count_ok,
            "run_keys": run_keys,
            "cat_runs": cat_runs,
            "dog_runs": dog_runs,
            "repeated_labels_separate_runs": repeated_labels_separate_runs,
        }
    }


def case2_unsorted_execute(records=None):
    records = records if records is not None else DATASET_ALL
    grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
    keys = [k for k, _ in grouped]
    sizes = [len(g) for _, g in grouped]
    names = [[r["name"] for r in g] for _, g in grouped]
    # Observable structure
    group_count_ok = len(grouped) == 4
    keys_ok = keys == ["cat", "dog", "cat", "dog"]
    sizes_ok = sizes == [2, 1, 1, 2]
    passed = group_count_ok and keys_ok and sizes_ok
    return {
        "passed": passed,
        "detail": {
            "group_count": len(grouped),
            "keys": keys,
            "sizes": sizes,
            "names": names,
            "group_count_ok": group_count_ok,
            "keys_match": keys_ok,
            "sizes_match": sizes_ok,
        }
    }


def case2_unsorted_verify(records=None):
    records = records if records is not None else DATASET_ALL
    grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
    keys = [k for k, _ in grouped]
    # Relation: raw groupby produces multiple groups for the same label; not global aggregation
    cat_group_count = keys.count("cat")
    dog_group_count = keys.count("dog")
    repeated_cat_groups = cat_group_count >= 2
    repeated_dog_groups = dog_group_count >= 2
    not_global_aggregation = repeated_cat_groups and repeated_dog_groups
    unique_labels = set(r["label"] for r in records)
    group_count_exceeds_unique_labels = len(keys) > len(unique_labels)
    passed = not_global_aggregation and group_count_exceeds_unique_labels
    return {
        "passed": passed,
        "detail": {
            "keys": keys,
            "cat_group_count": cat_group_count,
            "dog_group_count": dog_group_count,
            "repeated_cat_groups": repeated_cat_groups,
            "repeated_dog_groups": repeated_dog_groups,
            "not_global_aggregation": not_global_aggregation,
            "unique_labels": sorted(unique_labels),
            "group_count_exceeds_unique_labels": group_count_exceeds_unique_labels,
        }
    }


# ---------------------------------------------------------------------------
# Case 3: sorted_global_grouping_marker
# ---------------------------------------------------------------------------

def case3_sorted_inspect(records=None):
    records = records if records is not None else DATASET_ALL
    has_required_fields = all("name" in r and "label" in r for r in records)
    expected_labels = ["cat", "cat", "dog", "cat", "dog", "dog"]
    actual_labels = [r.get("label") for r in records] if has_required_fields else []
    label_sequence_ok = has_required_fields and actual_labels == expected_labels
    record_count_ok = len(records) == 6
    # Stable sort by label
    if has_required_fields:
        sorted_records = sorted(records, key=lambda r: r["label"])
        sorted_labels = [r["label"] for r in sorted_records]
        cat_names_sorted = [r["name"] for r in sorted_records if r["label"] == "cat"]
        dog_names_sorted = [r["name"] for r in sorted_records if r["label"] == "dog"]
    else:
        sorted_records = []
        sorted_labels = []
        cat_names_sorted = []
        dog_names_sorted = []
    sorted_ok = sorted_labels == ["cat", "cat", "cat", "dog", "dog", "dog"]
    # Stable sort preserves original relative order within each label
    cat_order_preserved = cat_names_sorted == ["c1", "c2", "c3"]
    dog_order_preserved = dog_names_sorted == ["d1", "d2", "d3"]
    stable_sort_ok = cat_order_preserved and dog_order_preserved
    passed = all([has_required_fields, label_sequence_ok, record_count_ok, sorted_ok, stable_sort_ok])
    return {
        "passed": passed,
        "detail": {
            "has_required_fields": has_required_fields,
            "label_sequence": actual_labels,
            "label_sequence_ok": label_sequence_ok,
            "record_count": len(records),
            "record_count_ok": record_count_ok,
            "sorted_labels": sorted_labels,
            "sorted_ok": sorted_ok,
            "cat_names_sorted": cat_names_sorted,
            "dog_names_sorted": dog_names_sorted,
            "cat_order_preserved": cat_order_preserved,
            "dog_order_preserved": dog_order_preserved,
            "stable_sort_ok": stable_sort_ok,
        }
    }


def case3_sorted_execute(records=None):
    records = records if records is not None else DATASET_ALL
    sorted_records = sorted(records, key=lambda r: r["label"])
    grouped = [(k, list(g)) for k, g in itertools.groupby(sorted_records, key=lambda r: r["label"])]
    keys = [k for k, _ in grouped]
    sizes = [len(g) for _, g in grouped]
    names = [[r["name"] for r in g] for _, g in grouped]
    group_count_ok = len(grouped) == 2
    keys_ok = keys == ["cat", "dog"]
    sizes_ok = sizes == [3, 3]
    passed = group_count_ok and keys_ok and sizes_ok
    return {
        "passed": passed,
        "detail": {
            "group_count": len(grouped),
            "keys": keys,
            "sizes": sizes,
            "names": names,
            "group_count_ok": group_count_ok,
            "keys_match": keys_ok,
            "sizes_match": sizes_ok,
        }
    }


def case3_sorted_verify(records=None):
    records = records if records is not None else DATASET_ALL
    sorted_records = sorted(records, key=lambda r: r["label"])
    grouped = [(k, list(g)) for k, g in itertools.groupby(sorted_records, key=lambda r: r["label"])]
    keys = [k for k, _ in grouped]
    names_per_group = [[r["name"] for r in g] for _, g in grouped]
    # Relation: each label appears exactly once
    cat_occurrences = keys.count("cat")
    dog_occurrences = keys.count("dog")
    each_label_once = cat_occurrences == 1 and dog_occurrences == 1
    # Original relative order within each label is preserved
    cat_names = names_per_group[keys.index("cat")] if "cat" in keys else []
    dog_names = names_per_group[keys.index("dog")] if "dog" in keys else []
    cat_order_ok = cat_names == ["c1", "c2", "c3"]
    dog_order_ok = dog_names == ["d1", "d2", "d3"]
    order_preserved = cat_order_ok and dog_order_ok
    passed = each_label_once and order_preserved
    return {
        "passed": passed,
        "detail": {
            "keys": keys,
            "cat_occurrences": cat_occurrences,
            "dog_occurrences": dog_occurrences,
            "each_label_once": each_label_once,
            "cat_names": cat_names,
            "dog_names": dog_names,
            "cat_order_ok": cat_order_ok,
            "dog_order_ok": dog_order_ok,
            "order_preserved": order_preserved,
        }
    }


# ---------------------------------------------------------------------------
# Case 4: shared_group_iterator_marker
# ---------------------------------------------------------------------------

def case4_shared_iter_inspect(records=None):
    records = records if records is not None else DATASET_ALL
    has_required_fields = all("name" in r and "label" in r for r in records)
    expected_labels = ["cat", "cat", "dog", "cat", "dog", "dog"]
    actual_labels = [r.get("label") for r in records] if has_required_fields else []
    label_sequence_ok = has_required_fields and actual_labels == expected_labels
    record_count_ok = len(records) == 6
    # Repeated labels in separate runs (needed for iterator sharing demo)
    if has_required_fields:
        runs = [(k, len(list(g))) for k, g in itertools.groupby(actual_labels)]
        run_keys = [k for k, _ in runs]
    else:
        run_keys = []
    repeated_labels_separate_runs = run_keys.count("cat") >= 2 and run_keys.count("dog") >= 2
    passed = all([has_required_fields, label_sequence_ok, record_count_ok, repeated_labels_separate_runs])
    return {
        "passed": passed,
        "detail": {
            "has_required_fields": has_required_fields,
            "label_sequence": actual_labels,
            "label_sequence_ok": label_sequence_ok,
            "record_count": len(records),
            "record_count_ok": record_count_ok,
            "run_keys": run_keys,
            "repeated_labels_separate_runs": repeated_labels_separate_runs,
        }
    }


def case4_shared_iter_execute(records=None):
    records = records if records is not None else DATASET_ALL
    # Path A: delayed consumption – advance outer iterator before consuming first group
    gb_a = itertools.groupby(records, key=lambda r: r["label"])
    key_a, group_a = next(gb_a)
    # Advance outer iterator, discarding the rest of group_a
    try:
        key_a2, group_a2 = next(gb_a)
        outer_advanced = True
    except StopIteration:
        outer_advanced = False
        key_a2 = None
    # Now try delayed consumption
    delayed_records = list(group_a)
    delayed_names = [r["name"] for r in delayed_records]
    # Path B: early materialization – consume first group before advancing
    gb_b = itertools.groupby(records, key=lambda r: r["label"])
    key_b, group_b = next(gb_b)
    materialized_records = list(group_b)
    materialized_names = [r["name"] for r in materialized_records]
    # Advance after materializing
    try:
        key_b2, group_b2 = next(gb_b)
        outer_advanced_b = True
    except StopIteration:
        outer_advanced_b = False
    passed = outer_advanced and outer_advanced_b
    return {
        "passed": passed,
        "detail": {
            "delayed_path": {
                "first_key": key_a,
                "advanced_outer": outer_advanced,
                "next_key": key_a2,
                "delayed_names": delayed_names,
                "delayed_count": len(delayed_names),
            },
            "materialized_path": {
                "first_key": key_b,
                "materialized_names": materialized_names,
                "materialized_count": len(materialized_names),
                "advanced_outer": outer_advanced_b,
            },
        }
    }


def case4_shared_iter_verify(records=None):
    records = records if records is not None else DATASET_ALL
    # Path A: delayed
    gb_a = itertools.groupby(records, key=lambda r: r["label"])
    key_a, group_a = next(gb_a)
    try:
        next(gb_a)
        outer_advanced_a = True
    except StopIteration:
        outer_advanced_a = False
    delayed = list(group_a)
    delayed_names = [r["name"] for r in delayed]
    # Path B: materialized
    gb_b = itertools.groupby(records, key=lambda r: r["label"])
    key_b, group_b = next(gb_b)
    materialized = list(group_b)
    materialized_names = [r["name"] for r in materialized]
    next(gb_b, None)
    # Relations
    # Delayed consumption no longer yields original first-group records
    # First group is c1, c2 – after advancing, delayed consumption should be empty / not yield c1,c2
    delayed_lost_original = delayed_names != ["c1", "c2"]
    # Early materialization preserves ["c1", "c2"]
    materialization_preserved = materialized_names == ["c1", "c2"]
    passed = delayed_lost_original and materialization_preserved and outer_advanced_a
    return {
        "passed": passed,
        "detail": {
            "delayed_names": delayed_names,
            "expected_first_group": ["c1", "c2"],
            "delayed_lost_original": delayed_lost_original,
            "materialized_names": materialized_names,
            "materialization_preserved": materialization_preserved,
            "outer_advanced": outer_advanced_a,
        }
    }


# ---------------------------------------------------------------------------
# Lab runner
# ---------------------------------------------------------------------------

CASES = [
    ("contiguous_label_runs_marker", case1_contiguous_inspect, case1_contiguous_execute, case1_contiguous_verify),
    ("unsorted_repeated_labels_marker", case2_unsorted_inspect, case2_unsorted_execute, case2_unsorted_verify),
    ("sorted_global_grouping_marker", case3_sorted_inspect, case3_sorted_execute, case3_sorted_verify),
    ("shared_group_iterator_marker", case4_shared_iter_inspect, case4_shared_iter_execute, case4_shared_iter_verify),
]

METHODS = [
    ("inspect_inputs", 1),
    ("execute_groupby", 2),
    ("verify_relation", 2),
]


def run_all():
    rows = []
    for case_name, inspect_fn, execute_fn, verify_fn in CASES:
        fns = {
            "inspect_inputs": inspect_fn,
            "execute_groupby": execute_fn,
            "verify_relation": verify_fn,
        }
        for method_name, _ in METHODS:
            fn = fns[method_name]
            result = fn()
            passed = bool(result.get("passed", False))
            rows.append({
                "case": case_name,
                "method": method_name,
                "passed": passed,
                "detail": result.get("detail", {}),
            })
    return rows


if __name__ == "__main__":
    rows = run_all()
    # Write observations.json
    with open("observations.json", "w") as f:
        json.dump(rows, f, indent=2)
    # Generate RESULTS.md from same in-memory rows
    total = len(rows)
    passed = sum(1 for r in rows if r["passed"])
    failed = total - passed
    lines = [
        "# RESULTS",
        "",
        f"Total rows: {total}",
        f"Passed: {passed}",
        f"Failed: {failed}",
        "",
        "| case | method | passed |",
        "|------|--------|--------|",
    ]
    for r in rows:
        lines.append(f"| {r['case']} | {r['method']} | {str(r['passed']).lower()} |")
    lines.append("")
    with open("RESULTS.md", "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote observations.json and RESULTS.md – {passed}/{total} passed")
