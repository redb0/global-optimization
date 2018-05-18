package main

import (
	"os"
	"fmt"
	"encoding/json"
	"testfunc"
	"algorithms"
	"algorithms/nr_gsa"
	"algorithms/sac"
	"algorithms/gsa"
	"algorithms/sac_acsa"
	"time"
)

//Result - структура для хранения данных, которые необходимо записать в json.
type Result struct {
	FBest float64   `json:"f_best"`
	XBest []float64 `json:"x_best"`
	BestChart []float64 `json:"best_chart"`
	Coordinates [][]float64 `json:"coordinates"`
	Dispersion interface{} `json:"dispersion"`
	NumberMeasurements int `json:"number_measurements"`
	StopIteration int `json:"stop_iteration"`
	RunTime float64 `json:"run_time"`
}

type RunGroup struct {
	Probability float64 `json:"probability"`
	Runs []Result       `json:"runs"`
}

//writeInFile запись результата работы алгоритма в json файл.
func writeInFile(fileName string, data RunGroup) {
	file, err := os.OpenFile(fileName, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
		fmt.Println("ошибка")
	}

	defer file.Close() //закрыть файл в конце выполнения функции

	inFile, err := json.Marshal(data)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
		fmt.Println("ошибка")
	}
	file.Write(inFile)
}

type runAlgFunc func(testfunc.TestFunction, algorithms.OptionsAlgorithm) (float64, []float64, []float64, interface{}, [][]float64, int, int)

func main() {
/*
	//замер времени выполнения для тестирования с горутинами и без
	//без горутин 4,4 секунды
	//с горутинами 9,7 секунд
	t := testfunc.TestFunction{}
	//t.ConfigureTestFunction(0, "", "C:\\go_projects\\StandardGSA\\src\\func1.json")
	t.ConfigureTestFunction(1, "C:\\go_projects\\StandardGSA\\src", "")

	//var options GSA.Options
	//options.SetOptions(500, 200, 1, 100, 20, 0,
	//	1, 1, 1, 1, 1)

	//epsilon := []float64{0.5, 0.5}
	//var res Result
	runs := 1
	fmt.Println("Начало прогонов")
	start := time.Now()
	//for i := 0; i < runs; i++ {
	//	//_, _, _, _, _ = GSA.GSA(t, options, 0)
	//	res.FBest, res.XBest, res.BestChart, res.Dispersion, res.NumberMeasurements, res.StopIteration = GSA.RunGSA(t, &options, options.KNoise)
	//	fmt.Println(res)
	//}
	//p := findProbability(t, GSA.RunGSA, &options, 1, epsilon)
	//fmt.Println(p)
	options := nr_gsa.Options{}
	//options.LoadConfiguration(configFile)
	options.SetOptions(500, 50, 1, 1, 100, 20, 0, 1, 2, 1, 0, 1, 5, 2, 4, 1)
	//res.FBest, res.XBest, res.BestChart, res.Dispersion, res.NumberMeasurements, res.StopIteration = nr_gsa.RunNRGSA(t, &options)
	//res = findProbability(t, nr_gsa.RunNRGSA, &options, options.NumberRuns, options.MinFlag, options.Epsilon)
	nr_gsa.NRGSA(t, options)
	end := time.Now()
	runtime := float64(end.Sub(start).Seconds())
	fmt.Println(fmt.Sprintf("Время выполнения %[1]d прогонов: %[2]f секунд", runs, runtime))
	fmt.Println(fmt.Sprintf("Среднее время выполнения: %[1]f секунд", runtime / float64(runs)))*/

	var configFile string
	var outputName string
	var testFuncFile string
	var algorithm string
	algorithm = os.Args[1]
	configFile = os.Args[2]   // пусть к файлу с параметрами алгоритма
	testFuncFile = os.Args[3] // путь к файлу с тестовой функцией
	outputName = os.Args[4]   // пусть к файлу с результатами

	t := testfunc.TestFunction{}
	t.ConfigureTestFunction(0, "", testFuncFile)
	var res RunGroup

	switch algorithm {
	case "StandardSAC" :
		options := SAC.Options{}
		options.LoadConfiguration(configFile)
		res = findProbability(t, SAC.RunSAC, &options, options.NumberRuns, options.MinFlag, options.Epsilon)

	case "StandardGSA" :
		options := GSA.Options{}
		options.LoadConfiguration(configFile)
		res = findProbability(t, GSA.RunGSA, &options, options.NumberRuns, options.MinFlag, options.Epsilon)

	case "NoiseResistanceGSA" :
		options := nr_gsa.Options{}
		options.LoadConfiguration(configFile)
		res = findProbability(t, nr_gsa.RunNRGSA, &options, options.NumberRuns, options.MinFlag, options.Epsilon)

	case "SAC-ACSA" :
		options := sac_acsa.Options{}
		options.LoadConfiguration(configFile)
		res = findProbability(t, sac_acsa.RunSACAcsa, &options, options.NumberRuns, options.MinFlag, options.Epsilon)
	}

	writeInFile(outputName, res)
}

func findProbability(tf testfunc.TestFunction, function runAlgFunc, options algorithms.OptionsAlgorithm, numberRuns, minFlag int, epsilon []float64) RunGroup {
	var res RunGroup
	res.Runs = make([]Result, numberRuns)
	var realExtrema []float64

	if minFlag == 1 {
		realExtrema = tf.RealMin
	} else {
		//заменить на realMax
		realExtrema = tf.RealMax
	}

	for i := 0; i < numberRuns; i++ {
		var run Result
		start := time.Now()
		run.FBest, run.XBest, run.BestChart, run.Dispersion, run.Coordinates, run.NumberMeasurements, run.StopIteration  = function(tf, options)
		end := time.Now()
		run.RunTime = float64(end.Sub(start).Seconds())
		res.Runs[i] = run
		for i := range run.XBest {
			flag := inInterval(run.XBest[i], realExtrema[i], epsilon[i])
			if !flag {
				break
			}
			if i == len(run.XBest) - 1 && flag {
				res.Probability++
			}
		}
	}

	res.Probability = float64(res.Probability) / float64(numberRuns)
	fmt.Println(res.Probability)

	return res
}

func inInterval(x, y, epsilon float64) bool {
	if !(x >= y - epsilon) || !(x <= y + epsilon) {
		return false
	}
	return true
}

func inEpsilon(x, y, epsilon []float64) bool {
	for i := range x {
		if !(x[i] >= y[i] - epsilon[i]) || !(x[i] <= y[i] + epsilon[i]) {
			return false
		}
	}
	return true
}

func inFloatEpsilon(x, y []float64, epsilon float64) bool {
	for i := range x {
		if !(x[i] >= y[i] - epsilon) || !(x[i] <= y[i] + epsilon) {
			return false
		}
	}
	return true
}
