available = ["TOYOTA", "BMW", "MERCEDES", "HYUNDAI"]
requested = ["FORD", "BMW", "MERCEDES"]
offer = []
index = 0
for a in range(len(available)):
	car = available[a]
	for r in range(len(requested)):
		car_two = requested[r]
		if car == car_two:
			offer.append(car)
	index += 1
re = "The following requested cars are available: "
index_two = 0
while(index_two < len(offer)):
	re = re + offer[index_two] + ", "
re = re.strip(", ")
re = re + "."
print(re)
