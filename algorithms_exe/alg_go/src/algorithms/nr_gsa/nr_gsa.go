package nr_gsa

import (
	"fmt"
	"os"
	"time"
	"math/rand"
	"math"
	"support"
	"sort"
	"testfunc"
	"algorithms/sac"
	"algorithms"
)

//Initialization - инициализации системы из N точек.
//Точки инициализируются случайным образом (по нормальному распределению) в области поиска.
func Initialization(function testfunc.TestFunction, options Options) [][]float64 {
	x := make([][]float64, options.StartNumberPoints)
	for j := range x {
		x[j] = make([]float64, function.Dimension)
		for i := 0; i < len(x[j]); i++ {
			x[j][i] = rand.Float64() * (function.Up[i] - function.Down[i]) +
				function.Down[i]
		}
	}
	return x
}

// GetEvaluateFunction - измерение значений целевой функции.
// Еси коэффициент помехи >= 0, то накладывается аддитивная равномерно распределенная помеха.
func GetEvaluateFunction(x [][]float64, function testfunc.TestFunction, kNoise float64) []float64 {
	var ok error
	f := make([]float64, len(x))
	for i := range x {
		f[i], ok = function.GetValue(x[i])
		if ok != nil {
			fmt.Println(ok)
			os.Exit(1)
		}
		if kNoise > 0 {
			f[i] = f[i] + (rand.Float64() - 0.5) * (function.AmplitudeNoise * 2 * kNoise)
		}
	}
	return f
}

// SpaceBound - функция проверки выхода точек за границы области поиска.
// Если точка выходит за границы, то она заного инициализируется случайным образом.
func SpaceBound(x [][]float64, function testfunc.TestFunction) [][]float64 {
	for i := range x {
		for j := range x[i] {
			highBorder := x[i][j] > function.Up[j]
			lowBorder := x[i][j] < function.Down[j]
			if highBorder || lowBorder {
				x[i][j] = rand.Float64() * (function.Up[j] - function.Down[j]) + function.Down[j]
			}
		}
	}
	return x
}

func massCalculationWithNuclearFunc(f []float64, options Options) []float64 {
	fitMin, _ := support.Min(f)
	fitMax, _ := support.Max(f)
	var best, worst float64
	var sumMass float64 = 0
	//var ok error
	mass := make([]float64, len(f))
	if fitMin == fitMax {
		for i := range mass {
			mass[i] = 1
		}
	} else {
		if options.MinFlag == 1 {
			best = fitMin
			worst = fitMax
		} else {
			best = fitMax
			worst = fitMin
		}
		for i := range mass {
			mass[i] = (f[i] - best) / (worst - best)
			//sumMass = sumMass + mass[i]
		}
	}
	for i := range mass {
		mass[i], _ = SAC.GetNuclearFunc(options.NfIdx, mass[i], options.SelectivityFactor)
		sumMass = sumMass + mass[i]
	}
	for i := range mass {
		mass[i] = mass[i] / sumMass
	}
	return mass
}

//TODO: добавить документацию
func accelerationCalculation (x [][]float64, mass []float64, g float64, t int, options Options) [][]float64 {
	var finalPer float64 = 2
	var kBest int
	var r float64
	eps := math.Nextafter(1.0,2.0)-1.0
	a := make([][]float64, options.StartNumberPoints)
	if options.ElitistCheck == 1 {
		var temp float64
		temp = float64(finalPer) + float64(1 - float64(t) / float64(options.MaxIterations)) * float64(100 - finalPer)
		temp = float64(options.StartNumberPoints) * temp / 100
		kBest = int(support.Round(temp))
	} else {
		kBest = options.StartNumberPoints
	}

	s := support.NewFloat64Slice(mass)
	sort.Sort(sort.Reverse(s))
	e := make([][]float64, options.StartNumberPoints)
	for i := range e {
		e[i] = make([]float64, len(x[i]))
		for ii := 0; ii < kBest; ii++ {
			j := s.Idx[ii]
			if j != i {
				r = support.Norm(x[i], x[j], options.RNorm)
				for k := 0; k < len(x[i]); k++ {
					e[i][k] = e[i][k] + rand.Float64() * mass[j] *
						((x[j][k] - x[i][k]) / (math.Pow(r, options.RPower) + eps))
				}
			}
		}
	}

	for i := range a {
		a[i] = make([]float64, len(x[0]))
		for j := range a[i] {
			a[i][j] = g * e[i][j]
		}
	}
	return a
}

//TODO: добавить документацию
func Move(x, a, v [][] float64) (xNew, vNew [][]float64) {
	vNew = make([][]float64, len(v))
	xNew = make([][]float64, len(x))
	for i := range vNew {
		vNew[i] = make([]float64, len(x[i]))
		xNew[i] = make([]float64, len(x[i]))
		for j := range vNew[i] {
			vNew[i][j] = v[i][j] * rand.Float64() + a[i][j]
			xNew[i][j] = x[i][j] + vNew[i][j]
		}
	}
	return
}

func getN(op Options, startNP, iteration int) int {
	var newN int = 0
	n, err := SAC.GetNuclearFunc(op.IdxLawChangeNP, float64(iteration) / float64(op.MaxIterations), op.Q)
	n = n * float64(startNP - op.EndNumberPoints) + float64(op.EndNumberPoints)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	newN = int(math.Floor(n))
	if newN <= op.StartNumberPoints {
		return newN
	} else {
		fmt.Println("закон изменения количества точек должен быть убывающим")
		os.Exit(1)
	}
	return newN
}


//TODO: добавить документацию
func NRGSA(function testfunc.TestFunction, options Options) (fBest float64, numberMeasurements int,
															 xBest, bestChart, meanChart, dispersion []float64, coordinates [][]float64, stopIteration int) {
	rand.Seed(time.Now().UTC().UnixNano())
	var x [][]float64
	var velocity, a [][]float64
	var fitness []float64
	var mass [] float64
	bestChart = make([]float64, options.MaxIterations)
	meanChart = make([]float64, options.MaxIterations)
	dispersion = make([]float64, options.MaxIterations)
	coordinates = make([][]float64, options.MaxIterations)

	var iteration int
	var best float64
	var bestX int
	//var N int
	//var numberMeasurements int
	numberMeasurements = 0

	startN := options.StartNumberPoints
	//N = startN

	x = Initialization(function, options)
	velocity = support.Zeros(len(x), len(x[0]))

	for i := 0; i < options.MaxIterations; i++ {
		iteration = i + 1

		x = SpaceBound(x, function)
		fitness = GetEvaluateFunction(x, function, options.KNoise)
		numberMeasurements = numberMeasurements + len(fitness)
		//fmt.Println(options.StartNumberPoints)

		if options.EndNumberPoints > 1 {
			newN := getN(options, startN, i)
			if newN < options.StartNumberPoints {
				delta := options.StartNumberPoints - newN
				//deleteX := make([]int, delta)
				for k := 0; k < delta; k++ {
					_, idxMax := support.Max(fitness)
					fitness = append(fitness[:idxMax], fitness[(idxMax + 1):]...)
					x = append(x[:idxMax], x[(idxMax + 1):]...)
					velocity = append(velocity[:idxMax], velocity[(idxMax + 1):]...)
				}
				//N = newN
				options.StartNumberPoints = newN
				//fmt.Println(iteration, " - ", len(x))
			}
		}
		//fmt.Println(options.StartNumberPoints)

		if options.MinFlag == 1 {
			best, bestX = support.Min(fitness)
		} else {
			best, bestX = support.Max(fitness)
		}
		//fBest = best
		//xBest = x[bestX]
		if iteration == 1 {
			fBest = best
			xBest = x[bestX]
		}
		if options.MinFlag == 1 {
			if best < fBest {
				fBest = best
				xBest = x[bestX]
			}
		} else {
			if best > fBest {
				fBest = best
				xBest = x[bestX]
			}
		}

		bestChart[i] = fBest
		coordinates[i] = make([]float64, len(xBest))
		copy(coordinates[i], xBest)
		//coordinates[i] = xBest
		meanChart[i] = support.Mean(fitness)
		if function.Dimension == 2 {
			dispersion[i], _ = support.Dispersion(x)
		} else {
			dispersion[i] = 0
		}

		mass = massCalculationWithNuclearFunc(fitness, options)
		g, err := GetG(iteration, options)
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		if g < math.Pow(10, -5) {
			fmt.Println(numberMeasurements)
			stopIteration = iteration
			fmt.Println(stopIteration)
			return
		}
		a = accelerationCalculation(x, mass, g, iteration, options) //
		//a = AccelerationCalculationWithGoroutine(x, mass, g, i, options) //
		x, velocity = Move(x, a, velocity)
	}
	fmt.Println(numberMeasurements)
	stopIteration = options.MaxIterations
	return
}

func RunNRGSA(function testfunc.TestFunction, options algorithms.OptionsAlgorithm) (float64, []float64, []float64, interface{}, [][]float64, int, int) {
	op := options.(*Options)
	fBest, numberMeasurements, xBest, bestChart, _, dispersion, coordinates, stopIteration:= NRGSA(function, *op)
	return fBest, xBest, bestChart, dispersion, coordinates, numberMeasurements, stopIteration
}