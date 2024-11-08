import os

from chromatic_tda import ChromaticAlphaComplex, plot_six_pack, plot_labeled_point_set
import numpy as np
from matplotlib import pyplot as plt

from chromatic_tda.utils.timing import TimingUtils


def run_test():
    pass
    # for embedding in TestBars().single_test('two_circles_cc', return_detailed=True):
    #     for group, result in embedding.items():
    #         print(group.ljust(12), result)
    #     print()

    # points = np.random.random((50, 2))
    # labels = list(map(int, 2 * np.random.random(len(points))))
    # cplx = ChromaticAlphaComplex(points, labels).get_simplicial_complex(sub_complex=((0,),))

    # TimingAnalysis(
    #     n=1000,
    #     color_range_splits=(.5, 1),
    #     sub_complex='monochromatic'
    # ).run()
    # TimingUtils().flush()
    #
    # TimingAnalysis(
    #     n=500,
    #     color_range_splits=(.3, .6),
    #     sub_complex='monochromatic'
    # ).run()

def run_mp_test():
    configurations = []
    configurations.extend([(2,2,n) for n in range(1000, 1001, 1000)])
    # configurations.extend([(2,3,n) for n in range(1000, 20001, 1000)])
    # configurations.extend([(2,4,n) for n in range(1000, 20001, 1000)])
    # configurations.extend([(3,2,n) for n in range(1000, 10001, 1000)])
    # configurations.extend([(3,3,n) for n in range(1000, 5001, 1000)])

    sequential = {}
    parallel = {}
    for d, c, n in configurations:
        points = np.random.random((n, d))
        labels = list(map(int, c * np.random.random(n)))

        # parallel
        TimingUtils(log_times=True).flush()
        TimingUtils().start('Total')
        ChromaticAlphaComplex(points, labels, multi_process=8)
        TimingUtils().stop('Total')
        parallel[(d, c, n)] = [TimingUtils().get('Total'), TimingUtils().get('Rad :: Construct Radius Function'),
                               TimingUtils().get('KKT :: Dual Computation')]

        # sequential
        TimingUtils(log_times=True).flush()
        TimingUtils().start('Total')
        ChromaticAlphaComplex(points, labels, multi_process=0)
        TimingUtils().stop('Total')
        sequential[(d, c, n)] = [TimingUtils().get('Total'), TimingUtils().get('Rad :: Construct Radius Function')]

    with open('mp_test.log', 'w') as f:
        f.write('parallel:\n')
        for d, c, n in parallel:
            f.write(f'{d}, {c}, {n} : {parallel[(d, c, n)]}')
        f.write('\n\nsequential:\n')
        for d, c, n in sequential:
            f.write(f'{d}, {c}, {n} : {sequential[(d, c, n)]}')

def main():
    run_mp_test()
    # np.random.seed(0)
    # points = np.random.random((20000, 2))
    # labels = list(map(int, 4 * np.random.random(len(points))))
    # # plot_labeled_point_set(points, labels)
    #
    # TimingUtils(log_times=True).flush()
    #
    # cplx = ChromaticAlphaComplex(points, labels, multi_process=8).get_simplicial_complex(sub_complex='mono-chromatic')
    #
    # TimingUtils().print()

    # plot_six_pack(cplx)
    # plt.show()


if __name__ == "__main__":
    main()
