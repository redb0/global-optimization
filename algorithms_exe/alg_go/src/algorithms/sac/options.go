package SAC

import (
	"os"
	"fmt"
	"encoding/json"
)

/*
TODO: переделать документацию
	Options - структура для хранения настроек алгоритма.
  	Она включает:
		MaxIterations int     : максимальное число итераций.
		NumberPoints  int     : количество точек.
		indexG        int     : индекс функции изменения гравитационной постоянной,
								функции определены в файле gFunc.go.
		g0            float64 : начальное значение гравитационной постоянной.
		alpha         float64 : коэффициент альфа,
								используется в функции гравитационной постоянной.
		MinFlag       int     : флаг минимизации, 1 - минимизация, 0 - максимизация.
		gamma         float64 : коэффициент гамма, используется в функции
								изменения гравитационной постоянной.
*/
type Options struct {
	MaxIterations int     `json:"MI"`
	NumberPoints  int     `json:"NP"`
	IndexNF       int     `json:"NF"`
	SFactor       float64 `json:"SF"`
	Q             float64 `json:"KQ"`
	MinFlag       int     `json:"min_flag"`
	Gamma         float64 `json:"GA"` //gamma
	KNoise        float64 `json:"KN"`

	Epsilon       []float64 `json:"epsilon"`
	NumberRuns    int     `json:"number_runs"`
}

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
func (op *Options) SetOptions(maxIterations, numberPoints, indexNF int,
	sFactor, q, kNoise float64, minFlag int, gamma float64) {
	op.MaxIterations = maxIterations
	op.NumberPoints = numberPoints
	op.IndexNF = indexNF
	op.SFactor = sFactor
	op.Q = q
	op.MinFlag = minFlag
	op.Gamma = gamma
	op.KNoise = kNoise
}
