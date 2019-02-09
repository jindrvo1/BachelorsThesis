library(ggplot2)
library(ggthemes)

x <- seq(-500, 500, by=1)
y <- 1/(1+10^((-x)/400))

data <- data.frame(x, y)

ggplot() + 
  theme_bw() + 
  geom_line(aes(x = x, y = y), data = data) + 
  scale_x_continuous(limits = c(min(x), max(x)), expand = c(0, 0), breaks=c(-400, -200, 0, 200, 400)) + 
  scale_y_continuous(limits = c(0, 1), expand = c(0,0)) + 
  ylab(expression('E'['A'])) + 
  xlab(expression('R'['A']*' - R'['B'])) + 
  geom_hline(yintercept = 0.5, colour=rgb(0,0,1,0.5)) + 
  geom_vline(xintercept = -400, colour=rgb(0,0,0,0.2)) + 
  geom_vline(xintercept = -200, colour=rgb(0,0,0,0.2)) + 
  geom_vline(xintercept = 0, colour=rgb(0,0,0,0.2)) + 
  geom_vline(xintercept = 200, colour=rgb(0,0,0,0.2)) + 
  geom_vline(xintercept = 400, colour=rgb(0,0,0,0.2)) +
  geom_point(aes(x = -400, y = y[101])) + 
  geom_text(aes(x = -400, y = y[101]), label=round(y[101], 2), vjust=2) + 
  geom_point(aes(x = -200, y = y[301])) + 
  geom_text(aes(x = -200, y = y[301]), label=round(y[301], 2), vjust=2) + 
  geom_point(aes(x = 0, y = y[501])) + 
  geom_text(aes(x = 0, y = y[501]), label=round(y[501], 2), vjust=2) + 
  geom_point(aes(x = 200, y = y[701])) + 
  geom_text(aes(x = 200, y = y[701]), label=round(y[701], 2), vjust=2) + 
  geom_point(aes(x = 400, y = y[901])) + 
  geom_text(aes(x = 400, y = y[901]), label=round(y[901], 2), vjust=2)
