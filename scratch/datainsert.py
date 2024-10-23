class Animal:
    def hacer_sonido(self):
        raise NotImplementedError("Este método debe ser implementado por las clases hijas")

class Perro(Animal):
    def hacer_sonido(self):
        return "Guau"

class Gato(Animal):
    def hacer_sonido(self):
        return "Miau"

class Vaca(Animal):
    def hacer_sonido(self):
        return "Muuu"

# Usamos polimorfismo
animales = [Perro(), Gato(), Vaca()]

for animal in animales:
    print(animal.hacer_sonido())
