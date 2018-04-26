package SAC

import (
	"math"
	"errors"
)

func GetNuclearFunc(idx int, g float64, selectivityFactor float64) (float64, error) {
	var value float64
	var err error

	switch idx {
	case 1: // линейное ядро
		value = math.Pow(1 - g, selectivityFactor)
		err = nil
	case 2: // параболическое ядро
		value = math.Pow(1 - math.Pow(g, 2), selectivityFactor)
		err = nil
	case 3:// кубическое ядро
		value = math.Pow(1 - math.Pow(g, 3), selectivityFactor)
		err = nil
	case 4: // экспоненциальное ядро
		value = math.Exp(-selectivityFactor * g)
		err = nil
	case 5: // гиперболическое
		value = math.Pow(g, -selectivityFactor)
		err = nil
	default:
		value = -1
		err = errors.New("передан несуществующий индекс ядерной функции")
	}
	return value, err
}
