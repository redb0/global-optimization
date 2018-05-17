package GSA

import (
	"math/rand"
	"fmt"
	"os"
	"support"
	"sort"
	"math"
	"sync"
	"time"
	"testfunc"
	"algorithms"
)

//Initialization - инициализации системы из N точек.
//Точки инициализируются случайным образом (по нормальному распределению) в области поиска.
func Initialization(function testfunc.TestFunction, options Options) [][]float64 {
	x := make([][]float64, options.NumberPoints)
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

// MassCalculation - функция рассчета масс (весов) точек.
// веса нормированы на отрезке [0, 1]
func MassCalculation(f []float64, options Options) []float64 {
	fitMin, _ := support.Min(f)
	fitMax, _ := support.Max(f)
	var best, worst float64
	var sumMass float64 = 0
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
			mass[i] = (f[i] - worst) / (best - worst)
			sumMass = sumMass + mass[i]
		}
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
	a := make([][]float64, options.NumberPoints)
	if options.ElitistCheck == 1 {
		var temp float64
		temp = finalPer + float64(1 - float64(t) / float64(options.MaxIterations)) * float64(100 - finalPer)
		temp = float64(options.NumberPoints) * temp / 100
		kBest = int(temp)
	} else {
		kBest = options.NumberPoints
	}

	s := support.NewFloat64Slice(mass)
	sort.Sort(sort.Reverse(s))
	//var e [][]float64
	e := make([][]float64, options.NumberPoints)
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

//функция расчета ускорения с использованием го-рутин
func AccelerationCalculationWithGoroutine(x [][]float64, mass []float64, g float64, t int, options Options) [][]float64 {
	var wg sync.WaitGroup // для гарантии завершения всех горутин
	var finalPer float64 = 2
	var kBest int
	//var r float64
	eps := math.Nextafter(1.0,2.0)-1.0
	a := make([][]float64, options.NumberPoints)
	if options.ElitistCheck == 1 {
		temp := finalPer + float64(1 - t / options.MaxIterations) * (100 - finalPer)
		temp = float64(options.NumberPoints) * temp / 100
		kBest = int(temp)
	} else {
		kBest = options.NumberPoints
	}

	s := support.NewFloat64Slice(mass)
	sort.Sort(sort.Reverse(s))
	e := support.Zeros(options.NumberPoints, len(x[0]))

	//pool := workerPool.NewPool(8, kBest*len(e))
	//var force Force

	wg.Add(kBest*len(e)) // ожидается запуск kBest*len(e) горутин
	for i := range e {
		for ii := 0; ii < kBest; ii++ {
			j := s.Idx[ii]
			//pool.Calc(force.calc(i, j, options.rNorm, x, e, mass, eps, options.rPower))
			go go1(i, j, options.RNorm, x, e, mass, eps, options.RPower, &wg)
		}
	}
	wg.Wait()

	//pool.Close()
	//pool.Wait()

	for i := range a {
		a[i] = make([]float64, len(x[0]))
		for j := range a[i] {
			a[i][j] = g * e[i][j]
		}
	}
	return a
}

//TODO: добавить документацию
func go1(i, j, rNorm int, x, e [][]float64, mass []float64, eps, rPower float64, wg *sync.WaitGroup) {
	if j != i {
		r := support.Norm(x[i], x[j], rNorm)
		for k := 0; k < len(x[i]); k++ { //создание двух го-рутин
			//go go2(i, k, j, x, e, mass, eps, rPower, r)
			e[i][k] = e[i][k] + rand.Float64() * mass[j] *
				((x[j][k] - x[i][k]) / (math.Pow(r, rPower) + eps))
		}
	}
	wg.Done()
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

//TODO: добавить документацию
func GSA(function testfunc.TestFunction, options Options) (fBest float64, xBest, bestChart, meanChart, dispersion []float64, coordinates [][]float64, numberMeasurements int, stopIteration int) {
	rand.Seed(time.Now().UTC().UnixNano())
	//op := options.(Options)

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
	numberMeasurements = 0

	x = Initialization(function, options)
	velocity = support.Zeros(len(x), len(x[0]))

	for i := 0; i < options.MaxIterations; i++ {
		iteration = i + 1

		x = SpaceBound(x, function)
		fitness = GetEvaluateFunction(x, function, options.KNoise)
		numberMeasurements = numberMeasurements + len(fitness)

		if options.MinFlag == 1 {
			best, bestX = support.Min(fitness)
		} else {
			best, bestX = support.Max(fitness)
		}
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

		mass = MassCalculation(fitness, options)
		g, err := GetG(i, options)
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		if g < math.Pow(10, -5) {
			stopIteration = iteration
			return
		}
		a = accelerationCalculation(x, mass, g, i, options) //
		//a = AccelerationCalculationWithGoroutine(x, mass, g, i, options) //
		x, velocity = Move(x, a, velocity)
	}
	stopIteration = options.MaxIterations
	return
}

func RunGSA(function testfunc.TestFunction, options algorithms.OptionsAlgorithm) (float64, []float64, []float64, interface{}, [][]float64, int, int) {
	op := options.(*Options)
	fBest, xBest, bestChart, _, dispersion, coordinates, numberMeasurements, stopIteration := GSA(function, *op)
	return fBest, xBest, bestChart, dispersion, coordinates, numberMeasurements, stopIteration
}