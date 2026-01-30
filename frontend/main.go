package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
)

type Scene struct {
	Scene    int    `json:"scene"`
	Desc     string `json:"desc"`
	ImageURL string `json:"image_url"`
	VideoURL string `json:"video_url,omitempty"`
}

type CampaignData struct {
	Strategy          string `json:"strategy"`
	Brand             string `json:"brand"`
	DirectorTreatment string `json:"director_treatment"`
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	apiURL := os.Getenv("API_URL")
	if apiURL == "" {
		apiURL = "http://localhost:8080"
	}

	// 1. Load Local Data for the Showcase
	var visuals []Scene
	visualsData, _ := os.ReadFile("../campaign_visuals_updated.json")
	if len(visualsData) == 0 {
		visualsData, _ = os.ReadFile("../campaign_visuals.json")
	}
	json.Unmarshal(visualsData, &visuals)

	var campaign CampaignData
	campData, _ := os.ReadFile("../campaign_data.json")
	json.Unmarshal(campData, &campaign)

	// Load Law.com case study data
	var lawVisuals []Scene
	lawVisualsData, _ := os.ReadFile("../law_campaign_visuals.json")
	json.Unmarshal(lawVisualsData, &lawVisuals)

	var lawCampaign CampaignData
	lawCampData, _ := os.ReadFile("../law_campaign_data.json")
	json.Unmarshal(lawCampData, &lawCampaign)

	// 2. Setup Router
	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.Static("/assets", "./assets")

	// 3. Routes
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", gin.H{
			"Title": "Agency Studio | Systems Over Story",
		})
	})

	r.GET("/showcase", func(c *gin.Context) {
		c.HTML(http.StatusOK, "showcase.html", gin.H{
			"Title":    "Case Study: Punch Card Logic",
			"Campaign": campaign,
			"Visuals":  visuals,
		})
	})

	// Law.com case study route
	r.GET("/showcase/law", func(c *gin.Context) {
		c.HTML(http.StatusOK, "showcase-law.html", gin.H{
			"Title":    "Case Study: Law.com - Intelligence Over Urgency",
			"Campaign": lawCampaign,
			"Visuals":  lawVisuals,
		})
	})

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// API Proxy
	r.Any("/api/*path", func(c *gin.Context) {
		proxyPath := c.Param("path")
		target := fmt.Sprintf("%s%s", strings.TrimRight(apiURL, "/"), proxyPath)
		req, _ := http.NewRequest(c.Request.Method, target, c.Request.Body)
		for k, v := range c.Request.Header {
			req.Header[k] = v
		}
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			c.JSON(http.StatusBadGateway, gin.H{"error": "Backend unreachable"})
			return
		}
		defer resp.Body.Close()
		for k, v := range resp.Header {
			c.Writer.Header()[k] = v
		}
		c.Status(resp.StatusCode)
		io.Copy(c.Writer, resp.Body)
	})

	r.Run(":" + port)
}