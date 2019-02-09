library(ggplot2)
library(ggthemes)

df <- read.csv("../../../Files/Ratings.csv")

ggplot(df, aes(x=df$rating)) +
  theme_bw() +
  geom_bar() +
  xlab("Rating") +
  ylab("Number of players")
