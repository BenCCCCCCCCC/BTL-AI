# BTL Unity 工程

既有工程`BTL/`，Unity **6000.3.10f1 LTS / Universal 2D**。当前本地交付为U5a首案体验定型版 **0.4.0**；C#拥有规则和状态，采访使用离线脚本候选。当前章保留三段调查、五材料、十二作者选稿、六类结果和本局回看；没有模型请求或存档。

## Windows试玩

运行`F:\BTL-AI\Builds\BTL-Internal-0.4.0-Windows\BTL.exe`，分发同名zip，解压后保留整个目录。0.3.0包原位保留。包附字体许可证、中文开始说明和BUILD-INFO源散列，不需要Unity、Python、账号或密钥。

选完整表达卡只准备原句，再核对全部采访意图、确认执行。编辑入口按需展开；脚本外文字保留，但不猜测执行。返回改写保留原句；输入框Enter换行、Tab离开，按钮可用Enter/Space。材料册独立翻阅，正文可复制；顶栏可调三档字号。最后一段显示当局开放的机会成本；标题完整复核后再明确签发或暂缓。刊发后先读人物余波，一次进入归档；工作单、原句路径和事件账可展开。

本轮定向C#检查通过，原生Windows走初访→A→B报价/接受500→S-A→H11→签发→人物余波→归档/回看。末次只修实际发现的重复正文/动作、名片、字号对比度和签发重复含义，增量构建后定向检查，未重复整案。原始截图与限制见[U5a证据](../docs/planning/2026-10-25-sol/verification/u5a/README.md)。真人理解/时长/乐趣待观察，使用[读者表](../docs/planning/2026-10-25-sol/FIRST_READER_NOTES.md)。

## 内容维护与重建

打开`Assets/BTL/Main.unity`按Play开发。当前可编辑作者源为仓库`ai/content/railyard_chapter.v1.1.json`及`railyard_presentation.v1.2.json`，作者正文在稿件第18节。旧源和fixture保留；不要手改Generated副本或在UI中另造证据事实。

停止Play、等待编译结束，再运行 **BTL → Prepare Internal Chapter**：显式导入两个新源，装配Main引用及已有三场景/三头像/字体、PanelSettings和0.4.0构建参数。它保留场景其他对象，但会更新本案指定引用与设置。源/Generated散列应一致。`ChapterPresentation`只读当前会话和实际回应；UI提交既有会话命令，合并阅读不增加结算。

**BTL → Build Windows Internal**生成`Builds/BTL-Internal-0.4.0-Windows/`；成功以控制台`BTL WINDOWS BUILD SUCCEEDED`为据。长等待超时先读最终报告，不重复启动构建。分发zip排除DoNotShip目录，保留全部运行文件和许可证，Builds仍被Git忽略。

**BTL → Check U5 Experience Changes**针对本轮新内容/余波/机会成本/阅读转换；仅在这些行为修改时复核。旧 **Check Chapter Presentation**、**Run U1 Focused Checks**保留历史用途，不因打包而重跑；Python历史套件与模型结果继续复用。

包内原创像素场景与头像来自`tools/generate_unity_art.py`，中文字体及许可来自`Assets/BTL/Fonts/`。现版静音，无实时动画。GitHub公开及本地同步状态见[交接](../docs/07_HANDOFF.md)，公开不表示新内容已经推送。

## 打开和连接

在Unity Hub中用“从磁盘添加项目”选择`F:\BTL-AI\unity\BTL`，然后用6000.3.10f1打开。若Hub尚未列出它，不要再新建同名工程。

本机MCP服务在`http://127.0.0.1:8080/mcp`。服务未运行时，先在PowerShell运行：

```powershell
& 'E:\AI\Tools\unity-mcp\Start-UnityMCP.ps1'
```

Editor中选择 **BTL → Connect Local MCP**。此命令只调用已安装桥接包连接本机服务；不修改场景、不启动模型、不配置其他AI客户端。包固定为`com.coplaydev.unity-mcp` v10.0.0，服务固定为`mcpforunityserver` 10.0.0。`Assets/Editor/BtlMcpConnection.cs`仅为编辑器工具，不进入游戏运行时。

## Git文件范围

使用上级BTL-AI仓库和根目录`.gitignore`，不在BTL下执行`git init`。

- 保留`Assets/`及所有`.meta`、`Packages/manifest.json`和`packages-lock.json`、`ProjectSettings/`。
- 忽略`Library/`、`Temp/`、`Obj/`、`Logs/`、`UserSettings/`、Build/Builds及自动生成的IDE项目文件。
- Unity采用Visible Meta Files与Force Text；不要删除或重新生成已有资产的`.meta`来修复冲突。
- 本机MCP服务环境、日志、许可证、账号凭据不复制到仓库。机器上的安装文件不属于工程源码。

环境历史见[环境准备](../docs/planning/2026-10-25-sol/UNITY_SETUP.md)；当前成果和下一步见[交接](../docs/07_HANDOFF.md)。
