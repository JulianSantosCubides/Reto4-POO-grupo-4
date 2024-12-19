class MenuItem:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def calculate_total_price(self, quantity=1):
        return self._price * quantity

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price


class Beverage(MenuItem):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self._size = size

    def calculate_total_price(self, quantity=1, with_main_course=False):
        if with_main_course: # Descuento del 10% por pedir con un plato principal
            discount = 10
        else:
            discount = 0


        total_price = super().calculate_total_price(quantity)
        price_with_discount = total_price - (total_price * (discount / 100))

        return price_with_discount

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size


class MainCourse(MenuItem):
    def __init__(self, name, price, is_vegetarian):
        super().__init__(name, price)
        self._is_vegetarian = is_vegetarian

    def is_vegetarian(self):
        return self._is_vegetarian

    def set_is_vegetarian(self, is_vegetarian):
        self._is_vegetarian = is_vegetarian


class Desert(MenuItem):
    def __init__(self, name, price, with_sugar):
        super().__init__(name, price)
        self._with_sugar = with_sugar

    def get_with_sugar(self):
        return self._with_sugar

    def set_with_sugar(self, with_sugar):
        self._with_sugar = with_sugar

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, menu_item, quantity=1):
        self.items.append((menu_item, quantity))

    def calculate_total_bill(self):

        # Determinar si algún tipo plato principal en la orden
        with_main_course = False
        for item, _ in self.items:
            if isinstance(item, MainCourse):
                with_main_course = True
                break

        # Calcular total teniendo en cuenta el descuento del 10% en las bebidas
        total = 0
        for item, quantity in self.items:
            if isinstance(item, Beverage): # Si el ítem es una bebida, aplicar el descuento
                total += item.calculate_total_price(quantity, with_main_course) # Se llama a 'calculate_total_price' de la subclase Beverage
            else:  # Total sin descuento
                total += item.calculate_total_price(quantity)

        return total

    def apply_discount(self, discount_percentage):
        total = self.calculate_total_bill()
        discount_value = total * discount_percentage / 100
        final_bill = total - discount_value

        return final_bill
    

# Clases para el pago
class MedioPago:
    def pagar(self, monto: float):
        pass

class Tarjeta(MedioPago):
    def __init__(self, numero: str, cvv: int):
        self.numero = numero
        self.cvv = cvv

    def pagar(self, monto: float):
        print(f"Pago procesado con tarjeta {self.numero} por un valor de ${monto:.2f}")

class Efectivo(MedioPago):
    def __init__(self, monto_entregado: float):
        self.monto_entregado = monto_entregado

    def pagar(self, monto: float):
        if self.monto_entregado >= monto:
            cambio = self.monto_entregado - monto
            print(f"Muchas gracias por tu compra. Tu cambio es: ${cambio:.2f}")
            print("\n¡Adios!")
        else:
            print(f"Monto insuficiente. Entregado: ${self.monto_entregado:.2f}, Total: ${monto:.2f}")


menu = [
    Beverage("Jugo de limón", 6000.0, "medio"),
    Beverage("Café", 3000.0, "grande"),
    Beverage("Gaseosa Cocacola", 4000.0, "medio"),
    Desert("Bolas de helado", 8000.0, False),
    Desert("Torta de maracuya", 10000.0, True),
    MainCourse("Pasta", 11000.0, True),
    MainCourse("Carne", 15000.0, False),
    MainCourse("Ensalada", 10000.5, True),
    Desert("Ensalada de frutas", 18000., True)
]

# Crear la orden
order = Order()

print("Lista de items disponibles en el menú:")
for i, item in enumerate(menu):
    print(f"{i + 1}. {item.get_name()} - ${item.get_price()}")

while True:
    choice = input("\nIngresa el número del item que quieres añadir (o escribe 'Fin' para finalizar la adición): ")
    if choice.lower() == 'fin':
        break
    
    choice_index = int(choice) - 1
    if 0 <= choice_index < len(menu):
        quantity = int(input(f"Ingresa la cantidad para {menu[choice_index].get_name()}: "))
        order.add_item(menu[choice_index], quantity)
    else:
        print("Número ingresado no válido. Por favor, ingresa una opción válida")

print("\nResumen de tu orden:")
for item, quantity in order.items:
    print(f"{item.get_name()} (x{quantity}) \t+ ${item.calculate_total_price(quantity):.2f}") # Mostrar solo dos decimales redondeando el segundo decimal

total_bill = order.calculate_total_bill()
print(f"Total a pagar: \t${total_bill:.2f}") # Mostrar solo dos decimales redondeando el segundo decimal

apply_discount = input("¿Deseas aplicar un descuento? (si/no): ").lower()
if apply_discount == 'si':
    discount = float(input("Ingresa el porcentaje de descuento (sin ingresar el símbolo '%'): "))
    discounted_total = order.apply_discount(discount)
    print(f"Total con descuento: ${discounted_total:.2f}")


# Sección para pagar
while True:
    metodo_pago = input("\n¿Cómo deseas pagar? (tarjeta/efectivo): ").lower()
    if metodo_pago == "tarjeta":
        numero = input("Ingresa el número de tu tarjeta: ")
        cvv = int(input("Ingresa el CVV: "))
        tarjeta = Tarjeta(numero, cvv)
        tarjeta.pagar(total_bill)
        break
    elif metodo_pago == "efectivo":
        monto_entregado = float(input("Ingresa el monto para hacer el pago: "))
        efectivo = Efectivo(monto_entregado)
        efectivo.pagar(total_bill)
        break
    else:
        print("Método de pago no válido. Intenta nuevamente.")



