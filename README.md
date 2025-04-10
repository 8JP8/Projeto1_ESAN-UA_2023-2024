# Apple Quality Control Application

### Overview
This application is designed for quality control of apples, utilizing detection and subsequent sorting based on size and condition (Large/Small/Defective). It detects apples either by color or alternatively by object detection using a YOLO model trained with the COCO dataset. It further classifies apples as defective using a pre-trained KERAS model with a dataset of both rotten and good apples.

### Technologies Used
- Python 3.10
- OpenCV
- Keras
- PyQt6
- Pyserial

### Dependencies
- Numpy
- opencv-python
- keras
- pyqt6
- configmanager
- pyserial

### Usage
1. Install Python from [Python Official Website](https://www.python.org/downloads/).

2. Install the required dependencies using the following command:
```
pip install numpy opencv-python keras pyqt6 configmanager pyserial tensorflow
```

3. Download the SourceCode and put the models.zip content (downloaded from the releases) inside the modules folder.
   
4. Run the application using the command or use the executable version from the releases:
```
python main.py
```

5. Follow the on-screen instructions to input apples for quality control, and view the results.

6. Alternatively, you can use the precompiled executable version of the application available in the [AppleCategorizationApp_EXE.zip](https://github.com/8JP8/Projeto1_ESAN-UA_2023-2024/releases/download/V1.6/AppleCategorizationApp_EXE.zip).

---
# Aplicação de Controlo de Qualidade de Maçãs

### Visão Geral
Esta aplicação é projetada para o controle de qualidade de maçãs, utilizando a detecção e subsequente classificação com base no tamanho e estado (Grande/Pequena/Defeituosa). Ela detecta maçãs pela cor ou, alternativamente, pela detecção de objetos usando um modelo YOLO treinado com o conjunto de dados COCO. Além disso, classifica as maçãs como defeituosas usando um modelo KERAS pré-treinado com um conjunto de dados de maçãs podres e boas.

### Tecnologias Utilizadas
- Python 3.10
- OpenCV
- Keras
- PyQt6
- Pyserial

### Dependências
- Numpy
- opencv-python
- keras
- pyqt6
- configmanager
- pyserial

### Utilização
1. Instale o Python a partir do [site oficial do Python](https://www.python.org/downloads/).

2. Instale as dependências necessárias usando o seguinte comando:
```
pip install numpy opencv-python keras pyqt6 configmanager pyserial tensorflow
```

3. Faça download do sourcecode e do models.zip (disponível nas releases) e coloque o conteúdo na pasta modules.

4. Execute a aplicação com o comando ou abra a versão executável disponível nas releases:
```
python main.py
```

5. Siga as instruções na tela para inserir maçãs para controle de qualidade e visualize os resultados.

6. Alternativamente, você pode usar a versão executável pré-compilada do aplicativo disponível no arquivo [AppleCategorizationApp_EXE.zip](https://github.com/8JP8/Projeto1_ESAN-UA_2023-2024/releases/download/V1.6/AppleCategorizationApp_EXE.zip).
