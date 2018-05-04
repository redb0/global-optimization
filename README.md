# GlobalOptimization

Программа для исследования алгоритмов глобальной оптимизации.

## Algorithms
1) Gravitation Search Algorithm [(GSA)](http://ahmetcevahircinar.com.tr/wp-content/uploads/2017/04/GSA_A_Gravitational_Search_Algorithm.pdf);
2) Noise Resistance Gravitation Search Algorithm (NR-GSA);
3) Algorithm Selective Averaging Coordinates [(SAC)](https://cyberleninka.ru/article/v/metod-globalnoy-optimizatsii-osnovannyy-na-selektivnom-usrednenii-koordinat-pri-nalichii-ogranicheniy);
4) Algorithm Selective Averaging Coordinates with asymmetric change of search area (SAC-ACSA).

Алгоритмы по умолчанию должны находиться в папке `algorithms_exe`.
Результаты работы по умолчанию сохраняются в виде json-файлов в папку `algorithms_exe/result`.

## Graphs
1) линейный график (Представляет собой зависимость оценки вероятности от выбранного параметра алгоритма);
2) тепловая карта;
3) сходимость по значениям функции (-);
4) сходимость по значениям координат (-);
5) дисперсии (-);
6) движение лучшей точки (-).

## Test Functions
Поддерживается работа со следующими многоэкстремальными тестовыми функциями:
1) функции Фельдбаума (с использованием метода минимум);
2) гиперболические потенциальные функции;
3) экспоненциальные потенциальные функции.

Пример содержимого json-файла с тестовой функцией сконструированной по методу Фельдбаума:
```json
{ 
  "index": 1,
  "dimension": 2,
  "type": "feldbaum_function",
  "number_extrema": 10,
  "coordinates":
  [[0,0], [-2,0], [0,-2], [0,4], [2,2],
   [4,0], [4,4], [-4,4], [-4,-4], [3,-5]],
  "func_values": [0, 6, 5, 8, 7, 9, 4, 3, 7.5, 8.5],
  "degree_smoothness":
  [[2,2], [0.5,0.5], [1.3,1.3], [1,1], [1.5,1.5],
   [1.8,1.8], [0.6,0.6], [0.6,1.6], [1.2,0.5], [0.9,0.3]],
  "coefficients_abruptness":
  [[7,7], [5,5], [5,5], [5,5], [4,4],
   [5,5], [6,6], [6,6], [3,3], [2,4]],
  "constraints_high": [6, 6],
  "constraints_down": [-6, -6],
  "real_extrema": [0, 0],
  "amp_noise": 23.87,
  "min_value": 0,
  "Max_value": 23.87
}
```
График изолиний данной функции будт следующим:
![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f3_contour.png)

Пример из файла `./example_tf/func5.json` имеет следующий графический вид:

![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f5.png)
![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f5_x1=x2.png)

При добавлении аддитивной равномерно распределенной помехи, превышающей по амплитуде полезный сигнал в 10 раз:

![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f5_k_sn%3D10.png)
![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f5_x1%3Dx2_k_sn%3D10.png)

## Usage

Compile the algorithmic part of the project by running the command:

```commandline
cd C:/GlobalOptimization/algorithms_exe/alg_go/src
go build -o ../../algorithms.exe main.go
```

Run the program:
```commandline
cd C:/GlobalOptimization/
python main.py
```

## Adding additional algorithms

Для добавления дополнительных алгоритмов необходимо выполнить следующие шаги:
1) Добавить класс алгоритма на языке python и поместить в папку `./algorithms/`.
Класс должен быть унаследован от класса Algorithm либо от существующих классов групп (GSA, SAC), 
если вы хотите добавить свою группу алгоритмов, то унаследуйте ее от класса Algorithm, 
а затем класс конкретного алгоритма делайте наследником новой группы. 
Класс для группы алгоритмов должен реализовать метод ```__init__``` и имть поле с названием группы.
Класс консретного алгоритма должен реализовать метод ```__init__``` и ```get_identifier_name```. 
Они должны быть реализованы по аналогии с методами классов в файлах `./algorithms/StandardSAC.py`, 
`./algorithms/StandardGSA.py`.
2) Добавить недостающие параметру алгоритма в файл AlgorithmParameter.py, по аналогии с уже созданными.
3) Добавить алгоритм к списку используемых в поле ```self.active_alg_1``` класса MainWindow.
3) Добавить реализацию алгоритма на языце Golang в папку `./algorithms_exe/alg_go/algorithms`, 
либо .exe файл в папку `./algorithms_exe/`.

API к алгоритму: (будет добавлено позже)

