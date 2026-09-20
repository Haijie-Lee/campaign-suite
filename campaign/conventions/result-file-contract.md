# 结果落盘契约（result-file-contract）

> campaign 插件约定 K4。被 dispatch 的执行单元必须遵守；编排者必须遵守「只读结论行」纪律。

## 1. 契约

被 dispatch 的单元（agent / 子任务）：

1. 把**过程与中间结果**写入 `result/<task-id>.md`（模板见同目录 `result-template.md`）；
2. **回传 ≤15 行**，且必须含四要素——**status / verdict / 结论 / 文件指针**：
   - `status`：封闭四态 `DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED`；
   - `verdict`：自评结论 `pass / fail / concerns`；
   - `结论`：产出了什么、验证证据是什么（数字到个位数）；
   - `文件指针`：`result/<task-id>.md` 的路径。

## 2. 编排者纪律

- 编排者**默认只读回传的 ≤15 行**；需要深究时才打开文件指针。
- 中间结果**不得**回流进编排者上下文——上下文是工作内存，不是存储（道层 D1）。

## 3. 例外

**inline 任务**（主线程自己执行、不经 dispatch 的任务）免落盘——其过程本就在主线程上下文内。
