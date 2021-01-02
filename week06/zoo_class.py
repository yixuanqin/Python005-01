from abc import ABC
import sys


class Zoo(object):
    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
    
    def add_animal(self, object):
        if isinstance(object, Cat):
            if not hasattr(self, 'Cat'):
                self.Cat = object
                print("Add {}".format(object))
            else:
                print("{} exists, will not add again".format(object))
        elif isinstance(object, Dog):
            if not hasattr(self, 'Dog'):
                self.Dog = object
                print("Add {}".format(object))
            else:
                print("{} exists, will not add again".format(object))
        else:
            sys.exit("Object class is not defined yet")


class Animal(ABC):
    def __init__(self, genre, size, nature):
        self.genre = genre       # 类型
        self.size = size        # 体型
        self.nature = nature    # 性格
        self.is_ferocious = self.ferocious_animal
    
    # 判断是否为凶猛动物
    @property
    def ferocious_animal(self):
        return self.genre == "食肉" and self.size in ["大", "中"] and self.nature == "凶猛"       

class Cat(Animal):
    voice = "meow"
    def __init__(self, name, genre, size, nature):
        super(Cat, self).__init__(genre, size, nature)
        self.name = name
        self.pet = self.is_pet
    
    # 判断是否适合作为宠物
    @property
    def is_pet(self):
        if super(Cat, self).ferocious_animal:
            return False
        else:
            return True

class Dog(Animal):
    voice = "woof"
    def __init__(self, name, genre, size, nature):
        super(Dog, self).__init__(genre, size, nature)
        self.name = name
        self.pet = self.is_pet
    
    # 判断是否适合作为宠物
    @property
    def is_pet(self):
        if super(Dog, self).ferocious_animal:
            return False
        else:
            return True



if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    cat2 = Cat('大花猫 2', '食肉', '小', '温顺')
    print(cat1.is_ferocious)
    print(cat1.is_pet)
    dog1 = Dog('大狼狗 1', '食肉', '大', '凶猛')
    print(dog1.is_ferocious)
    print(dog1.is_pet)
    z.add_animal(cat1)
    z.add_animal(cat2)
    z.add_animal(dog1)
    have_cat = hasattr(z, 'Cat')
    print(have_cat)
    have_dog = hasattr(z, 'Dog')
    print(have_dog)