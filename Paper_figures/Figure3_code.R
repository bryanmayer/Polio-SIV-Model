#Final prevalence across different levels of OPV transmission

library(lattice)
library(gridExtra)

#this data is from simulations across R0 and vaccination rates when 
#roBetaRate = 0.07, ramp = 2, OPVtrans(epsilon) = 0.025, 0.05, 0.1, 0.2, 0.25
data_figure3 = read.csv('figure3_data.csv',header=T)

#I removed R0 = 22 and OPV = 25% because they are not interesting, OPV = 5% in figure 2
data_figure3_sub = subset(data_figure3, R0 < 22 & OPVtrans != 0.25 & OPVtrans != 0.05)

#Set very low prevalances to  1 billion category
data_figure3_sub$finalPrev_0 = with(data_figure3_sub, 
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
OPV_plots = list()
j = 1
for (i in unique(data_figure3_sub$OPVtrans)){
  OPV_plots[[j]] = levelplot(log10(finalPrev_0) ~ vaccRate + R0,
                      subset(data_figure3_sub, OPVtrans == i),
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
j = j + 1
}

#pdf("Figure3.pdf", width=4, height=8, family="Times")
print(do.call(arrangeGrob, c(OPV_plots, list(nrow = 3))))
#dev.off()

