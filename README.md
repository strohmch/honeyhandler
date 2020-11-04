# MoneyHandler
A little python script to manage expenses among a group of persons e.g. friends during holiday.

Provided a list of `persons` and a list of `positions`, this script shows the
accounts stating the individuals total contribution. To even out the balances
a suggestion of money transfer is provided.

## Requirements
`python2` or `python3`. No third-party software is required.

## Usage

This script can be called upon a json file providing a list of `persons` and a list of `positions` - see more in the JSON Data format section.

```>python moneyhandler.py 2020_summer_vacation.json```

## JSON Data Format
The json file has to provide two keys, `persons` and `positions`.
### persons
The value of the key `persons` is supposed to be a list of all persons involved provided as a string each.
### positions
Collect all the positions of expenses in a list. 
Each position itself has to be a list of numbers that the according person contributed (each number's position in the position's list is associated the person of same position in the persons list). 
The position's list length must fit the number of persons. Hence, fill the remaining entries with zero if the according person should have a share but did not pay anything.
A negative value neglects the person's contribution to that position entirely (that is if this person is not supposed to pay for this position at all).
An example is given by distributed file `2020_summer_vacation.json`.