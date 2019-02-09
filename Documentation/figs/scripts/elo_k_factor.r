library(ggplot2)
library(ggthemes)

x <- seq(-500, 500, by=1)
e <- 1/(1+10^((-x)/400))
K <- 32
y_w <- K*(1 - e)
y_l <- K*(0 - e)
y_d <- K*(0.5 - e)

data_w <- data.frame(x, y_w)
data_l <- data.frame(x, y_l)
data_d <- data.frame(x, y_d)

ggplot() +
  theme_bw() +
  xlab(expression('R'['A']*' - R'['B'])) +
  ylab(expression('K(S'['A']*' - E'['A']*')')) +
  geom_line(aes(x = x, y = y_w, color="y_w"), data = data_w) + 
  geom_line(aes(x = x, y = y_l, color="y_l"), data = data_l) +
  geom_line(aes(x = x, y = y_d, color="y_d"), data = data_d) + 
  theme(legend.position = c(0, 0), legend.justification = c(-6.86, -4)) +
  scale_color_manual(values = c("blue","red","green"), 
                     name="Score", 
                     breaks=c("y_w", "y_d", "y_l"),
                     labels=c("1 (Win)", "0.5 (Draw)", "0 (Lose)")) +
  scale_x_continuous(limits = c(min(x), max(x)), expand = c(0, 0), breaks=c(-400, -200, 0, 200, 400)) + 
  scale_y_continuous(limits = c(-32, 32), expand = c(0,0), breaks=seq(-32, 32, by=8)) + 
  geom_vline(xintercept = 0.5, colour=rgb(0,0,0,0.3)) + 
  geom_hline(yintercept = -32, colour=rgb(0,0,0,0.3)) +
  geom_hline(yintercept = -16, colour=rgb(0,0,0,0.3)) + 
  geom_hline(yintercept = 0, colour=rgb(0,0,0,0.3)) +
  geom_hline(yintercept = 16, colour=rgb(0,0,0,0.3)) +
  geom_hline(yintercept = 32, colour=rgb(0,0,0,0.3)) + 
  geom_point(aes(x = 0, y = 16)) + 
  geom_text(aes(x = 0, y = 16), label=16, vjust=2) + 
  geom_point(aes(x = 0, y = 0)) + 
  geom_text(aes(x = 0, y = 0), label=0, vjust=2) + 
  geom_point(aes(x = 0, y = -16)) + 
  geom_text(aes(x = 0, y = -16), label=-16, vjust=2)
