package nr_gsa

import (
	"os"
	"fmt"
	"encoding/json"
)

type Options struct {
	MaxIterations     int `json:"MI"`
	StartNumberPoints int `json:"NP"`
	EndNumberPoints   int `json:"EndNP"`
	IdxLawChangeNP    int `json:"ILCNP"`
	IndexG        int     `json:"IG"`
	G0            float64 `json:"G0"`
	Alpha         float64 `json:"AG"`
	MinFlag       int     `json:"min_flag"`
	RNorm         int     `json:"RN"`
	RPower        float64 `json:"RP"`
	ElitistCheck  int     `json:"EC"`
	Gamma         float64 `json:"GA"`
	NfIdx         int     `json:"NF"`
	SelectivityFactor float64 `json:"SF"`
	Q             float64 `json:"KQ"`
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

func (op *Options) SetOptions(maxIterations, startNumberPoints, endNumberPoints, indexG int,
							  g0, alpha, kNoise float64, minFlag, rNorm int,
							  rPower float64, elitistCheck int, gamma, sf, q float64, nfIdx, lawNPIdx int) {
	op.MaxIterations     = maxIterations
	op.StartNumberPoints = startNumberPoints
	op.EndNumberPoints   = endNumberPoints
	op.IndexG        = indexG
	op.G0            = g0
	op.Alpha         = alpha
	op.MinFlag       = minFlag
	op.RNorm         = rNorm
	op.RPower        = rPower
	op.ElitistCheck  = elitistCheck
	op.Gamma         = gamma
	op.SelectivityFactor = sf
	op.NfIdx         = nfIdx
	op.KNoise        = kNoise
	op.Q = q
	op.IdxLawChangeNP = lawNPIdx
}
