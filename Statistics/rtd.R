this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)
best.known <- read.csv("bestSolutions.txt")
ils.rtd.files <- list.files("./RTD/ILS",pattern = "*.csv")
rii.rtd.files <- list.files("./RTD/RII", pattern = "*.csv")

lapply(ils.rtd.files, function(x) {
  name <- paste("./RTD/ILS/",x,sep='')
  file <- read.csv(name)
  times <- 1:1000
  results <- c()
  df <- data.frame(times)
  for(t in 1:length(times)) {
    found <- FALSE
    for(row in 1:nrow(file)) {
      if(file$time[row] > times[t]) {
        found <- TRUE
        if(row > 1) {
          results[t] <- file$solution[row-1]
        }
        else {
          results[t] <- file$solution[1]
        }
        break
      }
    }
    if(!found) {
      results[t] <- file$solution[nrow(file)]
    }
  }
  df <- cbind(df,results)
  write.csv(df,paste("./RTD/ILS/Ordered/ordered_",x,sep=''),row.names = FALSE)
})

lapply(rii.rtd.files, function(x) {
  name <- paste("./RTD/RII/",x,sep='')
  file <- read.csv(name)
  times <- 1:1000
  results <- c()
  df <- data.frame(times)
  for(t in 1:length(times)) {
    found <- FALSE
    for(row in 1:nrow(file)) {
      if(file$time[row] > times[t]) {
        found <- TRUE
        if(row > 1) {
          results[t] <- file$solution[row-1]
        }
        else {
          results[t] <- file$solution[1]
        }
        break
      }
    }
    if(!found) {
      results[t] <- file$solution[nrow(file)]
    }
  }
  df <- cbind(df,results)
  write.csv(df,paste("./RTD/RII/Ordered/ordered_",x,sep=''),row.names = FALSE)
})

ils.first.file <- list.files("./RTD/ILS/Ordered",pattern = "*.50_20_01")
ils.second.file <- list.files("./RTD/ILS/Ordered", pattern="*.50_20_02")
rii.first.file <- list.files("./RTD/RII/Ordered",pattern = "*.50_20_01")
rii.second.file <- list.files("./RTD/RII/Ordered", pattern="*.50_20_02")

count.deviation.0.5 <- numeric(1000)
count.deviation.1 <- numeric(1000)
count.deviation.1.5 <- numeric(1000)
count.deviation.2 <- numeric(1000)
count.deviation.2.5 <- numeric(1000)
count.deviation.3 <- numeric(1000)

lapply(ils.first.file,function(x) {
  name <- paste("./RTD/ILS/Ordered/",x,sep='')
  file <- read.csv(name)
  best.sol <- best.known[best.known$oiiProblem=="50_20_01 ",]$BS
  for(t in 1:nrow(file)) {
    deviation <- 100*(file$results[t] - best.sol)/best.sol
    if(deviation <= 0.5) {
      count.deviation.0.5[t] <<- count.deviation.0.5[t] + 1
    }
    if(deviation <= 1) {
      count.deviation.1[t] <<- count.deviation.1[t] + 1
    }
    if(deviation <= 1.5) {
      count.deviation.1.5[t] <<- count.deviation.1.5[t] + 1
    }
    if(deviation <= 2) {
      count.deviation.2[t] <<- count.deviation.2[t] + 1
    }
    if(deviation <= 2.5) {
      count.deviation.2.5[t] <<- count.deviation.2.5[t] + 1
    }
    if(deviation <= 3) {
      count.deviation.3[t] <<- count.deviation.3[t] + 1
    }
  }
})


count.deviation.0.5 <- count.deviation.0.5 / 26
count.deviation.1 <- count.deviation.1 / 26
count.deviation.1.5 <- count.deviation.1.5 / 26
count.deviation.2 <- count.deviation.2 / 26
count.deviation.2.5 <- count.deviation.2.5 / 26
count.deviation.3 <- count.deviation.3 / 26

#plot(1:1000,count.deviation.1,cex=1)
#lines(1:1000, count.deviation.1, pch=16)

x <- 1:1000
lo.0.5 <- loess(count.deviation.0.5~x)
p.lo.0.5 <- predict(lo.0.5)
p.lo.0.5[p.lo.0.5 < 0] <- 0
lo.1 <- loess(count.deviation.1~x)
p.lo.1 <- predict(lo.1)
p.lo.1[p.lo.1 < 0] <- 0
lo.1.5 <- loess(count.deviation.1.5~x)
p.lo.1.5 <- predict(lo.1.5)
p.lo.1.5[p.lo.1.5 < 0] <- 0
lo.2 <- loess(count.deviation.2~x)
p.lo.2 <- predict(lo.2)
p.lo.2[p.lo.2 < 0] <- 0
lo.2.5 <- loess(count.deviation.2.5~x)
p.lo.2.5 <- predict(lo.2.5)
p.lo.2.5[p.lo.2.5 < 0] <- 0

par(mar=c(5,6,4,1)+.1)
plot(1:1000,count.deviation.1,log="x",ylim=c(0,1),col='white',xlab="Execution time (s)",ylab="P(solve)",main="Qualified Runtime Distribution with ILS (50_20_01)")
lines(p.lo.0.5, col='black', lty="solid", lwd=2)
lines(p.lo.1, col='black', lty="dashed", lwd=2)
lines(p.lo.1.5, col='black', lty="dotted", lwd=2)
lines(p.lo.2, col='black', lty="dotdash", lwd=2)
legend(1, 1, legend=c("0.5%", "1%", "1.5%","2%"), lty=1:4, cex=1,pt.cex = 3)

count.deviation.0.5 <- numeric(1000)
count.deviation.1 <- numeric(1000)
count.deviation.1.5 <- numeric(1000)
count.deviation.2 <- numeric(1000)
count.deviation.2.5 <- numeric(1000)
count.deviation.3 <- numeric(1000)

lapply(ils.second.file,function(x) {
  name <- paste("./RTD/ILS/Ordered/",x,sep='')
  file <- read.csv(name)
  best.sol <- best.known[best.known$oiiProblem=="50_20_02 ",]$BS
  for(t in 1:nrow(file)) {
    deviation <- 100*(file$results[t] - best.sol)/best.sol
    if(deviation <= 0.5) {
      count.deviation.0.5[t] <<- count.deviation.0.5[t] + 1
    }
    if(deviation <= 1) {
      count.deviation.1[t] <<- count.deviation.1[t] + 1
    }
    if(deviation <= 1.5) {
      count.deviation.1.5[t] <<- count.deviation.1.5[t] + 1
    }
    if(deviation <= 2) {
      count.deviation.2[t] <<- count.deviation.2[t] + 1
    }
    if(deviation <= 2.5) {
      count.deviation.2.5[t] <<- count.deviation.2.5[t] + 1
    }
    if(deviation <= 3) {
      count.deviation.3[t] <<- count.deviation.3[t] + 1
    }
  }
})


count.deviation.0.5 <- count.deviation.0.5 / 26
count.deviation.1 <- count.deviation.1 / 26
count.deviation.1.5 <- count.deviation.1.5 / 26
count.deviation.2 <- count.deviation.2 / 26
count.deviation.2.5 <- count.deviation.2.5 / 26
count.deviation.3 <- count.deviation.3 / 26

#plot(1:1000,count.deviation.1,cex=1)
#lines(1:1000, count.deviation.1, pch=16)

x <- 1:1000
lo.0.5 <- loess(count.deviation.0.5~x)
p.lo.0.5 <- predict(lo.0.5)
p.lo.0.5[p.lo.0.5 < 0] <- 0
lo.1 <- loess(count.deviation.1~x)
p.lo.1 <- predict(lo.1)
p.lo.1[p.lo.1 < 0] <- 0
lo.1.5 <- loess(count.deviation.1.5~x)
p.lo.1.5 <- predict(lo.1.5)
p.lo.1.5[p.lo.1.5 < 0] <- 0
lo.2 <- loess(count.deviation.2~x)
p.lo.2 <- predict(lo.2)
p.lo.2[p.lo.2 < 0] <- 0
lo.2.5 <- loess(count.deviation.2.5~x)
p.lo.2.5 <- predict(lo.2.5)
p.lo.2.5[p.lo.2.5 < 0] <- 0

par(mar=c(5,6,4,1)+.1)
plot(1:1000,count.deviation.1,log="x",ylim=c(0,1),col='white',xlab="Execution time (s)",ylab="P(solve)",main="Qualified Runtime Distribution with ILS (50_20_02)")
lines(p.lo.0.5, col='black', lty="solid", lwd=2)
lines(p.lo.1, col='black', lty="dashed", lwd=2)
lines(p.lo.1.5, col='black', lty="dotted", lwd=2)
lines(p.lo.2, col='black', lty="dotdash", lwd=2)
legend(1, 1, legend=c("0.5%", "1%", "1.5%","2%"), lty=1:4, cex=1,pt.cex = 3)

count.deviation.0.5 <- numeric(1000)
count.deviation.1 <- numeric(1000)
count.deviation.1.5 <- numeric(1000)
count.deviation.2 <- numeric(1000)
count.deviation.2.5 <- numeric(1000)
count.deviation.3 <- numeric(1000)

lapply(rii.first.file,function(x) {
  name <- paste("./RTD/RII/Ordered/",x,sep='')
  file <- read.csv(name)
  best.sol <- best.known[best.known$oiiProblem=="50_20_01 ",]$BS
  for(t in 1:nrow(file)) {
    deviation <- 100*(file$results[t] - best.sol)/best.sol
    if(deviation <= 0.5) {
      count.deviation.0.5[t] <<- count.deviation.0.5[t] + 1
    }
    if(deviation <= 1) {
      count.deviation.1[t] <<- count.deviation.1[t] + 1
    }
    if(deviation <= 1.5) {
      count.deviation.1.5[t] <<- count.deviation.1.5[t] + 1
    }
    if(deviation <= 2) {
      count.deviation.2[t] <<- count.deviation.2[t] + 1
    }
    if(deviation <= 2.5) {
      count.deviation.2.5[t] <<- count.deviation.2.5[t] + 1
    }
    if(deviation <= 3) {
      count.deviation.3[t] <<- count.deviation.3[t] + 1
    }
  }
})


count.deviation.0.5 <- count.deviation.0.5 / 26
count.deviation.1 <- count.deviation.1 / 26
count.deviation.1.5 <- count.deviation.1.5 / 26
count.deviation.2 <- count.deviation.2 / 26
count.deviation.2.5 <- count.deviation.2.5 / 26
count.deviation.3 <- count.deviation.3 / 26

#plot(1:1000,count.deviation.1,cex=1)
#lines(1:1000, count.deviation.1, pch=16)

x <- 1:1000
lo.0.5 <- loess(count.deviation.0.5~x)
p.lo.0.5 <- predict(lo.0.5)
p.lo.0.5[p.lo.0.5 < 0] <- 0
lo.1 <- loess(count.deviation.1~x)
p.lo.1 <- predict(lo.1)
p.lo.1[p.lo.1 < 0] <- 0
lo.1.5 <- loess(count.deviation.1.5~x)
p.lo.1.5 <- predict(lo.1.5)
p.lo.1.5[p.lo.1.5 < 0] <- 0
lo.2 <- loess(count.deviation.2~x)
p.lo.2 <- predict(lo.2)
p.lo.2[p.lo.2 < 0] <- 0
lo.2.5 <- loess(count.deviation.2.5~x)
p.lo.2.5 <- predict(lo.2.5)
p.lo.2.5[p.lo.2.5 < 0] <- 0

par(mar=c(5,6,4,1)+.1)
plot(1:1000,count.deviation.1,log="x",ylim=c(0,1),col='white',xlab="Execution time (s)",ylab="P(solve)",main="Qualified Runtime Distribution with RII (50_20_01)")
lines(p.lo.0.5, col='black', lty="solid", lwd=2)
lines(p.lo.1, col='black', lty="dashed", lwd=2)
lines(p.lo.1.5, col='black', lty="dotted", lwd=2)
lines(p.lo.2, col='black', lty="dotdash", lwd=2)
legend(1, 1, legend=c("0.5%", "1%", "1.5%","2%"), lty=1:4, cex=1,pt.cex = 3)


count.deviation.0.5 <- numeric(1000)
count.deviation.1 <- numeric(1000)
count.deviation.1.5 <- numeric(1000)
count.deviation.2 <- numeric(1000)
count.deviation.2.5 <- numeric(1000)
count.deviation.3 <- numeric(1000)

lapply(rii.second.file,function(x) {
  name <- paste("./RTD/RII/Ordered/",x,sep='')
  file <- read.csv(name)
  best.sol <- best.known[best.known$oiiProblem=="50_20_02 ",]$BS
  for(t in 1:nrow(file)) {
    deviation <- 100*(file$results[t] - best.sol)/best.sol
    if(deviation <= 0.5) {
      count.deviation.0.5[t] <<- count.deviation.0.5[t] + 1
    }
    if(deviation <= 1) {
      count.deviation.1[t] <<- count.deviation.1[t] + 1
    }
    if(deviation <= 1.5) {
      count.deviation.1.5[t] <<- count.deviation.1.5[t] + 1
    }
    if(deviation <= 2) {
      count.deviation.2[t] <<- count.deviation.2[t] + 1
    }
    if(deviation <= 2.5) {
      count.deviation.2.5[t] <<- count.deviation.2.5[t] + 1
    }
    if(deviation <= 3) {
      count.deviation.3[t] <<- count.deviation.3[t] + 1
    }
  }
})


count.deviation.0.5 <- count.deviation.0.5 / 26
count.deviation.1 <- count.deviation.1 / 26
count.deviation.1.5 <- count.deviation.1.5 / 26
count.deviation.2 <- count.deviation.2 / 26
count.deviation.2.5 <- count.deviation.2.5 / 26
count.deviation.3 <- count.deviation.3 / 26

#plot(1:1000,count.deviation.1,cex=1)
#lines(1:1000, count.deviation.1, pch=16)

x <- 1:1000
lo.0.5 <- loess(count.deviation.0.5~x)
p.lo.0.5 <- predict(lo.0.5)
p.lo.0.5[p.lo.0.5 < 0] <- 0
lo.1 <- loess(count.deviation.1~x)
p.lo.1 <- predict(lo.1)
p.lo.1[p.lo.1 < 0] <- 0
lo.1.5 <- loess(count.deviation.1.5~x,span=0.1)
p.lo.1.5 <- predict(lo.1.5)
p.lo.1.5[p.lo.1.5 < 0] <- 0
lo.2 <- loess(count.deviation.2~x,span=0.1)
p.lo.2 <- predict(lo.2)
p.lo.2[p.lo.2 < 0] <- 0
lo.2.5 <- loess(count.deviation.2.5~x)
p.lo.2.5 <- predict(lo.2.5)
p.lo.2.5[p.lo.2.5 < 0] <- 0

par(mar=c(5,6,4,1)+.1)
plot(1:1000,count.deviation.2,log="x",ylim=c(0,1),col='white',xlab="Execution time (s)",ylab="P(solve)",main="Qualified Runtime Distribution with RII (50_20_02)")
lines(p.lo.0.5, col='black', lty="solid", lwd=2)
lines(p.lo.1, col='black', lty="dashed", lwd=2)
lines(p.lo.1.5, col='black', lty="dotted", lwd=2)
lines(p.lo.2, col='black', lty="dotdash", lwd=2)
legend(1, 1, legend=c("0.5%", "1%", "1.5%","2%"), lty=1:4, cex=1,pt.cex = 3)




