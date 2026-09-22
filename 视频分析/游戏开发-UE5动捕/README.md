# UE5 / UEFN 角色动作制作

## 分支定位

这里整合 UE5 / UEFN 角色动作制作相关的视频和实践知识，覆盖动作获取、视频动捕、AI 动作生成、骨骼重定向、Control Rig 和 AnimGen 运行时控制器。

## 知识库总览

- [角色动作制作知识库](角色动作制作知识库.md)：把现有视频整合为可执行的项目流程、验收门槛和故障排查规则。

## 视频资料

| 视频 | 内容 | 文档 |
|------|------|------|
| BV1baj26REMg | UE5.8 内置免费动捕与 MetaHuman 动画流程 | [summary.md](BV1baj26REMg/summary.md) |
| BV1ndMM6jEvv | 豆包视频到 UE5.8 动捕，再重定向到其他角色 | [summary.md](BV1ndMM6jEvv/summary.md) |
| BV1K7hB6PEm3 | Kimodo 生成 3D 动作、训练 AnimGen、制作个性化步态 | [summary.md](BV1K7hB6PEm3/summary.md) |

## 统一工作流

```text
真人视频 / AI 视频 / Kimodo 3D 动作
                    ↓
             动作解算或动作导出
                    ↓
           统一骨架与重定向清理
                    ↓
              Idle / Walk / Run / Stop
                    ↓
             AnimGen 控制器训练
                    ↓
              Animation Blueprint
                    ↓
                  游戏内验收
```

后续相关视频优先补充到这个分支，并更新知识库总览；只有完全不同的制作领域才新建大分支。
