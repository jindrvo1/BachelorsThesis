library(ggplot2)
library(ggthemes)

train = c(1.014101862651833, 
          0.9473305808695184, 
          0.9160322129617617, 
          0.8908252867614564, 
          0.8703743963984684,
          0.8539239126782675, 
          0.837781945826944, 
          0.8276923580217348,
          0.8220370115697391, 
          0.8165743963857461)
val = c(1.024571751367349, 
        1.031981565508949, 
        1.0382559606167512, 
        1.0499183109884358, 
        1.064403256293417, 
        1.0794091616964379, 
        1.1026647953858044, 
        1.126885391195389, 
        1.1488239800739448, 
        1.1680743026202591)
x = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

ggplot() +
  theme_bw() +
  xlab('Epoch') +
  ylab('Loss') +
  geom_line(aes(x, train, colour="train")) +
  geom_line(aes(x, val, colour="val")) +
  scale_x_continuous("Epoch", breaks=seq(0,10,2)) +
  scale_color_manual(values = c("blue","red"),
                     name="", 
                     breaks=c("train", "val"),
                     labels=c("Training", "Validation"))
  