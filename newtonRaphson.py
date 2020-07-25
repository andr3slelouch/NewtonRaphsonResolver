#https://github.com/felipemarkson/newtonpy

"""
Newton
A package to solve non-linear equations.
Copyright (c) 2020 Felipe Markson dos Santos Monteiro <fmarkson@gmail.com>
MIT License.
"""

from numpy.linalg import solve as default_solver
from numpy import ndarray
from typing import Tuple, Callable, Union
from error import err

def newtonRaphson(
    f,
    dx,
    x0: ndarray,
    *,
    tol: Union[int, float, ndarray] = 0.001,
    maxiter: int = 100,
    solver: Callable[[ndarray, ndarray], ndarray] = default_solver,
    verbose: bool = True,
) -> Tuple[bool, ndarray, ndarray]:
    """
    A Newton–Raphson method implementation for finding roots . See (https://en.wikipedia.org/wiki/Newton%27s_method)
        Ex:
            import newton
            import numpy as np

            (converged, error, solution) = newton.solve(
            lambda x: np.array([x ** 2]),
            lambda x: np.array([2 * x]),
            x0=np.array([1.2]),
            tol=0.001,
            maxiter=100,
            verbose=False,
            )

            print(solution)            
            >>> [0.01875]
    Args:
        func : The func is a F, where F: ℝᵏ → ℝᵏ and k is the number of dimensions.
        jacobian : The Jacobian Matrix of func. See (https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant).
        x0 : The intial guess, where x0 ∈ ℝᵏ.
        tol : The tolerance. If ndarray, the tolerance for each dimension must be specified.
        maxiter : The maximum number of iterations.
        solver : A linear matrix equation solver. If not specified, the numpy.linalg.solve is used. See (https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html)
        verbose :  If True, prints the iteration and the absolute maximum error. 
    Returns:
        If converged, the mismatch vectors, and the current solution.

    """  # noqa

    #Fx = func(x0)
    Fx = f(x0)
    for indx in range(0, maxiter):
        Jx = dx(x0)
        try:
            deltaX = solver(-Jx, Fx)
        except Exception as e:
            err("Error,La matriz es singular")
        x0 = x0 + deltaX
        Fx = f(x0)
        Fxabs = abs(Fx)
        if verbose:
            print(f"## Iteration {indx}. Absolute maximum error: {Fxabs.max()}")

        if all(Fxabs <= tol):
            return (True, Fx, x0, indx)

    return (False, Fx, x0, indx)
