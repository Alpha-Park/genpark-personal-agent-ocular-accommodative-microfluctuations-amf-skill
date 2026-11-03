"""
Example usage of Accommodative Microfluctuations (AMF) Skill.
Demonstrates baseline resting accommodation vs digital visual fatigue / ciliary strain.
"""

import json
import math
from client import AccommodativeMicrofluctuationClient


def main():
    print("=== Testing Accommodative Microfluctuations (AMF) Skill ===")
    client = AccommodativeMicrofluctuationClient(sampling_rate_hz=10.0)

    # 1. Rested state simulation (64 samples, steady 2.5 D with subtle low-frequency drift)
    rested_series = [
        2.5 + 0.08 * math.sin(2 * math.pi * 0.25 * (t / 10.0)) + 0.02 * math.sin(2 * math.pi * 1.5 * (t / 10.0))
        for t in range(64)
    ]
    res_rested = client.analyze_amf(rested_series, baseline_target_distance_m=0.40)
    print("\n[Case 1: Rested Eye - 0.40m Reading Distance]")
    print(json.dumps(res_rested, indent=2))

    # 2. Fatigued / Asthenopic state simulation (elevated high-frequency tremor 1.8 Hz, ciliary hypertonicity)
    fatigued_series = [
        2.2 + 0.06 * math.sin(2 * math.pi * 0.2 * (t / 10.0)) + 0.16 * math.sin(2 * math.pi * 1.8 * (t / 10.0))
        for t in range(64)
    ]
    res_fatigued = client.analyze_amf(fatigued_series, baseline_target_distance_m=0.40)
    print("\n[Case 2: Prolonged Screen Stare - Ciliary Strain / High HFC]")
    print(json.dumps(res_fatigued, indent=2))

    # Assertions
    assert res_rested["status"] == "success"
    assert res_fatigued["status"] == "success"
    assert res_fatigued["evaluation"]["ciliary_fatigue_index"] > res_rested["evaluation"]["ciliary_fatigue_index"]
    print("\n[SUCCESS] All Accommodative Microfluctuations (AMF) test cases passed!")


if __name__ == "__main__":
    main()
