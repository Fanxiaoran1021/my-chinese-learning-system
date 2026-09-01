# 中文自学系统 接口测试用例
## 用户模块
1. 创建用户 POST /api/users
请求体：
{
  "username":"test01",
  "password":"123456"
}
预期：返回用户对象，状态200

2. 查询用户 GET /api/users/1
预期：返回用户信息，不存在返回404

3. 修改用户 PUT /api/users/1
{
  "username":"updateuser",
  "password":"654321"
}

4. 删除用户 DELETE /api/users/1

## 词汇模块
1.新增词汇 POST /api/vocab
{
"word":"苹果",
"pinyin":"píng guǒ",
"meaning":"apple",
"example":"我爱吃苹果。"
}

2.查询、修改、删除 /api/vocab/{id}

## 学习记录模块
1.新增记录 POST /api/record
{
"user_id":1,
"vocab_id":1,
"status":"learning"
}

2.查询、修改、删除 /api/record/{id}