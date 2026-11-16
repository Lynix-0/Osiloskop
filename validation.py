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

    if amp <=0:
        raise ValueError("Genlik sıfırdan büyük olmalıdır!")

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

def validate_signal_parameters(frequency, amplitude, phase_deg=0.0, offset=0.0):
    """Arayüzden gelen tüm sinyal parametrelerini tek seferde doğrular ve float olarak döndürür."""
    freq = validate_frequency(frequency)
    amp = validate_amplitude(amplitude)
    phase = validate_number(phase_deg, "Faz açısı")
    dc_offset = validate_number(offset, "DC Ofset")

    return {
        "frequency": freq,
        "amplitude": amp,
        "phase_deg": phase,
        "offset": dc_offset,
    }
       

    
