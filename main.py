import json
import os
from pprint import pprint
# Stwórz pliki "bazy danych" dla historii operacji, stanu konta i stanu magazynu:
if not os.path.isfile('history.txt'):
    with open('history.txt', 'w') as fh:
        fh.write("Historia operacji: \n")

if not os.path.isfile('saldo.txt'):
    with open('saldo.txt', 'w') as fc:
        fc.write(str(0))

if not os.path.isfile('magazyn.json'):
    with open('magazyn.json', 'w') as fm:
        json.dump({}, fm)

# Stwórz klasę Manager, która będzie implementowała dwie kluczowe metody: execute i assign.
# Przy ich użyciu wywołuj poszczególne fragmenty aplikacji.


class Manager:
    def __init__(self):
        self.actions = {}
        self.history = []

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb

        return decorate

    def execute(self, name):
        if name not in self.actions:
            print("Nie ma takiej opcji.")
        else:
            self.actions[name](self)
            self.history.append(name)
            with open('history.txt', 'a') as hf:
                for item in self.history:
                    hf.write(item + '\n')


# Stwórz instancję klasy Manager:
manager = Manager()
polecenie = input("Wpisz polecenie: \n")


# Funkcjonalności:
#
# "Saldo" - pobierz/dodaj; pozwala pobrać/dodać środki na konto. Pobiera stan konta z pliku.
# Zapisuje ostateczny stan konta z powrotem do pliku 'saldo.txt'.
@manager.assign("saldo")
def zmien_saldo(manager):
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
            kwota_do_dodania = float(input("Wpisz kwotę do dodania: \n"))
            if kwota_do_dodania < 0:
                print("Uspokój się, dodawana kwota musi być większa od 0. Spróbuj ponownie.\n")
            elif kwota_do_dodania >= 0:
                stan_konta += kwota_do_dodania
                with open('saldo.txt', 'w') as fd:
                    fd.write(str(stan_konta))
                print(f"Dodano {kwota_do_dodania} PLN.\n"
                      f"Aktualny stan konta to {stan_konta} PLN. \n")


# "Sprzedaż" - Pobiera z inputu nazwę produktu, cenę oraz liczbę sztuk.
# Odejmuje ze stanu magazynowego, dodaje do stanu konta.
# Korzysta z plików "magazyn.json" i "saldo.txt".
@manager.assign("sprzedaż")
def sprzedaj(manager):
    nazwa_produktu = input("Podaj nazwę produktu: \n")
    liczba_sztuk = int(input("Podaj ilość: \n"))
    cena = float(input("Podaj cenę jednostkową produktu: \n"))
    with open('saldo.txt', 'r') as sld:  # dostęp do pliku ze stanem konta
        stan_konta_z_pliku = sld.readline()
        stan_konta = float(stan_konta_z_pliku)
    with open('magazyn.json', 'r') as m:  # otwarcie pliku ze stanem magazynowym
        magazyn = json.load(m)
    if nazwa_produktu not in magazyn:  # scenariusz, jeśli produkt nie istnieje w magazynie
        print(f"Nie można sprzedać produktu \"{nazwa_produktu}\", gdyż nie ma go na stanie.\n")
    elif nazwa_produktu in magazyn:  # scenariusz, jeśli produkt istnieje w magazynie
        dostepna_ilosc = magazyn[nazwa_produktu][0]
        zatwierdz_dostepnosc = dostepna_ilosc - liczba_sztuk
        if zatwierdz_dostepnosc <= 0:  # scenariusz, gdy produkt istnieje, ale nie w wystarczającej ilości
            print(f"Nie można sprzedać \"{nazwa_produktu}\". Na magazynie zostało: {dostepna_ilosc}. \n")
        elif zatwierdz_dostepnosc > 0:  # gdy produkt istnieje i jest go wystarczająca ilość
            magazyn[nazwa_produktu][0] = zatwierdz_dostepnosc
            zysk = cena * liczba_sztuk
            stan_konta += zysk
            with open('saldo.txt', 'w') as sl:
                sl.write(str(stan_konta))
            with open('magazyn.json', 'w') as mg:
                json.dump(magazyn, mg)


# "Zakup" - Pobiera nazwę produktu, cenę oraz liczbę sztuk.
# Dodaje do stanu magazynowego, odejmuje ze stanu konta.
# Korzysta z plików "magazyn.json" i "saldo.txt".
@manager.assign("zakup")
def kupuj(manager):
    nazwa_produktu = input("Podaj nazwę produktu: \n")
    liczba_sztuk = int(input("Podaj ilość: \n"))
    cena = float(input("Podaj cenę jednostkową produktu: \n"))
    with open('saldo.txt', 'r') as sld:  # dostęp do pliku ze stanem konta
        stan_konta_z_pliku = sld.readline()
        stan_konta = float(stan_konta_z_pliku)
    with open('magazyn.json', 'r') as m:  # otwarcie pliku ze stanem magazynowym
        magazyn = json.load(m)
    sprawdz_stan_konta = stan_konta - liczba_sztuk * cena  # walidacja stanu konta
    if sprawdz_stan_konta < 0:
        print("Uwaga! Nieprawidłowy stan konta po zakończeniu tej operacji. \n"
              "Operacja niedozwolona. Przerywam akcję. \n")
    elif sprawdz_stan_konta > 0:
        pass
    if nazwa_produktu not in magazyn:  # scenariusz, jeśli produkt nie istnieje w magazynie
        magazyn[str(nazwa_produktu)] = [liczba_sztuk, cena]
        with open('magazyn.json', 'w') as m:
            json.dump(magazyn, m)
        stan_konta -= int(liczba_sztuk) * float(cena)
        with open('saldo.txt', 'w') as f:
            f.write(str(stan_konta))
    elif nazwa_produktu in magazyn:  # scenariusz, jeśli produkt istnieje w magazynie
        magazyn[str(nazwa_produktu)][0] += liczba_sztuk
        magazyn[str(nazwa_produktu)][1] = cena  # aktualizuje cenę w magazynie dla wszystkich sztuk
        with open('magazyn.json', 'w') as mm:
            json.dump(magazyn, mm)
        stan_konta -= int(liczba_sztuk) * float(cena)
        with open('saldo.txt', 'w') as f:
            f.write(str(stan_konta))


# "Konto" - pokazuje aktualny stan konta. Pobiera dane z pliku "saldo.txt".
@manager.assign("konto")
def pokaz_konto(manager):
    with open('saldo.txt', 'r') as f:
        stan_konta = f.readline()
    print(f"Aktualny stan konta wynosi {stan_konta} PLN.")


# "Lista" - pokazuje aktualny stan całego magazynu. Pobiera dane z pliku "magazyn.json".
@manager.assign("lista")
def pokaz_magazyn(manager):
    with open('magazyn.json', 'r') as mag_file:
        lista = json.load(mag_file)
        pprint(lista, indent=2)


# "Magazyn" - Wyświetla stan magazynu dla konkretnego produktu. Pobiera z inputu nazwę produktu.
# Pobiera dane z pliku "magazyn.json".
@manager.assign("magazyn")
def pokaz_magazyn(manager):
    wybrany_produkt = input("Podaj nazwę produktu, \n"
                            "dla którego chcesz poznać stan magazynowy.\n")
    with open('magazyn.json', 'r') as mag:
        magazyn = json.load(mag)
    if wybrany_produkt not in magazyn:
        print(f"Brak produktu \"{wybrany_produkt}\" w magazynie.\n")
    elif wybrany_produkt in magazyn:
        print(f"Stan magazynowy dla produktu \"{wybrany_produkt}\":\n"
              f"Ilość: {magazyn[wybrany_produkt][0]} \n"
              f"Cena: {magazyn[wybrany_produkt][1]} PLN \n")


# "Przegląd" - Wyświetla wszystkie wprowadzone akcje. Pobiera dane z pliku "history.txt".
# @manager.assign("przegląd")
# def saldo(manager):
#     print("saldo")


# "Koniec" - Program kończy działanie.
@manager.assign("koniec")
def zakoncz(manager):
    exit()


# Wykonaj wpisane polecenie:
manager.execute(polecenie)

