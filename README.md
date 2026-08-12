# 凌云知境 · Knowledge Garden

5G 通信知识回顾与整理站点。作者：**通信小鱼**。

## 架构

```
content/topics/*.md   # 每日专题（Markdown + YAML 头信息）
src/                  # 页面模板、样式、脚本
build.py              # 构建：Markdown → 静态站 + 搜索索引
dist/                 # 构建产物（GitHub Pages 发布）
.github/workflows/    # 推送 main 后自动发布
```

### 信息流

1. 在 `content/topics/` 新增或修改专题 Markdown  
2. `push` 到 `main`  
3. Actions 构建并发布到 GitHub Pages  
4. 首页搜索框读取 `search-index.json` 做本地检索  

### 专题 Front Matter

```yaml
---
title: 标题
slug: url-slug
date: YYYY-MM-DD
tags: [标签1, 标签2]
summary: 一句话摘要
cover: https://...  # 可选封面图
---
```

## 本地开发

```bash
pip install markdown
python build.py
# 用任意静态服务器打开 dist/，例如：
# python -m http.server -d dist 4173
```

## 站点品牌

- 中文名：**凌云知境**
- 副题：5G 通信知识园地
- 作者：通信小鱼
