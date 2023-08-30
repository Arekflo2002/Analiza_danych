import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Iterable, List, Dict, Optional, Union



class Vector:
    """
        This class is supposed to get X and Y variable and calculate R and R0 for the variables 
    """

    def __init__(self, listof_X, Y ):
        self.vector_R = self.calculating_vector_R(listof_X)
        self.vector_R0 = self.calculating_vector_R0(listof_X,Y)


    def filling_na_values(self,df):
        """
            Filling the blank spaces in data that was inputed
        """

    #region Calculating R vector

    def checking_data(self,listOf_X):
        """
            The goal of this funciton is to check all of the errors that can happen when creating coeffcient matrix, and catch them here
            or transform the data a little
        """
        pass


    def calculating_vector_R(self,listOf_X):
        """
            Function has a choice, whether the variables are stored as columns or rows. More info inside numpyp.corrceof function 
        """

        return np.corrcoef(listOf_X,rowvar=False)

    #endregion


    def calculating_vector_R0(self,listOf_X,Y):
        """
            For every X variable I will calculate a coeff
        """
        coeffs = []
        for X in listOf_X.columns:
            coeff = np.corrcoef(listOf_X[X],Y["Y"],rowvar=True)
            
            coeffs.append(coeff[0][1])
        
        return coeffs


class Hellwig:

    def __init__(self,listOf_X,Y):
        self.vector = Vector(listOf_X,Y)

        self.main_algorithm(listOf_X)

    def main_algorithm(self,listOf_X):
        self.combination = pow(2,listOf_X.shape[1]) - 1
        



if __name__ == "__main__":
    X = [
        [1,2,4,8],
        [13,3,2,2],
        [1,3,4,5],
        [5,4,3,2]
    ]

    X = pd.DataFrame(X,columns = ["X1","X2","X3","X4"])

    X.dropna(inplace=True)
    Y = [1,2,3,4]
    Y = pd.DataFrame(Y,columns=["Y"])
    print(X,"\n",Y,"\n")

    obj = Hellwig(X,Y)

    print(obj.combination)