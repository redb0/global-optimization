package GSA

import (
	"os"
	"fmt"
	"encoding/json"
)

/*
Options - структура для хранения настроек алгоритма.
Поля:
    MaxIterations : максимальное число итераций.
    NumberPoints  : количество точек.
    IndexG        : индекс функции изменения гравитационной постоянной, функции определены в файле gFunc.go.
    G0            : начальное значение гравитационной постоянной.
    Alpha         : коэффициент альфа, используется в функции гравитационной постоянной.
    MinFlag       : флаг минимизации, 1 - минимизация, 0 - максимизация.
    RNorm         : норма для вычисления расстояния между точками, лучше использовать значение = 2.
    RPower        : степень влияния расстояния на силу гравитационного
					взаимодействия, испольуется в функции расчета ускорения.
    ElitistCheck  : использование элитных зондов, 1 - использование, 0 - нет
    Gamma         : коэффициент гамма, используется в функции изменения гравитационной постоянной.
    Epsilon       : размер эпсилон окрестности
	NumberRuns    : количество пусков
*/
type Options struct {
	MaxIterations int     `json:"MI"`
	NumberPoints  int     `json:"NP"`
	IndexG        int     `json:"IG"`
	G0            float64 `json:"G0"`
	Alpha         float64 `json:"AG"`
	MinFlag       int     `json:"min_flag"`
	RNorm         int     `json:"RN"`
	RPower        float64 `json:"RP"`
	ElitistCheck  int     `json:"EC"`
	Gamma         float64 `json:"GA"`
	KNoise        float64 `json:"KN"`

	Epsilon       []float64 `json:"epsilon"`
	NumberRuns    int     `json:"number_runs"`
}

//LoadConfiguration загружает конфигурацию алгоритма из json-файла.
func (op *Options) LoadConfiguration(file string)  {
	//var config SAC.Options
	configFile, err := os.Open(file)
	if err != nil {
		fmt.Println(err.Error())
	}
	jsonParser := json.NewDecoder(configFile)
	jsonParser.Decode(&op)
	configFile.Close()
}

// SetOptions - конструктор структуры Options.
func (op *Options) SetOptions(maxIterations, numberPoints, indexG int,
	g0, alpha, kNoise float64, minFlag, rNorm int, rPower float64,
	elitistCheck int, gamma float64) {
	op.MaxIterations = maxIterations
	op.NumberPoints = numberPoints
	op.IndexG = indexG
	op.G0 = g0
	op.Alpha = alpha
	op.MinFlag       = minFlag
	op.RNorm = rNorm
	op.RPower = rPower
	op.ElitistCheck = elitistCheck
	op.Gamma = gamma
	op.KNoise = kNoise
}
