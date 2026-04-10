#Task 1
def hello():
  return "Hello!"

#testing task 1
print("This is the result:", hello())


#Task 2
def greet(name):
  return f"Hello, {name}!"

#testing task 2
print(greet("Dani"))


#task 3
def calc(a, b, op="multiply"):
  try:
    match op:
      case "add":
        return a + b
      case "subtract":
        return a - b
      case "multiply":
        return a * b
      case "divide":
        return a / b
      case "modulo":
        return a % b
      case "int_divide":
        return a // b
      case "power":
        return a ** b
  except ZeroDivisionError:
    return "You can't divide by 0!"
  except TypeError:
    return "You can't multiply those values!"
  
#Task 4
def data_type_conversion(value, type_name):
  try:
    match type_name:
      case "int":
        return int(value)
      case "str":
        return str(value)
      case "float":
        return float(value)
  except ValueError:
    return f"You can't convert {value} into {type_name}."
  
#Task 5
def grade(*args):
  try:
    if not args:
      return "F"
    
    average = sum(args) / len(args)

    if average >= 90:
      return "A"
    elif average >= 80:
      return "B"
    elif average >= 70:
      return "C"
    elif average >= 60:
      return "D"
    else:
      return "F"
  except TypeError:
    "Invalid data was provided."

#test task 5
print(grade(66))

#Task 6
def repeat(string, count):
  result = ""
  for i in range(count):
    result += string
  return result
  
#test task 6
print(repeat("Bob", 4))


#Task 7
def student_scores(x, **kwargs):
  if not kwargs:
    return 0 if x == "mean" else None
  if x  == "mean":
    scores = kwargs.values()
    return sum(scores) / len(scores)
  if x == "best":
    best_student = max(kwargs, key= kwargs.get)
    return best_student


#test task 7
print(student_scores("best", Alice=90, Bob=80))
print(student_scores("mean", Alice=90, Bob=70))

#Task 8
def titleize(sentence):
  little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
  words = sentence.split()

  if not words:
    return ""
  
  result_words = []

  for i, word in enumerate(words):
    if i == 0 or i == len(words) - 1:
      result_words.append(word.capitalize())
    elif word.lower() not in little_words:
      result_words.append(word.capitalize())
    else:
      result_words.append(word.lower())
  
  return " ".join(result_words)

#test task 8
print("Task 8:", titleize("the prince and the pauper"))

#Task 9
def hangman(secret, guess):
  result = ""

  for letter in secret:
    if letter in guess:
      result += letter
    else: 
      result += "_"

  return result

#test task 9
print(hangman("rainbow", "abow"))


#Task 10
def pig_latin(text):
  vowels = "aeiou"
  words = text.split()
  result_words = []

  for word in words:
    if word[0] in vowels: 
      result_words.append(word + "ay")
    else:
      if word.startswith("qu"):
        cutoff = 2
      else:
        cutoff = 0
        for char in word:
          if char in vowels:
            break
          cutoff += 1

      prefix = word[:cutoff]
      suffix = word[cutoff:]
      result_words.append(suffix + prefix + "ay")

  return " ".join(result_words)

#test task 10
print(pig_latin("encyclopedia"))