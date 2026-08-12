---
title: 天线端口、QCL 与 NR 资源网格
slug: antenna-port-qcl-resource-grid
date: 2026-08-12
tags: [天线端口, QCL, 资源网格, Point A, BWP, 38.211]
summary: 从天线端口与准共址出发，串起 RE/RB、Point A、CRB/PRB/VRB、BWP 与 Common MBS 频率资源。
cover: https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=80
---

## 本篇地图

对照 3GPP **TS 38.211**（约 4.4 节）把下面概念收成一条链：

1. 天线端口：逻辑发射身份，同端口信道可互推  
2. QCL：跨端口的大尺度特性可互推  
3. 资源网格 / RE / RB：时频最小单元与 12 子载波块  
4. Point A 与 CRB/PRB/VRB：多把“频域尺子”  
5. BWP 与 Common MBS 频率资源：UE 工作窗 vs 组播公共资源  

---

## 1. 天线端口（Antenna port）

**天线端口不是一根物理天线**，而是协议定义的**逻辑发射端口**。

规范关键句：

> 同一天线端口上，符号经历的信道可相互推断。

含义：若两个 RE 属于同一端口 p，UE 可用该端口参考信号（如 DMRS）估出的信道，去均衡同端口上的数据符号。

| 对比 | 说明 |
| --- | --- |
| 物理天线 | 真实辐射单元、阵列 |
| 天线端口 | UE 看到的“可参考信道身份” |
| 映射关系 | 一端口可映射到多根天线（预编码/波束） |

![天线端口与 QCL 关系示意](../assets/img/nr-resource/antenna-port-qcl.svg)

*图：物理天线阵 → 逻辑端口 → QCL 大尺度关系*

---

## 2. 准共址（QCL）

若两天线端口的**大尺度特性**可互相推断，则称 **QCL（Quasi Co-Location）**。

常见大尺度特性：

- 时延扩展、多普勒扩展 / 频移  
- 平均增益、平均时延  
- 空间接收参数（如到达角、波束相关）

**同端口**解决小尺度信道复用；**QCL** 解决跨端口（如 SSB/CSI-RS 与 PDSCH DMRS）的大尺度参数借用。

| QCL 类型（直觉） | 可推断内容 | 典型用途直觉 |
| --- | --- | --- |
| Type A | 时延/多普勒扩展、平均时延/多普勒、平均增益 | 时频跟踪 |
| Type B | 多普勒扩展、多普勒频移 | 高速等 |
| Type C | 平均时延、多普勒频移 | 同步/定时 |
| Type D | 空间接收参数 | 波束/接收空间滤波 |

> 记忆：同端口 ≈ 细信道；QCL ≈ 大尺度（尤其波束与跟踪）。

---

## 3. 资源网格 / RE / RB

### 资源网格
在给定 **numerology μ**（子载波间隔 SCS = 15×2^μ kHz）与**载波**下，定义二维网格：

**子载波 k × OFDM 符号 l**

还可再落在天线端口 p 上。

### RE（Resource Element）
网格最小时频单元：一个子载波 × 一个 OFDM 符号上的一个复数位置，记作 (k, l)，并关联端口 p、间隔配置 μ。

### RB（Resource Block）
**频域连续 12 个子载波** = 1 个 RB。

![资源网格 RE 与 RB 示意](../assets/img/nr-resource/resource-grid.svg)

*图：橙色格子为单个 RE；整块 12 行子载波示意 1 个 RB*

---

## 4. Point A 与资源块层次

NR 有多套 RB 编号，先抓住 **Point A**。

### Point A
**公共资源块（CRB）网格的参考原点**。  
PCell 下行常由 SSB 位置 + **`offsetToPointA`**（相对 SSB 最低 RB 等）一类参数确定。

### 层次对照

| 名称 | 尺子相对谁 | 记忆 |
| --- | --- | --- |
| **CRB** | Point A | 载波级公共刻度 |
| **PRB** | 某个 BWP | UE 当前工作窗内的本地编号 |
| **VRB** | 调度信令 | 可再映射到 PRB（连续或交织） |
| **Interlaced RB** | 交错图案 | 共享频谱等场景常见 |

![Point A 与 RB 层次示意](../assets/img/nr-resource/point-a-hierarchy.svg)

*图：SSB + 偏移钉住 Point A → CRB；BWP 内重编号为 PRB；调度侧常见 VRB→PRB*

```text
Point A → CRB（公共）
            ↓
         BWP 内 → PRB（本地）
调度授予 VRB → 映射 → PRB
必要时使用 interlaced RB
```

---

## 5. BWP 与 Common MBS 频率资源

### BWP（Bandwidth Part）
UE 在载波上**激活的一段连续 RB**，是调度与测量的工作带宽。

作用直觉：

- 不必始终占用整段载波  
- 可在宽/窄 BWP 间切换（吞吐 vs 省电/能力）

### Common MBS 频率资源（约 4.4.6）
面向 **组播/广播（MBS）** 的**公共频域资源**：多个 UE 在约定公共资源上接收同一传输，而不是各自单播 BWP 授予那么简单。

![BWP 与 Common MBS 频率资源示意](../assets/img/nr-resource/bwp-mbs.svg)

*图：激活 BWP 是 UE 单播工作窗；Common MBS 是组播/广播对齐的公共频域*

---

## 总串图

```text
物理天线 / 波束
    ↓ 映射
天线端口 p     ← 同端口：信道可互推
    ↓
QCL 关系       ← 跨端口：大尺度可互推

Point A 钉住 CRB
    ↓
BWP（连续 RB 工作窗）→ PRB
资源网格：RE (k,l,p,μ)；12 子载波 = RB
调度：VRB → PRB（或 interlaced）
MBS：Common MBS 频率资源
```

## 回顾清单

1. 为什么天线端口不是物理天线？  
2. “同端口可推信道”和“QCL 可推大尺度”差在哪？  
3. RE、RB、BWP 谁小谁大？  
4. Point A、CRB、PRB 分别是哪把尺子？  
5. Common MBS 频率资源解决的是什么对齐问题？

> 一句话：端口管“信道身份”，QCL 管“大尺度借用”，Point A/BWP 管“频域尺子与工作窗”。
