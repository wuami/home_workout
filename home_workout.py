import argparse
import os
import pandas as pd
import random
import time

ORDINALS = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']

def say_and_wait(t, *args):
    before = time.time()
    os.system('say \'%s\'' % ' '.join(args))
    elapsed = time.time() - before
    time.sleep(max(0, t - elapsed))


def main():
    p = argparse.ArgumentParser(description = 'Randomly generate a full body workout')
    p.add_argument('-e', '--exercise_list', default = 'exercises.tsv')
    p.add_argument('-s', '--secs_on', default = 40, type = int)
    p.add_argument('-n', '--rounds', default = 3, type = int)
    p.add_argument('-r', '--rest', default = 60, type = int)
    p.add_argument('-x', '--n_exercises', default = 10, type = int)
    args = p.parse_args()

    all_exercises = pd.read_csv(args.exercise_list, sep = '\t')
    n_each = args.n_exercises // 4
    n_extra = args.n_exercises - n_each * 4
    counts = [n_each] * (4 - n_extra) + [n_each + 1] * n_extra
    random.shuffle(counts)

    exercises = all_exercises.groupby('type').apply(lambda x: x.sample(n = counts.pop()))
    exercises = exercises.sample(frac = 1).reset_index(drop = True)
    
    print('\n%d sets of %d exercises - %d seconds on, %d seconds off\n' %
          (args.rounds, args.n_exercises, args.secs_on, 60 - args.secs_on))
    print('\n'.join(['%d. %s' % (i + 1, row['exercise']) for i, row in exercises.iterrows()]))

    cont = input('\ncontinue? [y] ')
    if cont in ['', 'y', 'yes']:
      for r in range(args.rounds):
        for i, row in exercises.iterrows():
          if i == 0:
            if r == args.rounds - 1:
              say_and_wait(10,
                           'last round blast round, %s exercise, %s' % (ORDINALS[i], row['exercise']))
            else:
              say_and_wait(10,
                           'round %d, %s exercise, %s' % (r + 1, ORDINALS[i], row['exercise']))
          else:
            say_and_wait(60 - args.secs_on,
                         'rest, %s exercise, %s' % (ORDINALS[i], row['exercise']))
          say_and_wait(args.secs_on / 2, 'begin')
          if row['switch']:
            say_and_wait(args.secs_on / 2 - 10, 'switch sides')
          else:
            say_and_wait(args.secs_on / 2 - 10, 'halfway')
          say_and_wait(10, 'ten seconds')
        if r == args.rounds - 1:
          say_and_wait(0, 'end of round %d' % (r + 1))
        else:
          say_and_wait(args.rest - 10, 'end of round %d, %d seconds rest' %
                       (r + 1, args.rest))

      print('\nstretch for 5 minutes\n')
      say_and_wait(0, 'stretch for 5 minutes')


if __name__ == '__main__':
    main()
