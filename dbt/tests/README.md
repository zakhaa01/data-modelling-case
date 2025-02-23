# DBT Tests
## Overview
This directory handles project specific tests.
> e.g. Test for expected daily number of rows.  

It's highly couraged to introduce as many tests as project requires. Consider increasing number and depth of tests for complex and big DBT projects.  
For more information on user defined tests discover [official DBT Docs](https://docs.getdbt.com/docs/build/data-tests)

## Singular tests
Single tests against project's models. Supposed to be used when there is no need or possibility for generic tests.  

## Generic tests
Scalable and adaptive tests that can be used against multiple models. More advanced method of data validation that allows more standardized way of organazing data quality checks.
