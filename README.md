# Apple Quality Control Application

## English

### Overview
This application is designed for quality control of apples, utilizing detection and subsequent sorting based on size and condition (Large/Small/Defective). It detects apples either by color or alternatively by object detection using a YOLO model trained with the COCO dataset. It further classifies apples as defective using a pre-trained KERAS model with a dataset of both rotten and good apples.

### Technologies Used
- Python
- OpenCV
- Keras
- PyQt6

### Dependencies
- Numpy
- opencv-python
- keras
- pyqt6
- configmanager

### Usage
1. Install Python from [Python Official Website](https://www.python.org/downloads/).

2. Install the required dependencies using the following command in commandline:
```
pip install numpy opencv-python keras pyqt6 configmanager
```

3. Run the application using the command:
```
python python main.py
```

4. Follow the on-screen instructions to input apples for quality control, and view the results.

5. Alternatively, you can use the precompiled executable version of the application available in the [AppleCategorizationApp_EXE.zip](https://github.com/8JP8/Projeto1_ESAN-UA_2023-2024/releases/download/V1.6/AppleCategorizationApp_EXE.zip).

#-----------------------------------------------------


## Português

### Visão Geral
Esta aplicação é projetada para o controle de qualidade de maçãs, utilizando a detecção e subsequente classificação com base no tamanho e estado (Grande/Pequena/Defeituosa). Ela detecta maçãs pela cor ou, alternativamente, pela detecção de objetos usando um modelo YOLO treinado com o conjunto de dados COCO. Além disso, classifica as maçãs como defeituosas usando um modelo KERAS pré-treinado com um conjunto de dados de maçãs podres e boas.

### Tecnologias Utilizadas
- Python
- OpenCV
- Keras
- PyQt6

### Dependências
- Numpy
- opencv-python
- keras
- pyqt6
- configmanager

### Utilização
1. Instale o Python a partir do [site oficial do Python](https://www.python.org/downloads/).

2. Instale as dependências necessárias usando o seguinte comando no terminal:
```
pip install numpy opencv-python keras pyqt6 configmanager
```

4. Execute a aplicação com o comando:
```
python main.py
```

6. Siga as instruções na tela para inserir maçãs para controle de qualidade e visualize os resultados.

7. Alternativamente, você pode usar a versão executável pré-compilada do aplicativo disponível no arquivo [AppleCategorizationApp_EXE.zip](https://github.com/8JP8/Projeto1_ESAN-UA_2023-2024/releases/download/V1.6/AppleCategorizationApp_EXE.zip).
