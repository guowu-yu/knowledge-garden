---
title: 5G NR 无线接入架构速览
slug: 5g-nr-architecture
date: 2026-08-10
tags: [5G NR, 接入网, 架构]
summary: 从 gNB、CU/DU 拆分到 NG 接口，梳理 5G 无线接入网的核心组成与职责边界。
cover: https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=80
---

## 为什么先看架构

理解 5G，先抓住 **谁连谁、各自做什么**。NR（New Radio）接入侧以 **gNB** 为中心，对上连 5GC，对下服务 UE。

## 关键网元

- **UE**：终端，完成无线接入、移动性与业务承载。
- **gNB**：5G 基站，负责无线资源管理、调度、部分无线协议处理。
- **5GC**：核心网，负责会话、移动性、鉴权与策略等。

在云化/集中化部署中，gNB 常拆为：

| 单元 | 关注点 |
| --- | --- |
| **CU** | RRC / PDCP 等偏控制与高层处理 |
| **DU** | RLC / MAC / 高层 PHY 等实时性更强的部分 |
| **RU** | 射频与部分底层 PHY |

## 关键接口（记忆锚点）

- **Uu**：UE ↔ gNB 空口
- **Xn**：gNB ↔ gNB（切换、协作）
- **NG**：gNB ↔ 5GC（控制面/用户面）

## 回顾清单

1. CU/DU 拆分解决的是什么问题？（集中控制 vs 实时处理）
2. NSA 与 SA 在「基站是否直连 5GC」上有何不同？
3. 画一张：UE — gNB — AMF/UPF 的简图

> 一句话：5G 接入网是「可拆分的 gNB + 面向服务的核心网」组合拳。
