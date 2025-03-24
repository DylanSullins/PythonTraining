"""
These tests use the Hypothesis library: https://hypothesis.readthedocs.io/en/latest/index.html
uv can be used to run this script, automatically pulling down dependencies and creating a virtual environment: https://docs.astral.sh/uv/
run `uv run unit_test.py`
"""
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "hypothesis",
# ]
# ///

from __future__ import annotations
import re
import unittest
import hypothesis.strategies as st
from hypothesis import given
import typing as t
from copy import deepcopy

from definitions import RowType, GENDER, CASE_NUMBER, ISSUES, LANDLORD
from main import translate_data


# These were pulled from the CSV Rhodes provided. Hypothesis will generate arbitrary combinations.
_issues = [
    "Rent Increase",
    "Houselessness",
    "Sexual Violence",
    "Utilities issue Gas",
    "Utilities issue Water",
    "Wants to Break Lease",
    "Interested in organizing",
    "Utilities issue Internet",
    "Eviction or illegal lock out",
    "Domestic Violence",
    "Inability to pay rent",
    "Elderly Abuse",
    "Lease Dispute",
    "Seeking Housing",
    "Water Leak",
    "Living with Disabilities",
    "Landlord harassment",
    "Neighbor Dispute",
    "Fixed Income",
    "Unhealthy conditions at home",
    "Utilities issue Heat or AC",
    "Utilities issue Electricity",
]

_genders = [
    "",
    "Non-binary (they/them or others),Genderqueer",
    "Non-binary (they/them or others),Transgender",
    "Non-binary (they/them or others)",
    "Transgender,Female (she/her)",
    "Prefer not to identify",
    "Transgender",
    "Male (he/him)",
    "Male",
    "Female",
    "Non-binary (they/them or others),Female (she/her)",
    "TBD",
    "Non-binary (they/them or others),Transgender,Male (he/him),Genderqueer",
    "Male (he/him),Transgender",
    "Female (she/her)",
    "Female (she/her),Male (he/him)",
]

_landlords = [
    "Mac Properties, 211 Armor Blvd LLC % Mac Properties",
    "MAC",
    "Liberty Associates LLC",
    "Sentinel",
]


row_strategy = st.fixed_dictionaries(
    {
        CASE_NUMBER: st.integers(min_value=0, max_value=10000),
        GENDER: st.sampled_from(_genders),
        LANDLORD: st.sampled_from(_landlords),
        ISSUES: st.lists(st.sampled_from(_issues), unique=True).map(
            lambda l: ",".join(l)
        ),
    }
)

rows_strategy = st.lists(row_strategy, unique_by=(lambda x: x[CASE_NUMBER],))


def stub(rows):
    return rows, rows


def is_mac_row(row: RowType) -> bool:
    return re.compile(r"\bmac\b", re.IGNORECASE).search(row[LANDLORD])


class Test(unittest.TestCase):

    def get_output(self, rows: list[RowType]) -> RowType:
        return translate_data(deepcopy(rows))

    @given(rows_strategy)
    def test_output_is_sorted(self, rows: list[RowType]):
        output = self.get_output(rows)

        done_with_mac = False
        biggest_num_so_far = -1
        for row in output:
            # Reset the biggest number we've seen so far.
            if not done_with_mac and not is_mac_row(row):
                biggest_num_so_far = -1
                done_with_mac = True

            # If you've hit this assert, it likely means that you have incorrectly sorted "Mac" cases above non-"Mac" cases
            self.assertEqual(
                done_with_mac, not is_mac_row(row), f"\n{rows=}\n{output=}\n"
            )

            # If you've hit this assert, it likely means that you have incorrectly sorted "Mac" cases above non-"Mac" cases
            self.assertGreater(
                row[CASE_NUMBER], biggest_num_so_far, f"\n{rows=}\n{output=}\n"
            )
            biggest_num_so_far = row[CASE_NUMBER]

    @given(rows_strategy)
    def test_output_has_no_cases_divisible_by_9(self, rows: list[RowType]):
        output = self.get_output(rows)

        # If you've hit this assert, it likely means that you have either left a case in with a Case Number divisible by 9, or thrown out a case that should have been kept.
        self.assertEqual(len(output), sum([int(r[CASE_NUMBER]) % 9 != 0 for r in rows]))

        for row in output:
            # If you've hit this assert, it likely means that you've left a case in with a Case Number that is divisible by 9.
            self.assertNotEqual(int(row[CASE_NUMBER]) % 9, 0)

    @given(rows_strategy)
    def test_output_fixed_genders(self, rows: list[RowType]):
        output = self.get_output(rows)

        output = sorted(output, key=lambda row: row[CASE_NUMBER])
        case_number_to_orig_row = {int(row[CASE_NUMBER]): row for row in rows}

        for row in output:
            orig_row = case_number_to_orig_row[int(row[CASE_NUMBER])]
            orig_genders = sorted(orig_row[GENDER].split(","))
            updated_genders = sorted(row[GENDER].split(","))

            # If you've hit this assert, it likely means that you've not updated the right number of gender tags.
            self.assertEqual(len(orig_genders), len(updated_genders))
            for orig_gender, updated_gender in zip(orig_genders, updated_genders):
                # If you've hit this assert, it likely means that a gender entry wasn't updated correctly.
                if "female" in orig_gender.lower():
                    self.assertEqual(updated_gender, "Female (she/her)")
                # If you've hit this assert, it likely means that a gender entry wasn't updated correctly.
                elif "male" in orig_gender.lower():
                    self.assertEqual(updated_gender, "Male (he/him)")
                # If you've hit this assert, it likely means that a gender entry was unnecessarily updated.
                else:
                    self.assertEqual(orig_gender, updated_gender)

    @given(rows_strategy)
    def test_output_contains_same_data(self, rows: list[RowType]):
        output = self.get_output(rows)

        case_number_to_orig_row = {int(row[CASE_NUMBER]): row for row in rows}

        for updated_row in output:
            orig_row_edited = deepcopy(
                case_number_to_orig_row[int(updated_row[CASE_NUMBER])]
            )
            updated_row_edited = deepcopy(updated_row)

            orig_row_edited.pop(GENDER)
            updated_row_edited.pop(GENDER)

            # If you've hit this assert, it likely means that a gender entry wasn't updated correctly.
            self.assertDictEqual(
                deepcopy(orig_row_edited),
                updated_row_edited,
                f"\n{orig_row_edited=}\n{updated_row=}",
            )

if __name__ == "__main__":
    unittest.main()
