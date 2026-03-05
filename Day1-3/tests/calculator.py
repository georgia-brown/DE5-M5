class calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def get_sum(self):
        return self.num1 + self.num2
    
    def get_diff(self):
        return self.num1 - self.num2
    
    def get_product(self):
        return self.num1 * self.num2
    
    def get_quotient(self):
        return self.num1/self.num2
    
if __name__ == "__main__":
    num1 = 10
    num2 = 20    
    myCalc = calculator(num1 = num1, num2=num2)
    print(num1, "+",num2, "=" ,myCalc.get_sum())
    print(num1, "-",num2, "=" ,myCalc.get_diff())
    print(num1, "*", num2, "=" ,myCalc.get_product())
    print(num1, "/",num2, "=" ,myCalc.get_quotient())