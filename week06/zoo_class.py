from abc import ABC
import sys


class Zoo(object):
    animal_dict = {}
    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
    
    def add_animal(self, animal_object):
        animal_type = type(animal_object).__name__
        if animal_type not in self.animal_dict.keys():
            self.animal_dict[animal_type] = []
            setattr(self, animal_type, animal_type)
        if animal_object not in self.animal_dict[animal_type]:
            self.animal_dict[animal_type].append(animal_object)
            print("{} does not exist, added to the zoo".format(animal_object.name))
        else:
            print("{} exists, will not be added again".format(animal_object.name))


class Animal(ABC):
    def __init__(self, genre, size, nature):
        self.genre = genre       # 类型
        self.size = size        # 体型
        self.nature = nature    # 性格
    
    # 判断是否为凶猛动物，只读属性
    @property
    def is_ferocious(self):
        return self.genre == "食肉" and self.size in ["大", "中"] and self.nature == "凶猛"       

class Cat(Animal):
    voice = "meow"
    def __init__(self, name, genre, size, nature):
        super(Cat, self).__init__(genre, size, nature)
        self.name = name
    
    # 判断是否适合作为宠物，只读属性
    @property
    def is_pet(self):
        if super(Cat, self).is_ferocious:
            return False
        else:
            return True

class Dog(Animal):
    voice = "woof"
    def __init__(self, name, genre, size, nature):
        super(Dog, self).__init__(genre, size, nature)
        self.name = name
    
    # 判断是否适合作为宠物，只读属性
    @property
    def is_pet(self):
        if super(Dog, self).is_ferocious:
            return False
        else:
            return True



if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    cat2 = Cat('小橘猫 2', '食肉', '小', '凶猛')
    dog1 = Dog('大狼狗 1', '食肉', '大', '凶猛')
    print("################## If animal is ferocious? ############################")
    print(cat1.is_ferocious)
    print(cat2.is_ferocious)
    print(dog1.is_ferocious)
    print("################## If animal is pet? ############################")
    print(cat1.is_pet)
    print(cat2.is_pet)
    print(dog1.is_pet)
    print("################## Add animal to zoo ############################")
    z.add_animal(cat1)
    z.add_animal(cat1)
    z.add_animal(cat2)
    z.add_animal(dog1)
    print("################## If zoo contains specific animal? ############################")
    have_cat = hasattr(z, 'Cat')
    print(have_cat)
    have_dog = hasattr(z, 'Dog')
    print(have_dog)
    have_lion = hasattr(z, 'Lion')
    print(have_lion)
    print("################## Display zoo status ############################")
    print(z.animal_dict)
    print(z.__dict__)