#!/usr/bin/python
import argparse
import os
import random
import time

ORDINALS = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
LOWER = [
  "calf raise",
  "cossack squat",
  "curtsy lunge",
  "donkey kick",
  "glute bridge",
  "jump squat",
  "jumping lunges",
  "lunge to knee drive",
  "pistol squat",
  "single leg deadlift",
  "split squat",
  "step ups",
  "walking lunge"
]
UPPER = [
  "alternating curl",
  "band chest fly",
  "band pull aparts",
  "bent-over row",
  "lateral raise",
  "overhead press",
  "push up",
  "spiderman push up",
  "tricep dip",
  "tricep extension"
]
CORE = [
  "bicycle crunches",
  "crunch",
  "dead bug",
  "flutter kick",
  "leg lift",
  "plank jack",
  "plank rotations",
  "plank with leg extension",
  "reverse crunch",
  "side plank knee to elbow",
  "side plank with hip lift",
  "single leg lift",
  "superman",
  "tuck ups",
  "v-ups"
]
CARDIO = [
  "burpee",
  "butt kicks",
  "candlestick jump",
  "high knee",
  "inchworm",
  "jumping jack",
  "kick sits",
  "mountain climber",
  "speed skaters"
]
ALL_ = LOWER + UPPER + CORE + CARDIO


def say_and_wait(t, *args):
    before = time.time()
    os.system("say \"%s\"" % " ".join(args))
    elapsed = time.time() - before
    time.sleep(max(0, t - elapsed))


def main():
    p = argparse.ArgumentParser(description="Randomly generate a full body workout")
    p.add_argument("-s", "--secs_on", default=40, type=int)
    p.add_argument("-n", "--rounds", default=3, type=int)
    p.add_argument("-r", "--rest", default=60, type=int)
    p.add_argument("-x", "--n_exercises", default=10, type=int)
    args = p.parse_args()

    n_each = args.n_exercises // 4
    exercises = random.sample(LOWER, n_each) + random.sample(UPPER, n_each) + \
        random.sample(CORE, n_each) + random.sample(CARDIO, n_each)
    exercises += random.sample([x for x in ALL_ if x not in exercises],
                               args.n_exercises - 4 * n_each)
    random.shuffle(exercises)
    
    print("\n%d sets of %d exercises - %d seconds on, %d seconds off\n" %
          (args.rounds, args.n_exercises, args.secs_on, 60 - args.secs_on))
    print("\n".join(["%d. %s" % (i + 1, x) for i, x in enumerate(exercises)]))

    cont = raw_input("\ncontinue? [y] ")
    if cont in ["", "y", "yes"]:
      for r in range(args.rounds):
        for i, x in enumerate(exercises):
          if i == 0:
            say_and_wait(10,
                         "round %d, %s exercise, %s" % (r + 1, ORDINALS[i], x))
          else:
            say_and_wait(60 - args.secs_on,
                         "rest, %s exercise, %s" % (ORDINALS[i], x))
          say_and_wait(args.secs_on / 2, "begin")
          say_and_wait(args.secs_on / 2 - 10, "halfway")
          say_and_wait(10, "ten seconds")
        if r == args.rounds - 1:
          say_and_wait(0, "end of round %d" % (r + 1))
        else:
          say_and_wait(args.rest - 10, "end of round %d, %d seconds rest" %
                       (r + 1, args.rest))

      print("\nstretch for 5 minutes\n")
      say_and_wait(0, "stretch for 5 minutes")


if __name__ == '__main__':
    main()
