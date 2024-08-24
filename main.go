package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/Danielratmiroff/terminaider/config"
	"github.com/Danielratmiroff/terminaider/src"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "termi [prompt]",
	Short: "AI Chat Interface",
	Long:  `An AI-powered chat interface using the Groq API.`,
	Run: func(cmd *cobra.Command, args []string) {
		cfg, err := config.LoadConfig()
		if err != nil {
			fmt.Printf("Error loading config: %v\n", err)
			os.Exit(1)
		}

		var initialPrompt string
		if len(args) > 0 {
			initialPrompt = strings.Join(args, " ")
		}

		src.RunChat(cfg, initialPrompt)
	},
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
