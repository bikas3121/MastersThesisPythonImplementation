# MastersThesisPythonImplementation

This repository contains the python/gurobi implementation of the masters thesis. All the relevant files are present in the repository.

## Thesis Details:
In industrial processes as well as logistics applications, it is often required to allocate small rectangular items to larger rectangular items with a minimum waste. For example, in textile or paper manufacturing, standardized roll of cloths or cardboard are given and one needs to obtain certain required items by using a minimum roll length. In many applications, standard stock units are generally large rectangular sheets of one or few different sizes and the goal is to minimize the total area of the sheets necessary to produce given amounts of small rectangles of given sizes.

In literature, the relevant optimization models are referred to as two-dimensional (2D) B IN PACKING or
C UTTING STOCK problems, the difference lying in the number of each small item required (one or few units in the former case and many in the latter). In fact, those models extends well beyond stock cutting applica- tions, and include task scheduling, VLSI design, image processing, packing goods in crates, commercials assignment to TV breaks, truck loading, just to name a few.

For computational implementation, we use the benchmark data sets provided in
[Beasley](/AnExactTwo-DimensionalNonGuillotineCutting.pdf). 
The algorithm was programmed in Python and solved using GUROBI optimizer. There are two pythons files one provides the [horizontal relaxation](/relaxation_horizontal.py) and other the [vertical relaxation](/relaxation_vertical.py). 

#### Please see the [Master's Thesis](/MastersThesis.pdf) for more details. 



