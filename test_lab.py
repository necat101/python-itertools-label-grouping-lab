#!/usr/bin/env python3
"""test_lab.py — unittest verification for python-itertools-label-grouping-lab"""
import itertools
import json
import unittest

import run_lab


class TestLab(unittest.TestCase):

    def test_contiguous_keys(self):
        """contiguous keys ["cat", "dog", "cat"]"""
        records = run_lab.DATASET_CONTIGUOUS
        grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
        keys = [k for k, _ in grouped]
        self.assertEqual(keys, ["cat", "dog", "cat"])

    def test_contiguous_sizes(self):
        """contiguous sizes [2, 1, 1]"""
        records = run_lab.DATASET_CONTIGUOUS
        grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
        sizes = [len(g) for _, g in grouped]
        self.assertEqual(sizes, [2, 1, 1])

    def test_unsorted_repeated_group_keys(self):
        """raw grouping of all six records produces repeated cat and dog group keys"""
        records = run_lab.DATASET_ALL
        grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
        keys = [k for k, _ in grouped]
        self.assertEqual(keys, ["cat", "dog", "cat", "dog"])
        self.assertEqual(keys.count("cat"), 2)
        self.assertEqual(keys.count("dog"), 2)

    def test_unsorted_not_global_aggregation(self):
        """raw grouping is not global aggregation"""
        records = run_lab.DATASET_ALL
        grouped = [(k, list(g)) for k, g in itertools.groupby(records, key=lambda r: r["label"])]
        keys = [k for k, _ in grouped]
        unique_labels = set(r["label"] for r in records)
        # groupby produced more groups than unique labels → not global
        self.assertGreater(len(keys), len(unique_labels))
        self.assertEqual(len(unique_labels), 2)
        self.assertEqual(len(keys), 4)

    def test_sorted_one_group_per_label(self):
        """stable sorting produces one group per label"""
        records = run_lab.DATASET_ALL
        sorted_records = sorted(records, key=lambda r: r["label"])
        grouped = [(k, list(g)) for k, g in itertools.groupby(sorted_records, key=lambda r: r["label"])]
        keys = [k for k, _ in grouped]
        self.assertEqual(keys, ["cat", "dog"])
        self.assertEqual(keys.count("cat"), 1)
        self.assertEqual(keys.count("dog"), 1)

    def test_sorted_cat_names_preserved(self):
        """sorted cat names remain ["c1", "c2", "c3"]"""
        records = run_lab.DATASET_ALL
        sorted_records = sorted(records, key=lambda r: r["label"])
        grouped = [(k, list(g)) for k, g in itertools.groupby(sorted_records, key=lambda r: r["label"])]
        keys = [k for k, _ in grouped]
        cat_idx = keys.index("cat")
        cat_names = [r["name"] for r in grouped[cat_idx][1]]
        self.assertEqual(cat_names, ["c1", "c2", "c3"])

    def test_sorted_dog_names_preserved(self):
        """sorted dog names remain ["d1", "d2", "d3"]"""
        records = run_lab.DATASET_ALL
        sorted_records = sorted(records, key=lambda r: r["label"])
        grouped = [(k, list(g)) for k, g in itertools.groupby(sorted_records, key=lambda r: r["label"])]
        keys = [k for k, _ in grouped]
        dog_idx = keys.index("dog")
        dog_names = [r["name"] for r in grouped[dog_idx][1]]
        self.assertEqual(dog_names, ["d1", "d2", "d3"])

    def test_delayed_consumption_lost(self):
        """delayed first-group consumption is empty or otherwise no longer yields its original records after advancing the outer iterator"""
        records = run_lab.DATASET_ALL
        gb = itertools.groupby(records, key=lambda r: r["label"])
        key, group = next(gb)
        next(gb, None)  # advance outer
        delayed = list(group)
        delayed_names = [r["name"] for r in delayed]
        # Delayed consumption must NOT yield the original ["c1", "c2"]
        self.assertNotEqual(delayed_names, ["c1", "c2"])

    def test_early_materialization_preserves(self):
        """early materialization preserves ["c1", "c2"]"""
        records = run_lab.DATASET_ALL
        gb = itertools.groupby(records, key=lambda r: r["label"])
        key, group = next(gb)
        materialized = list(group)
        materialized_names = [r["name"] for r in materialized]
        next(gb, None)
        self.assertEqual(materialized_names, ["c1", "c2"])

    # Corruption tests – call actual production helpers
    def test_corrupt_case1_inspect(self):
        """all four production input inspectors reject deliberately corrupted inputs"""
        # Case 1: wrong label sequence
        bad = [{"name": "x", "label": "zzz"}]
        result = run_lab.case1_contiguous_inspect(bad)
        self.assertFalse(result["passed"])

    def test_corrupt_case2_inspect(self):
        bad = [{"name": "x"}]  # missing label field
        result = run_lab.case2_unsorted_inspect(bad)
        self.assertFalse(result["passed"])

    def test_corrupt_case3_inspect(self):
        # Empty list fails record_count check
        bad = []
        result = run_lab.case3_sorted_inspect(bad)
        self.assertFalse(result["passed"])

    def test_corrupt_case4_inspect(self):
        # Wrong label sequence
        bad = [{"name": "a", "label": "fish"}]
        result = run_lab.case4_shared_iter_inspect(bad)
        self.assertFalse(result["passed"])

    def test_twelve_rows_deterministic_unique_ordered(self):
        """the twelve rows are deterministic, unique, and in the required order"""
        rows1 = run_lab.run_all()
        rows2 = run_lab.run_all()
        # Deterministic
        self.assertEqual(rows1, rows2)
        # Twelve rows
        self.assertEqual(len(rows1), 12)
        # Unique (case, method) pairs
        pairs = [(r["case"], r["method"]) for r in rows1]
        self.assertEqual(len(pairs), len(set(pairs)))
        # Required order
        expected = [
            ("contiguous_label_runs_marker", "inspect_inputs"),
            ("contiguous_label_runs_marker", "execute_groupby"),
            ("contiguous_label_runs_marker", "verify_relation"),
            ("unsorted_repeated_labels_marker", "inspect_inputs"),
            ("unsorted_repeated_labels_marker", "execute_groupby"),
            ("unsorted_repeated_labels_marker", "verify_relation"),
            ("sorted_global_grouping_marker", "inspect_inputs"),
            ("sorted_global_grouping_marker", "execute_groupby"),
            ("sorted_global_grouping_marker", "verify_relation"),
            ("shared_group_iterator_marker", "inspect_inputs"),
            ("shared_group_iterator_marker", "execute_groupby"),
            ("shared_group_iterator_marker", "verify_relation"),
        ]
        self.assertEqual(pairs, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
