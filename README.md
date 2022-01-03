# MastersThesisPythonImplementation

This repository contains the python/gurobi implementation of the masters thesis. All the relevant files are present in the repository.

## Thesis Details:
In industrial processes as well as logistics applications, it is often required to allocate small rectangular items to larger rectangular items with a minimum waste. For example, in textile or paper manufacturing, standardized roll of cloths or cardboard are given and one needs to obtain certain required items by using a minimum roll length. In many applications, standard stock units are generally large rectangular sheets of one or few different sizes and the goal is to minimize the total area of the sheets necessary to produce given amounts of small rectangles of given sizes.

In literature, the relevant optimization models are referred to as two-dimensional (2D) B IN PACKING or
C UTTING STOCK problems, the difference lying in the number of each small item required (one or few units in the former case and many in the latter). In fact, those models extends well beyond stock cutting applica- tions, and include task scheduling, VLSI design, image processing, packing goods in crates, commercials assignment to TV breaks, truck loading, just to name a few.

For computational implementation, we use the benchmark data sets provided in
[Beasley](file://AnExactTwo-DimensionalNonGuillotineCutting.pdf). The instances are divided into four classes.
• Class1: W = H = 10 and wi and hi are random in [1, 10].
• Class2: W = 15, H = 10 and wi and hi are random in [1, 15].
• Class3: W = H = 20 and wi and hi are random in [1, 20].
• Class4: W = H = 30 and wi and hi are random in [1, 30].
where W and H are the width and height of the bin and wi and h i are the width
and height of item i, respectively. Each class of data set has 3 instances with n items
( n = 5, 7, 10 ).
The implementation was made in Intel Core i5-3210M with 8GB of RAM. The
algorithm was programmed in Python and solved using GUROBI optimizer. 
