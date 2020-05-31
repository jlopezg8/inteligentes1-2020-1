install.packages("wordcloud")
install.packages("tm")

library(wordcloud)
library(tm)

respuestas <- read.csv(
    "C:/Users/jlope/Documents/Semestre_9/Inteligentes I/Introducción/respuestas.csv",
    header=TRUE, encoding="UTF-8")
wordcloud(respuestas[,2], min.freq=1)
