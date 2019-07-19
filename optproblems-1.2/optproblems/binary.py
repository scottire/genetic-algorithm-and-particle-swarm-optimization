"""
Common binary test problems.

.. warning:: Note that the problems in this module are all maximization problems.

"""

import random

from optproblems.base import TestProblem, Individual


def hamming_dist(bitstring1, bitstring2):
    """Hamming distance."""
    assert len(bitstring1) == len(bitstring2)
    return sum(bitstring1[i] != bitstring2[i] for i in range(len(bitstring1)))



def one_max(phenome):
    """The bare-bones one-max function."""
    return sum(phenome)



def leading_ones(phenome):
    """The bare-bones leading-ones function."""
    ret = 0
    i = 0
    while i < len(phenome) and phenome[i] == 1:
        ret += 1
        i += 1
    return ret



def trailing_zeros(phenome):
    """The bare-bones trailing-zeros function."""
    ret = 0
    i = len(phenome) - 1
    while i >= 0 and phenome[i] == 0:
        ret += 1
        i -= 1
    return ret



class BinaryChecker:
    """A pre-processor for checking if a phenome is binary.

    .. note:: This class makes use of the decorator design pattern for
        potential chaining of pre-processors, see
        https://en.wikipedia.org/wiki/Decorator_pattern

    """
    def __init__(self, num_variables=None, previous_preprocessor=None):
        """Constructor.

        Parameters
        ----------
        num_variables : int, optional
            Optionally require a specific number of phenes.
        previous_preprocessor : callable, optional
            Another callable that processes the phenome before this one
            does.

        """
        self.num_variables = num_variables
        self.previous_preprocessor = previous_preprocessor


    def __call__(self, phenome):
        """Check constraints and raise exception if necessary."""
        if self.previous_preprocessor is not None:
            phenome = self.previous_preprocessor(phenome)
        if self.num_variables is not None:
            assert len(phenome) == self.num_variables
        for phene in phenome:
            assert phene in (0, 1)
        return phenome



class OneMax(TestProblem):
    """The most simple binary optimization problem."""

    def __init__(self, num_variables=30, phenome_preprocessor=None, **kwargs):
        """Constructor.

        Parameters
        ----------
        num_variables : int, optional
            The search space dimension.
        phenome_preprocessor : callable, optional
            A callable potentially applying transformations or checks to
            the phenome. Modifications should only be applied to a copy
            of the input. The (modified) phenome must be returned.
            Default behavior is to do no processing.
        kwargs
            Arbitrary keyword arguments, passed through to the constructor
            of the super class.

        """
        preprocessor = BinaryChecker(num_variables, phenome_preprocessor)
        TestProblem.__init__(self,
                             one_max,
                             num_objectives=1,
                             phenome_preprocessor=preprocessor,
                             **kwargs)
        self.num_variables = num_variables
        self.is_deterministic = True
        self.do_maximize = True


    def get_optimal_solutions(self, max_number=None):
        """Return the optimal solution.

        The returned solution does not yet contain the objective values.

        Returns
        -------
        solutions : list of Individual

        """
        assert max_number is None or max_number > 0
        opt = Individual([1] * self.num_variables)
        return [opt]


    get_locally_optimal_solutions = get_optimal_solutions



class LeadingOnes(TestProblem):
    """Counts the number of contiguous ones from the start of the bit-string."""

    def __init__(self, num_variables=30, phenome_preprocessor=None, **kwargs):
        """Constructor.

        Parameters
        ----------
        num_variables : int, optional
            The search space dimension.
        phenome_preprocessor : callable, optional
            A callable potentially applying transformations or checks to
            the phenome. Modifications should only be applied to a copy
            of the input. The (modified) phenome must be returned.
            Default behavior is to do no processing.
        kwargs
            Arbitrary keyword arguments, passed through to the constructor
            of the super class.

        """
        preprocessor = BinaryChecker(num_variables, phenome_preprocessor)
        TestProblem.__init__(self,
                             leading_ones,
                             num_objectives=1,
                             phenome_preprocessor=preprocessor,
                             **kwargs)
        self.num_variables = num_variables
        self.is_deterministic = True
        self.do_maximize = True


    def get_optimal_solutions(self, max_number=None):
        """Return the optimal solution.

        The returned solution does not yet contain the objective values.

        Returns
        -------
        solutions : list of Individual

        """
        assert max_number is None or max_number > 0
        opt = Individual([1] * self.num_variables)
        return [opt]


    get_locally_optimal_solutions = get_optimal_solutions



class LeadingOnesTrailingZeros(TestProblem):
    """A bi-objective binary problem."""

    def __init__(self, num_variables=30, phenome_preprocessor=None, **kwargs):
        """Constructor.

        Parameters
        ----------
        num_variables : int, optional
            The search space dimension.
        phenome_preprocessor : callable, optional
            A callable potentially applying transformations or checks to
            the phenome. Modifications should only be applied to a copy
            of the input. The (modified) phenome must be returned.
            Default behavior is to do no processing.
        kwargs
            Arbitrary keyword arguments, passed through to the constructor
            of the super class.

        """
        preprocessor = BinaryChecker(num_variables, phenome_preprocessor)
        TestProblem.__init__(self,
                             [leading_ones, trailing_zeros],
                             num_objectives=2,
                             phenome_preprocessor=preprocessor,
                             **kwargs)
        self.num_variables = num_variables
        self.is_deterministic = True
        self.do_maximize = True


    def get_optimal_solutions(self, max_number=None):
        """Return Pareto-optimal solutions.

        The returned solutions do not yet contain the objective values.

        Parameters
        ----------
        max_number : int, optional
            Optionally restrict the number of solutions.

        Returns
        -------
        solutions : list of Individual
            The Pareto-optimal solutions

        """
        assert max_number is None or max_number > 0
        individuals = []
        for i in range(self.num_variables + 1):
            opt = Individual([1] * i + [0] * (self.num_variables - i))
            individuals.append(opt)
        if max_number is not None:
            individuals = individuals[:max_number]
        return individuals



class Peak(list):
    """Helper class maintaining the data structures needed for one peak.

    Inherits from :class:`list`. The stored data is the position.

    """
    def __init__(self, position=None, slope=1.0, offset=0.0):
        """Constructor.

        Parameters
        ----------
        position : sequence, optional
            A point in the search space that will attain the maximum of
            this peak. If omitted, a position will be drawn random
            uniformly in the search space.
        slope : float, optional
            The slope of this peak.
        offset : float, optional
            The offset of this peak.

        """
        list.__init__(self, position)
        self.slope = slope
        self.offset = offset


    def function(self, phenome):
        dist = hamming_dist(phenome, self)
        return self.slope * (len(phenome) - dist) + self.offset



class PeakProblem(TestProblem):
    """Abstract base class for binary multiple-peaks problems."""

    def __init__(self, num_variables=10, peaks=None, **kwargs):
        """Constructor.

        Parameters
        ----------
        num_variables : int, optional
            The search space dimension.
        peaks : sequence of Peak
            Previously prepared peaks. If None, a few peaks are generated
            randomly.
        kwargs
            Arbitrary keyword arguments, passed through to the constructor
            of the super class.

        """
        TestProblem.__init__(self,
                             self.objective_function,
                             num_objectives=1,
                             **kwargs)
        self.num_variables = num_variables
        if peaks is None:
            peaks = self.rand_uniform_peaks(num_variables=num_variables)
        for peak in peaks:
            assert len(peak) == num_variables
        self.peaks = peaks
        self.is_deterministic = True


    @classmethod
    def rand_uniform_peaks(cls,
                           num_peaks=2,
                           num_variables=10,
                           slope_range=(1.0, 1.0),
                           offset_range=(0.0, 0.0)):
        """Create peaks with random uniform distribution.

        Parameters
        ----------
        num_peaks : int, optional
            The number of peaks to generate.
        num_variables : int, optional
            The number of decision variables of the search space.
        slope_range : tuple of float, optional
            The slope parameter of peaks is drawn random uniformly from this
            range.
        offset_range : tuple of float, optional
            The offset parameter of peaks is drawn random uniformly from this
            range.

        Returns
        -------
        peaks : list of Peak

        """
        assert num_peaks >= 0
        assert num_variables > 0
        peaks = []
        for _ in range(num_peaks):
            position = [random.randint(0, 1) for _ in range(num_variables)]
            peaks.append(Peak(position,
                              random.uniform(*slope_range),
                              random.uniform(*offset_range)))
        return peaks


    def get_closest_peaks(self, phenome):
        """Return all closest peaks in terms of hamming distance to `phenome`.

        Parameters
        ----------
        phenome : iterable
            The solution to which the distances are computed.

        Returns
        -------
        closest_peaks : list of Peak

        """
        closest_peaks = []
        min_distance = float("inf")
        for peak in self.peaks:
            distance = hamming_dist(phenome, peak)
            if distance < min_distance:
                min_distance = distance
                closest_peaks = [peak]
            if distance == min_distance:
                closest_peaks.append(peak)
        return closest_peaks


    def get_locally_optimal_solutions(self, max_number=None):
        """Return locally optimal solutions (includes global ones).

        Parameters
        ----------
        max_number : int, optional
            Potentially restrict the number of optima.

        Returns
        -------
        optima : list of Individual

        """
        local_optima = []
        for peak in self.peaks:
            peak_obj_value = self.objective_function(peak)
            all_worse_or_equal = True
            for i in range(len(peak)):
                neighbor = peak[:]
                neighbor[i] = not neighbor[i]
                if self.objective_function(neighbor) > peak_obj_value:
                    all_worse_or_equal = False
                    break
            if all_worse_or_equal:
                local_optima.append(Individual(phenome=list(peak)))
            if max_number is not None:
                local_optima = local_optima[:max_number]
        return local_optima


    def get_optimal_solutions(self, max_number=None):
        """Return globally optimal solutions.

        Parameters
        ----------
        max_number : int, optional
            Potentially restrict the number of optima.

        Returns
        -------
        optima : list of Individual

        """
        # test peaks
        optima = []
        max_obj_value = float("-inf")
        opt_phenomes = []
        for peak in self.peaks:
            peak_obj_value = self.objective_function(peak)
            if peak_obj_value > max_obj_value:
                opt_phenomes = [peak]
                max_obj_value = peak_obj_value
            elif peak_obj_value == max_obj_value:
                opt_phenomes.append(peak)
        for phenome in opt_phenomes:
            optima.append(Individual(phenome=list(phenome)))
        if max_number is not None:
            optima = optima[:max_number]
        return optima



class NearestPeakProblem(PeakProblem):
    """A binary test problem with a controllable number of local optima.

    In this problem the nearest peak is responsible for the objective
    value of a solution. The mathematical definition can be found in
    [Jansen2016]_.

    References
    ----------
    .. [Jansen2016] Thomas Jansen; Christine Zarges (2016). Example
        Landscapes to Support Analysis of Multimodal Optimisation. In:
        Parallel Problem Solving from Nature - PPSN XIV, pp. 792-802,
        Springer. https://dx.doi.org/10.1007/978-3-319-45823-6_74

    """
    def objective_function(self, phenome):
        """Return the function value for the nearest peak.

        Parameters
        ----------
        phenome : sequence of float
            The solution to be evaluated.

        Returns
        -------
        objective_value : float

        """
        assert len(phenome) == self.num_variables
        active_peak = self.get_active_peak(phenome)
        return active_peak.function(phenome)


    def get_active_peak(self, phenome):
        """Return the peak modeling the function at `phenome`."""
        assert len(phenome) == self.num_variables
        closest_peaks = self.get_closest_peaks(phenome)
        active_peak = closest_peaks[0]
        max_function_value = active_peak.function(phenome)
        for peak in closest_peaks:
            function_value = peak.function(phenome)
            if function_value > max_function_value:
                max_function_value = function_value
                active_peak = peak
        return active_peak


    get_basin = get_active_peak



class WeightedNearestPeakProblem(PeakProblem):
    """A multimodal binary test problem.

    The objective value is determined by the peak with the highest function
    value at a given position. This approach is analogous to
    :class:`optproblems.mpm.MultiplePeaksModel2`. The mathematical
    definition can be found in [Jansen2016]_.

    """
    def objective_function(self, phenome):
        """Return the maximal peak function.

        Parameters
        ----------
        phenome : sequence of float
            The solution to be evaluated.

        Returns
        -------
        objective_value : float

        """
        assert len(phenome) == self.num_variables
        return max(peak.function(phenome) for peak in self.peaks)


    def get_active_peak(self, phenome):
        """Return the peak modeling the function at `phenome`."""
        assert len(phenome) == self.num_variables
        active_peak = self.peaks[0]
        max_function_value = active_peak.function(phenome)
        for peak in self.peaks:
            function_value = peak.function(phenome)
            if function_value > max_function_value:
                max_function_value = function_value
                active_peak = peak
        return active_peak


    def get_basin(self, phenome):
        """Return the peak in whose attraction basin `phenome` is located.

        For this problem, the attraction basin may consist of several
        overlaid peaks. This method only yields an approximation, i.e., the
        returned peak may be not the one an ideal steepest descent algorithm
        would converge to.

        """
        get_active_peak = self.get_active_peak
        previous_peak = list(phenome)
        current_peak = get_active_peak(previous_peak)
        while previous_peak != current_peak:
            previous_peak = current_peak
            current_peak = get_active_peak(current_peak)
        return current_peak



class AllPeaksProblem(PeakProblem):
    """A multimodal binary test problem.

    In this case the landscape is generated by averaging all the peaks.
    Thus, the local optima of this problem are unknown and global optima are
    only known in the special case of identical slopes for all peaks.
    The mathematical definition can be found in [Jansen2016]_.

    """
    def objective_function(self, phenome):
        """Aggregate the function values of all peak functions.

        Parameters
        ----------
        phenome : sequence of float
            The solution to be evaluated.

        Returns
        -------
        objective_value : float

        """
        assert len(phenome) == self.num_variables
        return sum(peak.function(phenome) for peak in self.peaks)


    def get_active_peak(self, phenome):
        raise NotImplementedError()


    def get_basin(self, phenome):
        raise NotImplementedError()


    def get_locally_optimal_solutions(self, max_number=None):
        raise NotImplementedError()


    def get_optimal_solutions(self, max_number=None):
        raise NotImplementedError()
