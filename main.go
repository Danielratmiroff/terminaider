package main

import (
	"fmt"
	"os"

	"github.com/Danielratmiroff/terminaider/src"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "termi",
	Short: "AI Chat Interface",
	Long:  `An AI-powered chat interface using the Groq API.`,
	Run:   src.RunChat,
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
