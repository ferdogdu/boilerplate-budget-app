from itertools import zip_longest


class Category:

  def __init__(self, name):
    self.name = name
    self.total = 0.0
    self.ledger = list()

  def __str__(self):
    output = f"{self.name:*^30}\n"

    for item in self.ledger:
      output += f"{item['description']:23.23}{item['amount']:>7.2f}\n"

    output += f"Total: {self.total:.2f}"
    return output

  def deposit(self, amount, description=""):
    self.total += amount
    self.ledger.append({"amount": amount, "description": description})

  def get_balance(self):
    return self.total

  def check_funds(self, amount):
    return amount <= self.get_balance()

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.total -= amount
      self.ledger.append({"amount": -amount, "description": description})

    return self.check_funds(amount)

  def transfer(self, amount, DestinationCategory):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {DestinationCategory.name}")
      DestinationCategory.deposit(amount, f"Transfer from {self.name}")

    return self.check_funds(amount)


def create_spend_chart(categories):
  chartTitle = "Percentage spent by category\n"
  string = ""

  totalSpent = 0
  categoryPercentage = dict()

  for category in categories:
    categorySpent = 0

    for item in category.ledger:
      if item["amount"] < 0:
        categorySpent += abs(item["amount"])
        totalSpent += abs(item["amount"])
      categoryPercentage[category.name] = categorySpent

  for k in categoryPercentage.keys():
    categoryPercentage[k] = (categoryPercentage[k] / totalSpent) * 100

  for i in range(100, -1, -10):
    string += f"{i:>3}|"
    for v in categoryPercentage.values():
      if (v >= i):
        string += f"{'o':^3}"
      else:
        string += f"{' ':3}"
    string += "\n"

  string = string.replace('\n', " " + '\n')
  string += f"{' ' * 4}{'-'*3*len(categories)}{'-'}\n"

  categoryNames = ""

  for category in categories:
    categoryNames += f"{category.name} "

  for s in zip_longest(*categoryNames.split(), fillvalue=' '):
    string += f"{' ' * 5}{'  '.join(s):}  \n"

  return chartTitle + string.rstrip() + "  "