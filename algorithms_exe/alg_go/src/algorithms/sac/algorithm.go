package SAC

import (
	"math/rand"
	"fmt"
	"support"
	"math"
	"time"
	"testfunc"
	"algorithms"
)

func initializationOperatingPointAndDelta(function testfunc.TestFunction) ([]float64, [][]float64) {
	operatingPoint := make([]float64, function.Dimension)
	delta := make([][]float64, function.Dimension)
	low := function.Down
	high := function.Up
	for i := range operatingPoint {
		delta[i] = make([]float64, 2)
		operatingPoint[i] = 0
		//operatingPoint[i] = rand.Float64() * (high[i] - low[i]) + low[i]
		delta[i][0] = operatingPoint[i] - low[i]
		delta[i][1] = high[i] - operatingPoint[i]
	}
	return operatingPoint, delta
}

// Производит "разброс" тестовых точек в области вокруг рабочей точки.
// Примает:
//    function testFunctions.TestFunction - хранит размерность задачи оптимизации
//    options Options - хранит количество пробных точек
//    delta [][]float64 - двумерный массив ограничений сужаемой области
func initializationTestPoints(function testfunc.TestFunction, options Options, delta [][]float64, operationPoint []float64) [][]float64 {
	testPoints := make([][]float64, options.NumberPoints)
	for i := range testPoints {
		testPoints[i] = make([]float64, function.Dimension)
		for j := 0; j < len(testPoints[i]); j++ {
			low := operationPoint[j] - delta[j][0]
			high := operationPoint[j] + delta[j][1]
			testPoints[i][j] = rand.Float64() * (high - low) + low
		}
	}
	return testPoints
}

func findNormNuclearFunc(g []float64, options Options) ([]float64, error) {
	nuclearFuncNormValue := make([]float64, len(g))
	var ok error
	var sum float64 = 0
	for i := range nuclearFuncNormValue {
		nuclearFuncNormValue[i], ok = GetNuclearFunc(options.IndexNF, g[i], options.SFactor)
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
 * Расчет усредненного значения функции
 */
func findG(testPoints [][]float64, fitnessTestPointValue []float64, minFlag int) []float64 {
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

func evaluateFunc(testPoints [][]float64, operatingPoint []float64, function testfunc.TestFunction, kNoise float64) (float64, []float64, error) {
	var fitnessOperatingPointValue float64 = 0
	fitnessTestPointValue := make([]float64, len(testPoints))
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
	for i := range fitnessTestPointValue {
		fitnessTestPointValue[i], _ = function.GetValue(testPoints[i])
		fitnessTestPointValue[i] = fitnessTestPointValue[i] + funcAmplitude
	}
	return fitnessOperatingPointValue, fitnessTestPointValue, err
}

func moveCorrect(operatingPoint, nuclearFuncNormValue []float64, testPoints, delta [][]float64, options Options) ([]float64, [][]float64) {
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
			//u[i][j] = testPoints[i][j] - operatingPoint[j]
			sumUP[j] = sumUP[j] + nuclearFuncNormValue[i] * math.Pow(math.Abs(u[i][j]), options.Q)
			//sumUP[j] = sumUP[j] + nuclearFuncNormValue[i] * math.Pow(math.Abs((rand.Float64() - 0.5) * 2), options.q)
			uNorm[j] = uNorm[j] + nuclearFuncNormValue[i] * u[i][j]
		}
	}
	for i := range newOperatingPoint {
		newDelta[i] = make([]float64, len(delta[i]))
		newOperatingPoint[i] = operatingPoint[i] + (delta[i][0] + delta[i][1]) * uNorm[i]
		newDelta[i][0] = options.Gamma * delta[i][0] * math.Pow(sumUP[i], 1 / options.Q)
		newDelta[i][1] = options.Gamma * delta[i][1] * math.Pow(sumUP[i], 1 / options.Q)
	}
	//fmt.Println("дельта SAC ", newDelta)
	//fmt.Println("новая точка SAC ", newOperatingPoint)
	return newOperatingPoint, newDelta
}

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
}

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
			nuclearFuncNormValue[i], ok = GetNuclearFunc(options.IndexNF, gInOpPoint, options.SFactor)
			if ok != nil {
				fmt.Println(ok)
				return -1, ok
			}
		} else {
			nuclearFuncNormValue[i], _ = GetNuclearFunc(options.IndexNF, g[i - 1], options.SFactor)
		}
		sum = sum + nuclearFuncNormValue[i]
	}
	for i := range nuclearFuncNormValue {
		nuclearFuncNormValue[i] = nuclearFuncNormValue[i] / sum
	}
	return nuclearFuncNormValue[0], ok
}

func SAC(function testfunc.TestFunction, options Options) (fBest float64, xBest, bestChart, meanChart, nuclearFunc []float64, dispersion, coordinates [][]float64, numberMeasurements, stopIter int) {
	rand.Seed(time.Now().UTC().UnixNano())
	bestChart = make([]float64, options.MaxIterations)
	meanChart = make([]float64, options.MaxIterations)
	dispersion = make([][]float64, options.MaxIterations)
	coordinates = make([][]float64, options.MaxIterations)
	//coord = make([][]float64, options.MaxIterations)
	xBest = make([]float64, function.Dimension)
	nuclearFunc = make([]float64, options.MaxIterations)
	g := make([]float64, options.NumberPoints)

	operatingPoint, delta := initializationOperatingPointAndDelta(function)

	numberMeasurements = 0
	var iteration int
	for i := 0; i < options.MaxIterations; i++ {
		iteration = i + 1
		//fmt.Println("Итерация № ", iteration)

		testPoints := initializationTestPoints(function, options, delta, operatingPoint)
		fitnessOperatingPointValue, fitnessTestPointValue, ok := evaluateFunc(testPoints, operatingPoint, function, options.KNoise)
		if ok != nil {
			fmt.Println(ok)
			return
		}

		numberMeasurements = numberMeasurements + len(fitnessTestPointValue) + 1

		fBest = fitnessOperatingPointValue
		coordinates[i] = make([]float64, len(xBest))
		copy(coordinates[i], operatingPoint)
		copy(xBest, operatingPoint)
		bestChart[i] = fBest
		meanChart[i] = support.Mean(fitnessTestPointValue)

		//fmt.Println(fBest)
		//fmt.Println(xBest)

		dispersion[i] = make([]float64, function.Dimension)
		for j := range dispersion[i] {
			dispersion[i][j] = support.Sum(delta[j])
		}

		if iteration > 2 {
			if ((delta[0][0] + delta[0][1]) < math.Pow(10, -5)) || ((delta[1][0] + delta[1][1]) < math.Pow(10, -5)) {
				stopIter = iteration
				break
			}
			//if math.Abs(bestChart[i - 1] - bestChart[i]) < math.Pow(10, -6) {
			//	stopIter = iteration
			//	break
			//}
		}

		g = findG(testPoints, fitnessTestPointValue, options.MinFlag)
		nuclearFuncValues := make([]float64, options.NumberPoints)
		nuclearFuncValues, ok = findNormNuclearFunc(g, options)
		if ok != nil {
			fmt.Println(ok)
			return
		}

		nuclearFunc[i], _ = findPNorm(g, fitnessTestPointValue, fitnessOperatingPointValue, options)

		//operatingPoint, delta = move(operatingPoint, nuclearFuncValues, testPoints, delta, options)
		operatingPoint, delta = moveCorrect(operatingPoint, nuclearFuncValues, testPoints, delta, options)
		delta = checkDelta(delta, operatingPoint, function)
	}
	return
}

func RunSAC(function testfunc.TestFunction, options algorithms.OptionsAlgorithm) (float64, []float64, []float64, interface{}, [][]float64, int, int) {
	op := options.(*Options)
	fBest, xBest, bestChart, _, _, dispersion, coordinates, numberMeasurements, stopIteration := SAC(function, *op)
	return fBest, xBest, bestChart, dispersion, coordinates, numberMeasurements, stopIteration
}
