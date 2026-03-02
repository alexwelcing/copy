package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
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

	// Firebase config (public keys, safe to inline)
	firebaseAPIKey := os.Getenv("FIREBASE_API_KEY")
	if firebaseAPIKey == "" {
		firebaseAPIKey = "AIzaSyDEFAULT"
	}
	firebaseAuthDomain := os.Getenv("FIREBASE_AUTH_DOMAIN")
	if firebaseAuthDomain == "" {
		firebaseAuthDomain = "agency-studio.firebaseapp.com"
	}
	firebaseProjectID := os.Getenv("FIREBASE_PROJECT_ID")
	if firebaseProjectID == "" {
		firebaseProjectID = os.Getenv("GCP_PROJECT_ID")
		if firebaseProjectID == "" {
			firebaseProjectID = "agency-studio"
		}
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

	// Helper: base template data with Firebase config
	baseData := func(extra gin.H) gin.H {
		data := gin.H{
			"FirebaseAPIKey":    firebaseAPIKey,
			"FirebaseAuthDomain": firebaseAuthDomain,
			"FirebaseProjectID": firebaseProjectID,
		}
		for k, v := range extra {
			data[k] = v
		}
		return data
	}

	// 3. Routes
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", baseData(gin.H{
			"Title": "Agency Studio | Systems Over Story",
		}))
	})

	r.GET("/showcase", func(c *gin.Context) {
		c.HTML(http.StatusOK, "showcase.html", baseData(gin.H{
			"Title":    "Case Study: Punch Card Logic",
			"Campaign": campaign,
			"Visuals":  visuals,
		}))
	})

	// Law.com case study route
	r.GET("/showcase/law", func(c *gin.Context) {
		c.HTML(http.StatusOK, "showcase-law.html", baseData(gin.H{
			"Title":    "Case Study: Law.com - Intelligence Over Urgency",
			"Campaign": lawCampaign,
			"Visuals":  lawVisuals,
		}))
	})

	r.GET("/capabilities", func(c *gin.Context) {
		c.HTML(http.StatusOK, "capabilities.html", baseData(gin.H{
			"Title": "Capabilities",
		}))
	})

	r.GET("/welcome", func(c *gin.Context) {
		c.HTML(http.StatusOK, "welcome.html", baseData(gin.H{
			"Title": "Welcome to the Swarm",
		}))
	})

	r.GET("/pricing", func(c *gin.Context) {
		c.HTML(http.StatusOK, "pricing.html", baseData(gin.H{
			"Title": "Pricing",
		}))
	})

	r.GET("/login", func(c *gin.Context) {
		c.HTML(http.StatusOK, "login.html", baseData(gin.H{
			"Title": "Sign In",
		}))
	})

	r.GET("/dashboard", func(c *gin.Context) {
		c.HTML(http.StatusOK, "dashboard.html", baseData(gin.H{
			"Title": "Dashboard",
		}))
	})

	r.GET("/account", func(c *gin.Context) {
		c.HTML(http.StatusOK, "account.html", baseData(gin.H{
			"Title": "Account",
		}))
	})

	// Health check — validates backend reachability
	proxyClient := &http.Client{Timeout: 30 * time.Second}
	healthClient := &http.Client{Timeout: 5 * time.Second}

	r.GET("/health", func(c *gin.Context) {
		status := "healthy"

		// Check backend API reachability
		backendURL := fmt.Sprintf("%s/health", strings.TrimRight(apiURL, "/"))
		resp, err := healthClient.Get(backendURL)
		backendOK := err == nil && resp != nil && resp.StatusCode == 200
		if resp != nil {
			resp.Body.Close()
		}
		if !backendOK {
			status = "degraded"
		}

		c.JSON(http.StatusOK, gin.H{
			"status":  status,
			"backend": backendOK,
		})
	})

	// Safe headers to forward to the backend
	safeHeaders := map[string]bool{
		"Content-Type":    true,
		"Accept":          true,
		"Authorization":   true,
		"Accept-Language": true,
		"Accept-Encoding": true,
		"X-Request-Id":    true,
		"X-Anonymous-Id":  true,
	}

	// API Proxy
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

	// Graceful shutdown — Cloud Run sends SIGTERM with 10s grace period
	srv := &http.Server{
		Addr:    ":" + port,
		Handler: r,
	}

	go func() {
		log.Printf("Frontend listening on :%s", port)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server error: %v", err)
		}
	}()

	// Wait for SIGTERM or SIGINT
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down gracefully...")

	// Give in-flight requests 8 seconds to complete (Cloud Run gives 10s)
	ctx, cancel := context.WithTimeout(context.Background(), 8*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Printf("Forced shutdown: %v", err)
	}
	log.Println("Server stopped")
}
