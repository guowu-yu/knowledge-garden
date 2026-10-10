# 5G NTN 专题学习路线图

> 更新日期：2026-10-10 ｜ 站点：https://guowu-yu.github.io/knowledge-garden/
> 用法：逐个专题学习，完成后勾选；每个专题发布到知识站后把状态改为「已上线」并附链接。
>
> **当前进度**：已完成 15 篇（综合/再生载荷/UE 能力/SIB19/随机接入/多普勒/调度与 HARQ/定时器全表/移动性与卫星切换/功控/RLM 与 BFM/测量与 CSI/信道与链路预算/Rel-18 增强全集/轨道与系统架构深读），剩余 6 个待学专题。建议顺序：P3 射频频段 → P3 IoT NTN → P3 Rel-19/未来 → P3 TN/NTN 混合组网 → P3 IDLE/INACTIVE 行为。

## 已完成（基础层 · 静态视角）

| 状态 | 专题 | 回答的问题 | 线上地址 |
| --- | --- | --- | --- |
| ✅ 已上线 | 5G NTN 综合专题 | NTN 是什么、为什么要补偿 | https://guowu-yu.github.io/knowledge-garden/topics/5g-ntn.html |
| ✅ 已上线 | NTN 再生载荷（gNB 上星） | gNB 放在哪里（透明 vs 再生） | https://guowu-yu.github.io/knowledge-garden/topics/ntn-regenerative-payload.html |
| ✅ 已上线 | NTN UE 能力 | 终端声明自己能干什么 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-ue-capability.html |
| ✅ 已上线 | NTN SIB19 | 预补偿参数从哪广播下来 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-sib19.html |
| ✅ 已上线 | NTN 多普勒与时频补偿 | 时延与多普勒如何被预补偿、残差预算 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-doppler.html |
| ✅ 已上线 | NTN 随机接入增强 | RACH 在 NTN 里如何被自举反转改造 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-rach.html |
| ✅ 已上线 | NTN 调度与 HARQ | 停等重传在长管道里如何各就其位 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-harq.html |
| ✅ 已上线 | NTN 定时器与定时关系全表 | 偏移/拉长/新生三类机制、T430、全表汇总 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-timers.html |
| ✅ 已上线 | NTN 移动性与卫星切换 | 几何/时间驱动切换、CHO、硬/软换星重同步 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-mobility.html |
| ✅ 已上线 | NTN 功率控制 | 开环主导闭环微调、链路预算、功率等级与 PHR | https://guowu-yu.github.io/knowledge-garden/topics/ntn-power.html |
| ✅ 已上线 | NTN 无线链路监测与 BFM | RLM/BFD 判决机制、Rel-17 为何关闭 BFR、可预测与突发劣化的工程分工 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-rlm-bfm.html |
| ✅ 已上线 | NTN 测量与 CSI 上报 | 近远效应与位置/时间触发、CSI 老化与 K_offset、测量 gap 与 gap 内读 SI | https://guowu-yu.github.io/knowledge-garden/topics/ntn-measurement-csi.html |
| ✅ 已上线 | NTN 信道与链路预算 | 38.811 大尺度五件套、仰角新坐标轴、38.821 链路预算瀑布、S/Ka 两本余量账 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-channel-link-budget.html |
| ✅ 已上线 | Rel-18 NTN 增强全集 | FR2 Ka 频段（n510/511/512 与 VSAT 分级）、上行覆盖增强、NTN-TN/NTN-NTN 移动性、网络侧位置验证 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-rel18-enhancements.html |
| ✅ 已上线 | NTN 轨道与系统架构深读 | 斜距公式与 38.821 几何数字、三种波束模式、透明 vs 再生、五参考场景、馈电切换 | https://guowu-yu.github.io/knowledge-garden/topics/ntn-orbit-architecture.html |

---

## 待学习（6 个专题 · 动态过程视角）

### 模块一：接入与链路层过程（怎么接入、怎么发数据）

| 状态 | 专题 | 核心问题 | 规范锚点 | 优先级 |
| --- | --- | --- | --- | --- |
| ✅ 已上线 | NTN 随机接入增强 | PRACH 长前导、MSG1/MSG3 重传放大、ra-ResponseTimer 容忍分钟级延迟、两步 RACH 在 NTN 的适配 | 38.213 / 38.321 | P1 |
| ✅ 已上线 | NTN 多普勒与时频补偿 | UE 预补偿的具体算法：GNSS 时钟如何换算频偏、LoS 多普勒模型、公共/专用频偏的分工 | 38.211 / TR 38.811 | P1 |
| ✅ 已上线 | NTN 功率控制 | 路损估计基于 UE 位置而非测量、开环主导 + 闭环失配、PUSCH/PUCCH/PRACH 功控适配 | 38.213 §7 | P2 |
| ✅ 已上线 | NTN 调度与 HARQ | 32 个 HARQ 进程、feedback-disabled 模式与盲重传、Koffset 对调度时序的重塑、RLC/ARQ 大窗口 | 38.214 / 38.321 | P1 |

### 模块二：连接保持与移动性（怎么不掉线、怎么换星）

| 状态 | 专题 | 核心问题 | 规范锚点 | 优先级 |
| --- | --- | --- | --- | --- |
| ✅ 已上线 | NTN 定时器与定时关系全表 | 所有被放大的定时器：T310、DRX、MAC/RLC/PDCP 计时器、SI 窗口——一张表看懂「大时延改写了哪些钟」 | 38.321 / 38.331 | P1 |
| ✅ 已上线 | NTN 无线链路监测与 BFM | RLM/BFD 定时放大、慢衰落与卫星遮蔽的区分、Rel-17 关闭 BFR 的取舍、波束失败恢复在 NTN 的替代路径 | 38.213 §6 / 38.321 §5.17 | P2 |
| ✅ 已上线 | NTN 移动性与卫星切换 | 事件 D1/D2、条件切换（CHO）、硬切换/软切换/换星重同步、多波束小区边界管理 | 38.331 / 38.304 | P1 |
| ✅ 已上线 | NTN 测量与 CSI 上报 | 近远效应使 RSRP 失灵、位置/时间触发测量发起与 CondEvent T1/D1、CSI-RS 支持收窄与 TRS、K_offset 下的 CSI 老化、测量 gap 与 Rel-18 gap 内读 SI | 38.214 / 38.133 / 38.304 | P2 |
| ☐ | NTN IDLE/INACTIVE 态行为 | 基于 t-Service 的重选、位置触发测量、多 TAC 寻呼区域、TN/NTN 边界驻留策略 | 38.304 / 38.300 | P3 |

### 模块三：架构与工程（系统怎么设计、链路怎么算）

| 状态 | 专题 | 核心问题 | 规范锚点 | 优先级 |
| --- | --- | --- | --- | --- |
| ✅ 已上线 | 轨道与系统架构 | 轨道几何（斜距/仰角/延迟账）、准地球固定 vs 移动波束、透明 vs 再生载荷、馈电链路切换、38.821 五场景三轴组合 | TR 38.811 / 38.821 | P2 |
| ✅ 已上线 | NTN 信道与链路预算 | TR 38.811 信道模型（FSPL/杂波/阴影/大气/闪烁、TDL/CDL）、雨衰（ITU-R P.618）、遮蔽分级、EIRP/G/T 与链路预算计算实务 | TR 38.811 / 38.821 / P.618 | P2 |
| ☐ | NTN 射频与频段 | n255/n256 频段、UE 功率等级与带外发射、双卫星同时收发的射频要求 | 38.101-5 / 38.307 | P3 |
| ☐ | IoT NTN（NB-IoT/eMTC） | Rel-17/18/19 IoT NTN 与 NR NTN 的差异、SIB31、GNSS 定位增强、极端覆盖 | 36 系列 / 38.331 | P3 |

### 模块四：演进与组网（往哪走）

| 状态 | 专题 | 核心问题 | 规范锚点 | 优先级 |
| --- | --- | --- | --- | --- |
| ✅ 已上线 | Rel-18 NTN 增强全集 | Ka 频段频谱版图与 VSAT 分级、上行覆盖增强、TN/NTN 移动性接顺、RTT 位置验证、&gt;10 GHz 补偿与 IoT 节电 | TR 38.821 / 38.331 | P2 |
| ☐ | Rel-19 NTN 与未来 | IoT 增强、NTN 载波聚合、5G 核心网经再生载荷、6G NNI 展望 | TR 38.863 等 | P3 |
| ☐ | TN/NTN 混合组网 | 小区选择/重选偏好、ANR、切换策略、地面网 + 星座协同的运营商部署模式 | 38.300 / 38.304 | P3 |

---

## 建议学习顺序

1. **先啃 P1 的 6 个**：随机接入增强 → 多普勒补偿 → 调度与 HARQ → 定时器全表 → 卫星切换（NTN 相对地面 5G 改动最狠、最常被问的地方）
2. **再补 P2 的 2 个**：功控、RLM/BFM ✅、测量 CSI ✅、链路预算 ✅、Rel-18 全集 ✅、架构 ✅（P2 工程完整性达成）
3. **最后 P3 的 3 个**：射频频段、IoT NTN、Rel-19/混合组网（面向演进方向）

> 性价比提示：「NTN 定时器与定时关系全表」一张表收尽 T310/DRX/HARQ RTT/SI 窗口的放大量纲，与已发布的 SIB19 有效期、再生载荷 HARQ RTT 两篇互为索引。
