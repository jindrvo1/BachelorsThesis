library(ggplot2)
library(ggthemes)

df <- read.csv('../../../Files/MultipleTrainings.csv')
df['X'] <- NULL

ggplot(df, aes(x=df['iteration'], y=df['n_games'])) +
  theme_bw() + 
  geom_line() + 
  xlab('Iteration') +
  ylab('Percentage of correctly predicted') +
  scale_x_continuous() +
  scale_y_continuous(limits=c(0.4, 0.54), breaks=c(0.41,0.45,0.49,0.53))
  