# scripts

这个目录保存仓库维护脚本，不需要安装 npm 或额外的 Python 检查库。

## 文件

- [check-code.ps1](check-code.ps1)：统一运行 Python、JavaScript、PowerShell、HTML 和 Matlab 文件名检查
- [check-python-code.py](check-python-code.py)：使用 Python 标准库检查语法、行长、危险导入、网络超时、文本编码和旧 API
- [check-html-code.py](check-html-code.py)：检查 HTML 重复 ID、图片替代文本和按钮类型
- [check-docs.ps1](check-docs.ps1)：检查 Markdown 本地链接、代码块闭合情况，以及一级目录是否包含 README
- [MAINTAINER_GUIDE.md](MAINTAINER_GUIDE.md)：文档维护者指南，说明新增教程、更新导航和排查检查失败的流程

推荐运行顺序：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-code.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\check-docs.ps1
git diff --check
```

`check-code.ps1` 需要系统能够找到 `python`；仓库存在 JavaScript 文件时还需要 `node`。它不会运行网络、删除、邮件或算法示例，只做静态检查。
