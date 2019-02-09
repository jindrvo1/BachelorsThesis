library(ggplot2)
library(ggthemes)

away <- data.frame(x=c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), y=c(-2261, -511, 954, 930, 564, 203, 81, 22, -1, 7, 2))

ggplot(away, aes(x,y)) +
  theme_bw() +
  geom_col(fill="green4") + 
  scale_x_discrete(limits=c(0,1,2,3,4,5,6,7,8,9, 10)) +
  xlab("Number of goals") +
  ylab("Difference in matches between home and away team") +
  ggtitle("Home and away team difference") + 
  theme(plot.title = element_text(hjust = 0.5))
