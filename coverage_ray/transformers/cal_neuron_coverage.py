import numpy as np
from tensorflow.keras.models import Model

def neuron_coverage(model, X):
    # 创建一个字典来存储神经元的覆盖信息，初始化为 False
    neuron_covered = {layer.name: [False] * layer.units for layer in model.layers if hasattr(layer, 'units')}
    
    calculated_model = [layer for layer in model.layers if hasattr(layer, 'units')]

    # 获取模型的中间层输出
    intermediate_layer_outputs = [layer.output for layer in model.layers if hasattr(layer, 'units')]
    
    # 创建一个新的模型，输出为中间层的输出
    intermediate_model = Model(inputs=model.input, outputs=intermediate_layer_outputs)
    # print(intermediate_model.summary())

    # 設定判斷激活的閾值
    threshold=0.2

    for tensor in X:
        # 使用给定的输入数据获取中间层的输出
        intermediate_outputs = intermediate_model.predict(tensor)

        # 使用给定的输入数据获取中间层的输出
        # 遍历每一层的输出，并更新神经元的覆盖信息
        for i, layer_output in enumerate(intermediate_outputs):
            
            layer_name = calculated_model[i].name
            for j in range(layer_output.shape[1]):
                if abs(np.max(layer_output[:, j])) > threshold:  # 如果神经元被激活
                    neuron_covered[layer_name][j] = True

            total_neurons = sum(len(layer) for layer in neuron_covered.values())
            covered_neurons = sum(sum(layer) for layer in neuron_covered.values())
            coverage_percentage = covered_neurons / total_neurons * 100
            # print(f"layer:{i},neuron covered:{neuron_covered.values()}, coverage:{coverage_percentage}")
    

    
    # 计算神经元覆盖率
    total_neurons = sum(len(layer) for layer in neuron_covered.values())
    covered_neurons = sum(sum(layer) for layer in neuron_covered.values())
    coverage_percentage = covered_neurons / total_neurons * 100
    
    return coverage_percentage

# 使用示例
# model 是你的神经网络模型
# X 是输入数据，形状为 (样本数量, 输入维度)
# 注意：这个示例假设神经网络的每一层都是 Dense 层或有类似 units 属性的层

