package sac_acsa

import (
	"math/rand"
	"fmt"
	"support"
	"math"
	"time"
	"strconv"
	"strings"
	"testfunc"
	"algorithms/sac"
	"algorithms"
)

func getOctree(dim, lenSubArray int) [][][]float64 {
	x := make([][][]float64, dim)
	for i := range x {
		x[i] = make([][]float64, lenSubArray)
	}
	return x
}

//intToBitStr преобразует целое число в битовую строку.
//Аргументы:
//    n - число для преобразования
//    l - длина битовой строки
//Возвращаемые значения:
//    битовая строка
func intToBitStr(n, l int) string {
	s := strconv.FormatInt(int64(n), 2)
	var res string
	if len(s) < l {
		res = strings.Repeat("0", l - len(s)) + s
	} else {
		return s
	}
	return res
}

//bitStrToInt преобразует битовую строку в целое число
//Аргументы:
//    битовая строка
//Возвращаемые значения:
//    целое число
func bitStrToInt(s string) int {
	v, _ := strconv.ParseInt(s, 2, 64)
	return int(v)
}

//bitStrArrayToIntArray преобразует список битовых строк в список целых чисел
//Аргументы:
//    список битовых строк
//Возвращаемые значения:
//    список целых чисел
func bitStrArrayToIntArray(s []string) []int {
	res := make([]int, len(s))
	for i := range s {
		res[i] = bitStrToInt(s[i])
	}
	return res
}

//getNumBitStr выбирает битовые строки, в которых на месте idx находится бит v
//Аргументы:
//    bitsStrNum - список битовых строк
//    idx - номер бита
//    v - бит
//Возвращаемые значения:
//    список битовых строк
func getNumBitStr(bitsStrNum []string, idx, v int) []string {
	var res []string
	for i := range bitsStrNum {
		if string(bitsStrNum[i][idx]) == strconv.Itoa(v) {
			res = append(res, bitsStrNum[i])
		}
	}
	return res
}

//intsInBits преобразует список целых чисел в список битовых строк
//Аргументы:
//    number - список целых чисел
//    l - длина битовой строки
//Возвращаемые значения:
//    список битовых строк
func intsInBits(number []int, l int) []string {
	res := make([]string, len(number))
	for i := range res {
		res[i] = intToBitStr(number[i], l)
	}
	return res
}

/*
initializationOperatingPointAndDelta инициализирует рабочую точку и расстояния области поиска.
Аргументы:
    function - структура тестовой функции
Возвращаемые значения:
    координаты рабочей точки
    список расстояний области поиска.
Рабочая точка инициализируется в (0, 0)
Если имеется функция от двую переменных и наложены аграничения -6<=x1,x2<=6,
то operatingPoint = [0, 0], а
delta = [[6, 6], [6, 6]]
 */
func initializationOperatingPointAndDelta(function testfunc.TestFunction) ([]float64, [][]float64) {
	operatingPoint := make([]float64, function.Dimension)
	delta := make([][]float64, function.Dimension)
	low := function.Down
	high := function.Up
	for i := range operatingPoint {
		delta[i] = make([]float64, 2)
		//FIXME: сделать выбор инициализации operatingPoint: случайно либо вручную, передавая список координат
		operatingPoint[i] = 0
		//operatingPoint[i] = rand.Float64() * (high[i] - low[i]) + low[i]
		delta[i][0] = operatingPoint[i] - low[i]
		delta[i][1] = high[i] - operatingPoint[i]
	}
	return operatingPoint, delta
}

/*
initializationTestPoints инициализирует пробные точки.
Аргументы:
    function - структура тестовой функции
    options - структура настроек алгоритма
    delta - список расстояний области поиска
    operationPoint - координаты рабочей точки
Возвращаемые значения:
    список координат пробных точек
Пробные точки инициализируются случайным образом, с помощью равномерного закона распределения в области:
для x1: [x0-delta0_0, x0+delta0_1]
для x2: [x1-delta1_0, x1+delta1_1]
где, (x0, x1) - координаты рабочей точки;
delta = [[delta0_0, delta0_1], [delta1_0, delta1_1]].
 */
func initializationTestPoints(function testfunc.TestFunction, options Options, delta [][]float64, operationPoint []float64) [][][]float64 {
	numberQuadrants := math.Pow(2, float64(function.Dimension))
	quadTree := make([][][]float64, int(numberQuadrants))
	//for i := range quadTree {
	//	quadTree[i] = make([][]float64, int(float64(options.NumberPoints)/numberQuadrants))
	//}
	//testPoints := make([]float64, function.Dimension)
	for i := 0; i < options.NumberPoints; i++ {
		testPoints := make([]float64, function.Dimension)
		//arrayEqual := make([]bool, function.Dimension)
		var idx float64 = 0
		for j := 0; j < len(testPoints); j++ {
			low := operationPoint[j] - delta[j][0]
			high := operationPoint[j] + delta[j][1]
			testPoints[j] = rand.Float64() * (high - low) + low

			//arrayEqual[j] = testPoints[j] < operationPoint[j]
			if testPoints[j] < operationPoint[j] {
				idx = idx + math.Pow(2, float64(function.Dimension - j - 1))
			}
		}
		quadTree[int(idx)] = append(quadTree[int(idx)], testPoints)
	}
	return quadTree
}

/*
findNormNuclearFunc вычисляет нормированные значения ядерной функции
Аргументы:
    g - список нормированных значений функции
    options - структура настроек алгоритма
Возвращаемые значения:
    список нормированных значений ядерной функции
    ошибка
 */
func findNormNuclearFunc(g []float64, options Options) ([]float64, error) {
	nuclearFuncNormValue := make([]float64, len(g))
	var ok error
	var sum float64 = 0
	for i := range nuclearFuncNormValue {
		nuclearFuncNormValue[i], ok = SAC.GetNuclearFunc(options.IndexNF, g[i], options.SFactor)
		if ok != nil {
			fmt.Println(ok)
			return nuclearFuncNormValue, ok
		}
		sum = sum + nuclearFuncNormValue[i]
	}
	for i := range nuclearFuncNormValue {
		nuclearFuncNormValue[i] = nuclearFuncNormValue[i] / sum
	}
	return nuclearFuncNormValue, ok
}

/*
findG вычисляет нормированные значения целевой функции.
Аргументы:
    fitnessTestPointValue - список значений целевой функции
    minFlag - флаг минимизации
Возвращаемые значения:
    список нормированных значений функции
 */
func findG(fitnessTestPointValue []float64, minFlag int) []float64 {
	maxFitTP, _ := support.Max(fitnessTestPointValue)
	minFitTP, _ := support.Min(fitnessTestPointValue)
	g := make([]float64, len(fitnessTestPointValue))

	if maxFitTP == minFitTP {
		for i := range g {
			g[i] = 1
		}
	} else {
		if minFlag == 1 {
			best := minFitTP
			worst := maxFitTP
			for i := range g {
				g[i] = (fitnessTestPointValue[i] - best) / (worst - best)
			}
		} else {
			best := maxFitTP
			worst := minFitTP
			for i := range g {
				g[i] = (best - fitnessTestPointValue[i]) / (best - worst)
			}
		}
	}
	return g
}

func findDelta(delta [][]float64, nuclearFuncNormValue []float64, options Options) [][]float64 {
	//newDeltaLen := make([][]float64, len(delta))
	newDelta := make([][]float64, len(delta))
	uNorm := make([]float64, len(delta))
	for j := range uNorm {
		uNorm[j] = 0
		for i := range nuclearFuncNormValue {
			u := rand.Float64() * 2 - 1 // ошибка, здесь должно быть усреднение координат
			uNorm[j] = uNorm[j] + math.Pow(math.Abs(u), options.Q) * nuclearFuncNormValue[i]
		}
	}
	for i := range newDelta {
		newDelta[i] = make([]float64, len(delta[i]))
		for j := range newDelta[i] {
			newDelta[i][j] = options.Gamma * delta[i][j] * math.Pow(uNorm[i], options.Q)
		}
	}
	return newDelta
}

/*
checkDelta проверяет выходят ли граници области delta за допустимую область поиска, если да, то устанавливает новые.
Аргументы:
    delta - список расстояний области поиска
    operationPoint - координаты рабочей точки
    function - структура тестовой функции
Возвращаемые значения:
    скорректированная delta
 */
func checkDelta(delta [][]float64, operationPoint []float64, function testfunc.TestFunction) [][]float64 {
	high := function.Up
	low := function.Down
	for i := range operationPoint {
		realLow := operationPoint[i] - delta[i][0]
		realHigh := operationPoint[i] + delta[i][1]
		if realLow < low[i] {
			delta[i][0] = operationPoint[i] - low[i]
		}
		if realHigh > high[i] {
			delta[i][1] = high[i] - operationPoint[i]
		}
	}
	return delta
}

/*
evaluateFunc вычисляет значения целевой функции.
Дополнительно накладывает аддитивную центрированную помеху (если kNoise > 0),
имеющую равномерный закон распределения.
Аргументы:
    testPoints - список координат пробных точек
    operationPoint - координаты рабочей точки
    function - структура тестовой функции
    kNoise - коэффициент шум/сингал
    np - количество пробных точек
Возвращаемые значения:
    значение целевой функции в рабочей точке
    список значений целевой функции в рабочих точках
    ошибка
 */
func evaluateFunc(testPoints [][][]float64, operatingPoint []float64, function testfunc.TestFunction, kNoise float64, np int) (float64, []float64, error) {
	//FIXME: убрать аргумент np int, его можно узнать по len(testPoints)
	var fitnessOperatingPointValue float64 = 0
	fitnessTestPointValue := make([]float64, np)
	var err error
	var funcAmplitude float64 = 0
	if kNoise > 0 {
		funcAmplitude = (rand.Float64() - 0.5) * (2 * function.AmplitudeNoise)
		funcAmplitude = funcAmplitude * kNoise
	} else {
		funcAmplitude = 0
	}
	fitnessOperatingPointValue, err = function.GetValue(operatingPoint)
	if err != nil {
		return fitnessOperatingPointValue, fitnessTestPointValue, err
	}
	fitnessOperatingPointValue = fitnessOperatingPointValue + funcAmplitude
	var idx int
	for j := range testPoints {
		for i := range testPoints[j] {
			fitnessTestPointValue[idx], _ = function.GetValue(testPoints[j][i])
			fitnessTestPointValue[idx] = fitnessTestPointValue[idx] + funcAmplitude
			idx = idx + 1
		}
	}

	//for i := range fitnessTestPointValue {
	//	fitnessTestPointValue[i], _ = function.GetValue(testPoints[i])
	//	fitnessTestPointValue[i] = fitnessTestPointValue[i] + funcAmplitude
	//}
	return fitnessOperatingPointValue, fitnessTestPointValue, err
}

/*
move рассчитывает новые координаты рабочей точки и новые границы поиска.
Аргументы:
    testPoints - список координат пробных точек
    operationPoint - координаты рабочей точки
    nuclearFuncNormValue - список нормированных значений ядерной функции
    delta - список расстояний области поиска
    options - структура настроек алгоритма
Возвращаемые значения:
    новые координаты рабочей точки
    новые границы delta
 */
func move(operatingPoint, nuclearFuncNormValue []float64, testPoints [][][]float64, delta [][]float64, options Options) ([]float64, [][]float64) {
	//N := options.NumberPoints
	dimension := len(operatingPoint)
	//u := make([][]float64, N)
	newDelta := make([][]float64, len(delta))
	newOperatingPoint := make([]float64, dimension)
	sumUP := make([][]float64, int(math.Pow(2, float64(dimension))))
	uNorm := make([]float64, dimension)

	var idx int
	u := make([][]float64, options.NumberPoints)

	for j := range testPoints { // по квадрантам
		//var idx int
		//u := make([][]float64, len(testPoints[j]))
		sumUP[j] = make([]float64, dimension)
		for i := range testPoints[j] { // по точкам в квадрнте
			u[idx] = make([]float64, dimension)
			for d := range testPoints[j][i] {
				if testPoints[j][i][d] < operatingPoint[d] {
					u[idx][d] = (testPoints[j][i][d] - operatingPoint[d]) / delta[d][0]
				} else {
					u[idx][d] = (testPoints[j][i][d] - operatingPoint[d]) / delta[d][1]
				}
				sumUP[j][d] = sumUP[j][d] + nuclearFuncNormValue[idx] * math.Pow(math.Abs(u[idx][d]), options.Q)
				uNorm[d] = uNorm[d] + nuclearFuncNormValue[idx] * u[idx][d]
			}
			idx = idx + 1
		}
	}
	indexes := make([]int, len(testPoints))
	for i := range testPoints {
		indexes[i] = i
	}
	idxBitStr := intsInBits(indexes, dimension)

	for d := range newOperatingPoint {
		newDelta[d] = make([]float64, len(delta[d]))
		if uNorm[d] >= 0 {
			newOperatingPoint[d] = operatingPoint[d] + delta[d][1] * uNorm[d]
		} else {
			newOperatingPoint[d] = operatingPoint[d] + delta[d][0] * uNorm[d]
		}
		for i := 0; i < 2; i++ {
			var s []string
			if i == 0 {
				s = getNumBitStr(idxBitStr, d, 1)
			} else {
				s = getNumBitStr(idxBitStr, d, 0)
			}
			idxs := bitStrArrayToIntArray(s)
			var sum float64
			for j := range idxs {
				sum = sum + sumUP[idxs[j]][d]
			}
			newDelta[d][i] = options.Gamma * delta[d][i] * math.Pow(sum, 1 / options.Q)
		}
	}
	return newOperatingPoint, newDelta
}
/*
func move(operatingPoint, nuclearFuncNormValue []float64, testPoints, delta [][]float64, options Options) ([]float64, [][]float64) {
	N := options.NumberPoints
	dimension := len(operatingPoint)
	u := make([][]float64, N)
	newDelta := make([][]float64, len(delta))
	newOperatingPoint := make([]float64, dimension)
	sumUP := make([]float64, dimension)
	uNorm := make([]float64, dimension)
	for i := range u {
		u[i] = make([]float64, dimension)
		for j := range u[i] {
			u[i][j] = (testPoints[i][j] - operatingPoint[j]) / (delta[j][0] + delta[j][1])
			sumUP[j] = sumUP[j] + nuclearFuncNormValue[i] * math.Pow(math.Abs(u[i][j]), options.Q)
			uNorm[j] = uNorm[j] + nuclearFuncNormValue[i] * u[i][j]
		}
	}
	for i := range newOperatingPoint {
		newDelta[i] = make([]float64, len(delta[i]))
		newOperatingPoint[i] = operatingPoint[i] + (delta[i][0] + delta[i][1]) * uNorm[i]
		newDelta[i][0] = options.Gamma * delta[i][0] * math.Pow(sumUP[i], 1 / options.Q)
	}
	return newOperatingPoint, newDelta
}*/

/*
findPNorm рассчитывает значение ядерной функции в рабочей точке.
Чисто для построения графика.
Аргументы:
    g - список значений ядерной функции
    fitTestPointValue - список значений целевой функции в пробных точках
    fitOperatingPointValue - значение целевой функции в рабочей точке
    options - структура настроек алгоритма
Возвращаемые значения:
    значение ядерной функции в рабочей точке
    ошибка
 */
func findPNorm(g []float64, fitTestPointValue []float64, fitOperatingPointValue float64, options Options) (float64, error) {
	nuclearFuncNormValue := make([]float64, len(g) + 1)
	maxFitTP, _ := support.Max(fitTestPointValue)
	minFitTP, _ := support.Min(fitTestPointValue)
	var ok error
	var sum float64 = 0
	var gInOpPoint float64
	if maxFitTP == minFitTP {
		gInOpPoint = 1
	} else {
		if options.MinFlag == 1 {
			best := minFitTP
			worst := maxFitTP
			gInOpPoint = (fitOperatingPointValue - best) / (worst - best)
		} else {
			best := maxFitTP
			worst := minFitTP
			gInOpPoint = (best - fitOperatingPointValue) / (best - worst)
		}
	}

	for i := range nuclearFuncNormValue {
		if i == 0 {
			nuclearFuncNormValue[i], ok = SAC.GetNuclearFunc(options.IndexNF, gInOpPoint, options.SFactor)
			if ok != nil {
				fmt.Println(ok)
				return -1, ok
			}
		} else {
			nuclearFuncNormValue[i], _ = SAC.GetNuclearFunc(options.IndexNF, g[i - 1], options.SFactor)
		}
		sum = sum + nuclearFuncNormValue[i]
	}
	for i := range nuclearFuncNormValue {
		nuclearFuncNormValue[i] = nuclearFuncNormValue[i] / sum
	}
	return nuclearFuncNormValue[0], ok
}

/*
NewSAC основаная процедура алгоритма.
Аргументы:
    function - структура тестовой функции
    options - структура настроек алгоритма
Возвращаемые значения:
    fBest - найденное значение целевой функции
    xBest - найденные координаты экстремума
    bestChart - список лучших значений функции (значений в рабочей точке) по итерациям
    meanChart - список средних значений целевой функции (в тестовых точках) по итерациям
    nuclearFunc - список значений ядерной функции в рабочей точке
    dispersion - дисперсия, по итерациям
    coordinates - список координат рабочей точки по итерациям
    numberMeasurements - количество измерений целевой функции
    stopIter - количество пройденных итераций
 */
func NewSAC(function testfunc.TestFunction, options Options) (fBest float64, xBest, bestChart, meanChart, nuclearFunc, dispersion []float64, coordinates [][]float64, numberMeasurements, stopIter int) {
	rand.Seed(time.Now().UTC().UnixNano())
	bestChart = make([]float64, options.MaxIterations)
	meanChart = make([]float64, options.MaxIterations)
	dispersion = make([]float64, options.MaxIterations)
	coordinates = make([][]float64, options.MaxIterations)
	xBest = make([]float64, function.Dimension)
	nuclearFunc = make([]float64, options.MaxIterations)
	g := make([]float64, options.NumberPoints)

	operatingPoint, delta := initializationOperatingPointAndDelta(function)

	numberMeasurements = 0
	var iteration int
	for i := 0; i < options.MaxIterations; i++ {
		iteration = i + 1

		testPoints := initializationTestPoints(function, options, delta, operatingPoint)
		fitnessOperatingPointValue, fitnessTestPointValue, ok := evaluateFunc(testPoints, operatingPoint, function, options.KNoise, options.NumberPoints)
		if ok != nil {
			fmt.Println(ok)
			return
		}

		numberMeasurements = numberMeasurements + len(fitnessTestPointValue) + 1

		fBest = fitnessOperatingPointValue
		copy(xBest, operatingPoint)
		bestChart[i] = fBest
		coordinates[i] = make([]float64, len(xBest))
		copy(coordinates[i], xBest)
		meanChart[i] = support.Mean(fitnessTestPointValue)

		dispersion[i] = 0
		for j := range delta {
			var sum float64
			for k := range delta[j] {
				sum += delta[j][k]
			}
			dispersion[i] += math.Pow(sum, 2)
		}
		dispersion[i] = math.Pow(dispersion[i], 0.5)

		if iteration > 2 {
			if ((delta[0][0] + delta[0][1]) < math.Pow(10, -5)) || ((delta[1][0] + delta[1][1]) < math.Pow(10, -5)) {
				stopIter = iteration
				break
			}
		}

		g = findG(fitnessTestPointValue, options.MinFlag)
		nuclearFuncValues := make([]float64, options.NumberPoints)
		nuclearFuncValues, ok = findNormNuclearFunc(g, options)
		if ok != nil {
			fmt.Println(ok)
			return
		}

		nuclearFunc[i], _ = findPNorm(g, fitnessTestPointValue, fitnessOperatingPointValue, options)

		operatingPoint, delta = move(operatingPoint, nuclearFuncValues, testPoints, delta, options)
		delta = checkDelta(delta, operatingPoint, function)
	}
	return
}

/*
RunSACAcsa - функция обертка для запуска алгоритма.
Аргументы:
    см. NewSAC
Возвращаемые значения:
    см. NewSAC
 */
func RunSACAcsa(function testfunc.TestFunction, options algorithms.OptionsAlgorithm) (float64, []float64, []float64, interface{}, [][]float64, int, int) {
	op := options.(*Options)
	fBest, xBest, bestChart, _, _, dispersion, coordinates, numberMeasurements, stopIteration := NewSAC(function, *op)
	return fBest, xBest, bestChart, dispersion, coordinates, numberMeasurements, stopIteration
}
