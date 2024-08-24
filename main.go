package main

import (
	"fmt"
	"os"

	"github.com/Danielratmiroff/terminaider/config"
	"github.com/Danielratmiroff/terminaider/src"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "termi",
	Short: "AI Chat Interface",
	Long:  `An AI-powered chat interface using the Groq API.`,
	Run: func(cmd *cobra.Command, args []string) {
		cfg, err := config.LoadConfig()
		if err != nil {
			fmt.Printf("Error loading config: %v\n", err)
			os.Exit(1)
		}
		src.RunChat(cfg)
	},
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
