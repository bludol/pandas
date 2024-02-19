import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Načtení dat z Excel souboru
data_path = 'data/klementinum.xlsx'
data_sheet_name = 'data'
temperature_data = pd.read_excel(data_path, sheet_name=data_sheet_name)


# Definice třídy pro analýzu teplot
class TemperatureAnalytics:
    def __init__(self, data):
        self.data = data

    def get_average_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        return yearly_data['T-AVG'].mean()

    def get_max_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        max_temp = yearly_data['TMA'].max()
        date_of_max_temp = yearly_data[yearly_data['TMA'] == max_temp][['rok', 'měsíc', 'den']].iloc[0]
        return max_temp, date_of_max_temp

    def get_min_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        min_temp = yearly_data['TMI'].min()
        date_of_min_temp = yearly_data[yearly_data['TMI'] == min_temp][['rok', 'měsíc', 'den']].iloc[0]
        return min_temp, date_of_min_temp

    def get_monthly_averages(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        return yearly_data.groupby('měsíc')['T-AVG'].mean()

    def analyze_temperature_trends(self, start_year, end_year):
        trend_data = self.data[(self.data['rok'] >= start_year) & (self.data['rok'] <= end_year)]
        annual_average_temperatures = trend_data.groupby('rok')['T-AVG'].mean()
        return annual_average_temperatures

    def plot_anual_temperature_averages(self, start_year, end_year):
        filtered_data = self.data[(self.data['rok'] >= start_year) & (self.data['rok'] <= end_year)]
        annual_avg_temps = filtered_data.groupby('rok')['T-AVG'].mean()
        plt.figure(figsize=(10, 6))
        plt.plot(annual_avg_temps.index, annual_avg_temps.values, marker='o', linestyle='-', color='b')
        plt.title(f'Průměrné roční teploty mezi lety {start_year} a {end_year}')
        plt.xlabel('Rok')
        plt.ylabel('Průměrná teplota (C)')
        plt.grid(True)
        plt.show()

    def plot_yearly_temp(self, year):
        # Filtrujeme data pro zadaný rok
        year_data = self.data[self.data['rok'] == year]
        plt.figure(figsize=(10, 6))
        plt.plot(year_data['den'].index, year_data['TMA'].values, marker='o', linestyle='-', color='r')
        plt.plot(year_data['den'].index, year_data['T-AVG'].values, marker='o', linestyle='-', color='black')
        plt.plot(year_data['den'].index, year_data['TMI'].values, marker='o', linestyle='-', color='b')
        plt.xlabel('Měsíc')
        plt.ylabel('Průměrná teplota (°C)')
        plt.title(f'Průměrná teplota pro rok {year}')
        plt.grid(True)
        plt.xticks([])
        plt.show()

    def plot_temp_for_day(self, year, month, day):
        selected_day_data = self.data[
            (self.data['rok'] == year) & (self.data['měsíc'] == month) & (self.data['den'] == day)]

        if selected_day_data.empty:
            print("Pro zadaný den nejsou k dispozici žádná data.")
            return
        plt.plot(selected_day_data['TMI'], label='Min Teplota', marker='o', linestyle='-', color='b')
        plt.plot(selected_day_data['T-AVG'], label='Avg Teplota', marker='o', linestyle='-', color='black')
        plt.plot(selected_day_data['TMA'], label='Max Teplota', marker='o', linestyle='-', color='r')

        # Přidání popisků os a legendy
        plt.xlabel(f'{day}.{month}.{year}')
        plt.ylabel('Teplota (°C)')
        plt.title('Maximální, minimální a průměrná teplota pro zadaný den')
        plt.legend()
        plt.grid(True)
        plt.xticks([])
        plt.show()


def main():
    temperature_analytics = TemperatureAnalytics(temperature_data)

    while True:
        print("\n")

        vybrano = vyber()

        if vybrano == "1":
            rok = year_input(1)
            average_temp = temperature_analytics.get_average_temperature(int(rok))
            print(f"Průměrná teplota v roce {rok}: {average_temp:.1f}°C")
        elif vybrano == "2":
            rok = year_input(1)
            max_temp, date_of_max_temp = temperature_analytics.get_max_temperature(int(rok))
            min_temp, date_of_min_temp = temperature_analytics.get_min_temperature(int(rok))
            print(
                f"Maximální teplota v roce {rok}: {max_temp:}°C, datum: {date_of_max_temp['den']}.{date_of_max_temp['měsíc']}.{date_of_max_temp['rok']} \n"
                f"Minimální teplota v roce {rok}: {min_temp:}°C, datum: {date_of_min_temp['den']}.{date_of_min_temp['měsíc']}.{date_of_min_temp['rok']} ")

        elif vybrano == "3":
            rok = year_input(1)
            monthly_averages = temperature_analytics.get_monthly_averages(int(rok))
            print(f"Mesicni prumer pro rok {rok} jsou:")
            print(f"{monthly_averages}")
        elif vybrano == "4":
            rok1 = year_input(2)
            rok2 = year_input(3)
            temperature_analytics.plot_anual_temperature_averages(int(rok1), int(rok2))

        elif vybrano == "5":
            rok = year_input(1)
            temperature_analytics.plot_yearly_temp(int(rok))
        elif vybrano == "6":
            rok = year_input(1)
            měsíc = input("Zadej měsíc: ")
            den = input("Zadej den: ")
            temperature_analytics.plot_temp_for_day(int(rok), int(měsíc), int(den))
        elif vybrano == "0":
            return

        else:
            print("Nebylo zadano číslo v rozsahu od 1 do 7")


def vyber():
    while True:
        print("1 - Zobrazit průměrnou teplotu pro zadaný rok")
        print("2 - Zobrazit minimální a maximální teplotu pro zadaný rok")
        print("3 - Zobrazit měsíční průměry pro zadaný rok")
        print("4 - Vykreslit průměrnou teploty mezi lety")
        print("5 - Vykreslit roční teploty")
        print("6 - Vykreslit denní teplotní trendy")
        print("0 - Konec")
        vybrano = input("Zvolte akci:")
        try:
            vybrano = int(vybrano)
            if 0 <= vybrano <= 6:
                return str(vybrano)
            else:
                print("Zadal jsi číslo mimo rozsah.")
        except ValueError:
            print("Nezadal jsi platné celé číslo.")

def year_input(volba):
    num = 0
    while(True):
        if volba == 1:
            num = input("Zadej Rok:")
        elif volba == 2:
            num = input("Zadej počáteční rok: ")
        elif volba == 3:
            num = input("Zadej konečný rok: ")
        if 2023 > int(num) >= 1775:
            return num


if __name__ == '__main__':
    main()
