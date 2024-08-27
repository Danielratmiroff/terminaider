package config

import (
	"fmt"
	"os"

	"github.com/Danielratmiroff/terminaider/prompts"
	"github.com/spf13/viper"
)

type Config struct {
	GroqAPIKey string
	PromptType string
}

func LoadConfig() (*Config, error) {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	viper.AddConfigPath("$HOME/.terminaider")

	// set defaults
	viper.SetDefault("GroqAPIKey", "")
	viper.SetDefault("PromptType", prompts.DEFAULT)

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			// Config file not found; ignore error if desired
			fmt.Println("Config file not found. Using default values.")
		} else {
			return nil, fmt.Errorf("error reading config file: %w", err)
		}
	}

	// Check for environment variable
	if envAPIKey := os.Getenv("GROQ_API_KEY"); envAPIKey != "" {
		viper.Set("GroqAPIKey", envAPIKey)
	}

	var config Config
	err := viper.Unmarshal(&config)
	if err != nil {
		return nil, fmt.Errorf("unable to decode config into struct: %w", err)
	}

	return &config, nil
}
