package testfunc

import (
	"fmt"
	"os"
	"encoding/json"
	"io/ioutil"
	"path"
	"errors"
	"math"
	"support"
	"strconv"
)

//type FeldbaumFunction struct {
//	Coordinates            [][]float64 `json:"coordinates"`
//	FuncValues             []float64   `json:"func_values"`
//	DegreeSmoothness       [][]float64 `json:"degree_smoothness"`
//	CoefficientsAbruptness [][]float64 `json:"coefficients_abruptness"`
//}
//
//type PotentialFunction struct {
//	Coordinates            [][]float64 `json:"coordinates"`
//	FuncValues             []float64   `json:"func_values"`
//	DegreeSmoothness       [][]float64 `json:"degree_smoothness"`
//	CoefficientsAbruptness []float64 `json:"coefficients_abruptness"`
//}

/*

 */
//TODO: добавить документацию
type TestFunction struct {
	testFunc               func([]float64) float64
	Index                  int           `json:"index"`
	Dimension              int           `json:"dimension"`
	NumExtrema             int           `json:"number_extrema"`
	Type                   string        `json:"type"`
	Coordinates            [][]float64   `json:"coordinates"`
	FuncValues             []float64     `json:"func_values"`
	DegreeSmoothness       [][]float64   `json:"degree_smoothness"`

	CoefficientsAbruptness []interface{} `json:"coefficients_abruptness"`

	Up             []float64 `json:"constraints_high"`
	Down           []float64 `json:"constraints_down"`
	AmplitudeNoise float64   `json:"amp_noise"`
	RealMin        []float64 `json:"real_extrema"`
	MinValue       float64   `json:"min_value"`
	MaxValue       float64   `json:"max_value"`
}

//TODO: добавить документацию
func (f *TestFunction) ConfigureTestFunction(idx int, pathDir, file string) error {
	var pattern = "func" + strconv.Itoa(idx) + ".json"
	//re := regexp.MustCompile(`(func)(\d+)(\.json)`)
	if file != "" {
		err := f.readFromJson(file)
		f.constructionTestFunc()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		return nil
	} else {
		if (pathDir != "") && (idx >= 0) {
			files, err := ioutil.ReadDir(pathDir)
			if err != nil {
				fmt.Println(err)
				os.Exit(1)
			}
			for _, file := range files {
				//fmt.Println(file.Name())
				//regexp.MatchString(re, file.Name())
				if file.Name() == pattern {
					err := f.readFromJson(path.Join(pathDir, file.Name()))
					f.constructionTestFunc()
					if err != nil {
						fmt.Println(err)
						os.Exit(1)
					}
					return nil
				}
			}
			fmt.Println("файл " + pattern + " не найден")
			os.Exit(1)
		} else {
			err := errors.New("не указан путь или некорректно передан индекс")
			fmt.Println(err)
			os.Exit(1)
			//return err
		}
	}
	return nil
}

//TODO: добавить документацию
func (f *TestFunction) readFromJson(file string) error {
	configFile, err := os.Open(file)
	if err != nil {
		fmt.Println(err.Error())
		return err
	}
	jsonParser := json.NewDecoder(configFile)
	err = jsonParser.Decode(&f)
	if err != nil {
		fmt.Println(err.Error())
		return err
	}
	configFile.Close()
	return nil
}

//TODO: добавить документацию
func (f *TestFunction) constructionTestFunc() {
	if f.Type == "feldbaum_function" {
		//f.CoefficientsAbruptness = f.CoefficientsAbruptness.([]float64)
		f.testFunc = ConstructFeldbaumFunction(*f)
	}
	if f.Type == "hyperbolic_potential_abs" {
		f.testFunc = ConstructHyperbolicPotentialAbs(*f)
	}
	if f.Type == "exponential_potential" {
		f.testFunc = ConstructExponentialPotential(*f)
	}
}

//GetValue - возвращает значение тестовой функции, если она сконструирована, иначе - ошибка.
func (f *TestFunction) GetValue (x []float64) (float64, error) {
	if f.testFunc == nil {
		return -1, errors.New("тестовая функция не была сконфигурирована")
	}
	return f.testFunc(x), nil
}

// ConstructFeldbaumFunction - конструктор многоэкстремальной тестовой функции Фельдбаума.
// Применяется метод минимума к степенным модульным функциям.
// Возвращает функцию замыкание (на данных из структуры TestFunction).
func ConstructFeldbaumFunction(f TestFunction) func([]float64) float64 {
	c, err := support.ToFloat64Slice2D(f.CoefficientsAbruptness)
	if err != nil {
		print(err)
	}
	tf := func(x []float64) float64 {
		valuesSubfunc := make([]float64, f.NumExtrema)
		for i := 0; i < len(valuesSubfunc); i++ {
			var value float64 = 0
			for j := range x {
				value = value + c[i][j] * math.Pow(math.Abs(x[j] - f.Coordinates[i][j]), f.DegreeSmoothness[i][j])
			}
			value = value + f.FuncValues[i]
			valuesSubfunc[i] = value
		}
		result, _ := support.Min(valuesSubfunc)
		return result
	}
	return tf
}

// ConstructHyperbolicPotentialAbs - конструктор многоэкстремальной тестовой функции гиперболического потенциала.
// Применяется суммирование к одноэктремальным простейшим гиперболическим потенциалам.
// Возвращает функцию замыкание (на данных из структуры TestFunction).
func ConstructHyperbolicPotentialAbs(f TestFunction) func([]float64) float64 {
	c, err := support.ToFloat64SliceOD(f.CoefficientsAbruptness)
	if err != nil {
		fmt.Println(err)
	}
	tf := func(x []float64) float64 {
		var value float64 = 0
		for i := 0; i < f.NumExtrema; i++ {
			var v float64 = 0
			for j := range x {
				v = v + math.Pow(math.Abs(x[j] - f.Coordinates[i][j]), f.DegreeSmoothness[i][j])
			}
			v = c[i] * v + f.FuncValues[i]
			v = -(1 / v)
			value = value + v
		}
		return value
	}
	return tf
}

// ConstructExponentialPotential - конструктор многоэкстремальной тестовой функции - экспоненциального потенциала.
// Применяется суммирование к одноэктремальным простейшим экспоненциальным потенциалам.
// Возвращает функцию замыкание (на данных из структуры TestFunction).
func ConstructExponentialPotential(f TestFunction) func([]float64) float64 {
	c, err := support.ToFloat64SliceOD(f.CoefficientsAbruptness)
	if err != nil {
		fmt.Println(err)
	}
	tf := func(x []float64) float64 {
		var value float64 = 0
		for i := 0; i < f.NumExtrema; i++ {
			var tmp float64 = 0
			for j := range x {
				tmp = tmp + math.Pow(math.Abs(x[j] - f.Coordinates[i][j]), f.DegreeSmoothness[i][j])
			}
			tmp = (-f.FuncValues[i]) * math.Exp((-c[i]) * tmp)
			value = value + tmp
		}
		return value
	}
	return tf
}

