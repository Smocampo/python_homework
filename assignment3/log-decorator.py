#Task 1
import logging

logger = logging.getLogger(__name__ + "parameter_log")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("./decorator.log", "a")
logger.addHandler(handler)

def logger_decorator(func):
  def wrapper(*args, **kwargs):
    result = func(*args, **kwargs)
    pos_params = list(args) if args else "none"
    key_params = kwargs if kwargs else "none"
    log_message = (
      f"function: {func.__name__}\n"
      f"positional parameters: {pos_params}\n"
      f"keyword parameters: {key_params}\n"
      f"return: {result}\n"
      f"{'-'*30}"
    )
  
    logger.log(logging.INFO, log_message)
    return result
  return wrapper

@logger_decorator
def say_hello():
  print("Hello, World!")

@logger_decorator
def check_arguments(*args):
  return True

@logger_decorator
def return_decorator_ref(**kwargs):
  return logger_decorator

if __name__ == "__main__":
  print("Running test calls...")
  say_hello()
  check_arguments(10, "Python", [1, 2, 3])
  return_decorator_ref(user="Admin", status="Active", attempts=3)
    
  print("Tests complete. Check './decorator.log' for results.")


