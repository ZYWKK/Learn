# 现代 Web API 实验台

这是一个不依赖框架和构建工具的现代浏览器能力案例。页面把几个原生 API 组合成一个可操作的小实验台，同时为不支持新 API 的浏览器保留基础回退行为。

## 适合人群

- 已经了解 HTML、CSS 和 JavaScript 基础语法的学习者。
- 想知道“不使用 React/Vue，也能不能封装组件”的初学者。
- 想学习响应式组件、原生浮层和页面状态过渡的人。

## 学习目标

- 使用 Custom Elements 和 Shadow DOM 创建可复用组件。
- 使用 CSS Container Queries 让组件根据容器宽度变化，而不只看视口宽度。
- 使用 Popover API 创建由浏览器管理的非模态浮层。
- 使用 View Transition API 平滑切换页面状态，并提供无动画回退。
- 使用 `aria-pressed`、`aria-expanded`、`hidden` 和语义元素保持可访问状态。

## 文件说明

| 文件 | 作用 |
| :--- | :--- |
| [index.html](index.html) | 页面结构、实验控制和自定义元素实例 |
| [style.css](style.css) | 页面布局、容器查询、Popover 和过渡样式 |
| [script.js](script.js) | Web Component、筛选、宽度控制和渐进增强 |

## 如何打开

直接双击 [index.html](index.html) 即可。建议使用较新的 Chrome、Edge、Firefox 或 Safari。

页面仍会在不支持 Popover 或 View Transition API 的浏览器中完成主要操作，但原生浮层管理或切换动画可能会退化为普通显示效果。

## 观察顺序

1. 拖动“组件容器宽度”，观察卡片内部布局变化。
2. 点击筛选按钮，观察列表状态切换。
3. 打开“API 状态”，查看当前浏览器支持情况。
4. 阅读 `script.js` 中的 `LearningTopic` 类，找到 Shadow DOM 模板。
5. 阅读 `runViewUpdate()` 和 `setupPopover()`，理解特性检测与回退。

## 推荐修改点

- 给 `<learning-topic>` 增加新的属性，并在 `observedAttributes` 中监听它。
- 修改 `@container` 的宽度阈值，观察组件何时切换布局。
- 增加一个新的筛选类别。
- 为 Popover 增加关闭按钮，并比较原生关闭和手动关闭的区别。

## 参考来源

- [MDN Web Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components)
- [MDN CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries)
- [MDN Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)
- [MDN View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)

本案例为原创教学实现，没有复制外部项目源码。
