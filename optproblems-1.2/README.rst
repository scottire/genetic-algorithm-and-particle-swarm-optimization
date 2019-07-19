
optproblems has been tested with Python 2.7 and 3.6. The recommended version is
Python 3.x, because compatibility is reached by avoiding usage of xrange. So,
the code has a higher memory consumption under Python 2.

Everything in this package is pure Python. For a description of the contents
see DESCRIPTION.rst.


Changes
=======

1.2
---
* Fixed a bug in DTLZ1. Thanks to Julian Blank for the discovery.

1.1
---
* Changed the constructor arguments for Problem pertaining to multiprocessing.
  Instead of the desired number of processes, a pool of worker processes has
  to be supplied to the constructor. The provided pool is stored in an instance
  attribute. This saves a lot of overhead for creating and closing temporary
  worker pools, but requires slightly more know-how on multiprocessing from the
  user.

1.0
---
* Changed the archive in optproblems.base.Cache from dict to
  collections.OrderedDict.
* Added binary multimodal test problems by Jansen and Zarges.
* Added forgotten documentation for doublesum and DoubleSum test problem in
  optproblems.continuous.
* Bugfix in optproblems.realworld.GradientMethodConfiguration.

0.9
---
* Renamed optproblems.real to optproblems.continuous.
* Added module optproblems.realworld containing two real-world problems
  GradientMethodConfiguration and UniformityOptimization.
* Added more exception classes in optproblems.base.
* Made remaining_evaluations and consumed_evaluations writable in
  optproblems.base.Cache (values are written to the cached problem).
* Added forgotten documentation for EllipsoidFunction and Ellipsoid test
  problem in optproblems.continuous.

0.8
---
* Bugfix: added a call to pool.close() and pool.join() in
  Problem.batch_evaluate() to avoid leaking threads.
* Added a ScalingPreprocessor in optproblems.base to transform solutions from
  one hypercube to another. This is useful for normalizing the search space
  while the problem can keep using the native units.

0.7
---
* Fixed a bug in Shekel, Hartman3, Hartman6, and ModifiedRastrigin of
  optproblems.real, which caused that get_optimal_solutions() did not return
  the global optimum, but only a local one.

0.6
---
* Removed imports of submodules (except for base) into the optproblems
  namespace. Only now can optproblems.base be used without having numpy and
  diversipy installed.
* In turn removed the __all__ restriction for wildcard imports.

0.5
---
* Corrected the documentation in some places.
* Added the CEC 2005 test problems for single-objective optimization.
* Added some test problems and functions to module real (partly required by
  cec2005): Griewank, Schaffer6, Schaffer7.
* Restricted wildcard imports to important stuff by using __all__

0.4
---
* New method get_peaks_sorted_by_importance() of MultiplePeaksModel2.
* Added new module `real` containing the collection of Dixon and Szegö and some
  other problems.
* Fixed bug in base.BoundConstraintsChecker, where the previous preprocessor
  was not called before everything else.

0.3
---
* Added new module dtlz with multiobjective DTLZ problems 1-7.
* Added new module cec2007 with problems from the Special Session & Competition
  on Performance Assessment of Multi-Objective Optimization Algorithms at the
  Congress on Evolutionary Computation (CEC), Singapore, 25-28 September 2007.
* The problem classes in base are now (more) agnostic to the return type of the
  objective function, i.e., it is not required for objective functions to return
  sequences anymore.

0.2
---
* Slightly refined Pareto-front sampling for multiobjective test problems.
* Added module wfg with (multiobjective) test problems from the Walking
  Fish Group.

0.1
---
* Initial version containing binary problems, ZDT, and MPM2.
