this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
probabilities <- c(0.1,0.2,0.3,0.4,0.5)
best.known <- read.csv("bestSolutions.txt")
best.known.50 <- subset(best.known,grepl("50",oiiProblem))
best.known.100 <- subset(best.known,grepl("100",oiiProblem))

for(p in probabilities) {
  average.file <- read.csv(paste("./Measures/RII/Random/",p,"/average_",p,".csv",sep=''))
  percentage.deviation <- 100 * (average.file$solution-best.known$BS) / best.known$BS
  print(paste("Probability :",p))
  print(paste("Average percentage deviation :"))
  print(percentage.deviation)
  
  average.file.50 <- subset(average.file,grepl("50",instance))
  average.file.100 <- subset(average.file,grepl("100",instance))
  percentage.deviation.50 <- 100 * (average.file.50$solution-best.known.50$BS) / best.known.50$BS
  percentage.deviation.100 <- 100 * (average.file.100$solution-best.known.100$BS) / best.known.100$BS
  
  print(paste("Average percentage deviation for 50 jobs :",mean(percentage.deviation.50)))
  print(paste("Average percentage deviation for 100 jobs :",mean(percentage.deviation.100)))
}



