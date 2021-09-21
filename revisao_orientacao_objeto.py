from abc import abstractmethod, ABC


class Pessoa(ABC):
    def __init__(self, nome, sobrenome, data_de_nascimento):
        self.sobrenome = sobrenome
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self):
        return "minha idade"

    @abstractmethod
    def falar(self):
        pass

    @staticmethod
    def quanto_e_2_mais_2():
        return 4

    def __str__(self):
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"

class Brasileiro(Pessoa):
    def falar(self):
        return "Olá mundo"

andre = Brasileiro(nome="Andre", sobrenome="Sionek", data_de_nascimento="1991-01-09")
print(andre.data_de_nascimento)
print(andre.idade)


class Cachorro:
    def __init__(self, nome, raca, idade):
        self.raca = raca
        self.nome = nome
        self.idade = idade

    def __str__(self):
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"

    def is_cachorro(self):
        return False

andre = Pessoa(nome="Andre", sobrenome="Sionek", idade=30)
print(andre)

belisco = Cachorro(nome='Belisco', raca='Lhasa', idade=1.9)
print(belisco)
print(belisco.is_cachorro())


class EngenheiroDeDados(Pessoa):
    def __init__(self, nome, sobrenome, idade, experiencia):
        super().__init__(nome, sobrenome, idade)
        self.experiencia = experiencia
        self.print_var = super().__str__()

    def __str__(self):
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos, " \
               f"é Engenheiro de Dados e tem {self.experiencia} anos de experiencia"

andre = EngenheiroDeDados(nome='Andre', sobrenome='Sionek', idade=30, experiencia=4)
print(andre)
print(andre.print_var)

class CatiorinhoFiaDaPuta(Cachorro):
    def is_fiadaputa(self):
        return True


belisco = CatiorinhoFiaDaPuta(nome='Belisco', raca='Lhasa', idade=1.5)
print(belisco)
print(belisco.is_fiadaputa())
print(belisco.is_cachorro())
