package support

import (
	"fmt"
	"reflect"
	"math"
	"sort"
	"errors"
)

//Min - функция поиска минимума в одномерном слайсе, состоящем из float64.
//Возвращает значение минимального элемента и его индекс в слайсе.
//Min([]float64{4, 3, 1, 5, 8}) -> (1, 2)
func Min(x []float64) (float64, int) {
	var m float64
	var idx int
	if len(x) > 0 {
		m = x[0]
		idx = 0
	}
	for i, e := range x {
		if e < m {
			m = e
			idx = i
		}
	}
	return m, idx
}

//Max - функция поиска максимума в одномерном слайсе, состоящем из float64.
//Возвращает значение максимального элемента и его индекс в слайсе.
//Max([]float64{4, 3, 1, 5, 8}) -> (8, 4)
func Max(x []float64) (float64, int) {
	var m float64
	var idx int
	if len(x) > 0 {
		m = x[0]
		idx = 0
	}
	for i, e := range x {
		if e > m {
			m = e
			idx = i
		}
	}
	return m, idx
}

//ToFloat64SliceOD - to float64 slice one dimension.
//Преобразование одномерного слайса интерфейсов в одномерный слайс float64.
func ToFloat64SliceOD(x []interface{}) ([]float64, error) {
	if x == nil {
		return []float64{}, fmt.Errorf("не удаось преобразовать %#v типа %T в []float64", x, x)
	}
	var res []float64
	res = make([]float64, len(x))

	for i, n := range x {
		kind := reflect.TypeOf(n).Kind()
		switch kind {
		case reflect.Int, reflect.Float32, reflect.Float64:
			res[i] = reflect.ValueOf(n).Float()
		default:
			return []float64{}, fmt.Errorf("не удаось преобразовать %#v типа %T в []float64", x, x)
		}
	}
	return res, nil
}

//ToFloat64Slice2D конвертирует слайс интерфейсов в двумерный слайс.
func ToFloat64Slice2D(x []interface{}) ([][]float64, error) {
	if x == nil {
		return [][]float64{}, fmt.Errorf("не удаось преобразовать %#v типа %T в []float64", x, x)
	}
	var res [][]float64
	res = make([][]float64, len(x))

	for i, n := range x {
		kind := reflect.TypeOf(n).Kind() // тип как число (индекс в списке типов ???)
		switch kind {
		case reflect.Slice, reflect.Array:
			subarray := reflect.ValueOf(n)
			res[i] = make([]float64, subarray.Len())
			for j := 0; j < subarray.Len(); j++ {
				res[i][j] = subarray.Index(j).Interface().(float64)
			}
		default:
			return [][]float64{}, fmt.Errorf("не удаось преобразовать %#v типа %T в [][]float64", x, x)
		}

	}
	return res, nil
}

// Sum - возвращает сумму элементов одномерного слайса.
func Sum(f []float64) float64 {
	var sum float64 = 0
	for i := range f {
		sum = sum + f[i]
	}
	return sum
}

// Mean - возвращает среднее арифметическое одномерного слайса.
func Mean(f []float64) float64 {
	s := Sum(f)
	return s / float64(len(f))
}

// Zeros - создает двумерный слайс заданных размеров.
// Заполняет элементы нулями.
func Zeros(x, y int) [][]float64 {
	//var x [][]float64
	v := make([][]float64, x)
	for i := 0; i < x; i++ {
		v[i] = make([]float64, y)
	}
	return v
}

/*
Norm - вычисляет метрики линейного пространста для точек x и y. (Гёльдеровы нормы n-мерных векторов)
При rNorm = 1: будет вычислена метрика L1, норма l1 или манхэттенское расстояние.
При rNorm = 2: будет вычислена метрика L2, норма l2 или евклидова норма.
(геометрическое расстояние между двумя точками, вычисляемое по теореме пифагора)
Подробнее: https://en.wikipedia.org/wiki/Norm_(mathematics)
*/
func Norm(x, y []float64, rNorm int) float64 {
	var r float64
	var sum float64 = 0
	z := make([]float64, len(x))
	for i := range z {
		z[i] = math.Abs(x[i] - y[i])
	}
	for i := range z {
		sum = sum + math.Pow(z[i], float64(rNorm))
	}
	r = math.Pow(sum, float64(1 / float64(rNorm)))
	return r
}

type Slice struct {
	sort.Interface
	Idx []int
}

func (s Slice) Swap (i, j int) {
	s.Interface.Swap(i, j)
	s.Idx[i], s.Idx[j] = s.Idx[j], s.Idx[i]
}

func NewSlice(n sort.Interface) *Slice {
	s := &Slice{Interface: n, Idx: make([]int, n.Len())}
	for i := range s.Idx {
		s.Idx[i] = i
	}
	return s
}

func NewIntSlice(n ...int) *Slice         { return NewSlice(sort.IntSlice(n)) }
//func NewFloat64Slice(n ...float64) *Slice { return NewSlice(sort.Float64Slice(n)) }
func NewStringSlice(n ...string) *Slice   { return NewSlice(sort.StringSlice(n)) }

func NewFloat64Slice(n []float64) *Slice { return NewSlice(sort.Float64Slice(n)) }

func Dispersion(x [][]float64) (float64, error) {
	var sum  = make([]float64, len(x[0]))
	if len(sum) != 2 {
		err := errors.New("принимается только двумерные координаты")
		return -1, err
	}
	var sumSqr = make([]float64, len(x[0]))
	var dispY = make([]float64, len(x[0]))
	var dispersion float64
	for i := range sum {
		sum[i] = 0
		sumSqr[i] = 0
	}
	for i := range x {
		for j := range x[i] {
			sum[j] = sum[j] + x[i][j]
			sumSqr[j] = sumSqr[j] + math.Pow(x[i][j], 2)
		}
	}
	n := len(x)
	dispersion = 0

	for i := range dispY {
		dispY[i] = (sumSqr[i] - math.Pow(sum[i], 2) / float64(n)) / float64(n - 1)
		dispersion = dispersion + math.Pow(dispY[i], 2)
	}
	dispersion = math.Pow(dispersion, 0.5)
	return dispersion, nil
}

//Round - округление до ближайшего целого.
func Round(x float64) float64 {
	const (
		mask     = 0x7FF
		shift    = 64 - 11 - 1
		bias     = 1023

		signMask = 1 << 63
		fracMask = (1 << shift) - 1
		halfMask = 1 << (shift - 1)
		one      = bias << shift
	)

	bits := math.Float64bits(x)
	e := uint(bits>>shift) & mask
	switch {
	case e < bias:
		// Round abs(x)<1 including denormals.
		bits &= signMask // +-0
		if e == bias-1 {
			bits |= one // +-1
		}
	case e < bias+shift:
		// Round any abs(x)>=1 containing a fractional component [0,1).
		e -= bias
		bits += halfMask >> e
		bits &^= fracMask >> e
	}
	return math.Float64frombits(bits)
}