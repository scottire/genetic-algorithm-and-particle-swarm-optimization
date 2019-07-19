Description
===========

This package contains a collection of common benchmark problems for black-box
optimization. Under the term "black-box problem", we understand problems for
which only little is known about their structure and properties. Such problems
usually appear in practice when simulator output or some other complex system
with nonlinear behavior is to be optimized.

Contained test problems:

* Binary problems OneMax, LeadingOnes, and LeadingOnesTrailingZeros and three
  instance generators for multimodal problems
* CEC 2005 collection of single-objective problems
* CEC 2007 collection of multiobjective problems
* Dixon-Szegö collection for global optimization
* DTLZ problems 1-7
* Multiple-Peaks Model 2
* Walking Fish Group (WFG) toolkit
* ZDT collection for multiobjective optimization

Contained real-world problems:

* Configuration of a gradient method on test problem
* Uniformity optimization of points in the unit hypercube


The infrastructure of this package can also be used to wrap your own
(real-world) optimization problems in the problem base class. Reasons to do
this may be the following features:

* Support for single-objective and multi-objective problems
* In general, no assumptions about the search space are made
* Evaluations are automatically counted
* Can use true parallelism or concurrency via multiprocessing(.dummy)
* Provides functionality for checking bound constraints and repairing
  violations of them in continuous optimization
* Optionally: detection and subsequently avoidance of duplicate evaluations


Dependencies
============

Some modules of this package have additional dependencies on third-party
packages. However, these are not enforced during installation not to hinder
the utilization of the base module, which will always be free of dependencies.

===============  =================
Module           Dependencies
===============  =================
base             *none*
binary           *none*
cec2005          numpy
cec2007          numpy, diversipy
continuous       *none*
dtlz             diversipy
mpm              numpy
multiobjective   diversipy
realworld        numpy, diversipy
wfg              diversipy
zdt              diversipy
===============  =================


Documentation
=============

The documentation is located at
https://ls11-www.cs.tu-dortmund.de/people/swessing/optproblems/doc/