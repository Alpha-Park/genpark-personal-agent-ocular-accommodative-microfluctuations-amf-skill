---
name: genpark-personal-agent-ocular-accommodative-microfluctuations-amf-skill
description: Dynamic Ocular Accommodative Microfluctuations (AMF) spectral power analyzer. Evaluates crystalline lens dynamic focal oscillations, low-frequency component (LFC: <0.6 Hz), and high-frequency component (HFC: 1.0-2.3 Hz) to quantify visual fatigue and ciliary spasm.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - vision
  - optometry
  - asthenopia
  - ciliary-muscle
  - openclaw
  - genpark
  - mcp
---

# Ocular Accommodative Microfluctuations (AMF) Analysis Skill

## Overview
This skill computes the power spectral density (PSD) of high-speed continuous refractometer / autorefractor power recordings, isolating:
- **Low-Frequency Component (LFC: 0.1 - 0.6 Hz)**: Attributable to systemic slow visual drift, depth of focus exploration, and breathing fluctuations.
- **High-Frequency Component (HFC: 1.0 - 2.3 Hz)**: Directly correlated with arterial pulse micro-oscillations transmitted to the ciliary body and heightened sympathetic/parasympathetic tonus under visual stress.

Elevations in the HFC power and the `AMF_Ratio (HFC/LFC)` provide an early objective bio-marker for digital eye strain, visual asthenopia, and crystalline lens ciliary muscle spasm.

## Mathematical Formulation
1. **Accommodative Demand**:
   $$D = \frac{1}{\text{Target Distance (m)}}$$
2. **Discrete Power Spectral Density (PSD)**:
   $$X(k) = \sum_{t=0}^{N-1} x_w(t) e^{-i 2\pi k t / N}$$
3. **Band Power Integration**:
   $$P_{\text{HFC}} = \int_{1.0}^{2.3} S(f) df$$
   $$\text{AMF Ratio} = \frac{P_{\text{HFC}}}{P_{\text{LFC}} + \epsilon}$$
4. **Ciliary Fatigue Index (CFI)**:
   $$\text{CFI} = \min\left(100, \max\left(0, P_{\text{HFC}} \cdot 2500 + \text{AMF Ratio} \cdot 40\right)\right)$$

## Usage
```python
from client import AccommodativeMicrofluctuationClient

client = AccommodativeMicrofluctuationClient(sampling_rate_hz=10.0)
result = client.analyze_amf(
    diopter_series=[2.50, 2.52, 2.48, 2.55, ...],
    baseline_target_distance_m=0.40
)
print(result["evaluation"]["classification"])
```
