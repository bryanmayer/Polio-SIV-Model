
deathrates = np.loadtxt(open("Code/Input_data/deathrates.txt", "r"))
#deathrates from data
mu = deathrates[:, 1]
##birth rate * population size
b = 0.0249968 #this was fit manually to fix population size

#age group compartment sizes
ageGroupVacc = 10
ageGroupPostVacc = 10
ageGroupAdult = 14

#indices for upper bounds for age groups
ages0t5 = ageGroupVacc
ages5t15 = ageGroupVacc + ageGroupPostVacc
m = ageGroupVacc + ageGroupPostVacc + ageGroupAdult

#age-specific parameters
ageParms = {}
ageParms['vacc'] = ageGroupVacc
ageParms['postvacc'] = ageGroupPostVacc
ageParms['adult'] = ageGroupAdult
ageParms['0t5'] = ageGroupVacc
ageParms['5t15'] = ageGroupVacc+ageGroupPostVacc
ageParms['15p'] = m
ageParms['m'] = m
