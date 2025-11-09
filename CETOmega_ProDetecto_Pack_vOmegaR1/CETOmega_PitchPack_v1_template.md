# CET Ω — PitchPack v1 (4 páginas)

> **Propósito**: Documento conciso para iniciar colaboración experimental (AI / OM / cQED) y acordar un MRV (Minimum Runnable Verification).

---

## 1. Motivación y falsabilidad (1 página)
- **Qué**: CET Ω es un marco causal-informacional con correcciones no locales **positivas y causales**.
- **Cómo se falsifica**:
  1) Violación de positividad (matrices de Hankel no p.s.d.).
  2) Requerir polos complejos o adelantos (no-retardo).
  3) No reproducir una **firma Stieltjes** en barridos de frecuencia.
- **Firma experimental**: desviaciones pequeñas pero **monótonas y saturantes** en fase/frecuencia/ancho (10⁻⁴–10⁻³).

**Resultado mínimo publicable**: detección ≥5σ **o** límite superior competitivo + tests (positividad/causalidad) superados.

---

## 2. Especificación de kernel y magnitud prevista (1 página)
- Kernel **Padé–Stieltjes** (1–3 polos). Todos los pesos **c_j > 0**, masas **m_j > 0**.
- Escala objetivo: **M*** ≈ 10⁻³ m⁻¹.
- **Ejemplo (vΩ.R1)**:
  - j1: m₁ = 8×10⁻⁴ m⁻¹, c₁ = 6×10⁻⁴
  - j2: m₂ = 2×10⁻³ m⁻¹, c₂ = 5×10⁻⁴
- **Observables target**:
  - **AI**: |Δφ| ≥ 1×10⁻⁴ rad @ 0.1–10 kHz
  - **OM**: |δω/ω| ≥ 1×10⁻⁴; δγ/γ ≥ 1×10⁻⁴
  - **cQED**: |δω_r/ω_r| ≥ 1×10⁻⁴; δκ/κ ≥ 1×10⁻⁴

---

## 3. Requisitos instrumentales mínimos (1 página)
**AI (Interferometría atómica)**
- UHV ≤ 1×10⁻¹² mbar, vibración ≤ 1×10⁻⁸ g/√Hz
- Estabilidad láser < 1×10⁻¹³; T₂ ≥ 1 s; secuencias k-reversal/phase-cycling

**OM (Optomecánica)**
- Qₘ ≥ 10⁷; Tₑff ≤ 100 μK; readout ≤ 1×10⁻¹⁹ m/√Hz
- Barridos en detuning y potencia; *two-tone thermometry*

**cQED (Transmon + resonador)**
- Qᵣ ≥ 10⁶; T₁ ≥ 100 μs; Tφ ≥ 50 μs; T ≈ 10 mK
- Espectros de transmisión; Ramsey; *Purcell scan*

---

## 4. Plan de medición y verificación (1 página)
- **MRV**: 5–7 puntos en frecuencia + potencias/detunings (según plataforma).
- **Controles**: canales *null*, corridas ciegas (blind injections), rotaciones de base.
- **Análisis**:
  - Ajuste Padé (1–3 polos) con pesos positivos.
  - **Hankel p.s.d.** (orden 3–4), **Kramers–Kronig** (proxy) y monotonicidad/saturación.
- **Criterio GO/NO-GO**:
  - **GO**: tendencia Stieltjes + SNR≥3 en ≥2 frecuencias.
  - **NO-GO**: necesidad de polos complejos/negatividades, o ausencia total de tendencia.