package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

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
	visualsData, err := os.ReadFile("./data/campaign_visuals_updated.json")
	if err != nil {
		log.Printf("WARNING: could not read campaign_visuals_updated.json: %v", err)
		visualsData, err = os.ReadFile("./data/campaign_visuals.json")
		if err != nil {
			log.Printf("WARNING: could not read campaign_visuals.json: %v", err)
		}
	}
	if err := json.Unmarshal(visualsData, &visuals); err != nil && len(visualsData) > 0 {
		log.Printf("WARNING: could not parse campaign visuals JSON: %v", err)
	}

	var campaign CampaignData
	campData, err := os.ReadFile("./data/campaign_data.json")
	if err != nil {
		log.Printf("WARNING: could not read campaign_data.json: %v", err)
	}
	if err := json.Unmarshal(campData, &campaign); err != nil && len(campData) > 0 {
		log.Printf("WARNING: could not parse campaign_data.json: %v", err)
	}

	// Load Law.com case study data
	var lawVisuals []Scene
	lawVisualsData, err := os.ReadFile("./data/law_campaign_visuals.json")
	if err != nil {
		log.Printf("WARNING: could not read law_campaign_visuals.json: %v", err)
	}
	if err := json.Unmarshal(lawVisualsData, &lawVisuals); err != nil && len(lawVisualsData) > 0 {
		log.Printf("WARNING: could not parse law_campaign_visuals.json: %v", err)
	}

	var lawCampaign CampaignData
	lawCampData, err := os.ReadFile("./data/law_campaign_data.json")
	if err != nil {
		log.Printf("WARNING: could not read law_campaign_data.json: %v", err)
	}
	if err := json.Unmarshal(lawCampData, &lawCampaign); err != nil && len(lawCampData) > 0 {
		log.Printf("WARNING: could not parse law_campaign_data.json: %v", err)
	}

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
	proxyClient := &http.Client{Timeout: 30 * time.Second}

	// Safe headers to forward to the backend
	safeHeaders := map[string]bool{
		"Content-Type":    true,
		"Accept":          true,
		"Authorization":   true,
		"Accept-Language": true,
		"Accept-Encoding": true,
		"X-Request-Id":    true,
	}

	r.Any("/api/*path", func(c *gin.Context) {
		proxyPath := c.Param("path")
		target := fmt.Sprintf("%s%s", strings.TrimRight(apiURL, "/"), proxyPath)
		req, err := http.NewRequest(c.Request.Method, target, c.Request.Body)
		if err != nil {
			log.Printf("ERROR: failed to create proxy request: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
			return
		}
		// Copy only safe headers
		for k, v := range c.Request.Header {
			if safeHeaders[http.CanonicalHeaderKey(k)] {
				req.Header[k] = v
			}
		}
		// Set forwarded-for header
		if clientIP := c.ClientIP(); clientIP != "" {
			req.Header.Set("X-Forwarded-For", clientIP)
		}

		resp, err := proxyClient.Do(req)
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
