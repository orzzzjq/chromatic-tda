import numpy as np

from chromatic_tda.utils.linear_algebra_utils import LinAlgUtils
from chromatic_tda.utils.timing import TimingUtils


class GeometryUtils:
    @staticmethod
    def construct_equispace(*point_sets: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return the 'point + vector space' representation of the affine space A of points
        equidistant to all points of each argument. That is for a in A and for each argument P,
        all distances ||p - a|| for p in P are the same.

        :return: center `z`, list of generating vectors `ker`"""
        TimingUtils().start("Geom :: Construct Equispace")
        if len(point_sets) < 1:
            raise TypeError("At least one point set expected.")
        dim: int = point_sets[0].shape[1]
        k: int = len(point_sets)

        for point_set in point_sets[1:]:
            if point_set.shape[1] != dim:
                raise ValueError('All points need to be from the same dimension')

        a_mat_blocks: list[np.ndarray] = []
        b_vec_blocks: list[np.ndarray] = []
        for i, points in enumerate(point_sets):
            a_mat_blocks.append(GeometryUtils.one_hot_embedding(k, i, points))
            b_vec_blocks.append(np.array([(pt ** 2).sum() / 2 for pt in points]))
        a_mat = np.concatenate(a_mat_blocks)
        b_vec = np.concatenate(b_vec_blocks)
        z, ker = LinAlgUtils.solve(a_mat, b_vec)

        TimingUtils().stop("Geom :: Construct Equispace")
        return z[:dim], ker[:, :dim]

    @staticmethod
    def one_hot_embedding(number_of_categories: int, category: int, points: np.ndarray) -> np.ndarray:
        TimingUtils().start("Geom :: One Hot Embedding")
        if category >= number_of_categories:
            raise ValueError(f'Category out of range: need category < number_of_categories')
        suffix = np.zeros((len(points), number_of_categories))
        suffix[:, category] = 1
        one_hot_embedding = np.concatenate([points, suffix], axis=1)
        TimingUtils().stop("Geom :: One Hot Embedding")
        return one_hot_embedding

    @staticmethod
    def reflect_points_through_affine_space(shift: np.ndarray, vector_space: np.ndarray, *points: np.ndarray):
        TimingUtils().start("Geom :: Reflect Points Through Aff")
        u_mat = LinAlgUtils.orthogonalize_rows(vector_space).transpose()  # matrix with orthogonal columns
        trans_mat = 2 * u_mat @ u_mat.transpose() - np.identity(u_mat.shape[0])
        reflected_points = np.array([trans_mat @ (pt - shift) + shift for pt in points])
        TimingUtils().stop("Geom :: Reflect Points Through Aff")
        return reflected_points
