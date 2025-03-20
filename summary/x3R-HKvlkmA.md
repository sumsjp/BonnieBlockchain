## NVIDIA Blackwell 发布会内容详细梳理

以下是 NVIDIA Blackwell 发布会的详细内容整理，力求客观、细致地呈现原文信息，不添加任何个人评论。

**演讲开头：AI 驱动的变革**

Jensen Huang (黄俊英) 开场强调了科技发展的五个浪潮：通用计算、互联网、移动计算和云端计算，现在是 AI 浪潮。他指出，AI 正在重塑计算机产业，从数据中心到边缘，再到最终用户。

**工业数字化转型与 Siemens 合作**

NVIDIA 与 Siemens 建立深度合作，将 Siemens 的工业加速器平台与 NVIDIA Omniverse 连接。Siemens 技术应用于各个行业，例如船运制造商 HD&A，该公司需要处理数百万个离散部件。通过 Omniverse API，Teamcenter X 可以统一和可视化这些大规模工程数据，并通过生成 AI 来生成 3D 对象和 HDRI 背景，实现更直观的设计和制造流程。

合作的关键成果包括：

* **Siemens Accelerator 连接 Omniverse：** 实现工业级设计和制造项目的物理渲染和数据互操作性。
* **Teamcenter X 集成 Omniverse 和 AI:** 将数据整合到统一的数字双胞体中，以提高效率并减少浪费。

**Omniverse Cloud 的功能与应用**

* **数据统一性：** Omniverse 允许设计、艺术、架构、工程和市场营销部门在同一“真相基础”上协同工作，避免了数据交换、转换和错误。
* **Vision Pro 支持:** Omniverse Cloud 现在支持 Apple Vision Pro，允许用户在虚拟环境中漫游，并与数字双胞体进行交互。
* **多 CAD 工具集成：** Omniverse 集成了各种 CAD 工具，例如 Siemens NX 和 Star CCM+，实现无缝协作。

**General Robotics 003：人形机器人学习的基础模型**

NVIDIA 推出 General Robotics 003(Group) – 一种通用基础模型，旨在让人形机器人学习。

* **工作原理：** Group 模型接收多模式指令和过去互动信息作为输入，生成机器人执行的后续动作。
* **Isaac Lab 训练:** Group 模型在 Omniverse Isaac Sim 中进行训练。
* **Osmo 算力协调:** NVIDIA 推出 Osmo，用于协调 DGX 系统（用于训练）和 OVX 系统（用于模拟）的工作流程。
* **Jetson Thor 支持:**  Jetson Thor Robotics 芯片专为 Group 模型设计而成。

**迪士尼 BDX 机器人的展示：Isaac Lab 应用**

迪士尼的 Orange 和 Green (BDX机器人) 被展示出来，证明了 Isaac Lab 的学习应用。它们使用 Jetson 机器人电脑，并在 Isaac Sim 中学习行走。

**新型加速器 Blackwell 的发布**

NVIDIA 发布了全新的 Blackwell 加速器和相关平台，包括：

* **Blackwell GPU:** 设计为具有更强的性能和效率。
* **NVLink 交换机:** 用于连接多个GPU，提高计算能力。
* **Blackwell 系统设计：**  被形容为“奇迹”，注重性能和效率。
* ** Blackwell 平台:** 包含了完整的硬件生态系统，为AI和高性能计算提供支持。

**关键技术细节和平台组成:**

* **Transformer Engine:** 新增了用于快速训练和推理大型AI模型的Transformer Engine。
* **第二代 NVLink:** 提供了更高的带宽和更好的性能。
* **保密计算：**  Blackwell 提供了更高的安全性，保护数据隐私。
* **专用加速引擎:** 加快了AI和机器学习工作负载的处理速度。

**总结**

Jensen Huang总结了NVIDIA的愿景：构建一个完整的计算平台，能够支持各个行业的数字化转型。他认为 Blackwell 是实现这一愿景的关键，它将为开发者和服务提供商提供强大的算力，并让人工智能更加普及和易于访问。