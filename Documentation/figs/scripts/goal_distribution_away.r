library(ggplot2)
library(ggthemes)

away <- data.frame(x=rep(c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), c(7064, 7386, 4274, 1801, 609, 179, 56, 9, 5, 1, 0)))

ggplot(away, aes(x)) +
  theme_bw() +
  geom_bar(fill="red3") + 
  scale_x_discrete(limits=c(0,1,2,3,4,5,6,7,8,9, 10)) +
  xlab("Number of goals") +
  ylab("Number of matches") +
  ggtitle("Away team") + 
  theme(plot.title = element_text(hjust = 0.5))
