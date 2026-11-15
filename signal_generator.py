import numpy as np
import matplotlib.pyplot as plt

def generate_signal(wave_type, t, amplitude, frequency, phase_deg, offset):
    faz = np.radians(phase_deg)
    if wave_type == 'sine':
        ham_dalga = np.sin(2 * np.pi * frequency * t + faz)
    elif wave_type == 'square':
        ham_dalga = np.where(np.sin(2 * np.pi * frequency * t + faz) >=0, 1, -1)
    elif wave_type == 'triangle':
        ham_dalga = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * frequency * t + faz))
    signal = (amplitude * ham_dalga) + offset
    return signal
fs = 10000
time_div = float(input("Time/Div değerini giriniz(Örneğin:0.005): "))
sure = 10 * time_div
hesaplanan_nokta = int(fs * sure)
if hesaplanan_nokta >= 5000:
    toplam_nokta = 5000
else:
    toplam_nokta = hesaplanan_nokta

t = np.linspace(0, sure, toplam_nokta, endpoint=False)
"""
#wave_type = input("Dalga türünü girin (sine / square / triangle): ")
#frequency = float(input("Frekans değerini girin (Hz): "))
#amplitude = float(input("Genlik değerini giriniz: "))
#offset = float(input("DC Offset değerini giriniz: "))
#phase_deg = float(input("Faz açısını giriniz: "))
"""
ch1_sinyal = generate_signal('sine', t, 5, 50, 0, 0)
ch2_sinyal = generate_signal('triangle', t, 3, 100, 90, 2)

plt.clf()
ax = plt.gca()  # Mevcut ekseni (Get Current Axis) yakala
ax.spines['bottom'].set_position(('data', 0))  # Alt çizgiyi y=0 noktasına taşı
ax.spines['top'].set_visible(False)            # Üst çizgiyi görünmez yap
ax.spines['right'].set_visible(False)          # Sağ çizgiyi görünmez yap

plt.plot(t, ch1_sinyal, label='CH1', color='blue')
plt.plot(t, ch2_sinyal, label='CH2', color='red')
plt.show()