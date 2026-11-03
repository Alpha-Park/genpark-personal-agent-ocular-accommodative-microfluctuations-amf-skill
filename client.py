"""
Accommodative Microfluctuations (AMF) Spectral Power Client.
Zero-mock pure Python standard library implementation.
Analyzes crystalline lens dynamic power oscillations, low-frequency component (LFC: <0.6 Hz),
and high-frequency component (HFC: 1.0-2.3 Hz) to quantify visual fatigue and ciliary spasm.
"""

import math
from typing import Dict, Any, List, Optional


class AccommodativeMicrofluctuationClient:
    """
    Evaluates dynamic accommodative microfluctuations (AMF) from high-speed continuous
    refractometer / autorefractor power time series.
    """

    def __init__(self, sampling_rate_hz: float = 10.0):
        if sampling_rate_hz <= 0:
            raise ValueError("Sampling rate must be positive.")
        self.sampling_rate_hz = sampling_rate_hz

    def analyze_amf(
        self,
        diopter_series: List[float],
        baseline_target_distance_m: float = 0.40,
        age_years: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculates spectral power distribution, HFC, LFC, and ciliary fatigue index.
        diopter_series: Refractive power recordings in Diopters (D) at sampling_rate_hz.
        baseline_target_distance_m: Visual stimulus distance in meters (e.g., 0.40 m for screen reading).
        """
        if not diopter_series or len(diopter_series) < 16:
            raise ValueError("Diopter series must contain at least 16 continuous samples.")
        if baseline_target_distance_m <= 0:
            raise ValueError("Target distance must be greater than zero.")

        n = len(diopter_series)
        mean_power = sum(diopter_series) / n
        variance = sum((x - mean_power) ** 2 for x in diopter_series) / n
        rms_amf = math.sqrt(variance)

        # Accommodative demand in Diopters
        accommodative_demand_d = 1.0 / baseline_target_distance_m
        accommodative_lag_lead_d = accommodative_demand_d - mean_power

        # Discrete Fourier Transform for spectral power estimation
        # We compute PSD across frequency bins from 0 to Nyquist (sampling_rate_hz / 2)
        half_n = n // 2
        power_spectrum = []
        frequencies = []

        # Hann window to minimize spectral leakage
        windowed = []
        for i in range(n):
            w = 0.5 * (1.0 - math.cos(2.0 * math.pi * i / (n - 1)))
            windowed.append((diopter_series[i] - mean_power) * w)

        total_window_energy = sum(w ** 2 for w in [0.5 * (1.0 - math.cos(2.0 * math.pi * i / (n - 1))) for i in range(n)])
        norm_factor = 2.0 / (total_window_energy * self.sampling_rate_hz) if total_window_energy > 0 else 1.0

        for k in range(1, half_n):
            freq = k * self.sampling_rate_hz / n
            frequencies.append(freq)
            # Real and imaginary components
            real_part = 0.0
            imag_part = 0.0
            for t in range(n):
                angle = 2.0 * math.pi * k * t / n
                real_part += windowed[t] * math.cos(angle)
                imag_part -= windowed[t] * math.sin(angle)
            psd = (real_part ** 2 + imag_part ** 2) * norm_factor
            power_spectrum.append(psd)

        # Integrate spectral power across classic physiological bands:
        # LFC (Low Frequency Component): 0.1 to 0.6 Hz
        # MFC (Mid Frequency Component): 0.6 to 1.0 Hz
        # HFC (High Frequency Component): 1.0 to 2.3 Hz
        power_lfc = 0.0
        power_mfc = 0.0
        power_hfc = 0.0

        for freq, psd in zip(frequencies, power_spectrum):
            df = self.sampling_rate_hz / n
            if 0.1 <= freq <= 0.6:
                power_lfc += psd * df
            elif 0.6 < freq < 1.0:
                power_mfc += psd * df
            elif 1.0 <= freq <= 2.3:
                power_hfc += psd * df

        # AMF Ratio (HFC / LFC)
        amf_ratio = power_hfc / (power_lfc + 1e-9)

        # Ciliary Fatigue Index:
        # Standard rested eye: HFC < 0.005 D^2, AMF ratio < 0.35
        # Under sustained mental/visual load: HFC elevates to > 0.015 D^2, AMF ratio > 0.8
        fatigue_score = min(100.0, max(0.0, (power_hfc * 2500.0) + (amf_ratio * 40.0)))

        if fatigue_score < 25.0:
            classification = "Optimal Visual Rest / Intact Accommodation"
            clinical_guidance = "Ciliary body microfluctuations display balanced autonomic tonus with minimal high-frequency spasm."
            break_urgency = "Low"
        elif fatigue_score < 50.0:
            classification = "Mild Accommodative Effort"
            clinical_guidance = "Slight elevation in high-frequency tremor; lens accommodation is engaged without significant fatigue."
            break_urgency = "Routine"
        elif fatigue_score < 75.0:
            classification = "Moderate Ciliary Strain / Impending Asthenopia"
            clinical_guidance = "Elevated HFC power indicates ciliary muscle hypertonicity and arterial pulsatile coupling. Practice 20-20-20 rule."
            break_urgency = "Elevated"
        else:
            classification = "Severe Asthenopia / Ciliary Spasm"
            clinical_guidance = "Pronounced HFC microfluctuation surge reflecting persistent spasm and accommodative fatigue. Immediate break recommended."
            break_urgency = "Immediate"

        return {
            "status": "success",
            "sample_count": n,
            "sampling_rate_hz": self.sampling_rate_hz,
            "accommodative_demand_d": round(accommodative_demand_d, 2),
            "mean_refractive_power_d": round(mean_power, 3),
            "accommodative_lag_d": round(accommodative_lag_lead_d, 3),
            "rms_microfluctuation_d": round(rms_amf, 4),
            "spectral_metrics": {
                "power_lfc_d2": round(power_lfc, 6),
                "power_mfc_d2": round(power_mfc, 6),
                "power_hfc_d2": round(power_hfc, 6),
                "amf_ratio_hfc_lfc": round(amf_ratio, 3)
            },
            "evaluation": {
                "ciliary_fatigue_index": round(fatigue_score, 1),
                "classification": classification,
                "break_urgency": break_urgency,
                "clinical_guidance": clinical_guidance
            }
        }
