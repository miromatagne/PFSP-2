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

rii.deviations <- append(rii.percentage.deviation.100,rii.percentage.deviation.50)
#rii.deviations

ils.results.50 <- read.csv("./Measures/ILS/1/30/average_1_30.csv")
ils.results.50 <- subset(ils.results.50,grepl("50",instance))

ils.results.100 <- read.csv("./Measures/ILS/6/10/average_6_10.csv")
ils.results.100 <- subset(ils.results.100,grepl("100",instance))

ils.percentage.deviation.50 <- 100 * (ils.results.50$solution-best.known.50$BS) / best.known.50$BS
ils.percentage.deviation.100 <- 100 * (ils.results.100$solution-best.known.100$BS) / best.known.100$BS

ils.deviations <- append(ils.percentage.deviation.100,ils.percentage.deviation.50)

deviations.df <- cbind(best.known$oiiProblem,rii.deviations)
deviations.df <- cbind(deviations.df,ils.deviations)
deviations.df
colnames(deviations.df) <- c("Instance", "RII Percentage deviation","ILS Percentage Deviation")
write.csv(deviations.df,paste("./wilcoxon_test_data",sep=''), row.names = FALSE)

w.50 <- wilcox.test(rii.percentage.deviation.50, ils.percentage.deviation.50, paired=T)$p.value
w.100 <- wilcox.test(rii.percentage.deviation.100, ils.percentage.deviation.100, paired=T)$p.value

print("Wilcoxon test for 50 jobs (p-value) :")
w.50
print("Wilcoxon test for 100 jobs (p-value) :")
w.100



