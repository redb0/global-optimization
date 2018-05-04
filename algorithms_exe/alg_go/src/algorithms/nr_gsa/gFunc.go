package nr_gsa

import (
	"math"
	"errors"
)

/*
GetG - вычисляет новое значение гравитационной постоянной.
Возможные функции:
1 - G0 * exp(-a*t/T)     - экспоненциальная функция
2 - G0 * (1 - (t/T)^2)^a - квадратичная функция
3 - G0 * (1 - (t/T)^3)^a - кубическая функция
4 - G0 / (1 + t)         - линейная
5 - G0 / (exp(a*t))      -
6 - G0 / (a+t^gamma)     -
Принимает: индекс закона изменения гравитационной постоянной, параметры алгоритма.
Возвращает: значение гравитационной постоянной, ошибку.
 */
func GetG(t int, options Options) (float64, error) {
	var g float64

	//if options.IndexG == 1 {
	//	g = options.G0 *
	//		math.Exp(-options.Alpha* float64(t) / float64(options.MaxIterations))
	//	return g, nil
	//}
	////TODO: переделать
	//if options.IndexG == 2 {
	//	g = options.G0 / (math.Exp(options.Alpha * float64(t)))
	//	return g, nil
	//}
	//if options.IndexG == 3 {
	//	g = options.G0 / (options.Alpha + math.Pow(float64(t), options.Gamma))
	//	return g, nil
	//}

	if options.IndexG == 1 {
		g = options.G0 *
			math.Exp(-options.Alpha * float64(t) / float64(options.MaxIterations))
		return g, nil
	}
	if options.IndexG == 2 {
		g = options.G0 *
			math.Pow(1 - math.Pow(float64(t) / float64(options.MaxIterations), 2), options.Alpha)
		return g, nil
	}
	if options.IndexG == 3 {
		g = options.G0 *
			math.Pow(1 - math.Pow(float64(t) / float64(options.MaxIterations), 3), options.Alpha)
		return g, nil
	}
	if options.IndexG == 4 {
		g = options.G0 / (1 + float64(t))
		return g, nil
	}
	if options.IndexG == 5 {
		g = options.G0 / (math.Exp(options.Alpha * float64(t)))
		return g, nil
	}
	if options.IndexG == 6 {
		g = options.G0 / (options.Alpha + math.Pow(float64(t), options.Gamma))
		return g, nil
	}
	return -1, errors.New("передан некорректный индекс функции изменения гравитационной постоянной")
}
