library(ggplot2)
library(ggthemes)

x <- seq(-3, 3, 0.1)
p1 <- dnorm(x, mean=-0.4)
p2 <- dnorm(x, mean=0.7)
df <- data.frame(x=x, p1=p1, p2=p2)

ggplot(df, aes(x=x)) +
  theme_bw() +
  geom_line(aes(y=p1)) + 
  geom_area(aes(y=p1, fill=rgb(1,0,0), alpha=.3)) +
  geom_line(aes(y=p2)) +
  geom_area(aes(y=p2, fill=rgb(0,0,1), alpha=.3)) +
  scale_fill_discrete(name=NULL, labels=c("Player A", "Player B")) +
  guides(alpha=FALSE) +
  xlab("Rating") +
  ylab("Skill probability")
