import matplotlib

from scipy.special import binom, factorial
import matplotlib.pylab as plt

matplotlib.use('TkAgg')

N: int = 30
MIN_K: int = 3

values: list[dict] = [
    {
        'k': 3,
        'boxed': 24240,
        'typed': 12960,
        'time': 0.13
    },
{
        'k': 4,
        'boxed': 578280,
        'typed': 324000,
        'time': 2.4
    },
{
        'k': 5,
        'boxed': 7330440,
        'typed': 3693600,
        'time': 50
    },
{
        'k': 6,
        'boxed': 39011880,
        'typed': 13659840,
        'time': 564
    },
{
        'k': 7,
        'boxed': 81438600,
        'typed': 16161100,
        'time': 2038
    },
{
        'k': 8,
        'boxed': 88938120,
        'typed': 16549920,
        'time': 2407
    }
]

for v in values:
    v['base'] = sum([int(factorial(i) * binom(N, i)) for i in range(MIN_K, v['k'] + 1)])
xs = [v['k'] for v in values]
bases = [v['base'] for v in values]
boxes = [v['boxed'] for v in values]
types = [v['typed'] for v in values]
times_min = [v['time'] / 60 for v in values]

def comp(log=False):
    plt.figure(figsize=(8, 6))

    if log:
        plt.plot(xs, bases, label='all', color='blue', marker='.', linestyle='none')
        plt.yscale('log')
    plt.plot(xs, boxes, label='filtered length + time', color='green', marker='o', linestyle='none')
    plt.plot(xs, types, label='filtered length + time + type', color='red', marker='s', linestyle='none')


    plt.xlabel('sequence length')
    plt.ylabel(f'number of sequences{' (log scale)' if log else ''}')
    plt.title('Comparison between all sequences and filtered ones')
    plt.legend(loc='upper left')
    #plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.show()


def comp_time(log=False):
    plt.figure(figsize=(8, 6))

    plt.plot(xs, times_min, color='orange', marker='^', linestyle='none')
    if log:
        plt.yscale('log')

    plt.xlabel('sequence length')
    plt.ylabel(f'compute time / min.')
    plt.title('Computation time for filtered sequences')
    #plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.show()


def comp_comb(log=False):
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax2 = ax1.twinx()

    if log:
        ax1.plot(xs, bases, label='all', color='blue', marker='.', linestyle='none')
        ax1.set_yscale('log')
    ax1.plot(xs, boxes, label='filtered length + time', color='green', marker='o', linestyle='none')
    ax1.plot(xs, types, label='filtered length + time + type', color='red', marker='s', linestyle='none')

    ax1.set_xlabel('sequence length')
    ax1.set_ylabel(f'number of sequences{" (log scale)" if log else ""}', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    #ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax2.plot(xs, times_min, label='time (all filters)', color='orange', marker='^', linestyle='None')
    if log:
        ax2.set_yscale('log')
    ax2.set_ylabel('computation time / min.', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    fig.suptitle('Comparison between all sequences and filtered ones + computation time')
    ax1.legend(loc='upper left')
    ax2.legend(loc='center left')

    plt.show()




#comp(True)
#comp_time(True)
comp_comb(True)