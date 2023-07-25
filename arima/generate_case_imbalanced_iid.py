import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
from sklearn.model_selection import train_test_split

# Using ARIMA.py
from ARIMA import custom_ARIMA
def arima_custom(hospital, start_year = 2008, end_year = 2019, avg = 200, d =0, t = 0, mu = 0, sigma = 1):
    res = pd.DataFrame()

    for i in range(start_year, end_year):
        start = str(i) + "-01-01"
        end = str(i) + "-12-31"
        df = pd.DataFrame({"Date": pd.date_range(start, end)})
        res = pd.concat([res, df], ignore_index=True)
    
    n = len(res.index)
    phi = np.array([0.4087, -0.5934, -0.3317, -0.2706, -0.2912]) # AR part using 5 lag
    theta = np.array([-1.2007, 0.9153]) # MA part using 2 lag
    # np.random.seed(42) # to get comparable results

    transfused = custom_ARIMA(phi = phi, theta = theta, d = d, t = t, mu = mu, sigma= sigma, n = n) # simulate time series
    transfused = [i[0] + avg for i in transfused]
    min_transfused = min(transfused)
    if min_transfused < 0:
        transfused = -min_transfused + transfused + 1 # add 1 at end because MAPE will blow up if there are zeros
    res["Transfused"] = transfused
    res["Location"] = hospital

    return res

def generate_test():
    res = arima_custom("Random ", mu= 0, d=1, sigma= 6)
    plt.plot(res['Transfused'])
    plt.show()

    transfused_list = res["Transfused"].values.tolist()
    transfused_list = np.diff(res["Transfused"].values.tolist())

    acf_vals = acf(transfused_list)
    num_lags = 10
    plt.bar(range(num_lags), acf_vals[:num_lags])
    plt.show()
    print("Starting training on ARIMA model")
    
    pacf_vals = pacf(transfused_list)
    num_lags = 20
    plt.bar(range(num_lags), pacf_vals[:num_lags])
    plt.show()

    train, test = train_test_split(transfused_list,test_size=0.2, shuffle= False )
    predictions = []
    arima_model = ARIMA(train, order = (5,0, 2))
    model_fit = arima_model.fit()
    predictions = model_fit.forecast(steps = len(test))
    print(model_fit.summary())
    print("Evaluating arima model")

    # print("R2 score: ", r2_score(test, predict))
    # print("RMSE: ", mean_squared_error(test, predict))

    # x = [ i for i in range(len(test))]
    # plt.plot(x, test)
    
    # plt.plot(x, predict)

    x = [i for i in range(len(train) + len(test))]
    plt.plot(x, list(train) + list(test), label = "actual values")
    
    y = list(train) + list(predictions)
    plt.plot(x, y, label = "arima predicted")
    plt.legend()
    plt.show()

def generate_with_arima():
    np.random.seed(42) # to get comparable results
    res = arima_custom("C1", start_year= 1998, end_year=2018, sigma = 20, d=1)
    res.to_csv('./arima/C1.csv')
    plt.plot(res["Transfused"])
    plt.show()

    res = arima_custom("C2", start_year= 2008, end_year=2018, sigma = 20, d=1)
    res.to_csv('./arima/C2.csv')
    plt.plot(res['Transfused'])
    plt.show()

    res = arima_custom("C3", start_year= 2017, end_year=2018,  sigma = 20, d=1)
    res.to_csv("./arima/C3.csv")
    plt.plot(res['Transfused'])
    plt.show()

    res = arima_custom("C4", start_year=2013, end_year=2018, sigma = 20, d=1)
    res.to_csv("./arima/C4.csv")
    plt.plot(res['Transfused'])
    plt.show()

    res = arima_custom("C5", start_year=1978, end_year=2018, sigma = 20, d=1)
    res.to_csv("./arima/C5.csv")
    plt.plot(res['Transfused'])
    plt.show()

def main():
    generate_with_arima()

if __name__ == "__main__":
    main()