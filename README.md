# Ocular Accommodative Microfluctuations (AMF) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Dynamic Ocular Accommodative Microfluctuations (AMF) Spectral Analyzer. Evaluates crystalline lens focal oscillations, low-frequency component (LFC: <0.6 Hz), and high-frequency component (HFC: 1.0-2.3 Hz) to quantify visual fatigue and ciliary spasm.

```mermaid
flowchart TD
    A[Continuous Diopter Time Series] --> B[Hann Windowing & Mean Subtraction]
    B --> C[Discrete Fourier Transform PSD]
    C --> D[Band Integration: LFC 0.1-0.6 Hz]
    C --> E[Band Integration: HFC 1.0-2.3 Hz]
    D & E --> F[AMF Ratio Calculation: HFC / LFC]
    F --> G[Ciliary Fatigue Index & Ergonomic Classification]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Fourier Spectral Decomposition**: Hann-windowed discrete power spectrum analysis.
- **Objective Ergonomics**: Identifies ciliary hypertonicity and digital screen visual fatigue before subjective eyestrain symptoms escalate.
- **Dual Architecture**: Supports native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio interface.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
