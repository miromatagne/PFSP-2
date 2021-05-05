this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
best.known <- read.csv("bestSolutions.txt")
best.known.50 <- subset(best.known,grepl("50",oiiProblem))
best.known.100 <- subset(best.known,grepl("100",oiiProblem))

rii.results.50 <- read.csv("./Measures/RII/SRZ/0.04/average_0.04.csv")
rii.results.50 <- subset(rii.results.50,grepl("50",instance))

rii.results.100 <- read.csv("./Measures/RII/SRZ/0.02/average_0.02.csv")
rii.results.100 <- subset(rii.results.100,grepl("100",instance))

rii.percentage.deviation.50 <- 100 * (rii.results.50$solution-best.known.50$BS) / best.known.50$BS
rii.percentage.deviation.100 <- 100 * (rii.results.100$solution-best.known.100$BS) / best.known.100$BS

ils.results.50 <- read.csv("./Measures/ILS/1/30/average_1_30.csv")
ils.results.50 <- subset(ils.results.50,grepl("50",instance))

ils.results.100 <- read.csv("./Measures/ILS/6/10/average_6_10.csv")
ils.results.100 <- subset(ils.results.100,grepl("100",instance))

ils.percentage.deviation.50 <- 100 * (ils.results.50$solution-best.known.50$BS) / best.known.50$BS
ils.percentage.deviation.100 <- 100 * (ils.results.100$solution-best.known.100$BS) / best.known.100$BS

par(mar=c(5,6,4,1)+.1)

plot(rii.percentage.deviation.50,ils.percentage.deviation.50,xlim = c(0,3),ylim = c(0,3),pch=19,main="Correlation plot comparing RII and ILS on instances of 50 jobs",xlab="Average Relative Percentage Deviation RII [%]",ylab="Average Relative Percentage deviation ILS [%]")
abline(a=0,b=1,col="red",lwd=3)
abline(lm(ils.percentage.deviation.50 ~ rii.percentage.deviation.50),col="darkblue",lwd=3)
text(paste("Correlation:", round(cor(rii.percentage.deviation.50, ils.percentage.deviation.50,method = "spearman"), 2)), x = 0.5, y = 2)

cor.test(rii.percentage.deviation.50, ils.percentage.deviation.50,method="spearman")

plot(rii.percentage.deviation.100,ils.percentage.deviation.100,xlim = c(0,4),ylim = c(0,4),pch=19,main="Correlation plot comparing RII and ILS on instances of 100 jobs",xlab="Average Relative Percentage deviation RII [%]",ylab="Average Relative Percentage deviation ILS [%]")
abline(a=0,b=1,col="red",lwd=3)
abline(lm(ils.percentage.deviation.100 ~ rii.percentage.deviation.100),col="darkblue",lwd=3)
text(paste("Correlation:", round(cor(rii.percentage.deviation.100, ils.percentage.deviation.100,method = "spearman"), 2)), x = 1, y = 3)

cor.test(rii.percentage.deviation.100, ils.percentage.deviation.100,method="spearman")


