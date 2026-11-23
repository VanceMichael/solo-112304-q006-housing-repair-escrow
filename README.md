# 回迁房维修资金的跨账册冻结代办

房屋交付档案、产权登记和物业收款系统保留不同编号。维修专户仅接受登记的资金户和申请编号。

本地来源与合作端均使用合成业务资料。Python 3.11 运行来源服务，服务默认绑定回环地址。

```sh
python3 source_fixture.py --port 8765
python3 -m unittest -v
```

浏览器测试使用 Playwright 1.56.0 和随该版本安装的 Chromium。首次建立环境时运行 `python3 -m pip install -r requirements-browser.txt` 与 `python3 -m playwright install chromium`。

## 数据交换

- `/property/handover` 列明楼栋、交付单元和物业页地址。物业页使用各楼栋自己的分页地址，页眉标明账务快照。同快照金额明细的房号有相同适用期。
- `/registry/units` 以登记份额和 effective 指定权益事实。份额是本维修范围总份额的百分数，拆分前后不能同时计入。
- `/repairs/applications` 有签认日、范围、表决条件和拟出资。达到申请表所列的有效份额且有足额冻结才可拨款，代管户可被指为资金来源。
- `/escrow/effective` 的 frozen 和 paid 都是资金已占事实，released 表示冻结已解除。合作端条目用资金户编号，申请编号、划款或解冻金额放在业务明细。

演练运维端 `GET /__scene` 返回当前时间点，`POST /__scene` 接受 JSON 字段 `index`，从 0 开始顺序切换，每次加 1。换场不会清除合作端当次运行已生成的回执。需要开始新的独立演练时重启服务。业务时间以各来源的当前版本为准。

合作端允许按 `request` 字段查找同路径下的业务请求号，提交使用 `request`、`operation`、`items`（字符串数组）。业务明细使用可选 JSON 对象 `details`，以此请求内的条目编号为键。界面端填多项时按逗号分隔。来源约定的业务动作按下表允许值填写。统一回执含请求号、模拟回执号与各行状态。相同请求号的原样重交返回原回执，参数有变则返回 HTTP 409。回执检索的 404 表示该时刻未查到。描述业务状态的可读来源会随演练进度独立更新，某次提交回执不会提前改写该来源。

## 合作端动作

- `/escrow/portal` 接受 `freeze`、`release`、`pay`、`refer`。
