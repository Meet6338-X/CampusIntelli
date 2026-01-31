# Cost Estimation
## CampusIntelli Portal

---

## Estimation Methods

This document uses two estimation techniques:
1. **COCOMO II** - Constructive Cost Model for effort estimation
2. **Function Point Analysis** - Feature-based effort calculation

---

## 1. COCOMO II Estimation

### Project Size Estimation

| Module | Estimated SLOC | Language |
|--------|---------------|----------|
| Backend (Python) | 2,500 | Python |
| Frontend (HTML/CSS/JS) | 3,000 | Web |
| Tests | 800 | Python |
| **Total** | **6,300** | Mixed |

**KLOC** = 6.3 (Kilo Lines of Code)

### COCOMO II Basic Model

**Formula**: Effort = a × (KLOC)^b

For **Organic** project type (small team, familiar technology):
- a = 2.4
- b = 1.05

**Calculation**:
```
Effort = 2.4 × (6.3)^1.05
Effort = 2.4 × 7.12
Effort = 17.09 Person-Months
```

### Development Time

**Formula**: Time = c × (Effort)^d

For Organic:
- c = 2.5
- d = 0.38

**Calculation**:
```
Time = 2.5 × (17.09)^0.38
Time = 2.5 × 2.94
Time = 7.35 months ≈ 8 months (with buffer)
```

### Team Size

**Formula**: Team = Effort / Time

```
Team = 17.09 / 7.35
Team = 2.32 ≈ 2-3 developers
```

### COCOMO Summary

| Metric | Value |
|--------|-------|
| Project Size | 6.3 KLOC |
| Effort | ~17 Person-Months |
| Duration | ~8 Months |
| Team Size | 2-3 Developers |

---

## 2. Function Point Analysis

### Module: Room Booking System

Counting function points for the Room Booking feature:

#### External Inputs (EI)
| Function | Complexity | FP |
|----------|------------|-----|
| Create Booking | Average | 4 |
| Cancel Booking | Low | 3 |
| Update Booking | Average | 4 |
| **Subtotal** | | **11** |

#### External Outputs (EO)
| Function | Complexity | FP |
|----------|------------|-----|
| Booking Confirmation | Low | 4 |
| Available Rooms List | Average | 5 |
| My Bookings List | Low | 4 |
| **Subtotal** | | **13** |

#### External Inquiries (EQ)
| Function | Complexity | FP |
|----------|------------|-----|
| Check Room Availability | Low | 3 |
| View Booking Details | Low | 3 |
| **Subtotal** | | **6** |

#### Internal Logical Files (ILF)
| Function | Complexity | FP |
|----------|------------|-----|
| Bookings Table | Average | 10 |
| Rooms Table | Low | 7 |
| **Subtotal** | | **17** |

#### External Interface Files (EIF)
| Function | Complexity | FP |
|----------|------------|-----|
| User Data (from Auth) | Low | 5 |
| **Subtotal** | | **5** |

#### Total Unadjusted Function Points

| Category | FP |
|----------|-----|
| External Inputs | 11 |
| External Outputs | 13 |
| External Inquiries | 6 |
| Internal Logical Files | 17 |
| External Interface Files | 5 |
| **Total UFP** | **52** |

#### Value Adjustment Factor (VAF)

| Factor | Rating (0-5) |
|--------|-------------|
| Data Communications | 3 |
| Distributed Processing | 1 |
| Performance | 3 |
| Heavily Used Config | 2 |
| Transaction Rate | 2 |
| Online Data Entry | 4 |
| End User Efficiency | 3 |
| Online Update | 4 |
| Complex Processing | 2 |
| Reusability | 3 |
| Installation Ease | 4 |
| Operational Ease | 4 |
| Multiple Sites | 1 |
| Facilitate Change | 3 |
| **Total Degree of Influence (TDI)** | **39** |

**VAF** = 0.65 + (0.01 × TDI) = 0.65 + 0.39 = **1.04**

#### Adjusted Function Points

```
AFP = UFP × VAF
AFP = 52 × 1.04
AFP = 54.08 ≈ 54 FP
```

### Full System Function Points

| Module | UFP | AFP |
|--------|-----|-----|
| Authentication | 35 | 36 |
| Timetable | 28 | 29 |
| Assignments | 65 | 68 |
| Gradebook | 30 | 31 |
| Room Booking | 52 | 54 |
| Announcements | 25 | 26 |
| QR Attendance | 45 | 47 |
| Analytics | 40 | 42 |
| Admin Panel | 55 | 57 |
| **Total** | **375** | **390** |

### Effort from Function Points

Industry average: 10-15 hours per function point for Python/Web

```
Effort = 390 FP × 12 hours/FP
Effort = 4,680 hours
Effort = 4,680 / 160 hours/month
Effort = 29.25 Person-Months
```

*Note: This is higher than COCOMO due to full feature scope*

---

## 3. Cost Breakdown (Hypothetical)

### Assuming In-House Development

| Resource | Rate/Month | Duration | Cost |
|----------|-----------|----------|------|
| Developer 1 | $5,000 | 8 months | $40,000 |
| Developer 2 | $5,000 | 8 months | $40,000 |
| QA Engineer | $4,000 | 4 months | $16,000 |
| Project Manager | $6,000 | 8 months | $48,000 |
| **Subtotal** | | | **$144,000** |

### Infrastructure Costs (Annual)

| Item | Cost |
|------|------|
| Domain | $12 |
| Hosting (VPS) | $240 |
| SSL Certificate | $0 (Let's Encrypt) |
| Supabase (Future) | $0-$25/month |
| **Annual Total** | **~$550** |

### Total Project Cost

| Category | Cost |
|----------|------|
| Development | $144,000 |
| Infrastructure (Year 1) | $550 |
| Contingency (15%) | $21,600 |
| **Grand Total** | **$166,150** |

---

## 4. Estimation Comparison

| Method | Effort | Duration |
|--------|--------|----------|
| COCOMO II (Basic) | 17 PM | 8 months |
| Function Point Analysis | 29 PM | 8 months |
| **Average** | **23 PM** | **8 months** |

*Difference due to FPA counting all features, COCOMO using code size estimate*

---

## 5. Estimation Confidence

| Estimate Type | Confidence | Range |
|---------------|------------|-------|
| Effort | Medium | ±25% |
| Duration | High | ±10% |
| Cost | Low | ±30% |

---

**Recommendations:**
1. Use COCOMO for high-level budgeting
2. Use FPA for detailed module planning
3. Re-estimate after Sprint 1 with actual velocity
4. Track actuals vs. estimates for future projects

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-31
