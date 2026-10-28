# CCSDS 922.3-B-1 Forward Frame Service (FF-CSTS) Specification

**Document**: CCSDS 922.3-B-1 (Blue Book, Issue 1, April 2021\)  
**Framework**: CCSDS 921.1-B-2 (Cross Support Transfer Services — Specification Framework)  
**System**: FFCSTSForge Pro (v1.0.0)

## 1\. Executive Summary & Architectural Scope

CCSDS 922.3-B-1 defines the Forward Frame Service (FF-CSTS), an international cross-support transfer service within the CCSDS CSTS framework. It enables a spacecraft Mission Operations Center (the User, such as NASA JPL, ESA ESOC, JAXA) to transfer raw, uncoded Forward Transfer Frames (TC, AOS, or USLP) to a tracking ground station network (the Provider, such as NASA DSN, ESA ESTRACK, KSAT) for channel coding, Attached Sync Marker (ASM) attachment, RF subcarrier modulation, and radiative uplink transmission.

## 2\. Service Architecture & State Machine

- State Transitions (§3.2): State 1 (UNBOUND) \-\> State 2 (READY) \-\> State 3 (ACTIVE).  
- Supported Protocols: TC (CCSDS 232.0), AOS (CCSDS 722.0), and USLP (CCSDS 732.1).  
- Scheduling Modes: IMMEDIATE (FIFO) and TIMED (Earth Transmission Time ETT).  
- Carrier States: OFF, UNMODULATED, and MODULATING.