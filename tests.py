import numpy as np
from measurements import (
    get_all_measurements,
    measure_channels,
    calculate_scale_info,
    apply_coupling,
    calculate_cursor_measurements,
    calculate_frequency_and_period,
)
from validation import (
    validate_signal_parameters,
    validate_sampling_rate,
    validate_channel,
    validate_scale,
    validate_coupling,
    )

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

def test_square_and_triangle_measurements():
    """Kare ve üçgen dalgaların teorik RMS değerlerini doğrular."""
    amplitude = 10.0
    frequency = 50.0
    t = np.linspace(0, 1, 10000, endpoint=False)

    # 1. Kare Dalga Testi (Teorik RMS = Vp)
    square_signal = np.where(np.sin(2 * np.pi * frequency * t) >= 0, amplitude, -amplitude)
    square_results = get_all_measurements(square_signal)
    assert abs(square_results["rms"] - amplitude) < 0.01, "Kare dalga RMS ölçümü hatalı!"
    assert abs(square_results["vpp"] - 20.0) < 0.01, "Kare dalga Vpp ölçümü hatalı!"
    print(f"[BAŞARILI] Kare Dalga Testi Geçti! Teorik RMS: {amplitude:.4f} V | Ölçülen RMS: {square_results['rms']:.4f} V")

    # 2. Üçgen Dalga Testi (Teorik RMS = Vp / kök 3)
    triangle_signal = amplitude * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * frequency * t))
    triangle_results = get_all_measurements(triangle_signal)
    theoretical_tri_rms = amplitude / np.sqrt(3)
    assert abs(triangle_results["rms"] - theoretical_tri_rms) < 0.01, "Üçgen dalga RMS ölçümü hatalı!"
    assert abs(triangle_results["vpp"] - 20.0) < 0.01, "Üçgen dalga Vpp ölçümü hatalı!"
    print(f"[BAŞARILI] Üçgen Dalga Testi Geçti! Teorik RMS: {theoretical_tri_rms:.4f} V | Ölçülen RMS: {triangle_results['rms']:.4f} V")


def test_dc_offset_measurement():
    """Sinyale eklenen DC ofsetin ortalama (mean) değerini doğru değiştirdiğini test eder."""
    t = np.linspace(0, 1, 10000, endpoint=False)
    signal = 5.0 * np.sin(2 * np.pi * 50 * t) + 3.0  # 5V genlik + 3V DC ofset

    results = get_all_measurements(signal)
    assert abs(results["mean"] - 3.0) < 0.01, "DC Ofset (Mean) ölçümü hatalı!"
    assert abs(results["max"] - 8.0) < 0.01, "Ofsetli Max ölçümü hatalı!"
    assert abs(results["min"] - (-2.0)) < 0.01, "Ofsetli Min ölçümü hatalı!"
    assert abs(results["vpp"] - 10.0) < 0.01, "Ofsetli Vpp ölçümü hatalı!"
    print(f"[BAŞARILI] DC Ofset Testi Geçti! Beklenen Ortalama: 3.0000 V | Ölçülen: {results['mean']:.4f} V")


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


def test_dual_channel_measurements():
    """CH1 (50 Hz Sinüs) ve CH2 (100 Hz Kare) çift kanal ölçümlerini doğrular."""
    t = np.linspace(0, 1, 10000, endpoint=False)
    ch1_sine = 5.0 * np.sin(2 * np.pi * 50 * t)
    ch2_square = np.where(np.sin(2 * np.pi * 100 * t) >= 0, 4.0, -4.0)

    # İki kanal birden açıkken ölçüm
    dual_results = measure_channels(ch1_sine, ch2_square)
    assert abs(dual_results["CH1"]["rms"] - (5.0 / np.sqrt(2))) < 0.01, "CH1 RMS hatalı!"
    assert abs(dual_results["CH1"]["vpp"] - 10.0) < 0.01, "CH1 Vpp hatalı!"
    assert abs(dual_results["CH2"]["rms"] - 4.0) < 0.01, "CH2 RMS hatalı!"
    assert abs(dual_results["CH2"]["vpp"] - 8.0) < 0.01, "CH2 Vpp hatalı!"

    # Sadece CH1 açık, CH2 kapalı (None) iken ölçüm
    single_results = measure_channels(ch1_signal=ch1_sine, ch2_signal=None)
    assert single_results["CH1"] is not None and single_results["CH2"] is None, "Kapalı kanal None dönmeliydi!"

    print(
        f"[BAŞARILI] Çift Kanal Testi Geçti! "
        f"CH1 RMS: {dual_results['CH1']['rms']:.4f} V | CH2 RMS: {dual_results['CH2']['rms']:.4f} V"
    )


def test_edge_cases():
    """Sıfır genlik, yüksek DC ofset ve kanal seçimi uç durumlarını test eder."""
    t = np.linspace(0, 1, 10000, endpoint=False)

    # 1. Sıfır genlik (0V) doğrulama ve ölçüm testi
    params = validate_signal_parameters(50, 0)
    assert params["amplitude"] == 0.0, "Sıfır genlik kabul edilmeliydi!"
    zero_signal = 0.0 * np.sin(2 * np.pi * 50 * t)
    zero_res = get_all_measurements(zero_signal)
    assert zero_res["rms"] == 0.0 and zero_res["vpp"] == 0.0, "0V sinyal ölçümleri 0 olmalı!"

    # 2. Yüksek DC Ofset (+100V sabit DC gerilim) testi
    high_dc_signal = zero_signal + 100.0
    dc_res = get_all_measurements(high_dc_signal)
    assert abs(dc_res["mean"] - 100.0) < 0.01 and abs(dc_res["rms"] - 100.0) < 0.01, "Yüksek DC ofset hatalı!"
    assert abs(dc_res["vpp"] - 0.0) < 0.01, "Sabit DC sinyalin Vpp değeri 0 olmalı!"

    # 3. Kanal adı doğrulama testi ("ch1" -> "CH1")
    assert validate_channel("ch1") == "CH1" and validate_channel("CH2") == "CH2"

    print("[BAŞARILI] Uç Durum (0V Genlik, +100V DC Ofset ve Kanal Seçimi) Testleri Geçti!")

def test_scale_and_independence():
    """Volt/Div ve Time/Div ölçek hesaplamalarını ve ölçümlerin ölçekten bağımsızlığını test eder."""
    # 1. Ölçek: 2 V/div, 10 ms/div (0.01 s/div -> Toplam ekran süresi 0.1 s)
    scale1_info = calculate_scale_info(
        signal=5.0 * np.sin(2 * np.pi * 50 * np.linspace(0, 0.1, 10000, endpoint=False)),
        volt_per_div=validate_scale(2.0, "Volt/Div"),
        time_per_div=validate_scale(0.01, "Time/Div"),
    )
    assert abs(scale1_info["total_time"] - 0.1) < 1e-5, "Toplam ekran süresi 0.1 s olmalı!"
    assert abs(scale1_info["occupied_vertical_divs"] - 5.0) < 0.01, "10Vpp sinyal 2V/div ölçekte 5 kare kaplamalı!"

    # 2. Ölçek: 5 V/div, 20 ms/div (0.02 s/div -> Toplam ekran süresi 0.2 s)
    t1 = np.linspace(0, 0.1, 10000, endpoint=False)
    t2 = np.linspace(0, 0.2, 10000, endpoint=False)
    sig1 = 5.0 * np.sin(2 * np.pi * 50 * t1)
    sig2 = 5.0 * np.sin(2 * np.pi * 50 * t2)

    scale2_info = calculate_scale_info(sig2, volt_per_div=5.0, time_per_div=0.02)
    assert abs(scale2_info["occupied_vertical_divs"] - 2.0) < 0.01, "10Vpp sinyal 5V/div ölçekte 2 kare kaplamalı!"

    # Ölçek değişse de gerçek RMS ve Vpp ölçümleri değişmemeli!
    meas1 = get_all_measurements(sig1)
    meas2 = get_all_measurements(sig2)
    assert abs(meas1["rms"] - meas2["rms"]) < 0.01, "Ölçek değişimi RMS değerini değiştirmemeli!"
    assert abs(meas1["vpp"] - meas2["vpp"]) < 0.01, "Ölçek değişimi Vpp değerini değiştirmemeli!"

    # Negatif ölçek hata testi
    try:
        validate_scale(-2.0, "Volt/Div")
        assert False, "Negatif Volt/Div hata vermeliydi!"
    except ValueError as e:
        print(f"[BAŞARILI] Geçersiz ölçek yakalandı -> {e}")

    print("[BAŞARILI] 4. Hafta Ölçek (Volt/Div & Time/Div) ve Bağımsızlık Testi Geçti!")


def test_ac_dc_coupling():
    """DC ve AC kuplaj modlarının sinyal üzerindeki etkisini doğrular."""
    t = np.linspace(0, 1, 10000, endpoint=False)
    # 5V genlikli, +3V DC ofsetli sinüs sinyali
    raw_signal = 5.0 * np.sin(2 * np.pi * 50 * t) + 3.0

    # 1. DC Kuplaj Testi (Ofset korunmalı: Mean = 3V, Max = 8V)
    dc_signal = apply_coupling(raw_signal, validate_coupling("dc"))
    dc_meas = get_all_measurements(dc_signal)
    assert abs(dc_meas["mean"] - 3.0) < 0.01, "DC kuplajda ortalama 3V kalmalı!"
    assert abs(dc_meas["max"] - 8.0) < 0.01, "DC kuplajda Max 8V olmalı!"

    # 2. AC Kuplaj Testi (Ofset silinmeli: Mean = 0V, Max = 5V, RMS = 5/kök2)
    ac_signal = apply_coupling(raw_signal, validate_coupling("ac"))
    ac_meas = get_all_measurements(ac_signal)
    assert abs(ac_meas["mean"] - 0.0) < 0.01, "AC kuplajda ortalama 0V olmalı!"
    assert abs(ac_meas["max"] - 5.0) < 0.01, "AC kuplajda Max 5V'a inmeli!"
    assert abs(ac_meas["vpp"] - 10.0) < 0.01, "AC kuplaj Vpp değerini değiştirmemeli!"
    assert abs(ac_meas["rms"] - (5.0 / np.sqrt(2))) < 0.01, "AC kuplaj sonrası RMS 5/kök2 olmalı!"

    print(
        f"[BAŞARILI] 5. Hafta AC/DC Kuplaj Testi Geçti! "
        f"DC Mean: {dc_meas['mean']:.2f} V -> AC Mean: {ac_meas['mean']:.2f} V"
    )


def test_cursors_and_frequency():
    """Manuel imleç (delta_t, delta_v, 1/delta_t) ve otomatik frekans/periyot ölçümünü test eder."""
    # 1. Manuel İmleç Testi (t1=0.01s, t2=0.03s -> dt=0.02s, 1/dt=50Hz; v1=-5V, v2=5V -> dv=10V)
    cursor_res = calculate_cursor_measurements(t1=0.01, t2=0.03, v1=-5.0, v2=5.0)
    assert abs(cursor_res["delta_t"] - 0.02) < 1e-5, "İmleç delta_t hatalı!"
    assert abs(cursor_res["delta_v"] - 10.0) < 1e-5, "İmleç delta_v hatalı!"
    assert abs(cursor_res["inv_delta_t"] - 50.0) < 0.01, "İmleç 1/delta_t (50 Hz) hatalı!"

    # 2. Otomatik Periyot ve Frekans Ölçümü Testi (50 Hz, +2V ofsetli sinüs)
    t = np.linspace(0, 1, 100000, endpoint=False)
    signal = 5.0 * np.sin(2 * np.pi * 50 * t) + 2.0
    freq_res = calculate_frequency_and_period(t, signal)

    assert abs(freq_res["period"] - 0.02) < 0.001, "Otomatik periyot ölçümü 0.02 s olmalı!"
    assert abs(freq_res["frequency"] - 50.0) < 0.5, "Otomatik frekans ölçümü 50 Hz olmalı!"

    print(
        f"[BAŞARILI] 6. Hafta İmleç ve Otomatik Frekans Testi Geçti! "
        f"Ölçülen Frekans: {freq_res['frequency']:.2f} Hz | Periyot: {freq_res['period']:.4f} s"
    )


def test_channel_math():
    """7. Hafta: Kanal matematiği (CH1 + CH2 ve CH1 - CH2) sinyal ölçümlerini doğrular."""
    t = np.linspace(0, 1, 10000, endpoint=False)
    ch1 = 5.0 * np.sin(2 * np.pi * 50 * t)
    ch2 = 3.0 * np.sin(2 * np.pi * 50 * t)

    # 1. CH1 + CH2 (5V + 3V = 8V genlikli sinüs -> Vpp = 16V, RMS = 8/kök2)
    sum_signal = ch1 + ch2
    sum_meas = get_all_measurements(sum_signal)
    assert abs(sum_meas["vpp"] - 16.0) < 0.01, "CH1 + CH2 Vpp 16V olmalı!"
    assert abs(sum_meas["rms"] - (8.0 / np.sqrt(2))) < 0.01, "CH1 + CH2 RMS 8/kök2 olmalı!"

    # 2. CH1 - CH2 (5V - 3V = 2V genlikli sinüs -> Vpp = 4V, RMS = 2/kök2)
    diff_signal = ch1 - ch2
    diff_meas = get_all_measurements(diff_signal)
    assert abs(diff_meas["vpp"] - 4.0) < 0.01, "CH1 - CH2 Vpp 4V olmalı!"
    assert abs(diff_meas["rms"] - (2.0 / np.sqrt(2))) < 0.01, "CH1 - CH2 RMS 2/kök2 olmalı!"

    # 3. CH1 - CH1 (Birbirini sıfırlama -> Vpp = 0V, RMS = 0V)
    cancel_meas = get_all_measurements(ch1 - ch1)
    assert abs(cancel_meas["rms"] - 0.0) < 1e-5 and abs(cancel_meas["vpp"] - 0.0) < 1e-5

    print(
        f"[BAŞARILI] 7. Hafta Kanal Matematiği (CH1±CH2) Testi Geçti! "
        f"(CH1+CH2) Vpp: {sum_meas['vpp']:.1f} V | (CH1-CH2) Vpp: {diff_meas['vpp']:.1f} V"
    )

    
if __name__ == "__main__":
    print("--- SANAL OSİLOSKOP TÜM HAFTALAR (1-7) TESTLERİ BAŞLIYOR ---")
    test_sine_measurements()
    test_validation()
    test_square_and_triangle_measurements()
    test_dc_offset_measurement()
    test_dual_channel_measurements()
    test_edge_cases()
    test_scale_and_independence()
    test_ac_dc_coupling()
    test_cursors_and_frequency()
    test_channel_math()
    print("--- TÜM TESTLER BAŞARIYLA TAMAMLANDI! ---")
