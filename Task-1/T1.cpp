
#include <bits/stdc++.h>
#include <iostream>
#include <omp.h>


using namespace std;

const int sizen = 1000;
long long costMatrixA[sizen][sizen];
long long costMatrixB[sizen][sizen];

long long productMat[sizen][sizen];

long long resultA[sizen][sizen];
long long resultB[sizen][sizen];


//Simple recursion  which returns the minimum cost of going from i,j to n,n
long long FindMinCostA(int i, int j, int n)
{
    //going out of bounds
    if (i >= n)
        return 10*n + 1;
    //going out of bounds
    if (j >= n)
        return 10*n + 1;
    //reaching the last cell
    if (i == n - 1 && j == n - 1)
        return costMatrixA[i][j];
    //Memoization 
    if(resultA[i][j] == 0)
    {
        resultA[i][j] = costMatrixA[i][j] + min(FindMinCostA(i + 1, j, sizen), FindMinCostA(i, j + 1, sizen));
        return resultA[i][j];
    }
    return resultA[i][j];
}

//Simple recursion which returns the maximum cost of going from i,j to n,n
long long FindMaxCostB(int i, int j, int n)
{
    //going out of bounds
    if (i >= n)
        return 0;
    //going out of bounds
    if (j >= n)
        return 0;
    //reaching the last cell
    if(i != n - 1 && j == n - 1)
        return costMatrixB[i][j];
    //Memoization
    if(resultB[i][j] == 0)
    {
        resultB[i][j] = costMatrixB[i][j] + max(FindMaxCostB(i + 1, j, sizen), FindMaxCostB(i, j + 1, sizen));
        return resultB[i][j];
    }
    return resultB[i][j];
}

int main()
{
    int i, j, k;
    srand(time(0));
    omp_set_num_threads(omp_get_num_procs());
    // initialisation
    for (i = sizen - 1; i >= 0; i--)
    {
        for (j = sizen - 1; j >=0; j--)
        {
            costMatrixA[i][j] = 1 + rand() % 10;
            costMatrixB[i][j] = 1 + rand() % 10;
            productMat[i][j] = 0;
            resultA[i][j] = FindMinCostA(i, j, sizen);
            resultB[i][j] = FindMaxCostB(i, j, sizen);
        }
    }
    //creating productMat as explained in the beginning
    #pragma omp parallel for private(i,j,k) shared(resultA, resultB, productMat)
    for (i = 0; i < sizen; i++)
    {
        // loops swapped to avoid cache misses
        //#pragma omp parallel for private(i,j,k) shared(resultA, resultB, productMat)
        for (k = 0; k < sizen; k++)
        {
            for (j = 0; j < sizen; j++)
                productMat[i][j] += resultA[i][k] * resultB[k][j];
        }
    }
    //filter of size 4 x n
    long long filterArray[4][sizen];
    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < sizen; j++)
            filterArray[i][j] = rand() % 2;
    }
    // matrix of dimension (sizen/c) x 1 where c = 4
    long long finalMat[sizen / 4];

    // applying the filter
    int filterRow;
    #pragma omp parallel for private(i,j, filterRow) shared(productMat, finalMat, filterArray)
    for (i = 0; i < sizen - 4; i += 4)
    {
        // dot product of 4xn portion of productMat
        
        for (j = 0; j < sizen; j++)
        {
            for (filterRow = 0; filterRow < 4; filterRow++)
            {
                finalMat[i / 4] += productMat[i + filterRow][j] * filterArray[filterRow][j];
            }
        }
    }

    return 0;
}