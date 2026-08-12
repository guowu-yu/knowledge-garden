---
title: 5G 帧结构与 SS/PBCH Block
slug: frame-structure-ssb
date: 2026-08-12
tags: [5G, FrameStructure, SSB]
summary: 5G 的帧结构构成以及 SS/PBCH Block 的时频资源映射。
cover: https://images.unsplash.com/photo-1544197150-b99a580bb7a2?auto=format&fit=crop&w=1600&q=80
---

## 帧结构与物理资源

### Numerologies（子载波间隔）

NR 支持多种 OFDM 参数集（numerology）。下行或上行带宽部分（BWP）的子载波间隔与循环前缀分别由高层参数 **subcarrierSpacing**、**cyclicPrefix** 给出（见表 4.2-1）。

| μ | 子载波间隔 Δf | 循环前缀 | 典型场景 |
| :---: | :---: | :---: | :--- |
| 0 | 15 kHz | Normal | FR1 基线 |
| 1 | 30 kHz | Normal | FR1 常用 |
| 2 | 60 kHz | Normal / Extended | FR1/FR2；扩展 CP 用于大时延扩展 |
| 3 | 120 kHz | Normal | FR2 |
| 4 | 240 kHz | Normal | FR2（如 SSB） |
| 5 | 480 kHz | Normal | 更高频段演进 |
| 6 | 960 kHz | Normal | 更高频段演进 |

**记忆**：子载波间隔 = 15 × 2^μ kHz；μ 越大，符号越短、时隙越多，越适合高频与低时延。

## 帧结构

### 1. 帧与子帧

下行、上行、旁链路传输均按帧组织：**每帧时长 10 ms，含 10 个子帧（各 1 ms）**。

- 每帧分为两个半帧（各 5 个子帧）。
- 每个载波上，上行与下行各有一套帧编号。
- UE 侧上行帧相对下行帧提前发送，提前量由定时提前（TA）等决定；NTN 场景还可叠加公共定时漂移、星历/位置相关补偿（见 TS 38.213）。

### 2. 时隙（Slot）

对子载波间隔配置 μ，时隙在子帧内编号为 0 … 2^μ−1，在帧内编号为 0 … 10·2^μ−1。常规 CP 下每时隙通常为 **14** 个 OFDM 符号（扩展 CP 为 12）。

| μ | 每时隙符号数（常规 CP） | 每子帧时隙数 | 每帧时隙数 |
| :---: | :---: | :---: | :---: |
| 0 | 14 | 1 | 10 |
| 1 | 14 | 2 | 20 |
| 2 | 14 | 4 | 40 |
| 3 | 14 | 8 | 80 |
| 4 | 14 | 16 | 160 |
| 5 | 14 | 32 | 320 |
| 6 | 14 | 64 | 640 |

**时隙内符号可标记为 downlink / flexible / uplink**（时隙格式见 TS 38.213）。非全双工 UE 在收发切换时需满足规范给出的过渡时间约束（含 DAPS 切换场景）。

## 同步信号与小区 ID

物理层小区标识共 1008 个：

**NID_cell = 3 · NID⁽¹⁾ + NID⁽²⁾**

- **PSS**：主同步信号，检测 NID⁽²⁾（0…2）。
- **SSS**：辅同步信号，结合 PSS 得到完整小区 ID。

## PBCH

- 比特在调制前加扰；加扰初始化与候选 SSB 索引的低位比特等相关。
- 采用 QPSK 调制。
- 映射到物理资源在 §7.4.3 SS/PBCH block 中与 PSS/SSS/DM-RS 一并描述。

典型接收链路：

```text
CORESET / PDCCH → 调度 DCI → PDSCH → UE 解调（靠 DM-RS）
```

## SS/PBCH 块（SSB）

- **时域**：1 个 SSB = 4 个连续 OFDM 符号（符号 0…3）。
- **频域**：240 个连续子载波（编号 0…239）。
- PSS、SSS、PBCH 及 PBCH DM-RS 按表 7.4.3.1-1 映射到 SSB 内时频位置。
- **PSS/SSS/PBCH/DM-RS 使用同一天线端口、相同 CP 与子载波间隔**。
- 相对 Point A 的子载波偏移由 `ssb-SubcarrierOffset` 与 PBCH 载荷比特等共同确定（FR1 / FR2、共享频谱规则不同）。
- 存在 Type A / Type B 等结构差异（尤其 FR2 / FR2-2）。
- 相同索引、相同中心频点的 SSB 可假设在多普勒、时延、空间 Rx 等参数上 QCL。

> **PSS + SSS + PBCH + DM-RS = SS/PBCH block**

### 时频资源图示

[![SSB 时频资源示意](https://s41.ax1x.com/2026/08/12/pmLlXUf.png)](https://imgchr.com/i/pmLlXUf)

表 7.4.3.1-1：SS/PBCH block 内 PSS、SSS、PBCH 与 PBCH DM-RS 的资源映射（示意）：

| 信号 | 时域符号（SSB 内） | 频域子载波（示意） |
| --- | --- | --- |
| PSS | 符号 0 | 中间 127 个子载波 |
| SSS | 符号 2 | 中间 127 个子载波 |
| PBCH | 符号 1、2、3 | 与 PSS/SSS 交错分布，共约 576 个 RE（含 DM-RS） |
| PBCH DM-RS | 与 PBCH 同符号 | 按固定间隔插入 |

## 回顾

1. 5G 相较 LTE 在帧结构 / numerology 上的主要区别是什么？
2. SSB 由哪些信号构成，时频占用各是多少？
