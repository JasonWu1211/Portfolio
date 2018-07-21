#Time series - apple stocke price
source("http://www.rmetrics.org/Rmetrics.R")
install.Rmetrics()

# LOAD LIBRARIES
library(tseries)
library(fBasics)
library(zoo)
library(lmtest) # to compute t-test on model parameters
library(forecast)


#a. Exploratory analysis of the data
apple=read.table("day.csv",header=T, sep=',') 
head(apple)
applets=zoo(apple$Adj.Close, as.Date(as.character(apple$Date), format = "%Y-%m-%d"))
head(applets)
basicStats(applets)
par(mfrow=c(2,1))
plot(applets, type='l', ylab = " adj close price", main="Plot of 2002-2017 daily apple stock prices")
acf(coredata(applets))
#log retun of apple stock ts
rets=log(applets/lag(applets, -1))
basicStats(rets)
#normality test
normalTest(rets,method=c("jb"))
#plot returns, square returns and abs(returns)
par(mfrow=c(3,1))
# creates time plot of log returns
plot(rets, type='l', ylab = "price return", main="Plot of 2002-2017 daily apple stock price return")
# time plot of squared returns
plot(rets^2,type='l', ylab = "price return^2", main="Plot of 2002-2017 daily apple stock price squared return")

# time plot of abs returns
plot(abs(rets),type='l', ylab = "abs returns", main="Plot of 2002-2017 daily apple stock price abs return")


# strip off the dates and just create a simple numeric object 
ret = coredata(rets);
head(ret)
# Plots ACF function of vector data
par(mfrow=c(2,2))
acf(ret)
# Plot ACF of squared returns to check for ARCH effect
acf(ret^2)
# Plot ACF of absolute returns to check for ARCH effect 
acf(abs(ret))
#test of independence

#Ljung Box test on ret^2
Box.test(ret, lag=2, type="Ljung")
Box.test(ret, lag=4, type="Ljung")
Box.test(ret, lag=6, type="Ljung")
#Ljung Box test on ret^2
Box.test(ret^2, lag=2, type="Ljung")
Box.test(ret^2, lag=4, type="Ljung")
Box.test(ret^2, lag=6, type="Ljung")

#Ljung Box test on abs(ret)
Box.test(abs(ret), lag=2, type="Ljung")
Box.test(abs(ret), lag=4, type="Ljung")
Box.test(abs(ret), lag=6, type="Ljung")


#b. Model fitting
library(rugarch) 
#Fit ARMA(0,0)-eGARCH(1,1) model with t-distribution
egarch11.t.spec=ugarchspec(variance.model=list(model = "eGARCH", garchOrder=c(1,1)), mean.model=list(armaOrder=c(0,0)), distribution.model = "std")
#estimate model 
egarch11.t.fit=ugarchfit(spec=egarch11.t.spec, data=rets)
egarch11.t.fit
plot(egarch11.t.fit)

f=ugarchforecast(egarch11.t.fit, n.ahead=20)
f
plot(f)

#rolling forecasts
rff=ugarchfit(spec=egarch11.t.spec, data=rets, out.sample=500)
rf=ugarchforecast(rff, n.ahead=20, n.roll=450)
rf
plot(rf)


#backtesting
mod_egarch = ugarchroll(egarch11.t.spec, data = rets, n.ahead = 1,
                        n.start = 2500, refit.every = 200, refit.window = "recursive")

mod_egarch
# type=VaR shows VaR at 1% level: this is the tail probability.
report(mod_egarch, type="VaR", VaR.alpha = 0.01, conf.level = 0.95)



#risk
f
p01=qt(0.01, 5)
p01
r01=100000*exp(0.001257-p01*0.007904)
r01
