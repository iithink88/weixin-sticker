# 安装说明（Codex / WorkBuddy / 豆包工作 等支持 Skills 的 Agent）

这个包是一个**标准 Agent Skill**：根目录有 `SKILL.md`（含 `name` / `description` 元信息），辅以 `scripts/`、`assets/`、`references/`、`agents/`。
安装即“把整个文件夹放进该 Agent 的技能目录”。**不要只复制 `SKILL.md`**，否则会缺切割、抠图、校验和打包工具。

## 通用前提

- Python 3.9 及以上，并安装依赖：`python3 -m pip install -r requirements.txt`（只有 Pillow 一个依赖）
- 需要该 Agent 具备：图片生成能力、本地文件读写、执行 Python 脚本的权限
- 可选：Node.js 仅用于跑切割工具的测试，浏览器里使用切割 HTML 不需要 Node

## Codex

```bash
git clone <本包地址> ~/.codex/skills/weixin-sticker
# 或者：解压本 ZIP，把 weixin-sticker-1.1.0 文件夹改名成 weixin-sticker 放进该目录
python3 -m pip install -r ~/.codex/skills/weixin-sticker/requirements.txt
```

放好后开一个新对话，输入 `用 $weixin-sticker 帮我做一套 16 张微信表情包`。
`agents/openai.yaml` 已提供 Codex 的界面显示名与默认 prompt。

## WorkBuddy

方式一（推荐，图形界面）：打开「设置 → 技能 → 添加技能 → 上传技能包」，选择本 ZIP 直接导入。

方式二（本地目录）：解压后把文件夹放到用户级技能目录，所有项目可用：

```bash
mv weixin-sticker-1.1.0 ~/.workbuddy/skills/weixin-sticker
```

若项目内只用，则放到 `<项目>/.workbuddy/skills/weixin-sticker`。
**技能列表在会话开始时加载，装完要新开一个对话才会生效。**

注意：WorkBuddy 自带的托管 Python 环境里裸 `python` / `python3` 不一定装了 Pillow。稳妥做法是把依赖装进托管环境后再调用其解释器：

```bash
~/.workbuddy/binaries/python/versions/<版本>/bin/python3 -m pip install -r requirements.txt
```

## 豆包工作 / 其他支持 Skills 的 Agent

这类产品有各自的技能入口，不使用 Codex 的目录约定。通用做法：把 ZIP（或解压后的文件夹）通过“技能 / 插件 / 扩展”入口导入，然后确认运行环境满足上面「通用前提」。
如果产品只接受单个 Markdown 技能文件，把 `SKILL.md` 作为技能正文导入，并**同时**把 `scripts/`、`assets/`、`references/` 一并上传为其附件或工作区文件——缺少脚本时，切割、抠图、校验、打包四步都会失败。

## 自检

安装后跑一次依赖与脚本自检：

```bash
python3 scripts/validate_pack.py --help
python3 -c "import PIL; print('Pillow', PIL.__version__)"
```

两者都能正常输出，说明环境就绪。

## 许可与来源

本包基于 [zxd-666/weixin-sticker](https://github.com/zxd-666/weixin-sticker)（MIT）扩展：
保留其 `scripts/optimize_png.py`、`scripts/validate_pack.py`、`scripts/package_album.py`、`assets/表情包切割.html`、`references/wechat-album-spec.md`、`agents/openai.yaml` 与 `LICENSE`；
新增 `scripts/build_sticker.py`（绿幕色键抠图 + 中文文字排版）、`scripts/compose_reward.py`（赞赏图裁切/抹水印/文字排版），并在 `SKILL.md` 中补充了“生成与抠图”工艺章节。原始版权归 zxd-666，遵循 MIT 协议分发。
