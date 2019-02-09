library(ggplot2)
library(ggthemes)

home <- data.frame(x=rep(c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), c(4803, 6875, 5228, 2731, 1173, 382, 137, 31, 4, 8, 2)))

ggplot(home, aes(x)) +
  theme_bw() +
  geom_bar(fill="blue3") + 
  scale_x_discrete(limits=c(0,1,2,3,4,5,6,7,8,9,10)) +
  xlab("Number of goals") +
  ylab("Number of matches") +
  ggtitle("Home team") + 
  theme(plot.title = element_text(hjust = 0.5))
