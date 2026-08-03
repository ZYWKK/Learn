# Mathematica 可运行案例

这个目录把基础教程中的表达式、规则、符号计算、图计算和机器学习组合成三个完整 `.wl` 案例。代码可以粘贴到 Notebook 分段运行，也可以使用配置好 Kernel 的 `wolframscript` 执行。

## 适合人群

- 已读完 [Mathematica 基础教程](../Basics/README.md) 的初学者。
- 想从零散命令过渡到完整 Wolfram Language 脚本的人。
- 想了解符号计算如何帮助现代科学机器学习的人。

## 案例索引

| 顺序 | 案例 | 学习重点 | 说明 |
| :--- | :--- | :--- | :--- |
| 1 | [图社区发现](graph_community_detection.wl) | `Graph`、模式函数、`FindGraphCommunities`、可视化 | 完全本地运行 |
| 2 | [符号化物理约束损失](symbolic_physics_informed_loss.wl) | 导数、积分、损失函数、`NMinimize` | 完全本地运行 |
| 3 | [轻量神经分类](tiny_neural_classifier.wl) | 数据规则、`Classify`、概率输出、特征空间 | 首次运行可能初始化机器学习组件 |

## 在 Notebook 中运行

最适合初学者的方法是：

1. 新建 Notebook。
2. 打开一个 `.wl` 文件。
3. 每次复制一小段到 Notebook。
4. 按 `Shift + Enter` 逐段运行并观察输出。

也可以在 Notebook 中直接载入脚本：

```wolfram
Get["完整路径/graph_community_detection.wl"]
```

Windows 路径可以使用正斜杠，例如：

```wolfram
Get["F:/GithubData/Learn/Mathematica/Examples/graph_community_detection.wl"]
```

## 使用 wolframscript

已经安装 Wolfram Engine 或 Mathematica 并配置 Kernel 后，可以执行：

```powershell
wolframscript -file "Mathematica\Examples\graph_community_detection.wl"
wolframscript -file "Mathematica\Examples\symbolic_physics_informed_loss.wl"
wolframscript -file "Mathematica\Examples\tiny_neural_classifier.wl"
```

图形表达式在 Notebook 中显示最直观。命令行环境主要用于查看打印结果和检查脚本能否执行。

## 学习重点

### 图社区发现

案例先生成两个内部连接紧密的节点组，再添加少量跨组连接。`FindGraphCommunities` 会根据网络结构寻找社区，不需要提前告诉算法每个节点属于哪一组。

### 符号化物理约束损失

案例用符号求导直接得到微分方程残差，再把残差平方积分成物理损失。这展示了 Wolfram Language 在科学机器学习中的一个优势：公式、导数和数值优化可以放在同一套表达式系统中。

### 轻量神经分类

案例把二维坐标和类别写成规则：

```wolfram
{x, y} -> "Inner"
```

然后交给 `Classify[..., Method -> "NeuralNetwork"]`。这属于高层工作流，适合先理解数据输入、预测和概率；想研究网络层结构时再学习 `NetChain`、`NetGraph` 和 `NetTrain`。

## 推荐修改点

- 减少图中的跨组边，观察社区划分是否更清晰。
- 修改物理损失权重，比较数据拟合和方程约束的平衡。
- 给分类数据增加噪声，观察预测概率如何变化。
- 把分类方法改为 `"LogisticRegression"`，比较线性模型和神经网络。

## 权威参考

- [Wolfram FindGraphCommunities](https://reference.wolfram.com/language/ref/FindGraphCommunities.html)
- [Wolfram CommunityGraphPlot](https://reference.wolfram.com/language/ref/CommunityGraphPlot.html)
- [Wolfram Machine Learning](https://reference.wolfram.com/language/guide/MachineLearning.html)
- [Wolfram Neural Networks](https://reference.wolfram.com/language/tutorial/NeuralNetworksOverview.html)
- [Physics-informed neural networks](https://doi.org/10.1016/j.jcp.2018.10.045)

本目录代码为原创教学实现，外部资料只用于确认函数和方法。

## 下一步

- [Mathematica 专题学习指南](../TOPIC_GUIDE.md)
- [Mathematica Notebook 写作指南](../NOTEBOOK_GUIDE.md)
- [Matlab 现代计算案例](<../../Matlab/Modern Computing/README.md>)
