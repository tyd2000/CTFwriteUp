# Windows事件查看器

在Windows环境下，如果你想找出某个登录会话的IP地址，尤其是在使用CTF（Capture The Flag）挑战时，通常涉及到分析Windows事件日志。Windows的事件日志记录了系统的各种活动，包括登录尝试。

查看事件日志最简单的方法是使用Windows内置的事件查看器：

1. 按 `Win+R` 打开运行对话框
2. 输入 `eventvwr.msc` 并按回车

### Windows日志主要类型

1. 应用程序日志 (Application)
内容：记录应用程序或系统程序运行相关的事件
用途：查找程序崩溃原因、应用程序错误信息
默认位置：%SystemRoot%\System32\Winevt\Logs\Application.evtx
2. 系统日志 (System)
内容：记录操作系统组件产生的事件
用途：监控驱动程序、系统组件和软件的异常情况
默认位置：%SystemRoot%\System32\Winevt\Logs\System.evtx
3. 安全日志 (Security)
内容：记录系统安全相关的事件，如用户登录/注销、资源访问
用途：安全审计、入侵检测、行为分析
默认位置：%SystemRoot%\System32\Winevt\Logs\Security.evtx
4. 转发事件 (Forwarded Events)
内容：存储从远程计算机收集的事件
用途：集中管理多台机器的日志
默认位置：%SystemRoot%\System32\Winevt\Logs\ForwardedEvents.evtx

------

### 事件级别分类

Windows事件日志有5个事件级别，帮助区分不同严重程度的事件：

|   级别   |           说明           |          应用场景          |
| :------: | :----------------------: | :------------------------: |
|   信息   |    表示操作成功的事件    |   服务启动成功、任务完成   |
|   警告   |  可能导致未来问题的事件  |   磁盘空间不足、性能下降   |
|   错误   | 功能或数据丢失的重要问题 | 服务启动失败、系统功能异常 |
| 成功审核 |    成功的安全访问尝试    |   用户成功登录、权限使用   |
| 失败审核 |    失败的安全访问尝试    |     登录失败、访问拒绝     |

------

### 重要安全事件ID

Windows通过事件ID标识具体的操作行为。以下是一些关键的安全事件ID：

| 事件ID |       说明       |          安全意义          |
| :----: | :--------------: | :------------------------: |
|  1102  |   清理审计日志   | 可能表示攻击者正在清除痕迹 |
|  4624  |   账号成功登录   |    用于监控正常登录活动    |
|  4625  |   账号登录失败   |    可能表示密码爆破尝试    |
|  4720  |     创建用户     |    监控未授权的用户创建    |
|  4726  |     删除用户     |      检测账户删除操作      |
|  4732  |  添加安全组成员  |        监控权限提升        |
|  4733  | 从安全组移除成员 |        检测权限变更        |

------

### 实战案例：检测RDP爆破攻击

以下是一个使用Windows日志检测RDP爆破攻击的实际案例：

1. 在目标机器上打开事件查看器：`eventvwr.msc`
2. 导航至：Windows日志 → 安全
3. 在右侧操作面板中，点击"筛选当前日志"
4. 输入事件ID：4625（登录失败事件）

如果发现大量连续的4625事件，特别是针对同一用户账户，这通常表明服务器可能正在遭受RDP暴力破解攻击。

**分析要点**：

- 关注登录失败的时间模式（是否高频且规律）
- 查看来源IP地址（是否来自异常地理位置）
- 检查目标账户（是否针对管理员账户）
- 注意登录类型（类型10表示RDP登录）

------

### 实战案例：找出登录成功的IP地址

以下是一些步骤和工具，可以帮助你找出登录的IP地址：

#### 方法1：使用Windows事件查看器

1. ‌**打开事件查看器**‌：
   - 在Windows搜索栏中输入`eventvwr.msc`并打开它。
2. ‌**导航到安全日志**‌：
   - 在事件查看器中，展开“Windows 日志”，然后选择“安全”。
3. ‌**筛选事件**‌：
   - 在“安全”日志中，你可以通过点击右侧的“筛选当前日志...”来筛选特定的事件。例如，你可以筛选事件ID为4624的事件（这是一个登录成功的事件）。远程登录的事件号是4648。
4. ‌**查看事件详细信息**‌：
   - 找到对应的事件后，双击打开它。在“详细信息”标签页中，你会看到很多关于登录尝试的详细信息，包括登录帐户、登录类型和登录过程等信息。
   - 查找“IP 地址”字段，这将显示登录尝试的IP地址。

#### 方法2：使用PowerShell

如果你更喜欢使用命令行，可以使用PowerShell来查询安全日志。

1. ‌**打开PowerShell**‌：
   - 在Windows搜索栏中输入`PowerShell`并选择“以管理员身份运行”。
2. ‌**查询特定事件**‌：

```
Get-WinEvent -FilterHashtable @{Logname='Security'; ID=4624} | ForEach-Object {
    $Event = $_
    $IP = $Event.Properties[5].Value
    $AccountName = $Event.Properties[1].Value
    Write-Output "IP Address: $IP, Account Name: $AccountName"
}
```

这段脚本会显示所有成功登录事件的IP地址和账户名。

#### 方法3：使用Sysinternals工具（如Autoruns）

虽然Sysinternals的工具（如Autoruns）主要用于查看启动项和服务，但你也可以通过它们来间接获取某些登录信息。不过，最直接的方法还是使用Windows事件查看器和PowerShell。

注意事项：

- 确保你有足够的权限来查看安全日志。通常需要管理员权限。
- 某些情况下，可能需要开启Windows审核策略来记录特定的安全事件。你可以通过组策略编辑器（gpedit.msc）或使用PowerShell命令来配置审核策略。例如，启用审核登录事件：

```
Audit-ComputerSystemAccess -EnableLoginSuccess -EnableLoginFailure
```

### 常用Log Parser查询示例

查询所有登录成功事件

```
LogParser.exe -i:EVT --o:DATAGRID "SELECT * FROM [<盘符>:<路径>（比如c:\Security.evtx）] WHERE EventID=4624"
```

提取指定时间范围内的登录事件

```
LogParser.exe -i:EVT --o:DATAGRID "SELECT * FROM c:\Security.evtx WHERE TimeGenerated>'2025-01-01 08:00:00' AND TimeGenerated<'2026-01-01 08:00:00' AND EventID=4624"
```

例如查询2025年最后一次登录成功。

```
logparser -i:evt -o:datagrid "select timegenerated from <盘符>:<路径> where EventID = 4648 and to_date(timegenerated) between timestamp('2025-01-01','yyyy-mm-dd') and timestamp('2026-01-01','yyyy-mm-dd')"
```

提取登录成功的用户名和IP

```
LogParser.exe -i:EVT --o:DATAGRID "SELECT EXTRACT_TOKEN(Message,13,' ') AS EventType, TimeGenerated AS LoginTime, EXTRACT_TOKEN(Strings,5,'|') AS Username, EXTRACT_TOKEN(Message,38,' ') AS LoginIP FROM c:\Security.evtx WHERE EventID=4624"
```

统计登录失败次数最多的用户名

```
LogParser.exe -i:EVT "SELECT EXTRACT_TOKEN(Message,19,' ') AS User, COUNT(EXTRACT_TOKEN(Message,19,' ')) AS FailedAttempts, EXTRACT_TOKEN(Message,39,' ') AS LoginIP FROM c:\Security.evtx WHERE EventID=4625 GROUP BY Message ORDER BY FailedAttempts DESC"
```

查看系统历史开关机记录

```
LogParser.exe -i:EVT --o:DATAGRID "SELECT TimeGenerated, EventID, Message FROM c:\System.evtx WHERE EventID=6005 OR EventID=6006"
```

