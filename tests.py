import numpy as np
from measurements import get_all_measurements
from validation import validate_signal_parameters, validate_sampling_rate


def test_sine_measurements():
    """Saf sinüs sinyalinin teorik değerleri ile ölçüm fonksiyonlarını karşılaştırır."""
    amplitude = 10.0  # 10V tepe değeri (Vp)
    frequency = 50.0  # 50 Hz
    t = np.linspace(0, 1, 10000, endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)

    # Teorik RMS değeri (Vp / kök 2)
    theoretical_rms = amplitude / np.sqrt(2)

    # Tüm ölçümleri tek seferde sözlük olarak alalım
    results = get_all_measurements(signal)

    # Doğrulama (Karşılaştırma)
    assert abs(results["max"] - 10.0) < 0.01, "Max ölçümü hatalı!"
    assert abs(results["min"] - (-10.0)) < 0.01, "Min ölçümü hatalı!"
    assert abs(results["vpp"] - 20.0) < 0.01, "Vpp ölçümü hatalı!"
    assert abs(results["mean"] - 0.0) < 0.01, "Mean ölçümü hatalı!"
    assert abs(results["rms"] - theoretical_rms) < 0.01, "RMS ölçümü hatalı!"

    print(f"[BAŞARILI] Sinüs Testi Geçti! Teorik RMS: {theoretical_rms:.4f} V | Ölçülen RMS: {results['rms']:.4f} V")

def test_validation():
    """Doğrulama (validation) fonksiyonlarının doğru ve hatalı girişlere tepkisini test eder."""
    # 1. Doğru giriş testi ("50" Hz, "5" V)
    params = validate_signal_parameters("50", "5", "0", "0")
    assert params["frequency"] == 50.0 and params["amplitude"] == 5.0
    print("[BAŞARILI] Geçerli parametre testi geçti!")

    # 2. Negatif frekans testi (-50 Hz)
    try:
        validate_signal_parameters(-50, 5)
        assert False, "Negatif frekans hata vermeliydi!"
    except ValueError as e:
        print(f"[BAŞARILI] Negatif frekans yakalandı -> {e}")

    # 3. Boş giriş testi ("")
    try:
        validate_signal_parameters("", 5)
        assert False, "Boş giriş hata vermeliydi!"
    except ValueError as e:
        print(f"[BAŞARILI] Boş giriş yakalandı -> {e}")

    # 4. Metin/Harf girişi testi ("abc")
    try:
        validate_signal_parameters(50, "abc")
        assert False, "Metin girişi hata vermeliydi!"
    except ValueError as e:
        print(f"[BAŞARILI] Metin girişi yakalandı -> {e}")

    # 5. Nyquist (düşük örnekleme frekansı) testi (50 Hz sinyal için 80 Hz örnekleme)
    try:
        validate_sampling_rate(80, frequency=50)
        assert False, "Düşük örnekleme frekansı hata vermeliydi!"
    except ValueError as e:
        print(f"[BAŞARILI] Düşük örnekleme frekansı yakalandı -> {e}")


if __name__ == "__main__":
    print("--- 1. HAFTA TESTLERİ BAŞLIYOR ---")
    test_sine_measurements()
    test_validation()
    print("--- TÜM TESTLER BAŞARIYLA TAMAMLANDI! ---")
