import numpy as np

def add_channels(ch1, ch2):
    if not np.array_equal(ch1["zaman"], ch2["zaman"]):
        print("Hata: İki kanalın zaman dizileri aynı olmalıdır!")
    else:
        yeni_y = ch1["y_verisi"] + ch2["y_verisi"]
        return {
            "tur": "CH1 + CH2",
            "zaman": ch1["zaman"],
            "y_verisi": yeni_y
        }

def subtract_channels(ch1, ch2):
    if not np.array_equal(ch1["zaman"], ch2["zaman"]):
        print("Hata: İki kanalın zaman dizileri eşit olmalıdır!")
    else:
        yeni_y = ch1["y_verisi"] - ch2["y_verisi"]
        return {
            "tur": "CH1 - CH2",
            "zaman": ch1["zaman"],
            "y_verisi": yeni_y
        }
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from signal_generator import generate_signal

    t = np.linspace(0, 0.04, 400, endpoint=False)

    ch1 = generate_signal('sine', t, 5, 50, 0, 0)
    ch2 = generate_signal('sine', t, 2, 150, 0, 0)

    toplam_sinyal = add_channels(ch1, ch2)
    fark_sinyal = subtract_channels(ch1, ch2)

    plt.plot(ch1["zaman"], ch1["y_verisi"], label='CH1 (50 Hz, A=5', color='blue', linestyle='--')
    plt.plot(ch2["zaman"], ch2["y_verisi"], label='CH2 (150 Hz, A=2', color='red', linestyle='--')
    plt.plot(fark_sinyal["zaman"], fark_sinyal["y_verisi"], label='CH1 + CH2', color='green', linewidth=2)

    plt.grid(True)
    plt.legend()
    plt.show()
