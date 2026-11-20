---
title: "AI 极客喜欢的云计算资源：带免费层的常用清单"
date: 2026-11-20T10:00:00+08:00
draft: false
description: "主机、开发环境、应用托管、数据库、AI 模型、组网邮箱，六类带免费层的云资源一览。"
summary: "想给智能体安家、搭网站、跑模型，先看看这些带免费层的云资源。"
categories: ["Ai极客喜欢的云计算资源"]
tags: ["免费云服务", "VPS", "PaaS", "AI", "智能体"]
---

想给自己的 AI 智能体安个家、搭个小网站、跑个模型实验，其实不必一上来就掏钱。下面是互联网上口碑不错、带免费层的云资源，按用途分成六组，每条写了它是什么、免费能用到什么程度。

![一个打开的工具箱，格子里放着服务器、数据库、模型、邮件和网络的小图标](inline.webp)

## 云主机与 VPS

{{< pick name="Oracle Cloud Always Free" url="https://www.oracle.com/cloud/free/" mark="" >}}口碑最好的永久免费云主机，ARM 实例给得很大方；注册要绑卡验证，热门区域常常抢不到机器。{{< /pick >}}

{{< pick name="Google Cloud Free Tier" url="https://cloud.google.com/free" mark="" >}}永久免费一台 e2-micro 小主机（限美国部分区域），新用户另有试用赠金；需要绑卡。{{< /pick >}}

{{< pick name="AWS Free Tier" url="https://aws.amazon.com/free/" mark="" >}}新账号送试用额度，EC2、S3、Lambda 等常用服务都能练手；需要绑卡，记得设账单提醒。{{< /pick >}}

{{< pick name="Azure Free Account" url="https://azure.microsoft.com/free/" mark="" >}}新账号 12 个月热门服务免费，外加首月赠金；需要绑卡。{{< /pick >}}

{{< pick name="EUserv VS2-free" url="https://www.euserv.com/en/virtual-private-server/root-vserver/v2/vs2-free.php" mark="" >}}德国老牌主机商的免费 IPv6-only 小 VPS，资源很小、经常缺货，适合玩 IPv6 和轻量服务。{{< /pick >}}

{{< pick name="Openworld" url="https://openworld.eu.org" mark="own" >}}欧洲社区运营的免费 Proxmox VPS，按周续期，热门时段常缺货，需要蹲补货。{{< /pick >}}

{{< pick name="weeny.cloud" url="https://weeny.cloud" mark="wait" >}}面向 AI 智能体的轻量 VPS，免费名额要排队候补。{{< /pick >}}

{{< pick name="Altare" url="https://altare.gg" mark="own" >}}每个团队永久免费 6 GB 内存、1.5 核、10 GB 硬盘，可拆成最多 4 台，含可 root SSH 的 Linux 沙盒；不承诺在线率。{{< /pick >}}


## 开发环境与笔记本

{{< pick name="InstaBox" url="https://instabox.sh" mark="own" >}}给开发者和智能体的云端 Linux 机器，免费版 4 核 8 GB，闲置自动挂起，能装 VS Code 网页版和 Jupyter。{{< /pick >}}

{{< pick name="GitHub Codespaces" url="https://github.com/features/codespaces" mark="" >}}浏览器里的 VS Code 开发容器，个人账号每月有免费核心时长。{{< /pick >}}

{{< pick name="Google Colab" url="https://colab.research.google.com" mark="" >}}免费的 Jupyter 笔记本，附带有限的 GPU，跑模型实验的入门首选。{{< /pick >}}

{{< pick name="Kaggle Notebooks" url="https://www.kaggle.com" mark="" >}}每周有免费 GPU/TPU 时长，数据集和竞赛生态很丰富。{{< /pick >}}

{{< pick name="Lightning AI Studios" url="https://lightning.ai" mark="" >}}云端开发工作室，开箱即用的 GPU 环境，每月有免费额度。{{< /pick >}}


## 应用托管

{{< pick name="GitHub Pages" url="https://pages.github.com" mark="own" >}}静态网站免费托管，配合 Actions 自动构建部署，能绑自定义域名并开 HTTPS。{{< /pick >}}

{{< pick name="Cloudflare Workers & Pages" url="https://workers.cloudflare.com" mark="" >}}在全球边缘跑 JS/TS，免费版每天 10 万次请求，静态站点带宽不限。{{< /pick >}}

{{< pick name="Vercel" url="https://vercel.com" mark="" >}}前端和 Next.js 部署的首选，Hobby 免费版限非商业用途。{{< /pick >}}

{{< pick name="Netlify" url="https://www.netlify.com" mark="" >}}老牌静态站点和函数托管，免费版够个人项目用。{{< /pick >}}

{{< pick name="Render" url="https://render.com" mark="" >}}免费 Web 服务能直接跑后端，闲置约 15 分钟会休眠，首次访问冷启动较慢。{{< /pick >}}

{{< pick name="Deno Deploy" url="https://deno.com/deploy" mark="" >}}无服务器 JS/TS 托管，部署快，免费额度够个人小项目。{{< /pick >}}

{{< pick name="blitz.cloud" url="https://blitz.cloud" mark="own" >}}德国的欧盟 PaaS，免费 5 个应用加一个托管数据库，闲置 15 分钟休眠；条款禁止跑代理。{{< /pick >}}

{{< pick name="Cloady" url="https://cloady.com" mark="own" >}}NeptoLab 的应用托管平台，GitHub、Docker 镜像或模板一键部署，自带 MCP。德国、美东、美西三区永久免费 0.5 核、1 GB 内存、5 GB 盘，每月 10 GB 流量和 4 个 CPU 小时，闲置 7 天暂停；其他区只有一个月试用。{{< /pick >}}

{{< pick name="Hugging Face Spaces" url="https://huggingface.co/spaces" mark="" >}}一键部署 Gradio、Streamlit 或 Docker 演示，免费 CPU 实例，AI 圈展示作品的标配。{{< /pick >}}


## 数据库与存储

{{< pick name="Supabase" url="https://supabase.com" mark="" >}}开源的 Firebase 替代品，Postgres 加认证和文件存储，免费 2 个项目，闲置一周会暂停。{{< /pick >}}

{{< pick name="Neon" url="https://neon.com" mark="" >}}无服务器 Postgres，支持像 Git 一样开分支，空闲时自动缩到零。{{< /pick >}}

{{< pick name="Turso" url="https://turso.tech" mark="" >}}基于 libSQL（SQLite 分支）的边缘数据库，免费层很慷慨。{{< /pick >}}

{{< pick name="MongoDB Atlas" url="https://www.mongodb.com/products/platform/atlas-database" mark="" >}}永久免费的 M0 共享集群，512 MB 存储，文档数据库入门够用。{{< /pick >}}

{{< pick name="Cloudflare R2" url="https://www.cloudflare.com/developer-platform/products/r2/" mark="" >}}S3 兼容对象存储，每月 10 GB 免费，而且不收出口流量费。{{< /pick >}}

{{< pick name="IronShard" url="https://ironshard.ai" mark="own" >}}丹麦的 S3 兼容存储，免费 10 GiB，自带 MCP 接口，适合给几个智能体当共享网盘。{{< /pick >}}


## AI 模型与智能体平台

{{< pick name="OpenRouter" url="https://openrouter.ai" mark="" >}}一个 API 接几百个模型，常年有一批带 :free 后缀的免费模型（有限速）。{{< /pick >}}

{{< pick name="Groq" url="https://groq.com" mark="" >}}自研 LPU 推理速度极快，开放模型有免费额度（限速）。{{< /pick >}}

{{< pick name="Google AI Studio" url="https://aistudio.google.com" mark="" >}}Gemini API 有免费层，但部分国家和地区用不了。{{< /pick >}}

{{< pick name="Cloudflare Workers AI" url="https://developers.cloudflare.com/workers-ai/" mark="" >}}在边缘跑开源模型，每天有免费额度，和 Workers 配合很顺。{{< /pick >}}

{{< pick name="Pollinations.ai" url="https://pollinations.ai" mark="own" >}}开源的文本和图片生成 API，兼容 OpenAI 接口，做任务能领免费额度。{{< /pick >}}

{{< pick name="AgentScope" url="https://platform.agentscope.io" mark="own" >}}阿里通义开源的多智能体框架，平台上能在线部署和托管智能体。{{< /pick >}}


## 网络与邮箱

{{< pick name="Tailscale" url="https://tailscale.com" mark="" >}}基于 WireGuard 的组网工具，个人版免费，几分钟把散在各处的机器连成内网；也能自建 Headscale 控制端。{{< /pick >}}

{{< pick name="Cloudflare Tunnel" url="https://www.cloudflare.com/products/tunnel/" mark="" >}}不开公网端口，也能把家里或内网的服务安全地发布出去，免费。{{< /pick >}}

{{< pick name="Amelu" url="https://amelu.org" mark="own" >}}支持自定义域名的免费邮箱，IMAP 和 SMTP 都能用，手机邮件客户端直接收发。{{< /pick >}}

{{< pick name="Cooper Email" url="https://cooperemail.com" mark="own" >}}给 AI 智能体用的邮箱 API，免费 5 个收件箱、每月 5000 封。{{< /pick >}}

---

**说明**：免费额度和规则随时可能调整，以各家官网为准（整理于 2026 年 11 月 20 日）。很多平台的条款禁止用免费机跑代理或挖矿，违规容易被封号。

**图片**：AI 生成插图。
