# CleanYourTV Skill

[English](README.md) | **简体中文**

**更方便、更安全地定制电视：清理 Android TV、定制 LG webOS、为三星 Tizen 安装实用应用。**

用 AI 助手清理 Android TV、定制 LG webOS，或为三星 Tizen 安装 Jellyfin 和 Moonlight，使用自己的媒体库、串流电脑游戏。CleanYourTV Skill 将 [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) 的 Android 流程与 LG、三星应用流程结合：先识别系统、审查源码和计划，再执行你批准的变更。

## 为什么使用这个 Skill？

- **使用更方便。** 安装一份可复用技能，直接描述目标。助手按需使用审查、清理、桌面或恢复流程，并读取相关参考资料；你也可以使用现成的提问示例。
- **执行更安全。** 明确核对设备身份，先确认计划；Android 按单个应用逐项操作，LG 核对配对权限与连接限制；保护关键功能，记录恢复步骤。结果不明确时停止后续变更，不盲目重试。
- **适配不同助手。** 通用 Markdown 和仅依赖 Python 标准库的工具，让流程不绑定模型厂商。助手根据现有工具与权限工作；没有设备访问能力时，也可以只做计划。

这些约束旨在减少改错电视、误伤关键功能，以及未核对目标就复制命令或应用清单造成的错误。Android 流程保留原有桌面和设置向导；LG 流程保留系统 Home 与系统服务，使用独立的身份、配对和恢复流程。

## 可以做什么

- **清理 Android 应用。** 审查预装应用和推广服务，了解它们的作用，逐项停用你批准的应用包。
- **定制 Android 桌面。** 构建和配置上游轻量、Apple TV 风格的桌面，设置常用应用 Dock、应用网格和主题。能否切换默认 Home 取决于固件，原有桌面会保持启用。
- **使用新版桌面功能。** 逐张审查模块卡片，调整布局与动效，按需配置遥控按键辅助。Private DNS 和已有私有远程连接遵循[独立流程](references/network-extras.md)。
- **免 Root 控制 LG webOS。** 使用已有的 [Home Assistant LG 集成](https://www.home-assistant.io/integrations/webostv/) 或 [aiowebostv](https://github.com/home-assistant-libs/aiowebostv) 调整音量、导航、播放、启动已安装应用及切换 HDMI；通过官方开发模式和 [webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop) 或 LG CLI 测试自己的 webOS 应用。详见 [LG 流程](references/webos.md)。
- **为三星安装实用应用。** 构建、审阅并安装 [Jellyfin](https://github.com/jellyfin/jellyfin-tizen) 使用自己的媒体库，或安装 [Moonlight](https://github.com/OneLiberty/moonlight-chrome-tizen) 串流电脑游戏，包含最终 WGT 检查、私密电视签名与单应用恢复流程，不止遥控连接。[TizenBrew](https://github.com/reisxd/TizenBrew) 为独立可选模块路线，详见[三星流程](references/tizen.md)。
- **明确启用 LG Root。** [SlopBro 模块](references/slopbro-research.md)现支持针对授权 LG 电视、经审查和具体批准后的 Root 尝试，包含 Homebrew / 持久化影响、隔离网络和恢复限制。仅研究请求仍不执行。SlopBro 不适用于三星；[三星 Root](references/tizen-root-research.md)保留为实验性源码研究。
- **记录每一步变更。** 批准前先看预期影响与恢复方法，变更后确认电视的必要功能仍正常。

可以这样开始：

```text
请使用 cleanyourtv-skill，帮我清理 Android TV，
并设置更简洁的桌面。保留常用流媒体 App、投屏和语音功能。
修改前先给我看计划。
```

三星应用可以这样开始：

```text
请使用 cleanyourtv-skill，为我的三星 Tizen 电视准备 Jellyfin
接入自己的媒体库，或准备 Moonlight 串流自己的电脑游戏。
核对准确固件、源码、签名后的 WGT 和恢复限制。
先在本地构建与审阅，修改电视前给我看具体安装计划。
```

LG 可以这样开始：

```text
请使用 cleanyourtv-skill 协助我的 LG webOS 电视。
审阅我已有的 Home Assistant LG 实体及可用 App、HDMI 输入。
我会确认准确的电视。先给计划，不重新配对、不安装、不改设置或发送控制。
```

Android 设备访问使用 ADB 和电视调试授权；LG 使用对应的配对控制器或开发工具，不使用 ADB，也不安装 Android 桌面。聊天助手可根据必要的私密证据审阅两类计划。日常控制与官方开发应用测试无需 Root。

## 包含哪些内容

- 通用的 [SKILL.md](SKILL.md)，按任务逐步读取相关参考文件。
- 原创离线 WGT 检查器：报告应用身份、哈希、权限、服务和签名文件名，不解压、不执行；它不验证签名，也不批准安装。
- 离线 Python 计划检查器：拒绝格式错误、涉及受保护包名、缺少原始状态、设备不匹配或证据过期的计划。它只输出命令参数，不执行命令。
- 与已审查上游提交绑定的桌面、连接、恢复和隐私处理流程。
- 标准库测试、跨平台 CI、助手行为评估场景，以及许可、贡献和安全报告说明。

## 快速开始

1. 从 [v0.5.0 预发布版](https://github.com/songbihai/cleanyourtv-skill/releases/tag/v0.5.0) 下载源码或经过检查的技能 ZIP。使用自定义 ZIP 时，先核对相邻的 SHA-256 文件再解压。不要执行未经审阅分支中的设备命令。
2. 在助手中打开 [SKILL.md](SKILL.md)，或按客户端的安装方式安装整个技能目录。保留同级的 `references/` 和 `scripts/`。
3. 提问：`请使用 cleanyourtv-skill 审查我的 Android TV。先做计划，不修改设备。我会提供准确的 ADB 连接端点。`
4. Android 应用清理按[计划格式说明](references/plan-format.md)使用快照和离线检查器；LG 使用 [webOS 流程](references/webos.md)；三星使用 [Tizen 流程](references/tizen.md)与离线 WGT 检查器；明确启用的 LG Root 使用 [SlopBro 独立流程](references/slopbro-research.md)。执行前确认准确影响；Android 检查器不验证 LG / Tizen / Root 操作，WGT 检查器仅辅助审阅，不执行安装。

首次使用或需要完整的中文对话示例，请阅读[中文使用教程](docs/guide.zh-CN.md)。

没有电视也可以先运行合成示例。在技能根目录执行：

```text
python3 scripts/plan_guard.py --snapshot examples/snapshot.synthetic.json --plan examples/plan.synthetic.json --demo
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

`--demo` 只接受标记为合成数据的示例，并将输出标记为不可执行；它不会允许过期的真实快照通过检查。不要用示例证据操作真实设备。工具需要 Python 3.10 或更新版本，没有第三方运行依赖。Windows 环境若用 `python` 启动 Python 3，可将上述 `python3` 替换为 `python`。

## 模型与客户端兼容性

技能使用普通 Markdown 和 [Agent Skills 格式](https://agentskills.io/specification)。助手需要能够读取技能及其参考文件；流程会根据客户端的工具、权限和上下文能力调整。

| 客户端能力 | 使用方式 |
| --- | --- |
| 原生支持 Agent Skills | 安装整个目录，按客户端语法调用 `cleanyourtv-skill`。 |
| Codex | 将目录放入 `~/.agents/skills/cleanyourtv-skill/`，调用 `$cleanyourtv-skill`。可选的 `agents/openai.yaml` 提供界面文案。 |
| Claude Code | 按[兼容性指南](docs/compatibility.md)中的个人或项目技能位置安装和调用。 |
| Gemini CLI | 使用其文档规定的技能发现和授权流程，详见[兼容性指南](docs/compatibility.md)。 |
| 能读取文件、但没有终端的聊天助手 | 读取技能和相关参考文件，准备计划，并请用户提供命令输出。 |
| 无法读取文件或引用 | 将技能及所需引用正文提供给助手；必要内容缺失或上下文不足时停止。 |
| 无法可靠地选择目标、限制执行时间或取得明确批准 | 仅审查与计划，不修改设备。 |

[兼容性指南](docs/compatibility.md)包含客户端官方文档、可复制请求、命令参数处理和能力不足时的替代流程。

技能本身不要求 API、厂商 SDK、MCP 服务、特定模型的系统提示词或付费服务。Android 执行使用 Platform Tools；桌面构建还需要上游 JDK、Android SDK、Gradle。LG 可复用已有 Home Assistant 集成或 Dev Manager 图形界面；单独使用 aiowebostv 客户端需要 Python 3.11+ 及其依赖。三星 WGT 构建、安装需要 Tizen Studio、TV / 证书工具及对应应用的构建环境。可选工具安装、配对、签名和下载有各自的授权与信任要求。

## 支持范围

| 平台 / 模式 | 支持的操作 |
| --- | --- |
| Android TV / Google TV | 审查、经批准的逐用户应用停用，以及保留系统 Home 的上游桌面构建、安装和配置。 |
| LG webOS，免 Root | 指定目标的日常遥控、状态与 App / 输入源审阅，以及通过官方开发模式测试自己的应用。不提供系统精简或 Android 桌面替换。 |
| Samsung Tizen 应用 | Jellyfin 媒体库、Moonlight 电脑游戏串流、个人 WGT 构建 / 审阅 / 签名 / 安装 / 测试及恢复；TizenBrew 模块单独审查。 |
| 明确启用的 LG SlopBro Root | 源码与固件评估，以及独立批准、有超时限制的 Root 尝试，先审查依赖、启动与访问影响和恢复限制；只要求研究时不执行。 |
| 明确启用的三星 Root 研究 | 核对上游准确型号与固件并整理定制计划；不包含实验性漏洞执行。 |

Samsung Orsay、LG NetCast、Fire OS、受管理设备、Android 其他用户会话修改、刷机、移除系统应用及停用系统桌面或设置向导仍不在范围内。LG 客户端存在[连接信任和开发会话限制](references/webos.md)，需要可信私有网络并确认实体电视。

每次变更前都要核对真实设备输出和目标电视。离线检查器核对计划结构、受保护包名、设备身份字段和恢复数据；固件依赖仍需要针对具体设备审查。详见 [SECURITY.md](SECURITY.md)。

## 维护者的应用：TVRemoteX

<img src="assets/tvremotex/logo.png" alt="TVRemoteX 应用图标" width="72" height="72">

TVRemoteX 为 iPhone 和 iPad 提供日常电视遥控功能：使用触控板导航、用手机键盘输入、调整音量，并在兼容电视上启动 App。

[在 App Store 查看 TVRemoteX](https://apps.apple.com/us/app/tvremotex-universal-tv-remote/id6755671893)

<p>
  <img src="assets/tvremotex/01-brands-en-US.png" alt="TVRemoteX 英文截图 1：电视品牌" width="31%">
  <img src="assets/tvremotex/02-power-and-apps-en-US.png" alt="TVRemoteX 英文截图 2：电源、频道和应用控制" width="31%">
  <img src="assets/tvremotex/03-keyboard-and-touchpad-en-US.png" alt="TVRemoteX 英文截图 3：键盘、音量和触控板" width="31%">
</p>

由本技能的维护者开发。TVRemoteX 为可选应用，与技能独立运行。功能因电视型号和平台而异，部分功能需要 App 内购买。

## 项目状态与发布

**版本 0.5.0。** 已同步到审查过的 [cleanyourtv 源码提交](https://github.com/Gathin23/cleanyourtv/tree/7c61d3c57e561323b85d7096ee2b686685b9b499)，该提交的桌面版本为 2.3。离线工具和打包工具包含 **126 项测试**。已完成的检查见 [VALIDATION.md](VALIDATION.md)，跨平台 CI 结果见 [Actions](https://github.com/songbihai/cleanyourtv-skill/actions)。

技能基于上游的电视定制流程。可以查阅上游[设备示例](https://github.com/Gathin23/cleanyourtv/tree/main/examples)，再核对自己的型号、系统和固件；设备操作仍应遵守上述范围，并在执行前逐项审阅计划。

[上游审查记录](references/upstream-review.md)说明 Android 来源；[LG 来源审查](references/lg-source-review.md)记录工具版本及发现；[三星来源审查](references/tizen-source-review.md)说明应用和安装工具的选择；[行为评估场景](docs/evaluation.md)用于评估助手表现；[发布指南](docs/release.md)说明发布流程；最新 CI 状态见 [Actions](https://github.com/songbihai/cleanyourtv-skill/actions)。

需要构建只包含声明文件与已审查图片的归档时，执行 `python3 scripts/build_release.py --output /path/outside/repository/cleanyourtv-skill-0.5.0.zip`。工具拒绝覆盖已有输出，并生成相邻的 `.sha256` 文件。[审查报告](docs/audit.md)记录了审查范围与限制。

指令与工具采用 MIT 许可；推广图片遵循[独立条款](assets/tvremotex/NOTICE.md)。[NOTICE](NOTICE) 和 [LICENSE](LICENSE) 保留上游署名。这是独立项目，并非上游、三星、LG、Home Assistant 或 Android 官方项目。可选第三方工具遵循各自许可，技能不捆绑客户端、IPK 或漏洞代码。
