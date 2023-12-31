from datetime import datetime

# Define a function that takes an input time string and returns the preceding and following 15 minute intervals
def get_15_min_intervals(input_time):
  # Parse the input time string into a datetime object
  dt = datetime.strptime(input_time, "%H:%M:%S")
  # Get the minute part of the time
  minute = dt.minute
  # Perform integer division by 15 to get the number of 15 minute intervals that have passed in the hour
  interval = minute // 15
  # Multiply by 15 to get the start of the preceding interval
  prev_minute = interval * 15
  # Add 15 to get the start of the following interval
  next_minute = prev_minute + 15
  # Replace the minute part of the datetime object with the start of the intervals
  prev_dt = dt.replace(minute=prev_minute, second=0)
  next_dt = dt.replace(minute=next_minute, second=0)
  # Format the datetime objects into strings
  prev_time = prev_dt.strftime("%H:%M:%S")
  next_time = next_dt.strftime("%H:%M:%S")
  # Return the intervals as a tuple of strings
  return (prev_time, next_time)

# Define a function that takes two required parameters and two optional parameters
def func(a, b, c=10, d=20):
  # Do something with the parameters
  print(a + b + c + d)

# Call the function with only the required parameters
func(1, 2) # This will print 33

# Call the function with one optional parameter
func(1, 2, 3) # This will print 26

# Call the function with both optional parameters
func(1, 2, 3, 4) # This will print 10


# Test the function with a sample input time
input_time = datetime.now().strftime("%H:%M:%S")
intervals = get_15_min_intervals(input_time)
print(f"The 15 minute interval that preceded {input_time} is {intervals[0]}.")
print(f"The 15 minute interval that followed {input_time} is {intervals[1]}.")
