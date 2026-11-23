def validate_number(value, name="Değer"):
    """Girilen değerin boş olmadığını ve sayıya çevrilebildiğini doğrular."""
    if value is None or str(value).strip() == "":
        raise ValueError(f"{name} boş bırakılamaz!")

    try:
        return float(value)
    except ValueError:
        raise ValueError(f"{name} sayısal bir değer olmalıdır!")

def validate_frequency(frequency):
    """Girilen değerin negatif veya sıfıra eşit olmadığını doğrular."""
    freq = validate_number(frequency,"Frekans")

    if freq <=0:
        raise ValueError("Frekans sıfırdan büyük olmalıdır!")

    return freq

def validate_amplitude(amplitude):
    amp = validate_number(amplitude,"Genlik")

    if amp <0:
        raise ValueError("Genlik negatif olamaz!")

    return amp

def validate_sampling_rate(sampling_rate, frequency=None):
    """Örnekleme frekansının pozitif ve Nyquist kriterine uygun olduğunu doğrular."""
    fs = validate_number(sampling_rate, "Örnekleme frekansı")

    if fs <= 0:
        raise ValueError("Örnekleme frekansı sıfırdan büyük olmalıdır!")

    if frequency is not None:
        freq = validate_frequency(frequency)
        if fs <= 2 * freq:
            raise ValueError("Örnekleme frekansı, sinyal frekansının en az 2 katından büyük olmalıdır!")

    return fs


def validate_wave_type(wave_type):
    """Dalga türünün sine, square veya triangle olduğunu doğrular."""
    if wave_type is None or str(wave_type).strip() == "":
        raise ValueError("Dalga türü boş bırakılamaz!")

    wave = str(wave_type).strip().lower()
    valid_waves = ["sine", "square", "triangle"]

    if wave not in valid_waves:
        raise ValueError(f"Geçersiz dalga türü: '{wave_type}'. Sadece {valid_waves} kullanılabilir!")

    return wave


def validate_signal_parameters(frequency, amplitude, phase_deg=0.0, offset=0.0, wave_type="sine"):
    """Arayüzden gelen tüm sinyal parametrelerini tek seferde doğrular."""
    freq = validate_frequency(frequency)
    amp = validate_amplitude(amplitude)
    phase = validate_number(phase_deg, "Faz açısı")
    dc_offset = validate_number(offset, "DC Ofset")
    wave = validate_wave_type(wave_type)

    return {
        "frequency": freq,
        "amplitude": amp,
        "phase_deg": phase,
        "offset": dc_offset,
        "wave_type": wave,
    }
       
def validate_channel(channel):
    """Kanal seçiminin CH1 veya CH2 olduğunu doğrular."""
    if channel is None or str(channel).strip() == "":
        raise ValueError("Kanal seçimi boş bırakılamaz!")

    ch = str(channel).strip().upper()
    if ch not in ["CH1", "CH2"]:
        raise ValueError(f"Geçersiz kanal: '{channel}'. Sadece 'CH1' veya 'CH2' kullanılabilir!")

    return ch

def validate_scale(scale_value, name="Ölçek"):
    """Volt/Div veya Time/Div ölçek değerinin pozitif bir sayı olduğunu doğrular."""
    val = validate_number(scale_value, name)

    if val <= 0:
        raise ValueError(f"{name} sıfırdan büyük olmalıdır!")

    return val


def validate_coupling(coupling):
    """Kuplaj modunun AC veya DC olduğunu doğrular."""
    if coupling is None or str(coupling).strip() == "":
        raise ValueError("Kuplaj modu boş bırakılamaz!")

    mode = str(coupling).strip().upper()
    if mode not in ["AC", "DC"]:
        raise ValueError(f"Geçersiz kuplaj modu: '{coupling}'. Sadece 'AC' veya 'DC' kullanılabilir!")

    return mode   
