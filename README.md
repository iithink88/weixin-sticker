# weixin-sticker 1.1.0

制作可用于**微信表情开放平台投稿**的静态表情包：给一个角色或主题，产出 8–24 张 240×240 透明表情、详情页横幅、表情封面、聊天页图标，按需产出赞赏引导图与致谢图，校验尺寸格式后打包 ZIP。

适用于 Codex、WorkBuddy、豆包工作等支持 Skills 的 Agent。安装方式见 [INSTALL.md](INSTALL.md)。

## 示例（详情页横幅制作流程）

下图为一次示例制作中的三张图：左侧为用户提供的原始参考图，中间为绿幕后由 AI 生成的原始横幅，右侧为经 `optimize_png.py` 处理、最终投稿用的 750×400 详情页横幅。

| 原图（参考） | 生成的横幅（绿幕 AI 生成） | 详情页横幅（成品 750×400） |
| --- | --- | --- |
| ![原图](examples/原图详情页横幅.png) | ![生成的横幅](examples/生成的详情页横幅.png) | ![详情页横幅](examples/详情页横幅.png) |

> 示例文件位于 `examples/`，可直接在仓库中预览。

## 包含内容

```
weixin-sticker-1.1.0/
├── SKILL.md                    技能主流程（Agent 读这个）
├── INSTALL.md                  三平台安装与自检
├── requirements.txt            Pillow
├── agents/openai.yaml          Codex 界面适配
├── scripts/
│   ├── build_sticker.py        ★ 绿幕抠图 + 中文文字排版 → 240×240 透明表情
│   ├── compose_reward.py       ★ 赞赏图裁切 + 抹水印 + 文字排版
│   ├── optimize_png.py         横幅/封面/图标尺寸与透明画布处理
│   ├── validate_pack.py        数量、格式、尺寸、透明像素、体积校验
│   └── package_album.py        中文命名打包 ZIP
├── assets/表情包切割.html       离线切割工具，网格切割 + 智能拆分 + 主题名批量解析
└── references/wechat-album-spec.md  平台素材规格整理
```

## 一条命令看懂用法

```bash
python scripts/build_sticker.py 绿幕源图.png 专辑/表情/你好.png "你好"
python scripts/compose_reward.py 引导源图.png 专辑/赞赏引导图.png 750 560 "喜欢就赞赏一下吧"
python scripts/validate_pack.py 专辑
python scripts/package_album.py 专辑 "专辑名（十六张）.zip"
```

## 这套流程解决了什么

1. **透明背景**：生成模型的 `transparent` 参数常常画出棋盘格假透明；改为绿幕生成 + 色键抠图，能拿到真实 alpha。
2. **中文文字**：让模型写中文必出错字；文字统一由脚本用系统中文字体排版，字形准确、多张风格一致。
3. **角色一致性**：参考图 + 固定特征描述 + 逐张串行生成，避免多张人物走形。
4. **并行陷阱**：多数图像工具按秒级时间戳命名输出，并行生成会互相覆盖；脚本化流程里必须逐张串行。

## 许可

基于 [zxd-666/weixin-sticker](https://github.com/zxd-666/weixin-sticker)（MIT）扩展，原版权归原作者所有，遵循 MIT 分发。详见 LICENSE 与 INSTALL.md 的“许可与来源”。
