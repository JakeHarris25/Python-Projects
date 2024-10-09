# Rock Paper Scissors against an NPC
import random
import time

print("Welcome to Rock Paper Scissors!")
time.sleep(1)

# Asking player for input
name = input("What is your name?\n")
time.sleep(.5)
name_upper = name.title()

hand = input("Which hand will you throw? (rock, paper, scissors)\n")
time.sleep(.5)
hand_lower = hand.lower()

# some print statements
print(name_upper + " will throw " + hand_lower + ".")
time.sleep(1)

print("The NPC is now deciding...")
time.sleep(2)
print("They have chosen!\n")
time.sleep(1)

# Random number for NPC to choose Rock, Paper, or Scissors
randNum = random.randint(1, 3)

# assigned hands numerical values
rock = 1
paper = 2
scissors = 3

rockStr = "rock"
paperStr = "paper"
scissorsStr = "scissors"

# the showdown
print("Ready for the games to begin!?\n")
time.sleep(1.5)
print("Get ready to throw!\n")
time.sleep(1.5)
print("...anddd\n")
time.sleep(2)
print("NOW!!!\n")
time.sleep(1)
print(name_upper + " throws " + hand_lower + "!")
time.sleep(1)


msg1 = ("The NPC throws rock!") 
msg2 = ("The NPC throws paper!")
msg3 = ("The NPC throws scissors!")

# NPC deciding which hand to throw
if randNum == rock:
    print(msg1)
elif randNum == paper:
    print(msg2)
elif randNum == scissors:
    print(msg3)
else:
    print("null")

time.sleep(1)

if hand_lower == rockStr and randNum == rock:
    print("It's a draw...")
elif hand_lower == paperStr and randNum == paper:
    print("It's a draw...")
elif hand_lower == scissorsStr and randNum == scissors:
    print("It's a draw...")
elif hand_lower == rockStr and randNum == paper:
    print("The NPC wins!")
elif hand_lower == paperStr and randNum == rock:
    print("The NPC wins!")
elif hand_lower == scissorsStr and randNum == paper:
    print(name_upper + " wins!")
elif hand_lower == rockStr and randNum == scissors:
    print(name_upper + " wins!")