# Flash-Retention-Test-Tools

一些用于Flash Retention测试的代码，用于便捷地进行测试

## 为什么要进行Flash Retention的测试

Flash Memory的数据保存久了之后可能会出错，QLC Flash的期望出错时间则更短，一些前置知识可查看[Data Retention in MLC NAND Flash Memory: Characterization, Optimization, and Recovery](https://users.ece.cmu.edu/~omutlu/pub/flash-memory-data-retention_hpca15.pdf)这篇论文。为此，张杰老师让我进行了一些Data Retention的测试，希望能够测试不同的QLC Flash在不同的P/E Cycle下数据能够保存多长的时间，从而可以进一步地做出改进

如果我们的测试Flash放置在常温中，则所需的测试时间太长了，因此，我们需要一个恒温箱来使得Flash能够放置在高温环境中，从而加速数据丢失的过程。但是，这又引入了一个新问题，某一高温和常温的数据丢失时间如何对应，关于这方面可查看[How the common retention acceleration method of 3D NAND flash memory goes wrong?](https://dl.acm.org/doi/10.1145/3465332.3470877)这篇论文

## 设备的准备工作

