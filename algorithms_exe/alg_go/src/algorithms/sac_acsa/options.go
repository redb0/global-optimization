package sac_acsa

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
    IndexNF       : индекс ядерной функции.
    SFactor       : коэффициент селективности
	Q             : q
	MinFlag       : флаг минимизации, 1 - минимизации, 0 - максимизация
	Gamma         : gamma, коэффициент определяющий скорость сжатия/расширения области поиска
	KNoise        : коэффициент шум/сигнал
	Epsilon       : размер эпсилон окрестности
	NumberRuns    : количество пусков
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

//LoadConfiguration загружает конфигурацию настроек алгоритма из json-файла.
//Аргументы:
//    file - путь до файла с конфигурацией
//Возвращаемые значения:
//    нет
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
