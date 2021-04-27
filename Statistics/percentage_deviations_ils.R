this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
gammas <- c(2, 4, 8, 10)
best.known <- read.csv("bestSolutions.txt")
best.known.50 <- subset(best.known,grepl("50",oiiProblem))
best.known.100 <- subset(best.known,grepl("100",oiiProblem))

deviations.50 <- c()
deviations.100 <- c()

for(g in gammas) {
  print("Lambda = 3 (50 jobs) :")
  average.file <- read.csv(paste("./Measures/ILS/",g,"/30/average_",g,"_30.csv",sep=''))
  percentage.deviation <- 100 * (average.file$solution-best.known.50$BS) / best.known.50$BS
  print(paste("Gamma :",g))
  print(paste("Average percentage deviation :"))
  print(mean(percentage.deviation))
  
  #df <- cbind(average.file$instance,percentage.deviation)
  #colnames(df) <- c("Instance", "Percentage deviation")
  #write.csv(df,paste("./rii_random_",p,".csv",sep=''), row.names = FALSE)
  
  average.file.50 <- subset(average.file,grepl("50",instance))
  average.file.100 <- subset(average.file,grepl("100",instance))
  percentage.deviation.50 <- 100 * (average.file.50$solution-best.known.50$BS) / best.known.50$BS
  percentage.deviation.100 <- 100 * (average.file.100$solution-best.known.100$BS) / best.known.100$BS
  
  print(paste("Average percentage deviation for 50 jobs :",mean(percentage.deviation.50)))
  print(paste("Average percentage deviation for 100 jobs :",mean(percentage.deviation.100)))
  
  deviations.50 <- c(deviations.50,mean(percentage.deviation.50))
  deviations.100 <- c(deviations.100,mean(percentage.deviation.100))
}

#par(mar=c(5,6,4,1)+.1)
#x <- barplot(deviations.50,names.arg=probabilities,col="lightblue",main="Percentage deviations for 50 jobs", ylab="Percentage deviation (%)",ylim=c(0,30),cex.lab=2.5,cex.main=4,cex.axis=2,cex.names=2.5)
#y <- as.matrix(deviations.50)
#text(x,y+2,labels=as.character(round(y,digits=2)),cex=4)

#x <- barplot(deviations.100,names.arg=probabilities,col="lightblue",main="Percentage deviations for 100 jobs", ylab="Percentage deviation (%)",ylim=c(0,50),cex.lab=2.5,cex.main=4,cex.axis=2,cex.names=2.5)
#y <- as.matrix(deviations.100)
#text(x,y+2,labels=as.character(round(y,digits=2)),cex=4)

#deviations.50 <- c()
#deviations.100 <- c()

#for(g in gammas) {
  #print("Lambda = 6 (100 jobs) :")
  #average.file <- read.csv(paste("./Measures/ILS/6/",g,"/average_6_",g,".csv",sep=''))
  #percentage.deviation <- 100 * (average.file$solution-best.known.100$BS) / best.known.100$BS
  #print(paste("Gamma :",g))
  #print(paste("Average percentage deviation :"))
  #print(mean(percentage.deviation))
  
  #df <- cbind(average.file$instance,percentage.deviation)
  #colnames(df) <- c("Instance", "Percentage deviation")
  #write.csv(df,paste("./rii_srz_",p,".csv",sep=''), row.names = FALSE)
  
  #average.file.50 <- subset(average.file,grepl("50",instance))
  #average.file.100 <- subset(average.file,grepl("100",instance))
  #percentage.deviation.50 <- 100 * (average.file.50$solution-best.known.50$BS) / best.known.50$BS
  #percentage.deviation.100 <- 100 * (average.file.100$solution-best.known.100$BS) / best.known.100$BS
  
  #print(paste("Average percentage deviation for 50 jobs :",mean(percentage.deviation.50)))
  #print(paste("Average percentage deviation for 100 jobs :",mean(percentage.deviation.100)))
  
  #deviations.50 <- c(deviations.50,mean(percentage.deviation.50))
  #deviations.100 <- c(deviations.100,mean(percentage.deviation))
#}


x <- barplot(deviations.50,names.arg=gammas,col="lightblue",main="Percentage deviations for 50 jobs (lambda = 30)", ylab="Percentage deviation (%)",ylim=c(0,6),cex.lab=2.5,cex.main=3,cex.axis=2,cex.names=2.5)
y <- as.matrix(deviations.50)
text(x,y+0.3,labels=as.character(round(y,digits=2)),cex=4)

x <- barplot(deviations.100,names.arg=gammas,col="lightblue",main="Percentage deviations for 100 jobs (lambda = 30)", ylab="Percentage deviation (%)",ylim=c(0,6),cex.lab=2.5,cex.main=3,cex.axis=2,cex.names=2.5)
y <- as.matrix(deviations.100)
text(x,y+0.3,labels=as.character(round(y,digits=2)),cex=4)


this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
gammas <- c(10,20,30)
best.known <- read.csv("bestSolutions.txt")
best.known.50 <- subset(best.known,grepl("50",oiiProblem))
best.known.100 <- subset(best.known,grepl("100",oiiProblem))

deviations.50 <- c()
deviations.100 <- c()

for(g in gammas) {
  print("Lambda = 3 (50 jobs) :")
  average.file <- read.csv(paste("./Measures/ILS/3/",g,"/average_3_",g,".csv",sep=''))
  percentage.deviation <- 100 * (average.file$solution-best.known.50$BS) / best.known.50$BS
  print(paste("Gamma :",g))
  print(paste("Average percentage deviation :"))
  print(mean(percentage.deviation))
  
  #df <- cbind(average.file$instance,percentage.deviation)
  #colnames(df) <- c("Instance", "Percentage deviation")
  #write.csv(df,paste("./rii_random_",p,".csv",sep=''), row.names = FALSE)
  
  #average.file.50 <- subset(average.file,grepl("50",instance))
  #average.file.100 <- subset(average.file,grepl("100",instance))
  #percentage.deviation.50 <- 100 * (average.file.50$solution-best.known.50$BS) / best.known.50$BS
  #percentage.deviation.100 <- 100 * (average.file.100$solution-best.known.100$BS) / best.known.100$BS
  
  #print(paste("Average percentage deviation for 50 jobs :",mean(percentage.deviation.50)))
  #print(paste("Average percentage deviation for 100 jobs :",mean(percentage.deviation.100)))
  
  deviations.50 <- c(deviations.50,mean(percentage.deviation))
  #deviations.100 <- c(deviations.100,mean(percentage.deviation.100))
}

#par(mar=c(5,6,4,1)+.1)
#x <- barplot(deviations.50,names.arg=probabilities,col="lightblue",main="Percentage deviations for 50 jobs", ylab="Percentage deviation (%)",ylim=c(0,30),cex.lab=2.5,cex.main=4,cex.axis=2,cex.names=2.5)
#y <- as.matrix(deviations.50)
#text(x,y+2,labels=as.character(round(y,digits=2)),cex=4)

#x <- barplot(deviations.100,names.arg=probabilities,col="lightblue",main="Percentage deviations for 100 jobs", ylab="Percentage deviation (%)",ylim=c(0,50),cex.lab=2.5,cex.main=4,cex.axis=2,cex.names=2.5)
#y <- as.matrix(deviations.100)
#text(x,y+2,labels=as.character(round(y,digits=2)),cex=4)

#deviations.50 <- c()
#deviations.100 <- c()

for(g in gammas) {
  print("Lambda = 6 (100 jobs) :")
  average.file <- read.csv(paste("./Measures/ILS/6/",g,"/average_6_",g,".csv",sep=''))
  percentage.deviation <- 100 * (average.file$solution-best.known.100$BS) / best.known.100$BS
  print(paste("Gamma :",g))
  print(paste("Average percentage deviation :"))
  print(mean(percentage.deviation))
  
  #df <- cbind(average.file$instance,percentage.deviation)
  #colnames(df) <- c("Instance", "Percentage deviation")
  #write.csv(df,paste("./rii_srz_",p,".csv",sep=''), row.names = FALSE)
  
  #average.file.50 <- subset(average.file,grepl("50",instance))
  #average.file.100 <- subset(average.file,grepl("100",instance))
  #percentage.deviation.50 <- 100 * (average.file.50$solution-best.known.50$BS) / best.known.50$BS
  #percentage.deviation.100 <- 100 * (average.file.100$solution-best.known.100$BS) / best.known.100$BS
  
  #print(paste("Average percentage deviation for 50 jobs :",mean(percentage.deviation.50)))
  #print(paste("Average percentage deviation for 100 jobs :",mean(percentage.deviation.100)))
  
  #deviations.50 <- c(deviations.50,mean(percentage.deviation.50))
  deviations.100 <- c(deviations.100,mean(percentage.deviation))
}

x <- barplot(deviations.50,names.arg=gammas,col="lightblue",main="Percentage deviations for 50 jobs (gamma = 3)", ylab="Percentage deviation (%)",ylim=c(0,6),cex.lab=2.5,cex.main=3,cex.axis=2,cex.names=2.5)
y <- as.matrix(deviations.50)
text(x,y+0.3,labels=as.character(round(y,digits=2)),cex=4)

x <- barplot(deviations.100,names.arg=gammas,col="lightblue",main="Percentage deviations for 100 jobs (gamma = 6)", ylab="Percentage deviation (%)",ylim=c(0,6),cex.lab=2.5,cex.main=3,cex.axis=2,cex.names=2.5)
y <- as.matrix(deviations.100)
text(x,y+0.3,labels=as.character(round(y,digits=2)),cex=4)






