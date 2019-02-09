library(ggplot2)
library(ggthemes)

train = c(1.0292503192722071,
          0.9734585011080693,
          0.9485225911273895,
          0.9430981322364019,
          0.9380082608560986,
          0.9360612128920718,
          0.9335412936161451,
          0.9274357160185729,
          0.9268750867868218,
          0.9222393105550607)
val = c(1.0254600682308648,
        1.0289044612772373,
        1.027614892227082,
        1.0232529964843138,
        1.0260576017654004,
        1.0280392631613633,
        1.0340864863768424,
        1.027857189473801,
        1.025220986032729,
        1.0274272024631501)
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
