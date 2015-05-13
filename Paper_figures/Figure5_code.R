#Reinfection contribution to final force of infeciton  across different levels of OPV transmission

library(lattice)
library(gridExtra)

#this force of infection data is from simulations across R0 and vaccination rates when 
#roBetaRate = 0.04,0.07,0.1 ramp = 2, OPVtrans(epsilon) = 0.025, 0.05, 0.1, 0.2, 0.25
data_figure5 = read.csv('figure5_data.csv',header=T)

#The parameter settings used in Figure 5
data_figure5_sub = subset(data_figure5, R0 < 22 & 
                            OPVtrans != 0.25 & 
                            waneRate == 0.07)

#Calculate the contribution of re-infection, if finalprev < 1e9 then set to NA because there is no infection
#the commented calculations are age-specific
data_figure5_sub$forceReinf = with(data_figure5_sub, ifelse(finalPrev < 1e-9, NA, lambdaIoutReinfF/lambdaIoutF))
#data_figure5_sub$forceReinf0t5 = with(data_figure5_sub, ifelse(inalPrev < 1e-9, 0, lambdaIoutReinf0t5F/lambdaIout0t5F))
#data_figure5_sub$forceReinf5t15 = with(data_figure5_sub, ifelse(finalPrev < 1e-9, 0, lambdaIoutReinf5t15F/lambdaIout5t15F))
#data_figure5_sub$forceReinf15p = with(data_figure5_sub, ifelse(finalPrev < 1e-9, 0, lambdaIoutReinf15p/lambdaIout15p))

#how the colour key was selected
col.l <- colorRampPalette(rainbow(10000, start = 0, end = 4/6, alpha = 1), 
                          space = "Lab", bias = 0.8)

#Set up labels
propLabLoc = seq(0, 1, 0.25)
propLab = paste(propLabLoc * 100, "%", sep = "")
R0text = "Maximum Reproduction No."
xtext = expression(paste("Effective Vaccination Rate (yr"^{-1},")"))


reinf_plots = list()
j = 1
for (i in unique(data_figure5_sub$OPVtrans)){
  reinf_plots[[j]] = levelplot(forceReinf ~ vaccRate + R0,
                            subset(data_figure5_sub, OPVtrans == i),
                            as.table = T, cuts = 10000,
                            at = seq(0, 1, by = 0.001),
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
                            scales=list(tck=c(1,0),fontfamily="Times",
                                        x=list(at=seq(0,3,1), labels=seq(0,3,1))),
                            colorkey = list(space = "right", cuts = 1000, angle = 90,
                                            labels = list(fontface="plain", labels = propLab, at = propLabLoc, angle=180)),
                            interpolate = TRUE,
                            panel=panel.levelplot.raster
  )
  j = j + 1
}

pdf("Figure5.pdf", width=8, height=7, family="Times")
print(do.call(arrangeGrob, c(reinf_plots, list(nrow = 2, ncol = 2))))
dev.off()



