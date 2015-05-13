library(lattice)
library(gridExtra)

#this data is from simulations across R0 and vaccination rates when 
#roBetaRate = 0.07, ramp = 2, OPVtrans(epsilon) = 0.05
data_figure2 = read.csv('figure2_data.csv',header=T)

#I removed R0 = 22 and higher vaccination rates because they are unrealistic ranges
data_figure2_sub = subset(data_figure2, vaccRate <= 3 & R0 < 22)

#Set very low prevalances to  1 billion category
data_figure2_sub$finalPrev_0 = with(data_figure2_sub, ifelse(finalPrev < 1e-9, 1e-9, finalPrev))
data_figure2_sub$min0t50_0 =  with(data_figure2_sub, ifelse(min0t50 < 1e-9, 1e-9, min0t50))
data_figure2_sub$avg15t50_0 =  with(data_figure2_sub, ifelse(avg15t50 < 1e-9, 1e-9, avg15t50))

#how the colour key was selected
col.l <- colorRampPalette(rainbow(1000, start=0, end = 4/6, alpha = 1),
                           space = "Lab", bias = 0.8)


#Set up labels
prevLab = c("1 in 100", "1 in 1000", "1 in 10000", 
          "1 in 100000", "1 in million", "<1 in billion" )
prevLabLoc = c(-2, -3, -4, -5, -6, -9)
R0text = "Maximum Reproduction Number"
xtext = expression(paste("Effective Vaccination Rate (yr"^{-1},")"))

#The levelplot code
min_prev_plot = levelplot(log10(min0t50_0) ~ vaccRate + R0,
                          data_figure2_sub,
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
              panel=function(...){
                panel.levelplot.raster(...)
                panel.rect(0.8, 5.5, 2, 10.5, border = "black", lty = 2)
                panel.points(0.88, 10., col = "black", pch = 5, cex = 1.,  pos = 3)
                panel.points(1, 4, col = "black", pch = 1, cex = 1.)
                panel.points(2.5, 18, col = "black", pch = 8, cex = 1.1)
                panel.rect(0.25, 14.25, 1.5, 17.75, border = "black")
              }
)

final_prev_plot = levelplot(log10(finalPrev_0) ~ vaccRate + R0,
              data_figure2_sub,
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
              panel=function(...){
                panel.levelplot.raster(...)
                panel.rect(0.8, 5.5, 2, 10.5, border = "black", lty = 2)
                panel.points(0.88, 10., col = "black", pch = 5, cex = 1.,  pos = 3)
                panel.points(1, 4, col = "black", pch = 1, cex = 1.)
                panel.points(2.5, 18, col = "black", pch = 8, cex = 1.1)
                panel.rect(0.25, 14.25, 1.5, 17.75, border = "black")
              }
)

#pdf("Figure2.pdf", width=3.5*1.25, height=14/3*1.25, family="Times")
grid.arrange(min_prev_plot, final_prev_plot, nrow = 2)
#dev.off()

