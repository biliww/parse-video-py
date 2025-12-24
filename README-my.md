切换主题动画:

已为您优化了暗黑模式切换的动画效果。现在点击切换按钮时，会以点击位置为中心，通过圆形扩散的方式平滑过渡到新主题，而不是生硬的闪烁切换。
主要修改内容如下：
CSS 样式: 添加了 ::view-transition-old(root) 和 ::view-transition-new(root) 的样式，禁用了默认的淡入淡出动画，为自定义动画做准备。
JavaScript 逻辑:
引入了 Vue 的 nextTick。
重写了 toggleTheme 函数，使用 document.startViewTransition API。
计算了从点击位置到屏幕最远角的距离作为扩散半径。
使用 document.documentElement.animate 对 ::view-transition-new(root) 伪元素执行 clip-path 动画，实现圆形扩散效果。
保留了对不支持该 API 浏览器的兼容性处理（直接切换）。