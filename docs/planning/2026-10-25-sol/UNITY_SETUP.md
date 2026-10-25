# Unity 与 MCP 环境准备

2026-10-25 · 本地空工程与MCP已接通 · 游戏制作尚未开始

用户已明确授权建立本地工程、安装MCP并准备Git忽略规则。本次范围已完成；没有迁移Python规则、制作剧情/美术或执行U1/U2。Editor保持打开，下一轮可以从现有工程接续，不再创建同名工程。

## 本机位置与版本

| 项目 | 路径或配置 | 状态 |
| --- | --- | --- |
| Unity Hub | `E:\Unity Hub\Unity Hub.exe` | 原安装保留，未升级 |
| Editor | `E:\Unity Hub\6000.3.10f1\Editor\Unity.exe` | 6000.3.10f1，已实际打开BTL，许可证成功解析 |
| Hub下载目录 | `E:\Unity download` | 原设置保留 |
| BTL工程 | `F:\BTL-AI\unity\BTL` | 已创建，使用上级BTL-AI Git仓库，无嵌套.git |
| 模板 | Universal 2D 6.1.2 | 本地模板创建；URP实际解析为17.3.0 |
| MCP服务 | `E:\AI\Tools\unity-mcp` | mcpforunityserver 10.0.0，独立uv工具环境 |
| uv缓存 | `E:\AI\Cache\uv` | 不修改游戏Python环境 |
| Codex配置 | `E:\AI\Codex\config.toml` 的unityMCP | 复用原URL `http://127.0.0.1:8080/mcp`，未改其他条目 |
| Editor桥接包 | com.coplaydev.unity-mcp 10.0.0 | Git标签v10.0.0；锁文件提交hash `d49ae2953580f3481beb1e084a1da2682f0b5610` |

Editor已在E盘，不需要搬动或重装。检查时E盘约398GB、F盘约444GB可用；为当时读数。`E:\Unity editor`未发现版本，真实路径是上表。WindowsStandaloneSupport目录存在且当前平台为StandaloneWindows64；尚未实际构建可执行包，不等于构建验收通过。

## 创建与安装方式

Computer Use读取Unity Hub窗口时应用访问授权超时，没有进行任何界面输入；随后使用Unity官方命令行的`-createProject`与`-cloneFromTemplate`，从已安装的Universal 2D模板建立本地工程。创建批处理正常退出，日志明确返回0。[Unity命令行文档](https://docs.unity.com/en-us/engine/6000.0/manual/unity-editor/command-line-arguments/editor)

包清单加入固定地址`https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.0.0`，由Unity Package Manager完成安装并生成packages-lock.json。维护者说明该包是第三方开源Editor桥接，支持Unity 6.x；未启用其商业助手。[固定版本来源](https://github.com/CoplayDev/unity-mcp/tree/v10.0.0)

新增的唯一C#文件是`Assets/Editor/BtlMcpConnection.cs`，仅提供 **BTL → Connect Local MCP** 菜单和命令行连接入口。它调用包的公开服务，将HTTP范围设为local、地址设为127.0.0.1:8080并连接，不创建对象、不改变场景或游戏状态，不运行模型。首次打开工程时通过`-executeMethod BtlMcpConnection.Connect`执行成功。未添加自动执行的游戏脚本或全局开机启动。

工程保留模板SampleScene和URP2DSceneTemplate；没有另建Main、角色、剧情、美术或规则。模板自带包保持原状，不把自带版本控制包的存在写成云服务已启用；当前工程project_id为null。

## 后续启动与连接

1. 若Hub尚未列出BTL，使用“从磁盘添加项目”选择`F:\BTL-AI\unity\BTL`；不要再次点新建同名工程。本轮用Editor命令行创建，未声称已核验Hub项目列表。
2. 本地服务未运行时，在PowerShell执行下方启动脚本。8080已运行则复用，不启动第二份或杀死其他进程。
3. 用6000.3.10f1打开工程，选择 **BTL → Connect Local MCP**。连接选项保存在本机EditorPrefs，只配置当前本地传输，不重写Codex/其他客户端配置。
4. Codex读取实例资源，确认名称和工程路径后选择该实例。当前已连接的ID为`BTL@9e2f981c2b142ed8`；搬路径/新会话时重新发现，不盲用旧值。

```powershell
& 'E:\AI\Tools\unity-mcp\Start-UnityMCP.ps1'
```

服务端隐藏运行，仅监听127.0.0.1，服务端遥测关闭，日志在`E:\AI\Tools\unity-mcp\logs`。Unity包自身偏好未通过界面改动隐私设置。当前Codex会话已经出现Unity工具，并完成实际只读调用，不再仅是独立SDK握手成功。[Codex HTTP MCP配置说明](https://developers.openai.com/codex/mcp)

## Git准备与保留文件

根`.gitignore`原已有Unity缓存规则，本轮追加BTL范围的自动生成IDE文件与本地MCP状态目录规则。没有提交、推送、初始化新仓库或改写远端。

- 追踪：`Assets/`和全部`.meta`、`Packages/manifest.json`与`packages-lock.json`、`ProjectSettings/`、编辑器连接工具和[工程说明](../../../unity/README.md)。
- 忽略：Library、Temp、Obj、Logs、UserSettings、Build/Builds、自动生成.csproj/.sln等。
- 模板已设Visible Meta Files与Force Text，未另改序列化政策。
- 实际以NUL分隔输入运行git check-ignore：49个工程源文件未忽略；8项缓存/IDE路径均被忽略；BTL内无.git。初次临时检查脚本遇Windows CRLF路径尾字符问题，改用NUL后检查通过，不涉及修改Git规则来掩盖问题。
- 不把密钥、许可证、本机服务环境或日志加进仓库。工程.meta不是缓存，必须保留。

本轮只调用新的check-ignore核验，不重试此前被拒绝的分支/HEAD/status查询；记录分支沿用06/07，不声称重新核验HEAD。

## 实际验证与边界

- Unity创建日志正常退出0；MCP包及Editor工具编译成功。
- 使用当前会话的原生MCP工具选择BTL实例；project/info确认`F:/BTL-AI/unity/BTL`、6000.3.10f1、StandaloneWindows64。
- editor/state显示idle、is_compiling=false、is_updating=false、ready_for_tools=true，未运行Play Mode；活动场景为模板SampleScene。
- read_console读取error/warning，返回0项。没有为了清空结果而清理控制台。
- MCP服务端版本10.0.0；握手中的3.4.11是FastMCP框架版本。包锁同时记录Unity解析的Newtonsoft Json 3.2.2。
- 没有运行Python pytest、旧模型基线、Unity测试套件、游戏Play Mode或Windows构建；这些不属于空工程连接验收。模型请求历史仍12，未新增调用。

本轮交接源码：根.gitignore、unity/README.md、BTL的Assets/Packages/ProjectSettings，以及更新的README、06/07、主规划、规划索引、制作计划和本页。缓存无需同步；本机服务安装不在Git内，其他机器按环境记录单独安装。未commit/push/pull或刷新Project Sources。

下一步是另行开始U1规则迁移/U2首条可玩路径；U0环境子项已完成，但中文阅读/IME和目标界面仍未制作，不能把它们记成已验收。
