library(ggplot2)
library(ggthemes)

x <- seq(-5, 5, .1)
y_bell <- dnorm(x, 0, 1)
y_logistic <- exp(-(x))/(((1+exp(-(x))))^2)

ggplot() +
  theme_bw() +
  geom_line(aes(x, y_bell, colour="gauss")) + 
  geom_line(aes(x, y_logistic, colour="logistic")) + 
  xlab("x") +
  ylab("density") + 
  scale_color_manual(values = c("blue","red"), 
                     name="", 
                     breaks=c("gauss", "logistic"),
                     labels=c("Gaussian", "Logistic"))
