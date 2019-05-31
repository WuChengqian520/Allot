# 接口文档
**推荐使用MarkDown阅读器查看：[作业部落MarkDown编辑器](https://www.zybuluo.com/mdeditor)**

### WEB接口


### TreeATE接口
##### 获取sn
- 接口协议： HTTP
- 接口地址：`/getSn/`
- 请求方式： POST
- 数据格式： JSON
- 请求参数： 
    - series : 产品系列名称
    - barcode: 产品条码 
- 示例：
```json
{
	"series": "K901",
	"barcode": "189789423822157"
}
```

- 返回参数：
    - code: 状态码。200-成功，401-json格式错误，403-产品系列未注册
    - message: 提示信息
    - data: 返回的数据（仅code为200时有数据）
        - barcode: 条形码
        - password: 蓝牙密码
        - sn: 蓝牙sn
        - create_time: 创建时间

- 返回示例：
```json
{
    "code": 200,
    "message": "成功",
    "data": {
        "barcode": "123213124312",
        "password": "4D83379E04E2A040D7B69F96",
        "sn": "K901192210006",
        "create_time": "2019-05-31T10:36:37.162"
    }
}
```
