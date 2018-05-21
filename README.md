# GlOpPy

Program for the study of global optimization algorithms.

## Algorithms
1) Gravitation Search Algorithm [(GSA)](http://ahmetcevahircinar.com.tr/wp-content/uploads/2017/04/GSA_A_Gravitational_Search_Algorithm.pdf);
2) Noise Resistance Gravitation Search Algorithm (NR-GSA);
3) Algorithm Selective Averaging Coordinates [(SAC)](https://cyberleninka.ru/article/v/metod-globalnoy-optimizatsii-osnovannyy-na-selektivnom-usrednenii-koordinat-pri-nalichii-ogranicheniy);
4) Algorithm Selective Averaging Coordinates with asymmetric change of search area (SAC-ACSA).

The default algorithms must be in the folder `algorithms_exe`.
The default output is saved as json files to a folder `algorithms_exe/result`.

## Graphs
1) line chart (the dependence of the probability estimate on the parameter of the algorithm);
2) point graph;
3) heat map;
4) convergence in function values;
5) convergence in coordinate values;
6) dispersion;
7) best point motion.

## Test Functions
Поддерживается работа со следующими многоэкстремальными тестовыми функциями:
1) функции Фельдбаума (using the operation of a minimum);
2) гиперболические потенциальные функции;
3) экспоненциальные потенциальные функции.

Пример содержимого json-файла с тестовой функцией сконструированной по методу Фельдбаума:
```json
{
  "index": 5,
  "dimension": 2,
  "type": "feldbaum_function",
  "number_extrema": 10,
  "coordinates":
  [
    [-2, 4], [0, 0], [4, 4], [4, 0], [-2, 0],
    [0, -2], [-4, 2], [2, -4], [2, 2], [-4, -2]
  ],
  "func_values": [0, 3, 5, 6, 7, 8, 9, 10, 11, 12],
  "degree_smoothness":
  [
    [0.6, 1.6], [1.6, 2], [0.6, 0.6], [1.1, 1.8], [0.5, 0.5],
    [1.3, 1.3], [0.8, 1.2], [0.9, 0.3], [1.1, 1.7], [1.2, 0.5]
  ],
  "coefficients_abruptness":
  [
    [6, 6], [6, 7], [6, 7], [5, 5], [5, 5],
    [5, 5], [4, 3], [2, 4], [6, 4], [3, 3]
  ],
  "constraints_high": [6, 6],
  "constraints_down": [-6, -6],
  "global_min": [-2, 4],
  "global_max": [6, 6],
  "amp_noise": 11.5,
  "min_value": 0,
  "Max_value": 23
}
```
График изолиний данной функции будт следующим:
![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f3_contour.png)

Пример из файла `./example_tf/func5.json` имеет следующий графический вид:

![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f5.png)
![alt text](https://github.com/redb0/global-optimization/blob/master/examples_tf/f5_x1=x2.png)

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

