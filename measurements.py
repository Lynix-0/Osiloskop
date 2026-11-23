import numpy as np

def validate_signal(signal):
    """Sinyal dizisinin boş olmadığını doğrular ve NumPy dizisine çevirir."""
    if signal is None or len(signal) == 0:
        raise ValueError("Sinyal dizisi boş olamaz!")
    return np.asarray(signal, dtype=float)


def calculate_max(signal):
    """Sinyalin maksimum (tepe) değerini döndürür."""
    signal = validate_signal(signal)
    return float(np.max(signal))


def calculate_min(signal):
    """Sinyalin minimum (çukur) değerini döndürür."""
    signal = validate_signal(signal)
    return float(np.min(signal))

def calculate_vpp(signal):
    """Sinyalin peak to peak değerini döndürür."""
    return float(calculate_max(signal)-calculate_min(signal))

def calculate_mean(signal):
    """Sinyalin ortalamasını döndürür."""
    signal = validate_signal(signal)
    return float(np.mean(signal))

def calculate_rms(signal):
    """Sinyalin rms değerini döndürür."""
    signal = validate_signal(signal)
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

def measure_channels(ch1_signal=None, ch2_signal=None):
    """CH1 ve CH2 kanallarının ölçümlerini ayrı ayrı hesaplayıp sözlük olarak döndürür."""
    channel_results = {
        "CH1": None,
        "CH2": None,
    }

    if ch1_signal is not None:
        channel_results["CH1"] = get_all_measurements(ch1_signal)

    if ch2_signal is not None:
        channel_results["CH2"] = get_all_measurements(ch2_signal)

    return channel_results

def calculate_scale_info(signal, volt_per_div, time_per_div, horizontal_divs=10, vertical_divs=8):
    """Volt/Div ve Time/Div ölçeklerine göre ekran süresi, gerilim aralığı ve sinyalin kapladığı kare sayısını hesaplar."""
    if volt_per_div <= 0 or time_per_div <= 0:
        raise ValueError("Volt/Div ve Time/Div değerleri sıfırdan büyük olmalıdır!")

    vpp = calculate_vpp(signal)
    total_time = float(time_per_div * horizontal_divs)
    total_voltage_span = float(volt_per_div * vertical_divs)
    occupied_divs = float(vpp / volt_per_div)

    return {
        "total_time": total_time,
        "total_voltage_span": total_voltage_span,
        "occupied_vertical_divs": occupied_divs,
    }


def apply_coupling(signal, coupling="DC"):
    """Sinyale DC veya AC kuplaj uygular. AC modunda sinyalin DC bileşenini (ortalamasını) çıkarır."""
    signal = validate_signal(signal)
    mode = str(coupling).strip().upper()

    if mode == "DC":
        return signal.copy()
    elif mode == "AC":
        return signal - calculate_mean(signal)
    else:
        raise ValueError("Kuplaj modu sadece 'AC' veya 'DC' olabilir!")

def calculate_cursor_measurements(t1, t2, v1, v2):
    """İki imleç (cursor) arasındaki zaman farkını (dt), gerilim farkını (dv) ve 1/dt değerini hesaplar."""
    dt = float(abs(t2 - t1))
    dv = float(abs(v2 - v1))
    inv_dt = float(1.0 / dt) if dt > 0 else 0.0

    return {
        "delta_t": dt,
        "delta_v": dv,
        "inv_delta_t": inv_dt,
    }


def calculate_frequency_and_period(t, signal):
    """Sıfır geçişi (zero-crossing) yöntemiyle sinyalin periyodunu (T) ve frekansını (f) otomatik hesaplar."""
    t = validate_signal(t)
    ac_signal = apply_coupling(signal, "AC")

    # Negatiften pozitife geçiş (yükselen kenar) indekslerini bul
    crossings = np.where((ac_signal[:-1] < 0) & (ac_signal[1:] >= 0))[0]

    if len(crossings) < 2:
        return {"period": 0.0, "frequency": 0.0}

    crossing_times = t[crossings]
    period = float(np.mean(np.diff(crossing_times)))
    frequency = float(1.0 / period) if period > 0 else 0.0

    return {
        "period": period,
        "frequency": frequency,
    }
    
if __name__ == "__main__":
    # Test için 50 Hz, 5V genlikli, 1 saniyelik örnek bir sinüs sinyali oluşturalım
    t = np.linspace(0, 1, 10000, endpoint=False)
    test_signal = 5.0 * np.sin(2 * np.pi * 50 * t)

    results = get_all_measurements(test_signal)
    print("--- 5V Sinüs Sinyali Ölçüm Sonuçları ---")
    for key, value in results.items():
        print(f"{key.upper()}: {value:.4f} V")
