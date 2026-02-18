package main

import (
	"encoding/json"
	"net/http"

	"github.com/gin-gonic/gin"
)

// RiskInput represents the canonical input for NHRI V4 risk evaluation.
// See references/input-output-contract.json for field definitions.
type RiskInput struct {
	Gender   int     `json:"gender" binding:"required"`
	Age      int     `json:"age" binding:"required,min=20,max=90"`
	SBP      float64 `json:"sbp" binding:"required"`
	TG       float64 `json:"tg"`
	UA       float64 `json:"ua"`
	Chol     float64 `json:"chol"`
	HDLC     float64 `json:"hdlc"`
	LDLC     float64 `json:"ldlc"`
	GLU      float64 `json:"glu"`
	BMI      float64 `json:"bmi"`
	Height   float64 `json:"height"`
	Weight   float64 `json:"weight"`
	Ratio    float64 `json:"ratio"`
	Waist    float64 `json:"waist"`
	Hip      float64 `json:"hip"`
	HBP      int     `json:"hbp"`
	Diabetes int     `json:"diabetes"`
	Smoke    int     `json:"smoke"`
}

// RiskOutput represents the canonical output for NHRI V4 risk evaluation.
// See references/input-output-contract.json for field definitions.
type RiskOutput struct {
	Status        int     `json:"status"`
	Error         string  `json:"error,omitempty"`
	Message       string  `json:"message,omitempty"`
	Risk          float64 `json:"risk"`
	PopulationAvg float64 `json:"populationAvg"`
	MultipleDiff  float64 `json:"multipleDiff"`
	RiskType      int     `json:"riskType"`
	Version       int     `json:"version"`
}

// evaluateRisk handles POST /api/v1/evaluate
func evaluateRisk(c *gin.Context) {
	var input RiskInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status": 1,
			"error":  err.Error(),
		})
		return
	}

	// TODO: Call the NHRI V4 evaluator logic here.
	// Replace this placeholder with actual risk computation.
	result := RiskOutput{
		Status:  0,
		Message: "evaluation complete",
		Version: 4,
	}

	c.JSON(http.StatusOK, result)
}

// healthCheck handles GET /api/v1/health
func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":  "ok",
		"version": 4,
	})
}

func main() {
	r := gin.Default()

	v1 := r.Group("/api/v1")
	{
		v1.POST("/evaluate", evaluateRisk)
		v1.GET("/health", healthCheck)
	}

	r.Run(":8080")
}
