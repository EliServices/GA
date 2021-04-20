def add(number1, number2):
    number1 = int(float(number1) * 10000000000)
    number2 = int(float(number2) * 10000000000)
    end = (number1 + number2) / 10000000000
    return end

def subtract(number1, number2):
    number1 = int(float(number1) * 10000000000)
    number2 = int(float(number2) * 10000000000)
    end = (number1 - number2) / 10000000000
    return end

def save_add(number1, number2):
    number1 = str(number1)
    number2 = str(number2)
    num1 = []
    num2 = []
    for i in range(0, len(number1)):
        num1.append(number1[i:i+1])
    for k in range(0, len(number2)):
        num2.append(number2[k:k+1])
    x1 = number1.find(".")
    x2 = number2.find(".")
    
