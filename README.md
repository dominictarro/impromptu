
# impromptu

*Complex, variable-checking conditionals made simple and expressible at runtime.*

## Download & Install

> $ pip install -U git+https://github.com/dominictarro/impromptu

## About

The *Impromptu* language library makes it easy to filter what data is passed to compute functions
without extending your codebase to support complex or redundant conditionals statements.

# Language

*Impromptu* uses [MongoDB query syntax](https://docs.mongodb.com/manual/tutorial/query-documents/)
as supported by [mongoquery](https://github.com/kapouille/mongoquery).

*Impromptu* query documents extend mongoquery syntax with support of named filters through
an assignment operator. Named filters inherit or override conditional expressions from
filter documents they are nested within.

## Example: Named Filter

```json
{
    "highExpenditure": {
        "$assign": {
            "expenses": {
                "$gt": 1000
            }
        }
    }
}
```

### Example: Named Filter Inheritance

```json
{
    "revenue": {
        "$gt": 100
    },
    "highExpenditure": {
        "$assign": {
            "expenses": {
                "$gt": 1000
            }
        }
    },
    "highRevenue": {
        "$assign": {
            "revenue": {
                "$gt": 1000
            }
        }
    }
}
```

When using the named filter *highExpenditure*, the following query statement is applied.

```json
{
    "revenue": {
        "$gt": 100
    },
    "expenses": {
        "$gt": 1000
    }
}
```

And when using the named filter *highRevenue*, the following query statement is applied.

```json
{
    "revenue": {
        "$gt": 1000
    }
}
```

# Usage

*Example:*

```py
from impromptu import Impromptu

definition = {
    "revenue": {
        "$gt": 100
    },
    "highExpenditure": {
        "$assign": {
            "expenses": {
                "$gt": 1000
            }
        }
    },
    "highRevenue": {
        "$assign": {
            "revenue": {
                "$gt": 1000
            }
        }
    }
}
query = Impromptu.from_dict(definition)

# uses the root's boolean expressions
assert query.match(revenue=500, expenses=1500)
# uses the highRevenue filter
assert not query.match(revenue=500, expenses=1500, label='highRevenue')

# this wrapper decides whether or not to run the function
# based on the arguments given
@query.on_match(label='highExpenditure')
def calculate_net_gain(revenue, expenses):
    return revenue - expenses

assert calculate_net_gain(500, 1500) == -1000
assert calculate_net_gain(500, 500) is None

```
