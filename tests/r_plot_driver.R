#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(slingshot)
  library(ggplot2)
})

args <- commandArgs(trailingOnly = TRUE)
out_dir <- args[1]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

X <- as.matrix(read.csv("data/fixture_coords.csv"))
cl <- read.csv("data/fixture_labels.csv")$cluster

set.seed(42)
sds <- slingshot(X, clusterLabels = cl, start.clus = "1")
curves <- slingCurves(sds, as.df = TRUE)

df <- data.frame(Dim1 = X[,1], Dim2 = X[,2], cluster = as.factor(cl))
p <- ggplot(df, aes(x = Dim1, y = Dim2, color = cluster)) +
  geom_point(size = 1.5, alpha = 0.7) +
  geom_path(data = curves, aes(group = Lineage), color = "black", size = 1.2) +
  theme_classic()
ggsave(file.path(out_dir, "R_slingshot.png"), p, width = 6, height = 4, dpi = 100)
cat("R plot saved\n")
