#!/usr/bin/env Rscript
# R reference: run slingshot on the bundled bifurcation fixture.
suppressPackageStartupMessages({
  library(slingshot)
  library(SingleCellExperiment)
  library(uwot)
})

args <- commandArgs(trailingOnly = TRUE)
fixture <- args[1]   # path to coords CSV (n × d)
labels_path <- args[2]
out <- args[3]

X <- as.matrix(read.csv(fixture))
cl <- read.csv(labels_path)$cluster
cat("X:", dim(X), " clusters:", length(unique(cl)), "\n")

set.seed(42)
sds <- slingshot(X, clusterLabels = cl, start.clus = "1")

pt <- slingPseudotime(sds)
W  <- slingCurveWeights(sds)
curves <- slingCurves(sds)
write.csv(as.matrix(pt), file.path(dirname(out), "R_pt.csv"), row.names = FALSE)
write.csv(W, file.path(dirname(out), "R_W.csv"), row.names = FALSE)
# Dump first curve points
for (i in seq_along(curves)) {
  write.csv(curves[[i]]$s, file.path(dirname(out), sprintf("R_curve_%d.csv", i)), row.names = FALSE)
}
cat("R done\n")
