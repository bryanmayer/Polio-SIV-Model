#Final prevalence across different levels of OPV transmission and waning rates

library(lattice)
library(gridExtra)

data_figure4 = read.csv('figure4_data.csv',header=T)

#I removed R0 = 22 and OPV = 25% because they are not interesting, OPV = 5% is in figure 2
data_figure4_sub = subset(data_figure4, R0 < 22 & OPVtrans != 0.05)

#Set very low prevalances to  1 billion category
data_figure4_sub$finalPrev_0 = with(data_figure4_sub, 
                                    ifelse(finalPrev < 1e-9, 1e-9, finalPrev))

#how the colour key was selected
col.l <- colorRampPalette(rainbow(1000, start=0, end = 4/6, alpha = 1),
                          space = "Lab", bias = 0.8)

#Set up labels
prevLab = c("1 in 100", "1 in 1000", "1 in 10000", 
            "1 in 100000", "1 in million", "<1 in billion" )
prevLabLoc = c(-2, -3, -4, -5, -6, -9)
R0text = "Maximum Reproduction No."
xtext = expression(paste("Effective Vaccination Rate (yr"^{-1},")"))

#levelplot code (must simpler than Figure 2)
#i would use llply (plyr) instead of the loop if I did this again
wane_plot = list()
k = 1
for(j in unique(data_figure4_sub$OPVtrans)){
  for (i in unique(data_figure4_sub$waneRate)){
    wane_plots[[k]] = levelplot(log10(finalPrev_0) ~ vaccRate + R0,
                              subset(data_figure4_sub, OPVtrans == j & waneRate == i),
                              as.table = T, cuts = 1000,
                              col.regions = col.l,
                              xlab = xtext,
                              ylab = R0text,
                              par.settings = list(
                                layout.widths = list(
                                  ylab.axis.padding = -.25,
                                  axis.key.padding=-0.5 ),
                                layout.heights = list(
                                  xlab.axis.padding = 0)
                              ),
                              scales=list(tck = c(1,0), fontfamily = "Times",
                                          x=list(at = seq(0, 3, 1), labels = seq(0, 3, 1))),
                              colorkey = list(space = "right", cuts = 1000, angle = 90,
                                              labels = list(fontface="plain", labels = prevLab, at = prevLabLoc, angle=180)),
                              interpolate = TRUE,
                              panel=panel.levelplot.raster
    )
  k = k + 1
  }
}

#pdf("Figure4.pdf", width=8, height=8, family="Times")
print(do.call(arrangeGrob, c(wane_plots, list(nrow = 3, ncol = 2))))
#dev.off()

