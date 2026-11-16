import numpy as np


def calculate_max(signal):
    """Sinyalin maksimum (tepe) değerini döndürür."""
    return float(np.max(signal))


def calculate_min(signal):
    """Sinyalin minimum (çukur) değerini döndürür."""
    return float(np.min(signal))

def calculate_vpp(signal):
    """Sinyalin peak to peak değerini döndürür."""
    return float(calculate_max(signal)-calculate_min(signal))

def calculate_mean(signal):
    """Sinyalin ortalamasını döndürür."""
    return float(np.mean(signal))

def calculate_rms(signal):
    """Sinyalin rms değerini döndürür."""
    return float(np.sqrt(np.mean(signal ** 2)))

def get_all_measurements(signal):
    """Tüm temel osiloskop ölçümlerini sözlük (dict) olarak döndürür."""
    return {
        "max": calculate_max(signal),
        "min": calculate_min(signal),
        "vpp": calculate_vpp(signal),
        "mean": calculate_mean(signal),
        "rms": calculate_rms(signal),
    }

if __name__ == "__main__":
    # Test için 50 Hz, 5V genlikli, 1 saniyelik örnek bir sinüs sinyali oluşturalım
    t = np.linspace(0, 1, 10000, endpoint=False)
    test_signal = 5.0 * np.sin(2 * np.pi * 50 * t)

    results = get_all_measurements(test_signal)
    print("--- 5V Sinüs Sinyali Ölçüm Sonuçları ---")
    for key, value in results.items():
        print(f"{key.upper()}: {value:.4f} V")
