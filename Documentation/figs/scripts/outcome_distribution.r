library(ggplot2)
library(ggthemes)

x <- seq(-2, 4, .1)
p1 <- dnorm(x, mean=-0.4)
p2 <- dnorm(x, mean=0.7)
y <- dnorm(x, mean=1.1, sd=sqrt(2))
df <- data.frame(x=x, y=y)

x1 <- seq(-2, 0, .1)
y1 <- dnorm(x1, mean=1.1, sd=sqrt(2))
df1 <- data.frame(x1=x1, y1=y1)

x2 <- seq(0, 4, .1)
y2 <-dnorm(x2, mean=1.1, sd=sqrt(2))
df2 <- data.frame(x2=x2, y2=y2)

ggplot(df, aes(x, y)) +
  theme_bw() +
  geom_line() +
  geom_area(data=df1, aes(x1, y1, fill=rgb(1,0,0), alpha=.3)) +
  geom_area(data=df2, aes(x2, y2, fill=rgb(0,0,1), alpha=.3)) +
  geom_text(x=-0.75, y=0.05, label=paste(100*round(pnorm(0, 1.1, sqrt(2)), digits=4), '%')) +
  geom_text(x=1, y=0.05, label=paste(100*round(1-pnorm(0, 1.1, sqrt(2)), digits=4), '%')) +
  scale_fill_discrete(name=NULL, labels=c("Player A", "Player B")) +
  guides(alpha=FALSE)
