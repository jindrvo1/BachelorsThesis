library(ggplot2)
library(ggthemes)

df <- data.frame(x=rep(c("Wins","Draws","Loses"), c(9810, 5398, 6166)))
positions <- c("Wins", "Draws", "Loses")
colors <- c("blue3", "green4", "red3")

ggplot(df, aes(x)) +
  theme_bw() + 
  geom_bar(width=0.5, fill = colors) + 
  scale_x_discrete(limits = positions) + 
  xlab("") + 
  ylab("Number of matches")
