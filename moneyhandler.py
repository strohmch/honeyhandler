#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to balance expenses among a group of people.

Provided a list of 'persons' and a list of 'positions', this script shows the
accounts stating the individuals total contribution. To even out the balances
a suggestion of money transfer is provided.

This script can be called upon a json file providing the two data sets.
See the README.txt for more information on the data format.
"""
# -----------------------------------------------------------------------------
# The full license is in the file LICENSE, distributed with this code.
#
# REFERENCES:
# https://github.com/strohmch/moneyhandler
# -----------------------------------------------------------------------------

import json
import sys

currency = "EUR"


def calc_accounts(persons, positions):
    """Calculates the persons' accounts with due positions (sorted)."""

    balances = [0] * len(persons)

    for pos in positions:
        assert len(persons) == len(pos)

        # persons obligated to contribute
        con = [i for i, c in enumerate(pos) if c >= 0]

        # total expense on position
        expense = sum(pos[i] for i in con)

        share = expense / len(con)

        # calculate balance
        for i in con:
            balances[i] += pos[i] - share

        # sort the persons according to their balances from dept to claim
        accounts = sorted(zip(persons, balances), key=lambda x: x[1])

    return accounts


def suggested_actions(accounts):
    """Suggests actions to balance sorted accounts."""

    # the following algorithm provides a suggestion of how to balance the accounts
    persons_s, balances_s = zip(*accounts)
    baltmp = list(balances_s)

    # the actions of transactions are stored here
    actions = []

    for i in range(len(baltmp)):
        if not baltmp[i] < 0:
            break

        for j in range(len(baltmp) - 1, i, -1):
            if not baltmp[j] > 0:
                continue

            if baltmp[j] + baltmp[i] >= 0:
                bal_to_trans = baltmp[i]
            else:
                bal_to_trans = -baltmp[j]

            actions.append([i, j, -bal_to_trans])
            baltmp[i] -= bal_to_trans
            baltmp[j] += bal_to_trans

            if baltmp[i] == 0:
                break

    return actions


def main(filename):
    """Main script running on jason file named "filename'"""

    # read the json file with input data
    with open(filename, mode="r") as f:
        data = json.load(f)

    # calculate the according sorted accounts
    accounts = calc_accounts(data['persons'], data['positions'])

    for pers, bal in accounts:
        print(f'{pers}: {bal:.2f} {currency}')
    print("=" * 80)

    # obtain suggested actions
    actions = suggested_actions(accounts)

    persons_s = list(zip(*accounts))[0]

    for i, j, bal in actions:
        print(f'{persons_s[i]} transfers to {persons_s[j]}: {bal:.2f} {currency}')


if __name__ == '__main__':

    if len(sys.argv) > 1:
        json_filename = sys.argv[1]
    else:
        json_filename = "2020_summer_vacation.json"
        print(f"Got no input, using the example json file: {json_filename}")

    main(json_filename)
