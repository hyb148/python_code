library("randomForest")
library("yhatr")

df <- read.csv("data/churn.csv")
churn.result <- factor(df$Churn.)

to.drop <- c('State','Area.Code','Phone','Churn.')
churn.feat.space <- df[,!(names(df) %in% to.drop)]

yes.no.cols <- c("Int.l.Plan","VMail.Plan")
churn.feat.space[yes.no.cols] <- churn.feat.space[yes.no.cols] == "yes"

feats <- names(churn.feat.space)

clf <- randomForest(churn.feat.space,y=churn.result)

model.require <- function() {
    library(randomForest)
}

model.transform <- function(df) {
    df <- df[feats]
    df[yes.no.cols] <- df[yes.no.cols] == "yes"
    df 
}

model.predict <- function(df) {
    churn.prob <- predict(clf,newdata=df,type="prob")
    churn.risk <- churn.prob[colnames(churn.prob) == "True."]
    customer.value <- rowSums(df[c("Day.Charge","Eve.Charge","Night.Charge")])
    expected.loss <- churn.risk * customer.value
    data.frame(churn.risk,customer.value,expected.loss)
}

yhat.config  <- c(
  username="USERNAME",
  apikey="APIKEY",
  env="ENTERPRISE URL"
)
yhat.deploy("RChurnModel")
