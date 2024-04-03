import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fungsi interpretasi untuk mengubah nilai fuzzy menjadi label kategori
def interpretasi_tingkat_kualitas(nilai):
    if nilai <= 20:
        return 'Buruk'
    elif nilai <= 40:
        return 'Rendah'
    elif nilai <= 60:
        return 'Sedang'
    elif nilai <= 80:
        return 'Bagus'
    else:
        return 'Sangat Bagus'

# Membaca data dari Excel
data = pd.read_excel(r'C:\Users\Eka\data_pakan_ikan.xlsx')

# Definisikan variabel input
karbohidrat = ctrl.Antecedent(np.arange(5, 11, 1), 'karbohidrat')
lemak = ctrl.Antecedent(np.arange(7, 13, 1), 'lemak')
protein = ctrl.Antecedent(np.arange(20, 31, 1), 'protein')

# Definisikan variabel output
tingkat_kualitas = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_kualitas')

# Fungsi keanggotaan untuk variabel input dan output
karbohidrat.automf(3)
lemak.automf(3)
protein.automf(3)

tingkat_kualitas['rendah'] = fuzz.trimf(tingkat_kualitas.universe, [0, 0, 40])
tingkat_kualitas['sedang'] = fuzz.trimf(tingkat_kualitas.universe, [30, 50, 70])
tingkat_kualitas['tinggi'] = fuzz.trimf(tingkat_kualitas.universe, [60, 80, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(karbohidrat['poor'] | lemak['poor'] | protein['poor'], tingkat_kualitas['rendah'])
rule2 = ctrl.Rule(karbohidrat['average'] | lemak['average'] | protein['average'], tingkat_kualitas['sedang'])
rule3 = ctrl.Rule(karbohidrat['good'] | lemak['good'] | protein['good'], tingkat_kualitas['tinggi'])

# Sistem kontrol fuzzy
tingkat_kualitas_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tingkat_kualitas_sim = ctrl.ControlSystemSimulation(tingkat_kualitas_ctrl)

# Inisialisasi list untuk menyimpan hasil
hasil_tingkat_kualitas = []

# Iterasi melalui setiap record
for index, row in data.iterrows():
    # Masukkan nilai variabel input dari data yang dibaca
    tingkat_kualitas_sim.input['karbohidrat'] = row['karbohidrat']
    tingkat_kualitas_sim.input['lemak'] = row['lemak']
    tingkat_kualitas_sim.input['protein'] = row['protein']

    # Hitung nilai variabel output
    tingkat_kualitas_sim.compute()

    # Simpan hasil
    hasil_tingkat_kualitas.append(tingkat_kualitas_sim.output['tingkat_kualitas'])

# Tambahkan hasil ke data frame
data['tingkat_kualitas'] = hasil_tingkat_kualitas

# Interpretasikan nilai fuzzy menjadi kategori
data['kategori_tingkat_kualitas'] = data['tingkat_kualitas'].apply(interpretasi_tingkat_kualitas)

# Simpan ke file Excel
data.to_excel('pakan_ikan_eka.xlsx', index=False)
