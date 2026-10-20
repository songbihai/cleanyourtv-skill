# CleanYourTV Skill

[English](README.md) | **简体中文**

**让 AI 助手帮你更方便、更安全地清理和定制 Android TV。**

用 AI 助手审查不需要的预装应用，并为常用 App 配置更简洁的电视桌面。CleanYourTV Skill 将 [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) 整理为适用于 Android TV 和 Google TV 的可复用流程：核对电视、审阅清理计划，只执行你批准的变更。

## 为什么使用这个 Skill？

- **使用更方便。** 安装一份可复用技能，直接描述目标。助手按需使用审查、清理、桌面或恢复流程，并读取相关参考资料；你也可以使用现成的提问示例。
- **执行更安全。** 明确核对设备身份，先确认计划，再按单个应用逐项操作；保护关键功能，记录恢复步骤。结果不明确时停止后续变更，不盲目重试。
- **适配不同助手。** 通用 Markdown 和仅依赖 Python 标准库的工具，让流程不绑定模型厂商。助手根据现有工具与权限工作；没有设备访问能力时，也可以只做计划。

这些约束旨在减少改错电视、误伤关键功能，以及未核对目标就复制命令或应用清单造成的错误。整个流程保留原有桌面和设置向导。

## 可以做什么

- **清理不需要的应用。** 审查预装应用和推广服务，了解它们的作用，逐项停用你批准的应用包。
- **定制电视桌面。** 构建和配置上游轻量、Apple TV 风格的桌面，设置常用应用 Dock、应用网格和主题。能否切换默认 Home 取决于固件，原有桌面会保持启用。
- **使用新版桌面功能。** 逐张审查模块卡片，调整布局与动效，按需配置遥控按键辅助。Private DNS 和已有私有远程连接遵循[独立流程](references/network-extras.md)。
- **记录每一步变更。** 批准前先看预期影响与恢复方法，变更后确认电视的必要功能仍正常。

可以这样开始：

```text
请使用 cleanyourtv-skill，帮我清理 Android TV，
并设置更简洁的桌面。保留常用流媒体 App、投屏和语音功能。
修改前先给我看计划。
```

实际连接设备，需要助手具备终端访问能力、Android SDK Platform Tools（ADB），以及电视端的调试授权。也可以在聊天助手中提供必要的命令输出，仅审阅计划。无需 Root。

## 包含哪些内容

- 通用的 [SKILL.md](SKILL.md)，按任务逐步读取相关参考文件。
- 离线 Python 计划检查器：拒绝格式错误、涉及受保护包名、缺少原始状态、设备不匹配或证据过期的计划。它只输出命令参数，不执行命令。
- 与已审查上游提交绑定的桌面、连接、恢复和隐私处理流程。
- 标准库测试、跨平台 CI、助手行为评估场景，以及许可、贡献和安全报告说明。

## 快速开始

1. 从 [v0.3.0 预发布版](https://github.com/songbihai/cleanyourtv-skill/releases/tag/v0.3.0) 下载源码或经过检查的技能 ZIP。使用自定义 ZIP 时，先核对相邻的 SHA-256 文件再解压。不要执行未经审阅分支中的设备命令。
2. 在助手中打开 [SKILL.md](SKILL.md)，或按客户端的安装方式安装整个技能目录。保留同级的 `references/` 和 `scripts/`。
3. 提问：`请使用 cleanyourtv-skill 审查我的 Android TV。先做计划，不修改设备。我会提供准确的 ADB 连接端点。`
4. 实际操作前，按[计划格式说明](references/plan-format.md)准备快照与计划，审阅检查器输出，再批准准确的变更范围。

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

技能本身不要求 API、厂商 SDK、MCP 服务、特定模型的系统提示词或付费服务。实际执行需要 Android SDK Platform Tools 和电视授权。构建上游桌面还需要对应的 JDK、Android SDK、Gradle 工具链及依赖下载。

## 支持范围

在 Android TV / Google TV 上进行审查和经过仔细审阅的逐用户应用停用；构建、安装和配置上游桌面，并保留系统原有 Home。Samsung Tizen、LG webOS、Fire OS、受管理设备、其他用户会话的修改、Root、刷机，以及停用系统桌面或设置向导，均不在当前范围内。这些边界也适用于上游提供了更广泛操作流程的情况。

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

**版本 0.3.0。** 已同步到审查过的 [cleanyourtv 源码提交](https://github.com/Gathin23/cleanyourtv/tree/7c61d3c57e561323b85d7096ee2b686685b9b499)，该提交的桌面版本为 2.3。离线工具和打包工具包含 **98 项测试**。已完成的检查见 [VALIDATION.md](VALIDATION.md)，跨平台 CI 结果见 [Actions](https://github.com/songbihai/cleanyourtv-skill/actions)。

技能基于上游的电视定制流程。可以查阅上游[设备示例](https://github.com/Gathin23/cleanyourtv/tree/main/examples)，再核对自己的型号、系统和固件；设备操作仍应遵守上述范围，并在执行前逐项审阅计划。

[上游审查记录](references/upstream-review.md)说明固定提交与来源；[行为评估场景](docs/evaluation.md)用于评估助手表现；[发布指南](docs/release.md)说明发布流程；最新 CI 状态见 [Actions](https://github.com/songbihai/cleanyourtv-skill/actions)。

需要构建只包含声明文件与已审查图片的归档时，执行 `python3 scripts/build_release.py --output /path/outside/repository/cleanyourtv-skill-0.3.0.zip`。工具拒绝覆盖已有输出，并生成相邻的 `.sha256` 文件。[审查报告](docs/audit.md)记录了审查范围与限制。

指令与工具采用 MIT 许可；推广图片遵循[独立条款](assets/tvremotex/NOTICE.md)。[NOTICE](NOTICE) 和 [LICENSE](LICENSE) 保留上游署名。这是独立项目，并非上游或 Android 官方项目。
