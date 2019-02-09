library(ggplot2)
library(ggthemes)

df <- read.csv('../../../Files/GoalsPerOutcomes.csv', head=T)


ggplot() +
  theme_bw() +
  scale_x_discrete(breaks=c('Win', 'Draw', 'Lose'), limits=c('Win', 'Draw', 'Lose')) +
  geom_col(data=df, aes(x=outcome, y=goalspergame, fill=home_away), position="dodge", width=.5) +
  ylab("Goals per game") +
  scale_fill_discrete(name=NULL, labels=c("Away team", "Home team"))
