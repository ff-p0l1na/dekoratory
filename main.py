import json
import os

if not os.path.isfile('history.txt'):
    with open('history.txt', 'w') as fh:
        fh.write("Historia operacji: \n")

if not os.path.isfile('saldo.txt'):
    with open('saldo.txt', 'w') as fc:
        fc.write(str(0))

if not os.path.isfile('magazyn.json'):
    with open('magazyn.json', 'w') as fm:
        json.dump({}, fm)


class Manager:
    def __init__(self):
        self.actions = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb

        return decorate

    def execute(self, name):
        if name not in self.actions:
            print("Nie ma takiej opcji.")
        else:
            self.actions[name](self)


manager = Manager()


@manager.assign("saldo")
def saldo(manager):
    with open('saldo.txt', 'r') as f:
        stan_konta_z_pliku = f.readline()
        stan_konta = float(stan_konta_z_pliku)
        decyzja_dla_salda = input('Jeśli chcesz POBRAĆ środki z konta, napisz "pobierz". \n'
                                  'Jeśli chcesz DODAĆ środki do konta, napisz "dodaj".\n')
        if decyzja_dla_salda == "pobierz":
            kwota_do_pobrania = float(input("Wpisz kwotę do pobrania z konta: \n"))
            weryfikuj_stan_konta = stan_konta - kwota_do_pobrania
            if weryfikuj_stan_konta <= 0:
                print(f"Uwaga! Stan konta po tej operacji nie może być mniejszy lub równy 0 PLN. \n"
                      f"Wpisz kwotę mniejszą niż {stan_konta} PLN. \n")
            else:
                stan_konta -= kwota_do_pobrania
                with open('saldo.txt', 'w') as fs:
                    fs.writelines(str(stan_konta))
                    print(f"Pobrano {kwota_do_pobrania} PLN. \n"
                          f"Na koncie pozostało {stan_konta} PLN. ")
        elif decyzja_dla_salda == "dodaj":
            kwota_do_dodania = float(input("Wpisz kwotę do dodania: "))
            if kwota_do_dodania < 0:
                print("Uspokój się, dodawana kwota musi być większa od 0. Spróbuj ponownie.\n")
            elif kwota_do_dodania >= 0:
                stan_konta += kwota_do_dodania
                with open('saldo.txt', 'w') as fd:
                    fd.write(str(stan_konta))
                print(f"Dodano {kwota_do_dodania} PLN.\n"
                      f"Aktualny stan konta to {stan_konta} PLN. \n")


@manager.assign("sprzedaż")
def saldo(manager):
    print("saldo")

@manager.assign("zakup")
def saldo(manager):
    print("saldo")

@manager.assign("konto")
def saldo(manager):
    with open('saldo.txt', 'r') as f:
        stan_konta = f.readline()
    print(f"Aktualny stan konta wynosi {stan_konta} PLN.")

@manager.assign("lista")
def saldo(manager):
    print("saldo")

@manager.assign("magazyn")
def saldo(manager):
    print("saldo")

@manager.assign("przegląd")
def saldo(manager):
    print("saldo")

@manager.assign("koniec")
def konczyciel(manager):
    exit()

manager.execute("konto")
