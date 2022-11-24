"""
7.6. Case study
Porównanie odsetek kredytowych
Zdążyliśmy już poznać niektóre możliwości biblioteki NumPy. Czas, aby wykorzystać nowo nabyte umiejętności w celu rozwiązania problemu osadzonego w otaczających nas realiach.

Kredyt bankowy można spłacać na kilka sposobów. Rata płacona na rzecz banku może składać się z dwóch części:

kapitałowej
odsetkowej
Część kapitałowa dotyczy spłaty nominalnej wartości pożyczonego kapitału, z kolei część odsetkowa to koszt pożyczenia tego kapitału – innymi słowy jest to zarobek banku.

Dwie najpopularniejsze formy spłaty kredytu to spłata w ratach równych oraz spłata w ratach malejących.

Przy ratach malejących część kapitałowa jest zawsze taka sama. Oblicza się ją jako wartość pożyczonego kapitału podzieloną przez liczbę okresów spłaty kredytu. Zatem jeśli bierzemy 12000 zł kredytu na rok, spłacanego w okresach miesięcznych, to część kapitałowa będzie wynosiła 1000 zł.

Część odsetkowa w tym przypadku będzie zawsze liczona jako procent od wartości kapitału pozostałego do spłaty. Kontynuując przykład z poprzedniego akapitu – w pierwszej racie płacimy odsetki od kwoty 12 tys. zł, a miesiąc później od kwoty 11 tys. zł i tak dalej.

Przy ratach równych, jak sama nazwa wskazuje, płacona rata jest przez cały okres kredytowania taka sama. Część odsetkową liczymy w taki sam sposób, tj. jako procent od kapitału pozostałego do spłaty. Z tego powodu stosunek części kapitałowej w kwocie raty zmienia się z każdym okresem. Przy pierwszych płatnościach część kapitałowa jest niewielka i systematycznie rośnie aż do spłaty 100% kapitału.

Używając biblioteki NumPy, postaramy się obliczyć kwotę odsetek, jaką po 30 latach kredytowania zapłacimy w zależności od sposobu jego spłacania.

Na początku ustalimy warunki zaciąganego kredytu:

kapitalizacja odsetek i płatności z tytułu raty – 12 razy w roku
stopa procentowa 6,75% w skali roku
okres kredytowania – 30 lat
kwota kredytu 200 000 zł
Przeskoczmy w tym momencie do Notebooka i przeniesiemy tam przedstawione założenia.

freq = 12
rate = 0.0675
years = 30
pv = 200000

rate /= freq  # konwersja stopy do okresu miesięcznego
nper = years * freq  # liczba wszystkich okresów
Od razu korygujemy zmienną rate i wprowadzamy nową - nper (number of periods). Stopę procentową wyrażoną w skali roku musimy najpierw dopasować do okresu kapitalizacji. Z kolei nper oznacza liczbę wszystkich okresów kredytowania (liczbę wszystkich płatności ratalnych).

periods = np.arange(1,nper+1,dtype=int)
Następnie, będziemy potrzebowali licznika każdej kolejnej płatności. Tworzymy go, przypisując odpowiednio skonstruowany wektor do zmiennej periods.

Na pierwszy ogień weźmiemy równe płatności. Dla każdej z nich obliczymy część odsetkową raty. W tym celu wykorzystamy bibliotekę numpy_financial. Biblioteka ta zawiera zestaw funkcji przydatnych w matematyce finansowej.

Pamiętaj o doinstalowaniu numpy-financial do twojego środowiska:

pip install numpy-financial
import numpy_financial as npf
interest_equal = - np.around(npf.ipmt(rate,periods,nper,pv),2)
interest_equal[:10]
image
Do zmiennej interest_equal przypisujemy wektor kolejnych części odsetkowych dla równych płatności, który tworzymy, wykorzystując funkcję ipmt.

Tylko odrobinę więcej pracy będziemy mieli z ratami malejącymi. Na początek stwórzmy wektor, który będzie zawierał tylko część kapitałową spłacanej raty.

np.set_printoptions(suppress=True)

principal_decreasing = np.around(np.zeros(nper)+(pv/nper),2)
principal_decreasing[:10]
image
W celu obliczenia części odsetkowej każdej płatności musimy znać aktualny stan kapitału pozostałego do spłaty. Zrobimy to w dwóch krokach:

Na początek stworzymy bilans końcowy dla każdej transakcji (tj. już po płatności kolejnej raty).
Potem stworzymy bilans otwarcia, który jest bilansem końcowym przed spłatą kolejnej raty kapitałowej.
balance = np.zeros(nper) + pv
balance_close = np.around(balance - np.cumsum(principal_decreasing),2)
balance_close[[0,1,2,-3,-2,-1]]
image
W pierwszym kroku tworzymy wektor zawierający tylko wartości zaciągniętego długu. Następnie od tego wektora odejmujemy — dzięki funkcji cumsum – skumulowaną płatność części odsetkowej dla każdego okresu, czyli:

np.cumsum(principal_decreasing)[:10]
image
Na końcu bilans spłaconego kapitału zamyka nam się w okolicy 0. Wartość -1,6 w tym przykładzie wynika z zaokrągleń.

Mając bilans końcowy, możemy obliczyć bilans początkowy, od którego będziemy naliczać część odsetkową.

balance_open = balance_close + principal_decreasing
Nie pozostaje zatem nic innego, jak tylko obliczyć części odsetkowe każdej płatności!

interest_decreasing = np.around(balance_open * rate,2)
interest_decreasing[:10]
image
Na koniec porównamy sumę zapłaconych odsetek w obu wariantach.

print("Wartość odsetek do zapłaty w wariancie kredytu w równych ratach wynosi: " + str("{:.2f}".format(interest_equal.sum())))
print("Wartość odsetek do zapłaty w wariancie kredytu w ratach malejących wynosi: " + str("{:.2f}".format(interest_decreasing.sum())))
image
Widzimy zatem, że spłacając tę samą wartość zobowiązania wobec banku, wybierając płatności równymi ratami – w ciągu 30 lat wpłacimy ponad 60 tys. zł więcej odsetek.

Porównajmy to sobie jeszcze na wykresie, korzystając z biblioteki matplotlib.

import matplotlib.pyplot as plt

plt.plot(interest_equal.cumsum(),label='raty równe')
plt.plot(interest_decreasing.cumsum(),label='raty malejące')
plt.legend()
plt.xlabel('Liczba okresów')
plt.ylabel('Skumulowana wartość odsetek')
image
O bibliotece matplotlib będziemy mówić dużo więcej w kolejnych modułach. Na potrzeby tego zadania prezentujemy prosty sposób stworzenia wykresu korzystającego z obiektów biblioteki NumPy.

Zadanie: kupujemy mieszkanie
Zamierzasz kupić mieszkanie. Upatrzone M kosztuje w tym momencie 120 tys. zł, jednak przewidujesz, że przez następne 5 lat ceny mieszkań będą rosły w tempie 5% rocznie. W tym momencie nie dysponujesz wystarczającymi środkami, dlatego znajdujesz ofertę banku, który proponuje lokatę, do której dopłacasz pewna stałą kwotę na koniec każdego miesiąca. Bank oferuje nominalną stopę procentową w wysokości 12% w skali roku, przy kapitalizacji miesięcznej.

Ile będzie wynosiła orientacyjna cena mieszkania za 5 lat?
Ile musisz wpłacać do banku każdego miesiąca, aby przy przedstawionej ofercie uzbierać na mieszkanie w ciągu 5 lat?
Stwórz wykres przedstawiający, jak w interwałach miesięcznych zmieniać się będzie cena mieszkania (liniowy wzrost w całym okresie) oraz wartość twojej lokaty.
Do wykonania powyższego zadania wykorzystaj biblioteki NumPy, NumPy-financial oraz Matplotlib. Odpowiedzi na pytania umieść w Notebooku (jeśli korzystasz) lub w komentarzach w kodzie.

Rozwiązanie umieść w twoim repozytorium na GitHub i prześlij Mentorowi.
"""
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

"""freq = 12
rate = 0.0675
years = 30
pv = 200000

rate /= freq  # konwersja stopy do okresu miesięcznego
nper = years * freq  # liczba wszystkich okresów

print(rate)
print(nper)

periods = np.arange(1, nper+1, dtype=int)
print(periods)
interest_equal = - np.around(npf.ipmt(rate, periods, nper, pv), 2)
print(f'raty malejące: {interest_equal[:10]}')

np.set_printoptions(suppress=True)
principal_decreasing = np.around(np.zeros(nper)+(pv/nper),2)
print(f"raty stałe: {principal_decreasing[:10]}")

balance = np.zeros(nper) + pv
balance_close = np.around(balance - np.cumsum(principal_decreasing), 2)
print(balance_close[[0, 1, 2, -3, -2, -1]])
print(np.cumsum(principal_decreasing)[:10])
balance_open = balance_close + principal_decreasing
interest_decreasing = np.around(balance_open * rate, 2)
print(interest_decreasing[:10])
print("Wartość odsetek do zapłaty w wariancie kredytu w równych ratach wynosi: " + str("{:.2f}".format(interest_equal.sum())))
print("Wartość odsetek do zapłaty w wariancie kredytu w ratach malejących wynosi: " + str("{:.2f}".format(interest_decreasing.sum())))
plt.plot(interest_equal.cumsum(), label='raty równe')
plt.plot(interest_decreasing.cumsum(), label='raty malejące')
plt.legend()
plt.xlabel('Liczba okresów')
plt.ylabel('Skumulowana wartość odsetek')
plt.show()"""
m_price = 120 * 10 ** 3
pp_increase = 0.05
pp_locate = 0.12
nper = 5 * 12


def price_change(years_in_months):
    return npf.fv(pp_increase, years_in_months / 12, 0, -m_price)


def interest(years_in_months, pv):
    return npf.ipmt(pp_locate/12, years_in_months, nper, -pv, fv=0, when='end')


if __name__ == '__main__':
    # 1. Ile będzie wynosiła orientacyjna cena mieszkania za 5 lat?

    m_fut_price = npf.fv(pp_increase, 5, 0, -m_price)
    print('1. Ile będzie wynosiła orientacyjna cena mieszkania za 5 lat?')
    print(
        'Mieszkanie o wartości 120 000.00 zł w okresie 5 lat przy stałym rocznym wzroście ceny podrożeje o: {0:.2f} zł i będzie kosztować {1:.2f} zł.'.format(
            m_fut_price - m_price, m_fut_price))

    # 2.Ile musisz wpłacać do banku każdego miesiąca, aby przy przedstawionej ofercie uzbierać na mieszkanie w ciągu 5 lat?

    print(
        '2. Ile musisz wpłacać do banku każdego miesiąca, aby przy przedstawionej ofercie uzbierać na mieszkanie w ciągu 5 lat?')
    monthly_to_save = npf.pmt(0.12 / 12, 5 * 12, 0, -m_fut_price)
    print(
        'Przy stopie procentowej 12% w skali roku oraz kapitalizacji miesięcznej w okresie 5 lat należy odkładać co miesiąc: {0:.2f} zł.'.format(
            monthly_to_save))

    # 3. Stwórz wykres przedstawiający, jak w interwałach miesięcznych zmieniać się będzie cena mieszkania (liniowy wzrost w całym okresie) oraz wartość twojej lokaty.

    periods_savings = []
    year = 0
    new_periods = []
    months = 0
    for i in range(72):
        if i == 0:
            continue
        if i < 12:
            months = 0
        if i % 12 == 0:
            months += 12
        new_periods.append(months)
    new_periods = np.array(new_periods)

    periods = np.arange(0, 61, dtype=int)
    savings = monthly_to_save * periods
    price = []
    for i in new_periods:
        price.append(price_change(i))

    plt.plot(price, label='wzrost wartości mieszkania')
    plt.plot(savings, label='wpłaty na lokatę')
    plt.legend()
    plt.xlabel('Liczba okresów')
    plt.ylabel('Skumulowana wartość')
    plt.show()
